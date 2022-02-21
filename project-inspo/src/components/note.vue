<template>
  <div v-for="note in notes" :key="note.name" class="card container">
    <div class="header">
      <div class="title-space">
        <div class="card-title">{{ note.name }}</div>
        <div class="line"></div>
      </div>
      <img class="dismiss-x" src="../assets/icons/cross.png" @click="dismiss" />
    </div>
    <ul class="card-body">
      <li class="list-item" v-for="(str, index) in note.notes" :key="index">
        {{ str }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "note",
  data() {
    return {
      msg: "hi",
      notes: [
        {
          name: "biology",
          notes: [
            "the mitochondria is the powerhouse of the cell",
            "hank green whooo",
            "more random notes",
          ],
        },
        {
          name: "math",
          notes: [
            "1 + 1 = 2",
            "2 + 2 = 4",
            "math is fun!",
          ],
        },  
      ],
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

.card {
  height: 404px;
  width: 404px;
  border: 4px solid var(--orange);
  border-radius: 21px;
  padding: 5%;
  flex-direction: column;
  align-items: flex-start;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
}

.header {
  height: 20%;
  width: 100%;
  display: flex;
  justify-content: space-between;
}

.title-space {
  width: 100%;
}

.card-title {
  text-align: start;
  font-family: "Sofia Pro Black";
  font-size: 30px;
  color: black;
}

.line {
  margin-top: 5px;
  width: 100%;
  height: 3px;
  background: var(--orange);
  border-radius: 21px;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
}

.list-item {
  font-size: 30px;
  font-family: "Sofia Pro Medium";
  color: black;
  text-align: start;
}

.dismiss-x {
  position: relative;
  bottom: 20px;
  left: 10px;
  height: 40%;
}
</style>
