<template>
  <div class="course-box">
    <div class="box box-style has-icons-left">
      <div class="columns is-mobile">
        <div class="column is-four-fifths">
          {{ name }}
        </div>
        <!-- <div class="column push-left">
          
          5
      
        </div> -->
        <div class="column push-left">
          <span class="icon is-small is-left is-size-7">
            <i class="fas fa-times-circle"></i>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["name"],
};
</script>

<style>
.box-style {
  padding: 0.25rem;
  box-shadow: 0px 0px 0px 0px;
  font-size: 0.75rem;
}
.course-box:hover {
  box-shadow: 1px 1px 1px 0px rgb(231, 231, 231);
}
.push-left {
  text-align: left;
}
.icon {
  opacity: 50%;
}
</style>