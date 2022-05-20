<template>
  <!-- <index />  -->
  <!-- <work /> -->
  <todo />
</template>

<script>
//import index from './components/index.vue'
// import work from './components/work.vue'
import todo from './components/todo.vue'
export default {
  name: 'App',
  components: {
    //index,
    // work,
    todo
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
