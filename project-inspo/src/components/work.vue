<template>
  <div class="container">
    <div class="half wrapped container">
        <div class="less-blue semi-title">work</div>
        <div class="blue title">00:10</div>

    </div>
    <div class="half">
        <div class="blue semi-title">sticky notes</div>
        <note />
    </div>
  </div>
</template>

<script>

import note from './note.vue'

export default {
  name: "index",
   components: {
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
