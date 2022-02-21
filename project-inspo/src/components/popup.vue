<template>
    <Transition>
        <div id="popup" class="centered" v-if="show" @keyup.stop.prevent="keyEvent($event)">
            <img id="pop-up-cat" src="../assets/pop_up_cat.png">
            <div class="settings">
                <div class="setting">
                    <span class="semi-title set-type">work</span>
                    <span class="timer">
                        <span class="input" @click="change_selected_input">00</span>
                        <span>:</span>
                        <span class="input" @click="change_selected_input">00</span>
                    </span>
                </div>
                <div class="setting">
                    <span class="semi-title set-type">break</span>
                    <span class="timer">
                        <span class="input" @click="change_selected_input">00</span>
                        <span>:</span>
                        <span class="input" @click="change_selected_input">00</span>
                    </span>
                </div>
                <div class="start btn" @click="show = false">start</div>
            </div>
            <div id="popup-cancel" class="top-right-btn btn">cancel</div>
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
        change_selected_input(event) {
            this.selected_input = event.target
        },
        keypress(event) {

            // validation
            if (this.selected_input == null)
                return

            let original_content = this.selected_input.textContent
            if (0 <= event.key || event.key < 9) {
                let new_content = original_content.charAt(1) + event.key;

                if (new_content < 60)
                    this.selected_input.textContent = new_content
                else
                    this.selected_input.textContent = "00"

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
}
.input:hover, .btn:hover {
    cursor: pointer;
}
.start {
    width: 180px;
    padding: 15px;
    margin: 35px auto 0 auto;
    border-radius: 135px;
    background-color: #FF8D5D;
    font-size: 25px;
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