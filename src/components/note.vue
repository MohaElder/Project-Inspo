<template>
  <div class="note">
    <div class="blue semi-title">sticky notes</div>
    <div class="cards-container" v-if="notes.length > 0">
      <img class="card-control-btn" src="../assets/icons/prev_btn.png" @click="go_prev" />
      <card :note="getNote"/>
      <img class="card-control-btn" src="../assets/icons/next_btn.png" @click="go_next" />
    </div>
    <div v-else> You don't have any sticky notes. </div>
  </div>
</template>

<script>
import { User } from "../middleware/data.js";
import card from "./card.vue";

export default {
  name: "note",
  components: {
    card,
  },

  props:
  {
    user: User
  },

  data() {
    return {
      notes: this.user.notes,
      card_index: 0
    };
  },

  computed: {
    getNote() {
      return this.notes[this.card_index];
    }
  },

  methods: {
    go_next() {
      if (this.card_index < this.notes.length - 1) {
        this.card_index++;
      }
    },
    go_prev() {
      if (this.card_index > 0) {
        this.card_index--;
      }
    }
  }
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

.cards-container {
  margin-top: 20px;
  display: flex;
  flex-direction: row;
}

.card-control-btn {
  height: 96px;
  width: 96px;
  margin: auto 20px;
}

.card-control-btn:hover {
  cursor: pointer;
}
</style>
