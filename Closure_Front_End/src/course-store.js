import { reactive , shallowReadonly, watch } from 'vue'
import { default as INITIAL_COURSES }  from './test-courses.js'


let lsCourses = localStorage.getItem("courses")
let initialCourses = INITIAL_COURSES
if (lsCourses) {
    initialCourses = JSON.parse(lsCourses)
}

const state = {
    courses: reactive(initialCourses),
    last_saved: null
}


export const addCourse = (course) => {
    state.courses.push({
        course_id: course.course_id,
        name: course.name,
        points: course.points,
        year: 1,
        semester: 1,
    })
}

export const moveCourse = ({course, newYear, newSemester}) => {
    course.year = newYear
    course.semester = newSemester
}

export const deleteCourse = (course) => {
    const index = courses.indexOf(course)
    state.courses.splice(index, 1)
}

export const addCourses = (courses) => {
    state.courses.splice(0, state.courses.length)
    state.courses.push(...courses)
}

watch(state.courses, newCourses => {
    localStorage.setItem("courses", JSON.stringify(newCourses))
})

export const courses = shallowReadonly(state.courses)