<template>
  <div class="container">
    <div class="half wrapped container">
        <div class="less-blue semi-title">work</div>
        <div class="blue title">00:10</div>

    </div>
    <div class="half">
        <div class="blue semi-title">to-do</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "index",
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
