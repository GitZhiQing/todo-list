import axios from "axios";
import { ElLoading } from "element-plus";

const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_BASE_URL}${import.meta.env.VITE_API_PREFIX}`,
  headers: { "Content-Type": "application/json" },
  timeout: Number(import.meta.env.VITE_API_TIMEOUT) || 10000,
});

let loadingInstance = null;

/**
 * 开启全屏 loading
 */
function startLoading() {
  if (loadingInstance) return;
  loadingInstance = ElLoading.service({ fullscreen: true });
}
/**
 * 关闭全屏 loading
 */
function closeLoading() {
  loadingInstance?.close();
  loadingInstance = null;
}

api.interceptors.request.use(
  (config) => {
    if (config.method === "get") {
      config.url += (config.url.includes("?") ? "&" : "?") + `_=${Date.now()}`;
    }
    if (config.showLoading !== false) startLoading();
    return config;
  },
  (error) => {
    closeLoading();
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => {
    closeLoading();
    const { code, msg, data } = response.data;
    if (![200, 201, 204].includes(code)) {
      if (code === 404) window.location.href = "/404";
      if (code === 500) window.location.href = "/500";
      return Promise.reject(new Error(msg || "未知错误"));
    }
    return data;
  },
  (error) => {
    closeLoading();
    return Promise.reject(error);
  }
);

export default {
  /**
   * 创建 Todo
   * @param { {title: string, content?: string, completed?: boolean} } todoData
   * @returns {Promise<Todo>}
   */
  createTodo(todoData, config = {}) {
    return api.post("/todos", todoData, config);
  },

  /**
   * 获取单个 Todo
   * @param {number} id
   * @returns {Promise<Todo>}
   */
  getTodoById(id, config = {}) {
    return api.get(`/todos/${id}`, config);
  },

  /**
   * 分页获取 Todo 列表
   * @param {number} page
   * @param {number} size
   * @param {string} keyword
   * @param {boolean} completed
   * @returns {Promise<{items: Todo[], total: number}>}
   */
  getTodos({ page = 1, size = 10, keyword = "", completed } = {}, config = {}) {
    return api.get("/todos", {
      params: { page, size, keyword, completed },
      ...config,
    });
  },

  /**
   * 更新 Todo
   * @param {number} id
   * @param {Partial<Todo>} updateData
   * @returns {Promise<Todo>}
   */
  updateTodo(id, updateData, config = {}) {
    return api.put(`/todos/${id}`, updateData, config);
  },

  /**
   * 删除 Todo
   * @param {number} id
   * @returns {Promise<void>}
   */
  deleteTodo(id, config = {}) {
    return api.delete(`/todos/${id}`, config);
  },

  ///**
  // * 批量删除
  // * @param {number[]} ids
  // * @returns {Promise<void>}
  // */
  //batchDelete(ids, config = {}) {
  //  return api.delete("/todos/batch", { data: { ids }, ...config });
  //},

  ///**
  // * 切换完成状态
  // * @param {number} id
  // * @param {boolean} completed
  // * @returns {Promise<Todo>}
  // */
  //toggleDone(id, completed, config = {}) {
  //  return api.patch(`/todos/${id}/done`, { completed }, config);
  //},
};
