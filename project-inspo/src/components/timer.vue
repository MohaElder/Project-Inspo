<template>
  <div class="timer">
      <div class="less-blue semi-title">work</div>
      <div class="blue title">{{ displayMinutes }}:{{ displaySeconds }}</div>
      <div class="controls">
        <img id="studying" class="bg" src="../assets/studying.png" />
        <img
          class="play-btn"
          :src="isPlaying ? pause : play"
          key="pause"
          @click="toggleTimer"
        />
      </div>
    </div>
</template>

<script>
import play from "../assets/play.png";
import pause from "../assets/pause.png";

export default {
  name: "timer",
  props: {
    time: Number,
  },
  data() {
    return {
      timerInstance: null,
      totalSeconds: 20,
      isPlaying: false,
      play: play,
      pause: pause,
    };
  },

  computed: {
    displayMinutes() {
      const minutes = Math.floor(this.totalSeconds / 60);
      return this.formatTime(minutes);
    },
    displaySeconds() {
      const seconds = this.totalSeconds % 60;
      return this.formatTime(seconds);
    },
  },

  mounted() {
    this.totalSeconds = this.time;
  },

  methods: {
    formatTime(time) {
      if (time < 10) {
        return "0" + time;
      }
      return time.toString();
    },
    toggleTimer() {
      clearInterval(this.timerInstance);
      this.isPlaying = !this.isPlaying;
      if (this.isPlaying) {
        this.timerInstance = setInterval(() => {
          if (this.totalSeconds <= 0) {
            console.log("work completed");
            clearInterval(this.timerInstance);
            return;
          }
          this.totalSeconds -= 1;
        }, 1000);
      }
    },
    changeCurrentTimer(num) {
      this.currentTimer = num;
    },
    finishTimer() {},
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url("../global.css");

.play-btn {
  align-self: center;
  transition-duration: 0.4s;
  text-decoration: none;
  overflow: hidden;
}

.play-btn:hover {
  animation: bounce; /* referring directly to the animation's @keyframe declaration */
  animation-duration: 2s; /* don't forget to set a duration! */
}

.timer {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.icon {
  width: 84px;
  height: 84px;
  display: flex;
  align-self: center;
}
.bg {
  width: 550px;
  height: auto;
}
.controls {
  display: flex;
  flex-direction: column;
}
</style>
