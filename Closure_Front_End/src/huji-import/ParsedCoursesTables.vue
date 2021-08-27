<template> 
    <unsupported-courses :courses="unsupportedCourses" />
    <candidate-courses v-model:courses="candidateCourses"
                       :totalCourseCount="parsedCourses.length"
                       v-if="finishedProcessing"
                       @import="$emit('import', $event)" />
</template>

<script>
import { inject, toRefs, computed, onMounted, reactive, ref } from "vue";
import UnsupportedCourses from './UnsupportedCourses.vue';
import CandidateCourses from './CandidateCourses.vue'

const processCourses = async (parsedCourses, http) => {
    return await Promise.all(
      // TODO: do this in a single API call
      parsedCourses.value.map(async course => {
        const res = await http.get(`/courses`, {
          params: {
            course_id: course.course_id,
            data_year: course.year
          }
        });
        if (res.data.count === 0) {
            console.error(`Course ${course.course_id} - ${course.name} isn't in the DB`)
            return {...course, notInDb: true}
        }
        if (res.data.count > 1) {
            console.error(`Course ${course.course_id} - ${course.name} has more than 1 DB entry, how is that possible?`)
            console.error(res.data.results)
        }
        const gottenCourse = res.data.results[0]
        const finalCourse = { ... course, name: gottenCourse.name, type: gottenCourse.type }
        if (["FIRST", "SECOND"].includes(gottenCourse.semester)) {
            if (course.semester && course.semester !== gottenCourse.semester) {
              console.warn(`Course ${course.course_id} - ${course.name} at year ${course.year} is offered only in semester `
                          +`${gottenCourse.semester}, but student took it in ${course.semester}`)
              finalCourse.semester = course.semester
            } else {
              finalCourse.semester = gottenCourse.semester
            }
        } else if (gottenCourse.semester === "EITHER") {
          finalCourse.ambiguous = !course.semester
        } else if (["ANNUAL", "SUMMER"].includes(gottenCourse.semester)) {
          finalCourse.semester = 'FIRST'
          console.warn(`Course ${course.course_id} - ${course.name} at year ${course.year} which is offered at unsupported period `
                        +`${gottenCourse.semester}, will be considered as part of the first semester`)
        }
        return finalCourse
      })
    );
}

export default {
  props: {
    parsedCourses: Array  
  },
  emits: ["import"],
  components: { UnsupportedCourses, CandidateCourses },
  setup(props) {
    const { parsedCourses } = toRefs(props);

    const courses = reactive([])
    const http = inject("http");
    const finishedProcessing = ref(false)
    
    onMounted(async () => {
      console.log(`processing ${parsedCourses.value.length} courses`);
      const processedCourses = await processCourses(parsedCourses, http)

      processedCourses.sort((a, b) => {
        if (a.ambiguous === b.ambiguous) {
          // if both are ambigious(both true) or both are not(both undefined)
          // sort them by IDs
          return a.course_id - b.course_id
        }
        // otherwise, ensure ambiguous courses appear first
        if (a.ambiguous) {
          return -1
        }
        if (b.ambiguous) {
          return 1
        }
      })

      courses.push(...processedCourses)
      finishedProcessing.value = true
    })
    const unsupportedCourses = computed(() => courses.filter(course => course.notInDb || course.unsupportedPeriod))
    const candidateCourses = computed(() => courses.filter(course => !course.notInDb && !course.unsupportedPeriod))

    const canImport = computed(() => candidateCourses.value.every(course => course.semester))

    return { courses, unsupportedCourses, candidateCourses, canImport, finishedProcessing }
  }
};
</script>

<style>
</style>