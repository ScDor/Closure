// if you are using library directly from CDN
// just don't forget to access default prop
// https://unpkg.com/vue-draggable@1.0.9/lib/vue-draggable.js
Vue.use(VueDraggable.default);

new Vue({
  template: `
  <div v-drag-and-drop:options="options" class="drag-wrapper">
    <ul>
      <li>Item 1</li>
      <li>Item 2</li>
      <li>Item 3</li>
    </ul>
    <ul>
      <li>Item 4</li>
      <li>Item 5</li>
      <li>Item 6</li>
    </ul>
    <ul>
      <li>Item 7</li>
      <li>Item 8</li>
      <li>Item 9</li>
    </ul>
  </div>
  `,
  data() {
    const componentInstance = this;
    
    return {
      options: {
        // dropzoneSelector: 'ul',
        // draggableSelector: 'li',
        // showDropzoneAreas: true,
        // multipleDropzonesItemsDraggingEnabled: true,
        // onDrop(event) {
        //   console.log(event);
        // },
        // onDragstart(event) {
        //   event.stop();
        // },
        onDragend(event) {
          // if you need to stop d&d
          // event.stop();

          // you can call component methods, just don't forget 
          // that here `this` will not reference component scope,
          // so out from this returned data object make reference
          // to component instance
          componentInstance.someDummyMethod();

          // to detect if draggable element is dropped out
          if (!event.droptarget) {
            console.log('event is dropped out');
          }
        }
      }
    }
  },
  methods: {
    someDummyMethod() {
      console.log('Hello from someDummyMethod');
    }
  }
}).$mount("#app");
