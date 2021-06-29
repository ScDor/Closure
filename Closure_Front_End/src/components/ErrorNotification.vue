<template>
    <div class="notification is-danger" v-if="errorMessage">
        <p>{{errorMessage}}</p>
        <button class="delete" v-on:click="closeErrorMessage()"></button>
    </div>
</template>


<script>
    export default {

        inject: ["errorState", "setErrorMessage"],

        computed:{
            errorMessage: function () {
                if (this.errorState){
                    return this.errorState.errorMessage;
                }
                return ''
            }
        },

        methods: {
            closeErrorMessage: function () {
                this.setErrorMessage("");
            }
        }
    }
</script>

<style scoped>
    .notification {
        position: fixed;
        top: 0%;
        left: 32%;
        display: flex;
        justify-content: center;
        min-height: 20vh;
        min-width: 80vh;
        z-index: 9999;
    }
</style>

