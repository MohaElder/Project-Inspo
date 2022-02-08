<template>
  <div class="container">
    <h1>{{ msg }}</h1>
    <input type="text" v-model="msg" />
    <button @click="change">You can also click me to change content</button>
  </div>
</template>

<script>
export default {
  name: "index",
  data() {
    return {
      msg: "hello",
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
.container {
  display: grid;
  grid-gap: 30px;
  height: 500px;
}
</style>
