<template>
  <div class="blue semi-title">to-do</div>
  <!-- <input type="text" class="todo-input" placeholder="enter a new task" v-model="newTodo" @keyup.enter="addTodo"> -->
  <div v-for="(todo, index) in todos" :key="todo.id" class="todo-item">
    <div class="todo-item-left">
      <input class="check" type="checkbox" v-model="todo.completed" />
      <div
        v-if="!todo.editing"
        @dblclick="editTodo(todo)"
        class="todo-item-label"
        :class="{ completed: todo.completed }"
      >
        {{ todo.title }}
      </div>
      <input
        v-else
        class="todo-item-edit"
        type="text"
        v-model="todo.title"
        @blur="doneEdit(todo)"
        @keyup.enter="doneEdit(todo)"
        @keyup.esc="cancelEdit(todo)"
        v-focus
      />
    </div>
    <div class="remove-item" @click="removeTodo(index)">&times;</div>
  </div>
  <div>
    <button @click="placeholderTodo" class="newTask" type="button">+</button>
  </div>
</template>

<script>
export default {
  name: "todo",
  data() {
    return {
      newTodo: "",
      idForTodo: 3,
      beforeEditCache: "",
      todos: [
        {
          id: 1,
          title: "Do the dishes",
          completed: false,
          editing: false,
        },
        {
          id: 2,
          title: "Essay2",
          completed: false,
          editing: false,
        },
      ],
    };
  },
  directives: {
    focus: {
      inserted: function (el) {
        el.focus();
      },
    },
  },
  methods: {
    placeholderTodo() {
      this.todos.push({
        id: this.idForTodo,
        title: "enter a new task",
        completed: false,
      });
      //   this.newTodo=""
      this.idForTodo++;
    },
    addTodo() {
      if (this.newTodo.trim().length == 0) {
        return;
      }
      this.todos.push({
        id: this.idForTodo,
        title: this.newTodo,
        completed: false,
      });
      this.newTodo = "";
      this.idForTodo++;
    },
    removeTodo(index) {
      this.todos.splice(index, 1);
    },
    doneEdit(todo) {
      if (todo.title.trim() == "") {
        todo.title = this.beforeEditCache;
      }
      todo.editing = false;
    },
    editTodo(todo) {
      this.beforeEditCache = todo.title;
      todo.editing = true;
    },
    cancelEdit(todo) {
      todo.title = this.beforeEditCache;
      todo.editing = false;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url("../global.css");
/* .todo-input{
    width: 75%;
    padding: 10px 18px;
    font-size: 18px;
    margin-bottom: 16px;
} */
.todo-item {
  margin-bottom: 12px;
  margin-left: 75px;
  display: flex;
  align-items: center;
  justify-content: left;
}
.remove-item {
  cursor: pointer;
  margin-left: 14px;
  color: #ff8d5d;
  &:hover {
    color: black;
  }
}
.todo-item-left {
  display: flex;
  align-items: center;
}
.todo-item-label {
  padding: 0px;
  border: 1px solid white;
  margin-left: 12px;
}
.todo-item-edit {
  font-size: 18px;
  color: #ff8d5d;
  margin-left: 12px;
  width: 75%;
  padding: 0px;
  /* border:1px solid #FF8D5D; */
  &:focus {
    outline: none;
  }
}
.completed {
  text-decoration: line-through;
  color: #ff8d5d;
}
.semi-title {
  display: flex;
  align-content: left;
}
.newTask {
  color: #ff8d5d;
  padding: 0px;
  border: 1px dashed #ff8d5d;
  background-color: white;
  width: 75%;
  border-radius: 21px;
  font-size: 30px;
}
.newTask:hover {
  background-color: #ff8d5d;
  border: 1px dashed white;
  color: white;
}
/* .check{
    background-color:#FF8D5D
}
.check input:checked ~ .check:after {
    background-color:#FF8D5D
} */
</style>
