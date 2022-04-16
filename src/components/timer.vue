<template>
  <div class="timer">
      <div class="less-blue semi-title">{{section}}</div>
      <div class="blue title">{{ displayMinutes }}:{{ displaySeconds }}</div>
      <div class="controls">
        <img class="bg" :src="image"/>
        <img class="play-btn" :src="isPlaying ? pause : play" @click="toggleTimer"/>
        <!--the isPlaying ? pause : play means: if isPlaying is True? Then use pause src, else show play src -->
      </div>
    </div>
</template>

<script>
import rest from "../assets/rest.png";
import play from "../assets/play.png";
import pause from "../assets/pause.png";
import { User } from "../middleware/data.js";
import studying from "../assets/studying.png";


export default {
  name: "timer",

  props:
  {
    user: User
  },

  data() {
    return {
      timerInstance: null,
      totalSeconds: 20,
      isPlaying: false,
      play: play,
      pause: pause,
      image: studying,
      section: "work",
    };
  },

  mounted() {
    this.totalSeconds = this.user.workTime;
  },

  computed: {
    displayMinutes() {
      return this.formatTime(Math.floor(this.totalSeconds / 60));
    },
    displaySeconds() {
      return this.formatTime(this.totalSeconds % 60);
    },
  },

  methods: {
    setUserTime() {
      if (this.section == "work") {
        this.totalSeconds = this.user.workTime;
      }
      else if (this.section == "break") {
        this.totalSeconds = this.user.breakTime;
      }
    },

    toggleSection(){

      if(this.section === "work") {
        this.section = "break"
        this.image = rest
        console.log("work completed");
      }

      else if(this.section==="break") {
        this.section = "work"
        this.image = studying
        console.log("break is over");
      }

    },

    formatTime(time) {
      if (time < 10) {
        return "0" + time;
      }
      return time.toString();
    },

    toggleTimer() { //I merged toggle, pause, and start to one function! It's just some simple changes based on your code~

      clearInterval(this.timerInstance);
      this.isPlaying = !this.isPlaying;

      if (this.isPlaying) {

        this.timerInstance = setInterval(() => {
          if (this.totalSeconds <= 0) {
            this.toggleSection();
            clearInterval(this.timerInstance);
            this.setUserTime();
            this.isPlaying = false;
            return;
          }
          this.totalSeconds -= 1;
        }, 1000);

      }
    },
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
  animation-duration: 2s; /*don't forget to set a duration! */
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
