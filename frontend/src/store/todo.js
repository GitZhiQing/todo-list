import { defineStore } from "pinia";
import todoApi from "@/api/todo";

export const useTodoStore = defineStore("todo", {
  state: () => ({
    todos: [],
    currentTodo: null,
    pagination: {
      page: 1,
      size: 10,
      total: 0,
    },
  }),

  actions: {
    // 获取分页列表
    async fetchTodos() {
      const { data } = await todoApi.getTodos(this.pagination.page, this.pagination.size);

      if (data.code === 200) {
        this.todos = data.data.items;
        this.pagination.total = data.data.total;
      }
    },

    // 获取单个 Todo
    async fetchTodo(id) {
      const { data } = await todoApi.getTodoById(id);
      if (data.code === 200) {
        this.currentTodo = data.data;
      }
    },

    // 创建 Todo
    async createTodo(todoData) {
      const { data } = await todoApi.createTodo(todoData);
      return data;
    },

    // 更新 Todo
    async updateTodo(id, updateData) {
      const { data } = await todoApi.updateTodo(id, updateData);
      return data;
    },

    // 删除 Todo
    async deleteTodo(id) {
      const { data } = await todoApi.deleteTodo(id);
      if (data.code === 204) {
        this.fetchTodos(); // 刷新列表
      }
    },
  },
});
