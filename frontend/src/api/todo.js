import axios from "axios";
import { ElLoading } from "element-plus";

// 创建 axios 实例
const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_BASE_URL}${import.meta.env.VITE_API_PREFIX}`,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: import.meta.env.VITE_API_TIMEOUT || 10000, // 超时时间
});

let loadingInstance = null;

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 防止 GET 请求缓存
    if (config.method === "get") {
      const now = new Date().getTime();
      config.url += (config.url.includes("?") ? "&" : "?") + `_=${now}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    const { code, msg, data } = response.data;

    // 判断后端返回的 code 是否为成功状态
    if (code !== 200 && code !== 201 && code !== 204) {
      console.error(`API Error: [${code}] ${msg}`);
      if (code === 404) {
        window.location.href = "/404";
      }
      if (code === 500) {
        window.location.href = "/500";
      }
      return Promise.reject(new Error(msg || "未知错误"));
    }

    return data;
  },
  (error) => {
    console.error("网络请求异常:", error.message);
    return Promise.reject(error);
  }
);

export default {
  /**
   * 创建 Todo
   * @param {Object} todoData
   * @returns {Promise}
   */
  createTodo(todoData) {
    return api.post("/todos", todoData);
  },

  /**
   * 获取单个 Todo
   * @param {Number} id
   * @returns {Promise}
   */
  getTodoById(id) {
    return api.get(`/todos/${id}`);
  },

  /**
   * 分页获取 Todo 列表
   * @param {Number} page
   * @param {Number} size
   * @returns {Promise}
   */
  getTodos(page = 1, size = 10) {
    return api.get("/todos/", {
      params: { page, size },
    });
  },

  /**
   * 更新 Todo
   * @param {Number} id
   * @param {Object} updateData
   * @returns {Promise}
   */
  updateTodo(id, updateData) {
    return api.put(`/todos/${id}`, updateData);
  },

  /**
   * 删除 Todo
   * @param {Number} id
   * @returns {Promise}
   */
  deleteTodo(id) {
    return api.delete(`/todos/${id}`);
  },
};
