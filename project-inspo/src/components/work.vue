<template>
  <div class="container">    
    <timer time=10 key=""/>
    <div class="half">
        <div class="blue semi-title">to-do</div>
    </div>
  </div>
</template>

<script>
import timer from './timer.vue'

export default {
  name: "index",
  components:{
        timer,
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
