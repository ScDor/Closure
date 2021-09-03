import { reactive, shallowReadonly, computed, watch } from "vue";
import { http } from "./auth";

const LS_PATH = "course-store-state-v1";

const getInitialState = () => {
  const storedLSState = localStorage.getItem(LS_PATH);
  if (storedLSState !== null) {
    return JSON.parse(storedLSState);
  } else {
    return {
      courses: [],
      dirty: false,
      track: null,
      courseplan: null,
    };
  }
};

const state = reactive(getInitialState());

/*   */
watch(state, (newState) => {
  localStorage.setItem(LS_PATH, JSON.stringify(newState));
});

/* course-plan save/load operations */

const getCoursesAsTakes = () => {
  return state.courses.map((course) => ({
    course: course.id,
    year_in_studies: course.take.year,
    semester: course.take.semester,
  }));
};

export const save = async () => {
  const res = await http.put(`/course_plans/${state.courseplan.id}/`, {
    name: state.courseplan.name,
    track: state.track?.id,
    public: state.courseplan.public,
    takes: getCoursesAsTakes(),
  });
  const plan = res.data;
  console.log(`save() course plan, gotten: `, plan);
  return onSavedSuccessfully(plan);
};

export const saveAs = async ({ name, publicize }) => {
  const res = await http.post("/course_plans/", {
    name,
    track: state.track?.id,
    public: publicize,
    takes: getCoursesAsTakes(),
  });
  const plan = res.data;
  console.log(`saveAs() course plan, gotten: `, plan);
  return onSavedSuccessfully(plan);
};

const onSavedSuccessfully = (newPlan) => {
  state.courseplan = newPlan;
  state.dirty = false;
  return newPlan;
};

export const deletePlan = async (plan) => {
  const res = await http.delete(`/course_plans/${plan.id}`)
  console.log("deleted plan", plan, "result:", res)
  if (plan.id === state.courseplan?.id) {
    console.log("deleting own plan")
    state.courseplan = null
    state.dirty = true
  }
}

export const loadPlan = async (planId) => {
  // console.assert(typeof(planId) === "number", "loadPlan() - planId must be a number")
  const res = await http.get(`/course_plans/${planId}`)
  const plan = res.data
  console.log("loaded plan", plan)
  state.courseplan = plan
  state.track = plan.track ?? null
  const loadedCourses = plan.takes.map(take => ({
    ...take.course, take: {
      semester: take.semester,
      year: take.year_in_studies
    }
  }))
  addCourses(loadedCourses, true)
  state.dirty = false
}

/* course  operations */

export const addCourse = (course) => {
  if (!course) {
    throw new Error("Course must not be undefined/null");
  }
  state.courses.push({
    ...course,
    year: 1,
    semester: 1,
  });
  state.dirty = true;
};

export const moveCourse = ({ course, newYear, newSemester }) => {
  if (!course) {
    throw new Error("Course must not be undefined/null");
  }
  course.take.year = newYear;
  course.take.semester = newSemester;
  state.dirty = true;
};

export const deleteCourse = (course) => {
  if (!course) {
    throw new Error("Course must not be undefined/null");
  }
  const index = courses.indexOf(course);
  state.courses.splice(index, 1);
  state.dirty = true;
};

export const addCourses = (courses, overwrite) => {
  if (overwrite) {
    state.courses.splice(0, state.courses.length);
  }
  state.courses.push(...courses);
  state.dirty = true;
};

/* track operations */

export const setTrack = (newTrack) => {
  console.log("Changing track, from", state.track, "to", newTrack);
  state.track = newTrack;
  state.dirty = true;
}

/* store state getters */

export const courses = shallowReadonly(state.courses);
export const currentTrack = computed(() => state.track);
export const currentCourseplan = computed(() => state.courseplan);
export const isDirty = computed(() => state.dirty);
