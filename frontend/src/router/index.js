import { createRouter, createWebHistory } from "vue-router";
import TodoList from "@/views/TodoList.vue";
import TodoDetail from "@/views/TodoDetail.vue";
import TodoForm from "@/views/TodoForm.vue";

const routes = [
  { path: "/", redirect: "/todos" },
  { path: "/todos", name: "todo-list", component: TodoList },
  { path: "/todos/create", name: "todo-create", component: TodoForm },
  { path: "/todos/:id", name: "todo-detail", component: TodoDetail },
  { path: "/todos/:id/edit", name: "todo-edit", component: TodoForm },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
