<template>
  <div class="card">
    <img class="dismiss-x" src="../assets/icons/cross.png" @click="dismiss" />
    <div class="card-header">
      {{ getName }}
      <div class="card-header-line"></div>
    </div>
    <ul class="card-body">
      <li class="card-item" v-for="(str, index) in getNotes" :key="index">
        {{ str }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "card",
  props: {
    note: Object,
  },
  data() {
    return {
    };
  },
  computed: {
    getName() {
      return this.note.name;
    },
    getNotes() {
      return this.note.notes;
    }
  },
  methods: {
    dismiss() {
      console.log("dismissed!");
      console.log(this.note);
    },
  },
};
</script>

<style>
@import url("../global.css");
.card {
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
.card-header {
  height: 50px;
  width: 100%;
  display: flex;
  flex-direction: column;
  text-align: start;
  font-family: "Sofia Pro Black";
  font-size: 30px;
  color: black;
}
.card-header-line {
  width: 100%;
  height: 3px;
  background: var(--orange);
  margin-top: 5px;
  border-radius: 21px;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
}
.card-item {
  margin: 5px 0;
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