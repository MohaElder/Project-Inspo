<template>
  <!-- <index />  -->
  <timer />
  <work />

</template>

<script>
//import index from './components/index.vue'
import timer from './components/timer.vue'
import work from './components/work.vue'


export default {
  name: 'App',
  components: {
    //index,
    timer,
    work
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
