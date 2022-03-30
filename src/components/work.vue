<template>
  <div class="container">    
    <timer worktime=.5 breaktime=.2 key=""/>
    <div class="half">
        <div class="blue semi-title">sticky notes</div>
        <note />
    </div>
  </div>
</template>

<script>

import timer from './timer.vue'
import note from './note.vue'
import popup from './components/popup.vue'

export default {
  name: "index",
  components:{
        timer,
        note

  },
  data() {
    return {
      msg: "hi",
    };
  },
  methods: {
    change() {
      this.msg = "See? Now it's changed";
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

@import url("../global.css");

</style>
