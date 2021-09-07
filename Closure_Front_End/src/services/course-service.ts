/**
 * @file Module responsible for fetching and caching(via IndexedDB) courses from
 * the API.
 */

import Dexie from "dexie";
import { http } from "@/auth";
import { djangoPaginatedGet } from './util';

// TODO: generate types from backend and centralize them

type Semester = "FIRST" | "SECOND" | "SUMMER" | "EITHER" | "ANNUAL";

type CourseType =
  | "MUST"
  | "CHOICE"
  | "CHOOSE_FROM_LIST"
  | "CORNER_STONE"
  | "SUPPLEMENTARY";

interface CourseModel {
  id: number;
  course_id: number;
  data_year: number;
  name: String;
  semester: Semester;
  is_given_this_year: boolean;
  points: number;
}

interface CourseTypeRecord {
  course_pk: number;
  track_pk: number;
  type: CourseType;
}

class CourseDB extends Dexie {
  courses: Dexie.Table<CourseModel, number>;
  types: Dexie.Table<CourseTypeRecord, [number, number]>;
  constructor() {
    super("Closure_CourseDB");
    this.version(2024).stores({
      courses: "id, [course_id+db_version], data_year, &[course_id+data_year]",
      types: "[course_pk+track_pk]",
    });
    this.courses = this.table("courses");
    this.types = this.table("types");
  }
}

let db = new CourseDB();
// TODO delete these clears!!

function compareCourseByYear(
  course1: CourseModel,
  course2: CourseModel
): number {
  if (course1.data_year < course2.data_year) {
    return 1;
  }
  if (course1.data_year > course2.data_year) {
    return -1;
  }
  return 0;
}

const MAX_POSSIBLE_YEAR = 2022

/** Finds all courses with given course ID (with differing years),
 *  sorted by their years in descending order.
 * @param course_id A HUJI course ID
 */
export async function getCoursesForID(
  course_id: number
): Promise<CourseModel[]> {
  if (!db.isOpen) {
    await db.open();
  }
  let instances = await db.courses
    .where({
      course_id: course_id,
      db_version: MAX_POSSIBLE_YEAR,
    })
    .toArray();
  if (instances.length === 0) {
    [instances] = await djangoPaginatedGet(http, `/courses/`, {
      params: { course_id: course_id },
    });
    instances = instances.map(obj => ({...obj, db_version: MAX_POSSIBLE_YEAR}))
    await db.courses.bulkPut(instances);
  }
  instances.sort(compareCourseByYear);
  return instances;
}

/** Caches the given courses in the DB. */
export async function cacheCourses(courses: CourseModel[]): Promise<void> {
  if (!db.isOpen) {
    await db.open();
  }
  const coursesToCache = courses.map((course) => ({
    ...course,
    type: undefined,
  }));
  await db.courses.bulkPut(coursesToCache);
}

/** Finds the type of courses(given by their primary keys) within context of a track(given by its primary key)
 * @param course_pks The primary keys of the courses whose types we're trying to find.
 * @param track_pk The primary key of the track
 * @returns A mapping between course PKs to their types. If no type exists(e.g, the coruse doesn't belong to given track),
 *          null will be given instead.
 */
export async function getCourseTypes(
  course_pks: number[],
  track_pk: number
): Promise<Map<number, CourseType | null>> {
  if (!db.isOpen) {
    await db.open();
  }
  const instances = await db.types
    .where(["course_pk", "track_pk"])
    .anyOf(course_pks.map((course_pk) => [course_pk, track_pk]))
    .toArray();
  const map = new Map(
    instances.map((typeRecord) => [typeRecord.course_pk, typeRecord.type])
  );
  const missing = new Set(course_pks.filter((pk) => !map.has(pk)));

  if (missing.size > 0) {
    const [entries] = await djangoPaginatedGet(http, `/tracks/${track_pk}/courses/`, {
      params: {
        id__in: Array.from(missing).join(","),
        limit: missing.size
      },
    });

    await cacheCourses(entries);
    await db.types.bulkPut(
      entries.map((course) => ({
        course_pk: course.id,
        track_pk: track_pk,
        type: course.type,
      }))
    );

    for (const entry of entries) {
      missing.delete(entry.id);
      map.set(entry.id, entry.type);
    }
  }

  for (const stillMissingPk of missing) {
    map.set(stillMissingPk, null);
  }
  await db.types.bulkPut(
    [...missing].map((missingCoursePk) => ({
      course_pk: missingCoursePk,
      track_pk: track_pk,
      type: null,
    }))
  );

  console.log("course type map given track ID", track_pk, ":", map);
  return map;
}
