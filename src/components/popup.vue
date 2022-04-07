<template>
  <Transition>
    <div
      id="popup"
      class="centered"
      v-if="show"
      @keyup.stop.prevent="keyEvent($event)"
    >
      <img id="pop-up-cat" src="../assets/pop_up_cat.png" />
      <div class="settings">
        <div class="setting">
          <span class="semi-title set-type">work</span>
          <span class="timer">
            <span
              class="input"
              @click="
                change_selected_input();
                activeNumber = 'workMinute';
              "
              >{{ Math.floor(user.getWorkTime() / 60) }}</span
            >
            <span>:</span>
            <span
              class="input"
              @click="
                change_selected_input();
                activeNumber = 'workSecond';
              "
              >{{ user.getWorkTime() % 60 }}</span
            >
          </span>
        </div>
        <div class="setting">
          <span class="semi-title set-type">break</span>
          <span class="timer">
            <span
              class="input"
              @click="
                change_selected_input();
                activeNumber = 'breakMinute';
              "
              >{{ Math.floor(user.getBreakTime() / 60) }}</span
            >
            <span>:</span>
            <span
              class="input"
              @click="
                change_selected_input();
                activeNumber = 'breakSecond';
              "
              >{{ user.getBreakTime() % 60 }}</span
            >
          </span>
        </div>
        <div class="start btn" @click="show = false">start</div>
      </div>
      <div id="popup-cancel" class="top-right-btn btn" @click="show = false">
        cancel
      </div>
    </div>
  </Transition>
</template>

<script>
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

import { User } from "../middleware/data";

export default {
  name: "popup",
  selected_input: null,
  props: {
    user: User,
  },
  data() {
    return {
      show: false,
      multiplier: 1,
      breakMinute: 0,
      breakSecond: 0,
      workMinute: 0,
      workSecond: 0,
      activeNumber: '',
    };
  },
  methods: {
    change_selected_input(event, activeNumber) {
      if (this.selected_input != null) {
        this.selected_input.classList.toggle("clear");
      }
      this.selected_input = event.target;
      this.selected_input.classList.toggle("clear");
      this.activeNumber = activeNumber;
    },
    async keypress(event) {
      // validation
      if (this.selected_input == null) return;

      let original_content = this.selected_input.textContent;
      if (0 <= event.key || event.key < 9) {
        let new_content = original_content.charAt(1) + event.key;

        if (new_content < 60) {
          this.selected_input.textContent = new_content;
          this.selected_input.classList.add("clear");
        } else {
          this.selected_input.textContent = new_content;
          await sleep(100);
          this.selected_input.textContent = "00";
        }
      }

      if (event.key == "Backspace") {
        this.selected_input.textContent = "0" + original_content.charAt(0);
      }

      var ret = parseInt(this.selected_input.textContent);

      switch (this.activeNumber){
          case 'workminute':
            this.workMinute = ret
            break;
          case 'worksecond':
            this.workSecond = ret
            break;
          case 'breakminute':
            this.breakMinute = ret
            break;
            case 'breaksecond':
            this.breakSecond = ret
            break;
      }
    },
  },
  async mounted() {
    window.addEventListener("keydown", this.keypress);
    await sleep(500);
    this.show = true;
  },
};
</script>

<style>
@import "../global.css";

#popup {
  height: 373px; /* 643 - 135 * 2 */
  width: 672px; /* 832 - 80 * 2 */
  padding: 135px 80px;
  display: flex;
  border-radius: 32.2px;
  background-color: #3d5a76;
  font-family: "Sofia Pro Bold";
  color: #fff;
  z-index: 1;
}
.centered {
  position: fixed;
  top: 50%;
  left: 50%;
  margin-top: -321.5px;
  margin-left: -416px;
}
#pop-up-cat {
  height: 370px;
  width: 205px;
}
.settings {
  width: 370px;
  padding: 50px 0px 30px 50px;
  display: flex;
  flex-direction: column;
  font-size: 80px;
}
.setting {
  padding: 10px 0;
  display: flex;
  justify-content: space-between;
}
.set-type {
  padding-top: 20px;
}
.input {
  min-width: 90px;
  opacity: 0.5;
}
.input:hover,
.btn:hover {
  cursor: pointer;
  opacity: 1;
}
.clear {
  opacity: 1;
}
.start {
  display: block;
  width: 180px;
  height: 50px;
  margin: 40px auto;
  padding: 15px 40px;
  border-radius: 30px;
  background-color: #ff8d5d;
  font-size: 22px;
  color: #fff;
  transition: all 0.3s;
}
.start:hover {
  width: 230px;
  cursor: pointer;
  background-color: #f36817;
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.2);
  transform: translateY(-5px);
}
.top-right-btn {
  position: absolute;
  top: 40px;
  right: 60px;
  color: #ff8d5d;
  font-family: "Sofia Pro Black";
}
#popup-cancel {
  font-size: 30px;
}
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>