<template>
  <div class="notification" v-if="showError">
    <p>{{errorMessage}}</p>
    <button class="delete" onclick="closeErrorMessage"></button>
  </div>
</template>



<script>
export default {
    props: ["errorMessage"],

    /**
    * inject: ['showError'],
    */

    methods: {
        closeErrorMessage() {
          this.showError = false
        }
    }
}
</script>

<style scoped>
.notification {
    position: fixed;
    top: 30%;
    left: 30%;
    background: gray;
    display: flex;
    justify-content:center;
    nim-height: 20vh;
    min-width: 80vh;
}
</style>

