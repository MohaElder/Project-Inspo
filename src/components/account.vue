<template>
  <div id="account">
    <div class="top-left-route semi-title">
      <span class="orange">home / </span>
      <span class="blue">{{ isSignup ? "Sign up" : "Log in" }}</span>
    </div>
    <div class="main-section">
      <img v-if="isSignup" src="../assets/sign_up.png" />
      <img v-else src="../assets/log_in.png" />
      <div class="sub-section">
        <form class="form" @submit="login">
          <div id="form-title" class="blue">{{ form_title }}</div>
          <label>email</label><br />
          <input type="email" placeholder="example@gmail.com" /><br />
          <label>password</label><br />
          <input type="password" /><br />
          <input
            type="submit"
            :value="isSignup ? 'Sign up' : 'Log in'"
            id="submit-btn"
          />
        </form>
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
    isSignup: Boolean,
  },
  data() {
    return {
      form_title: this.isSignup ? "make an account" : "welcome back!",
      question: this.isSignup ? "have an account? " : "don't have an account? ",
      answer: this.isSignup ? "log in" : "sign up",
    };
  },
  mounted() {},
  methods: {
    login() {
      localStorage.setItem('loggedin', "True")
    },
  },
};
</script>

<style>
@import "../global.css";
#account {
  font-family: "Sofia Pro Bold";
  font-size: 18px;
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
  height: calc(
    100vh - 5vh - 8px * 2
  ); /* 8px cause body somehow has the margin of 8px */
  width: calc(100vw - 12vw - 10vw - 8px * 2);
  max-width: 1500px;
  padding: 5vh 12vw 0 10vw;
  margin: 0 auto;
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
  text-align: left;
}
#form-title {
  margin: 45px 0 15px 50px;
  font-size: 45px;
}
label {
  display: inline-block;
  margin: 20px 0 5px 50px;
}
input {
  display: block;
  height: 40px;
  width: calc(100% - 70px - 50px);
  margin: 10px 0 0 50px;
  border: none;
  padding: 5px 20px;
  border-radius: 15px;
  background-color: #a9bedd;
  font-family: "Sofia Pro Bold";
  font-size: 14px;
}
#submit-btn {
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
#submit-btn:hover {
  width: 230px;
  cursor: pointer;
  background-color: #f36817;
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.2);
  transform: translateY(-5px);
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