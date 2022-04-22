<template>
  <div class="note">
    <div class="blue semi-title">sticky notes</div>
    <div v-for="note in notes" :key="note.name" class="card-container">
      <img class="dismiss-x" src="../assets/icons/cross.png" @click="dismiss" />
      <div class="header">
        <div class="card-title">{{ note.name }}</div>
        <div class="line"></div>
      </div>
      <ul class="card-body">
        <li class="card-item" v-for="(str, index) in note.notes" :key="index">
          {{ str }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { User } from "../middleware/data.js";

export default {
  name: "note",

  props:
  {
    user: User
  },

  data() {
    return {
      notes: this.user.notes
    };
  },
  methods: {
    dismiss() {
      console.log("dismissed!");
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url("../global.css");

.note {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.card-container {
  position: relative;
  height: 404px;
  width: 404px;
  border: 4px solid var(--orange);
  border-radius: 21px;
  padding: 36px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  background-color: white;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
}

.header {
  height: 50px;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.card-title {
  text-align: start;
  font-family: "Sofia Pro Black";
  font-size: 30px;
  color: black;
}

.line {
  width: 100%;
  height: 3px;
  background: var(--orange);
  margin-top: 5px;
  border-radius: 21px;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
}

.card-item {
  margin: 10px 0;
  padding: 10px 0;
  text-align: start;
  font-size: 30px;
  font-family: "Sofia Pro Medium";
  color: black;
}

.dismiss-x {
  position: absolute;
  top: 20px;
  right: 20px;
  height: 40px;
}

.dismiss-x:hover {
  cursor: pointer;
}
</style>
