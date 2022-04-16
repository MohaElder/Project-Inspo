<template>
  <div class="container">
    <span v-if="user != null">
      <!-- <popup :user="user" @submit-time="unmountPopup"/> -->
      <timer :user="user" ref="timer"/>
      <div class="half">
        <div class="blue semi-title">sticky notes</div>
        <note />
      </div>
    </span>
    <span v-else> aaaa </span>
  </div>
</template>

<script>
import timer from "./timer.vue";
import note from "./note.vue";
// import popup from "./popup.vue";
import { User } from "../middleware/data.js";

export default {
  name: "index",
  components: {
    timer,
    note,
    // popup,
  },

  data() {
    return {
      user: null,
    };
  },

  mounted() {
    console.log("mounted");
    this.user = new User();
    // TODO: Add the effect of blue covering showing up
  },

  methods: {

    unmountPopup() {
      this.updateUserTime()
      // TODO: Add the effect of blue covering disappearing
    },

    updateUserTime(time_info) {
      this.user.setTime(time_info)
      this.$refs.timer.setUserTime();
    }
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url("../global.css");


</style>
