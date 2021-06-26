import { reactive , shallowReadonly } from 'vue'
import { default as INITIAL_COURSES }  from './test-courses.js'



const state = {
    courses: reactive(INITIAL_COURSES)
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


export const courses = shallowReadonly(state.courses)