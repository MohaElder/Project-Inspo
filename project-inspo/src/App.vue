<template>
  <!-- <account v-if="!account_state"/> -->
  <index />
</template>

<script>
import index from './components/index.vue'
// import account from './components/account.vue'

export default {
  name: "App",
  components: {
    index,
    // account,
  },
  data:() => ({
    account_state: localStorage.getItem('loggedin') == "True",
  }),
};
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
