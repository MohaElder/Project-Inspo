<template>
    <div class="index">
      <div v-if="user != null" id="main-section">
        <popup :user="user" @submit-time="unmountPopup" />
        <div class="half">
          <timer :user="user" ref="timer" />
        </div>
        <div class="half">
          <note :user="user" />
          <todo />
        </div>
      </div>
    </div>
</template>

<script>
import timer from "./timer.vue";
import note from "./note.vue";
import popup from "./popup.vue";
import todo from './todo.vue'
import { User } from "../middleware/data.js";
export default {
  name: "index",
  components: {
    timer,
    note,
    popup,
    todo,
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
    unmountPopup(time_info) {
      this.updateUserTime(time_info);
      // TODO: Add the effect of blue covering disappearing
    },
    updateUserTime(time_info) {
      this.user.setTime(time_info);
      this.$refs.timer.setUserTime();
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url("../global.css");
.index {
  margin: 5% calc((100% - 1350px) / 2) 0 calc((100% - 1350px) / 2);
  height: 100%;
}
#main-section {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
}
.half {
  height: 100%;
  max-width: 550px;
  min-width: 550px;
  margin: 50px auto 50px auto;
}
@media (max-width: 1550px) {
  .index {
    margin: 5% 100px 0 100px;
  }
}
</style>