<template>
  <div class="box box-style">
    <div class="media">
      <span class="icon is-small is-right is-size-7">
        <i class="fas fa-circle"></i>
      </span>

      <div class="media-content">
        {{ course.name }}
      </div>

      <div class="media-left">
        {{ course.points }}
      </div>

      <div class="media-left" @click="$emit('clickclose', $event, course)">
        <span class="icon is-small is-left is-size-7">
          <i class="fas fa-times-circle"></i>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["course"],
};
</script>

<style>
.box-style {
  padding: 0.25rem;
  box-shadow: 0px 0px 0px 0px;
  font-size: 0.75rem;
}

.box:hover {
  box-shadow: 1px 1px 1px 0px rgb(231, 231, 231);
}

.icon {
  opacity: 30%;
}

.fa-times-circle:hover {
  cursor: pointer;
}
</style>