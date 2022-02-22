<template>
    <div id="account">
        <div class="top-left-route semi-title">
            <span class="orange">home / </span>
            <span class="blue">{{ type.replace('_', ' ') }}</span>
        </div>
        <div class="main-section">
            <img v-if="type == 'sign_up'" src="../assets/sign_up.png">
            <img v-else src="../assets/log_in.png">
            <div class="sub-section">
                <div class="form">
                    <div id="form-title" class="blue">{{ form_title }}</div>
                    <!-- <div>email</div>
                    <input type="email" placeholder="example@gmail.com">
                    <div>password</div>
                    <input type="password"> -->
                </div>
                <div class="prompt">
                    <span class="question">{{ question }}</span>
                    <span class="answer less-blue">{{ answer }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    props: {
        type: String,
    },
    data() {
        return {
            form_title: this.type == "sign_up" ? "make an account" : "welcome back!",
            question: this.type == "sign_up" ? "have an account? " : "don't have an account? ",
            answer: this.type == "sign_up" ? "log in" : "sign up"
        }
    },
    mounted() {
        console.log(this.type)
    }
}

</script>

<style>

@import '../global.css';

#account {
    font-family: "Sofia Pro Bold";
}

.top-left-route {
    position: absolute;
    top: 50px;
    left: 50px;
}

img {
    height: 800px;
    width: 800px;
    z-index: 1;
}

.main-section {
    height: calc(100vh - 5vh - 8px * 2); /* 8px cause body somehow has the margin of 8px */
    width: calc(100vw - 12vw - 10vw - 8px * 2);
    padding: 5vh 12vw 0 10vw;
    display: flex;
    flex-direction: row;
}

.sub-section {
    height: calc(100% - 175px);
    width: calc(100% - 700px + 100px); /* 100px cause margin left is -100px*/
    margin-top: 175px;
    margin-left: -120px;
    display: flex;
    flex-direction: column;
}

.form {
    height: 480px;
    width: 100%;
    border-radius: 21px;
    box-shadow: 0 10px 60px rgba(0, 0, 0, 0.2);
}

#form-title {
    padding: 45px 50px;
    text-align: left;
    font-size: 45px;
}

.prompt {
    margin-top: 50px;
    font-size: 30px;
}

.answer:hover {
    cursor: pointer;
}

@media (max-width: 1500px) {

    .main-section {
        width: 100%;
        padding: 0;
        justify-content: center;
    }

    img {
        display: none;
    }

    .sub-section {
        width: 70%;
        max-width: 750px;
        margin: 200px 0 0 0;
    }
}

</style>


