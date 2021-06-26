import { reactive , shallowReadonly } from 'vue'
import { default as INITIAL_COURSES }  from './test-courses.js'



const state = {
    courses: reactive(INITIAL_COURSES)
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


export const courses = shallowReadonly(state.courses)