import axios from "axios";

const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_BASE_URL}${import.meta.env.VITE_API_PREFIX}`,
  headers: { "Content-Type": "application/json" },
});

export default {
  // 创建 Todo
  createTodo(todoData) {
    return api.post("/todos", todoData);
  },

  // 获取单个 Todo
  getTodoById(id) {
    return api.get(`/todos/${id}`);
  },

  // 分页获取列表
  getTodos(page = 1, size = 10) {
    return api.get("/todos/", { params: { page, size } });
  },

  // 更新 Todo
  updateTodo(id, updateData) {
    return api.put(`/todos/${id}`, updateData);
  },

  // 删除 Todo
  deleteTodo(id) {
    return api.delete(`/todos/${id}`);
  },
};
