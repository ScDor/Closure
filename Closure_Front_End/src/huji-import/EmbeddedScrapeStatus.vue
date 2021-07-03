<template>
  <h1>Embedded Scrape Status - {{now}} </h1>
</template>

<script>
export default {
  data: function() {
    return {
      now: new Date().toUTCString()
    }
  }
}
</script>

<style>

</style>