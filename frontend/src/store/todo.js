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
      try {
        const data = await todoApi.getTodos(this.pagination.page, this.pagination.size);
        if (data && data.items) {
          this.todos = data.items;
          this.pagination.total = data.total;
        } else {
          console.error("API 返回数据异常:", data);
        }
      } catch (error) {
        console.error("获取 Todo 列表失败:", error);
      }
    },

    // 切换页码并刷新列表
    setPage(page) {
      this.pagination.page = page;
      this.fetchTodos();
    },

    // 切换每页数量并刷新列表
    setSize(size) {
      this.pagination.size = size;
      this.fetchTodos();
    },

    // 获取单个 Todo
    async fetchTodo(id) {
      const data = await todoApi.getTodoById(id);
      this.currentTodo = data;
    },

    // 创建 Todo
    async createTodo(todoData) {
      const data = await todoApi.createTodo(todoData);
      this.fetchTodos(); // 刷新列表
      return data;
    },

    // 更新 Todo
    async updateTodo(id, updateData) {
      const data = await todoApi.updateTodo(id, updateData);
      this.fetchTodos(); // 刷新列表
      return data;
    },
    // 删除 Todo
    async deleteTodo(id) {
      try {
        await todoApi.deleteTodo(id);
        this.fetchTodos(); // 成功后再刷新
      } catch (error) {
        console.error("删除 Todo 失败:", error);
      }
    },
  },
});
