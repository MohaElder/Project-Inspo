<template>
  <div class="index">
    <div v-if="user != null" id="main-section">
      <!-- <popup :user="user" @submit-time="unmountPopup"/> -->
      <div class="half" id="left-half">
        <timer :user="user" ref="timer"/>
      </div>
      <div class="half" id="left-half">
        <div class="blue semi-title">sticky notes</div>
        <!-- <note /> -->
      </div>
    </div>
    <div v-else> aaaa </div>
  </div>
</template>

<script>
import timer from "./timer.vue";
// import note from "./note.vue";
// import popup from "./popup.vue";
import { User } from "../middleware/data.js";

export default {
  name: "index",
  components: {
    timer,
    // note,
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
    // timer_half.margin_left = timer_half.width;
    // TODO: Add the effect of blue covering showing up
  },

  methods: {

    unmountPopup(time_info) {
      this.updateUserTime(time_info)
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
  margin: 50px auto 50px auto;
}

#left-half {
  max-width: 550px;
  min-width: 550px;
}

#right-half {
  max-width: 800px;
  min-width: 800px;
}

@media (max-width: 1550px) {

  .index {
    margin: 5% 100px 0 100px;
  }

}

</style>
