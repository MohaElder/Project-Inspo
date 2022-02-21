<template>
    <div id="popup" class="centered">
        <image id="pop-up-cat" src="../assets/pop_up_cat.png"></image>
        <div class="settings">
            <div class="setting">
                <span class="semi-title set-type">work</span>
                <span class="timer">
                    <span class="input">00</span>
                    <span>:</span>
                    <span class="input">00</span>
                </span>
            </div>
            <div class="setting">
                <span class="semi-title set-type">break</span>
                <span class="timer">
                    <span class="input">00</span>
                    <span>:</span>
                    <span class="input">00</span>
                </span>
            </div>
            <div class="start">start</div>
        </div>
        <div id="popup-cancel" class="top-right-btn">cancel</div>
    </div>
</template>

<script>

export default {
    name: 'popup'
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
</style>