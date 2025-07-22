import { defineStore } from "pinia";
import { ElMessage } from "element-plus";
import todoApi from "@/api/todo";

export const useTodoStore = defineStore("todo", {
  state: () => ({
    todos: [],
    currentTodo: null,
    pagination: { page: 1, size: 10, total: 0 },
    loading: false,
    keyword: "", // 搜索关键字
    completed: undefined, // 筛选状态
  }),

  getters: {
    totalPages: (state) => Math.ceil(state.pagination.total / state.pagination.size),
  },

  actions: {
    /**
     * 设置 loading
     */
    setLoading(flag) {
      this.loading = flag;
    },

    /**
     * 统一处理异常
     */
    handleError(err) {
      ElMessage.error(err?.message || "操作失败");
      console.error(err);
    },

    /**
     * 分页获取列表
     */
    async fetchTodos() {
      this.setLoading(true);
      try {
        const { items, total } = await todoApi.getTodos({
          page: this.pagination.page,
          size: this.pagination.size,
          keyword: this.keyword,
          completed: this.completed,
        });
        this.todos = items || [];
        this.pagination.total = total || 0;
      } catch (e) {
        this.handleError(e);
      } finally {
        this.setLoading(false);
      }
    },

    /**
     * 切换页码
     */
    setPage(page) {
      this.pagination.page = page;
      this.fetchTodos();
    },

    /**
     * 切换每页条数
     */
    setSize(size) {
      this.pagination.size = size;
      this.pagination.page = 1;
      this.fetchTodos();
    },

    /**
     * 设置关键字
     */
    setKeyword(keyword) {
      this.keyword = keyword;
      this.pagination.page = 1;
      this.fetchTodos();
    },

    /**
     * 设置完成状态筛选
     */
    setCompletedFilter(status) {
      this.completed = status;
      this.pagination.page = 1;
      this.fetchTodos();
    },

    /**
     * 获取单个
     */
    async fetchTodo(id) {
      try {
        this.currentTodo = await todoApi.getTodoById(id, { showLoading: false });
      } catch (e) {
        this.handleError(e);
      }
    },

    /**
     * 创建
     */
    async createTodo(todoData) {
      try {
        const newTodo = await todoApi.createTodo(todoData, { showLoading: false });
        this.todos.unshift(newTodo);
        this.pagination.total += 1;
        return newTodo;
      } catch (e) {
        this.handleError(e);
      }
    },

    /**
     * 更新
     */
    async updateTodo(id, updateData) {
      try {
        const updated = await todoApi.updateTodo(id, updateData, { showLoading: false });
        const idx = this.todos.findIndex((t) => t.id === id);
        if (idx > -1) this.todos[idx] = { ...this.todos[idx], ...updated };
        return updated;
      } catch (e) {
        this.handleError(e);
      }
    },

    /**
     * 删除
     */
    async deleteTodo(id) {
      try {
        await todoApi.deleteTodo(id, { showLoading: false });
        this.todos = this.todos.filter((t) => t.id !== id);
        this.pagination.total -= 1;
      } catch (e) {
        this.handleError(e);
      }
    },

    ///**
    // * 批量删除
    // */
    //async batchDelete(ids) {
    //  try {
    //    await todoApi.batchDelete(ids, { showLoading: false });
    //    this.todos = this.todos.filter((t) => !ids.includes(t.id));
    //    this.pagination.total -= ids.length;
    //  } catch (e) {
    //    this.handleError(e);
    //  }
    //},

    ///**
    // * 切换完成状态（乐观更新）
    // */
    //async toggleDone(id) {
    //  const idx = this.todos.findIndex((t) => t.id === id);
    //  if (idx === -1) return;
    //  const old = this.todos[idx].completed;
    //  this.todos[idx].completed = !old;
    //  try {
    //    await todoApi.toggleDone(id, !old, { showLoading: false });
    //  } catch (e) {
    //    this.todos[idx].completed = old; // 回滚
    //    this.handleError(e);
    //  }
    //},

    /**
     * 重置 store
     */
    resetStore() {
      this.$reset();
    },
  },
});
