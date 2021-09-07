import { watch, reactive, toRefs, readonly, WatchSource } from "vue";
import { getCoursesForID, getCourseTypes } from "@/services/course-service";

// TODO: generate types from backend and centralize them
interface Track {
  id: number;
}

interface Course {
  id: number;
  type: string | null | undefined;
}

/** This hook is responsible for updating course types based
 *  on given track
 */
export function syncCourseTypesToTrack(
  courses: WatchSource<Course[]>,
  track: WatchSource<Track>
) {
  const state = reactive({
    error: null,
    loading: false,
  });
  watch(
    [courses, track],
    async ([curCourses, curTrack]) => {
      console.log("updateCourseTypes hook, courses:", curCourses, "track:", curTrack)
      if (curTrack == null) {
          console.log("\tnullifying course types")
          for (const course of curCourses) {
              course.type = null
          }
          return
      }
      try {
        state.loading = true;
        const coursePksToTypes = await getCourseTypes(
          curCourses.map((c) => c.id),
          curTrack.id
        );
        for (const course of curCourses) {
          course.type = coursePksToTypes.get(course.id);
        }
      } catch (ex) {
        state.error = ex;
        throw ex;
      } finally {
        state.loading = false;
      }
    },
    { immediate: true, deep: true }
  );

  return {...toRefs(readonly(state))};
}
