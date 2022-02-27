<template>
  <div class="container">
    <div class="half wrapped container timer">
        <div class="less-blue semi-title">work</div>
        <div class="blue title">
            {{displayMinutes}}:{{displaySeconds}}
        </div>
        <img id="studying" class = "bg" src="../assets/studying.png">
        <div class="controls">
            <button type="button" class="button" @click = "startTimer"><img id="play" class = "icon" src="../assets/play.png"></button>
            <button type="button" class="button" @click = "pauseTimer"><img id="pause" class = "icon" src="../assets/pause.png"></button>
        </div>
    </div>
    
  </div>
</template>

<script>
export default {
  name: "timer",
  data() {
    return {
        timerInstance: null,
        totalSeconds:60
    }
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
      }
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

@import url("../global.css");
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
  width:720px;
  height: auto;
}
.controls{
    display:flex;
    align-self: center;
}
.button{
    border:none;
    background-color: #FFFFFF;
}
</style>
