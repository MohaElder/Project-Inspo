<template>
    <Transition>
        <div id="popup" class="centered" v-if="show" @keyup.stop.prevent="keyEvent($event)">
            <img id="pop-up-cat" src="../assets/pop_up_cat.png">
            <div class="settings">
                <div class="setting">
                    <span class="semi-title set-type">work</span>
                    <span class="timer">
                        <span class="input" @click="changeSelectedInput" ref="work_mins">00</span>
                        <span>:</span>
                        <span class="input" @click="changeSelectedInput" ref="work_secs">00</span>
                    </span>
                </div>
                <div class="setting">
                    <span class="semi-title set-type">break</span>
                    <span class="timer">
                        <span class="input" @click="changeSelectedInput" ref="break_mins">00</span>
                        <span>:</span>
                        <span class="input" @click="changeSelectedInput" ref="break_secs">00</span>
                    </span>
                </div>
                <div class="start btn" @click="submitTime">start</div>
            </div>
            <div id="popup-cancel" class="top-right-btn btn" @click="show = false">cancel</div>
        </div>
    </Transition>
</template>

<script>
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
export default {
    name: 'popup',
    selected_input: null,
    methods: {
        submitTime() {
          let time_info = {
            "work": this.getWorkTime(),
            "break": this.getBreakTime()
          }
          this.$emit('submitTime', time_info)
          this.show = false
        },
        getWorkTime() {
          return {
            "mins": this.$refs.work_mins.textContent,
            "secs": this.$refs.work_secs.textContent
          }
        },
        getBreakTime() {
          return {
            "mins": this.$refs.break_mins.textContent,
            "secs": this.$refs.break_secs.textContent
          }
        },
        changeSelectedInput(event) {
            if (this.selected_input != null) {
                this.selected_input.classList.toggle("clear")
            }
            this.selected_input = event.target
            this.selected_input.classList.toggle("clear")
        },
        async keypress(event) {
            // validation
            if (this.selected_input == null)
                return
            let original_content = this.selected_input.textContent
            if (0 <= event.key || event.key < 9) {
                let new_content = original_content.charAt(1) + event.key;
                if (new_content < 60) {
                    this.selected_input.textContent = new_content
                    this.selected_input.classList.add("clear")
                }
                else {
                    this.selected_input.textContent = new_content
                    await sleep(100)
                    this.selected_input.textContent = "00"
                }
            }
            if (event.key == "Backspace") {
                this.selected_input.textContent = "0" + original_content.charAt(0)
            }
        }
    },
    async mounted() {
        window.addEventListener("keydown", this.keypress)
        await sleep(500)
        this.show = true;
    },
    data() {
        return {
            show: false
        }
    }
}
</script>

<style>
@import '../global.css';
#popup {
    height: 373px; /* 643 - 135 * 2 */
    width: 672px; /* 832 - 80 * 2 */
    padding: 135px 80px;
    display: flex;
    border-radius: 32.2px;
    background-color: #3D5A76;
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
.input:hover, .btn:hover {
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
    background-color: #FF8D5D;
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
    color: #FF8D5D;
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
