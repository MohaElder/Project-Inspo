<template>
  <div class="container">
    <div class="half wrapped container timer">
        <div class="less-blue semi-title">work</div>
        <div class="blue title">
            {{displayMinutes}}:{{displaySeconds}}
        </div>
        <img id="studying" class = "bg" src="../assets/studying.png">
        <div class="controls">

            <button
                class="button"
                @click="toggle"
                >
                <transition-group name="toggle-buttons">
                    <img :src="pause"
                    v-if="isPlaying"
                    key="pause"
                    @click= "pauseTimer"
                    />
                    <img :src="play"
                    v-else
                    key="play"
                    @click= "startTimer"
                    />
                </transition-group>
            </button>
        </div>
    </div>
    
  </div>
</template>

<script>

import play from "../assets/play.png"
import pause from "../assets/pause.png"

export default {
  name: "timer",
  data() {
    return {
        timerInstance: null,
        totalSeconds:20,
        isPlaying: false,
        play:play,
        pause:pause,
    };
  },

  computed: {
      displayMinutes(){
          const minutes = Math.floor(this.totalSeconds/60)
          return this.formatTime(minutes)
      },
      displaySeconds(){
          const seconds = this.totalSeconds%60
          return this.formatTime(seconds)
      }
  },

  
  methods: {
      formatTime(time){
          if(time<10){
              return'0' + time
          }
          return time.toString()  
      },
      startTimer(){
            this.pauseTimer()
            this.timerInstance=setInterval(() => {
                if(this.totalSeconds<=0){
                    console.log("work completed")
                    this.pauseTimer()
                    return
                }
                this.totalSeconds-=1;
            }, 1000)
      },
      pauseTimer(){
          clearInterval(this.timerInstance)
      },
      changeCurrentTimer(num){
          this.currentTimer=num
      },
       finishTimer(){
      },
      toggle() {
        this.isPlaying = !this.isPlaying
        this.$emit('toggleIsPlaying', this.isPlaying)
        },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

@import url("../global.css");
.half{
  margin-left:3%;
  border-style: dotted;
}
.timer {
  display: flex;
  flex-direction:column;
  align-items: flex-start;

}
.icon {
  width:84px;
  height: 84px;
  display:flex;
  align-self: center;
}
.bg {
  width:550px;
  height: auto;
}
.controls{
    display:flex;
    align-self: center;
}
.button{
    border:none;
    background-color: transparent;
}
</style>
