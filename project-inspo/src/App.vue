<template>
  <!-- <index />  -->
  <!-- <work /> -->
  <account type="log_in"></account>
</template>

<script>
// import index from './components/index.vue'
// import work from './components/work.vue'
import account from './components/account.vue'

export default {
  name: 'App',
  components: {
    // index,
    // work,
    account
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
}

button {
  position: absolute;
}
</style>
