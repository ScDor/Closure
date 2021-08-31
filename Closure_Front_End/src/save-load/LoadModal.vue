<template>
<div class="box" dir="rtl">
    <h1 class="title">טעינת תכנית לימודים</h1>


    <div v-if="course_plans">
        <loadable-course-plan :plan="plan" v-for="plan in course_plans" :key="plan.id" 
         @deletedPlan="handleDeletedPlan" @loadedPlan="handleLoadedPlan"/>

        <div v-if="course_plans.length === 0">
            אין תכניות שמורות
        </div>
    </div>

    <div v-if="isValidating">
        טוען ...
        <progress class="progress is-small is-primary" max="100">15%</progress>
    </div>

    <div class="control">
        <button class="button is-link is-light" @click="$emit('close')">
            ביטול
        </button>
    </div>
</div>
</template>

<script>
import { inject } from 'vue'
import LoadableCoursePlan from "@/save-load/LoadableCoursePlan.vue"
import useSWRV from 'swrv'


export default {
    components: { LoadableCoursePlan },
    emits: [ "close"],
    setup(_props, { emit}) {
        console.log("LoadModal setup()")
        const http = inject("http")
        const fetcher = key => http.get(key).then(res => res.data.course_plans)
        const { data: course_plans, mutate, isValidating, error } = useSWRV("/student/me/", fetcher)

        // used to hide deleted courses from the UI until the data is revalidated
        const deletedIds = new Set()

        const handleDeletedPlan = async (deletedPlan) => {
            deletedIds.add(deletedPlan.id)
            await mutate()
            deletedIds.delete(deletedPlan.id)
        }

        const handleLoadedPlan = () => {
            emit('close')
        }

        return {
            course_plans, handleDeletedPlan, isValidating, error, handleLoadedPlan
        }
    }
}
</script>

<style>

</style>