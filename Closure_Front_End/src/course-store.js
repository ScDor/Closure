import { reactive , shallowReadonly, watch } from 'vue'
import { default as INITIAL_COURSES }  from './test-courses.js'


let lsCourses = localStorage.getItem("courses")
let initialCourses = INITIAL_COURSES
if (lsCourses) {
    initialCourses = JSON.parse(lsCourses)
}

const state = {
    courses: reactive(initialCourses)
}


export const addCourse = (course) => {
    if (!course) {
        throw new Error("Course must not be undefined/null")
    }
    state.courses.push({
        ...course,
        year: 1,
        semester: 1
    })
}

export const moveCourse = ({course, newYear, newSemester}) => {
    if (!course) {
        throw new Error("Course must not be undefined/null")
    }
    course.year = newYear
    course.semester = newSemester
}

export const deleteCourse = (course) => {
    if (!course) {
        throw new Error("Course must not be undefined/null")
    }
    const index = courses.indexOf(course)
    state.courses.splice(index, 1)
}

export const addCourses = (courses, overwrite) => {
    if (overwrite) {
        state.courses.splice(0, state.courses.length)
    }
    state.courses.push(...courses)
}

watch(state.courses, newCourses => {
    localStorage.setItem("courses", JSON.stringify(newCourses))
})

export const courses = shallowReadonly(state.courses)