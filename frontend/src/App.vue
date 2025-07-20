<template>
  <div class="app-container">
    <!-- 全局导航栏 -->
    <!-- 重构后的导航栏结构 -->
    <el-header class="app-header">
      <div class="header-content">
        <!-- Logo区域 -->
        <div class="logo-container">
          <router-link to="/todos"
                       class="logo">
            <h1>Todo List</h1>
          </router-link>
        </div>

        <!-- 导航链接容器 -->
        <div class="nav-container">
          <nav class="nav-links">
            <router-link to="/todos">任务列表</router-link>
            <router-link to="/todos/create">新建任务</router-link>
            <el-button type="primary"
                       @click="toggleDark()"
                       size="small"
                       class="theme-toggle">
              {{ isDark ? '亮色' : '暗黑' }}
            </el-button>
          </nav>
        </div>
      </div>
    </el-header>
    <!-- 主内容区域 -->
    <el-main class="app-main">
      <!-- 全局加载状态 -->
      <el-skeleton v-if="globalLoading"
                   :rows="6"
                   animated />

      <!-- 错误提示容器 -->
      <div v-if="globalError"
           class="error-container">
        <el-alert :title="globalError"
                  type="error"
                  show-icon />
        <div class="error-actions">
          <el-button @click="reloadPage"
                     type="primary">重新加载</el-button>
          <el-button @click="copyError"
                     plain>复制错误</el-button>
        </div>
      </div>

      <!-- 路由视图 -->
      <router-view v-slot="{ Component }">
        <transition name="fade"
                    mode="out-in">
          <component :is="Component"
                     :key="$route.path" />
        </transition>
      </router-view>
    </el-main>

    <!-- 全局页脚 -->
    <el-footer class="app-footer">
      <div>© 2025 Todo List App</div>
    </el-footer>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElIcon, ElButton, ElAlert } from 'element-plus'
import { useDark, useToggle } from '@vueuse/core'
import { Menu } from '@element-plus/icons-vue'
import { debounce } from 'lodash-es'

const isDark = useDark({
  storageKey: 'todo-list-theme',
  onChange: (isDark) => {
    document.body.classList.toggle('dark', isDark)
  }
})
const toggleDark = useToggle(isDark)

export default {
  name: 'App',
  components: {
    ElIcon,
    ElButton,
    ElAlert,
    ElMenu: Menu
  },
  setup() {
    const router = useRouter()
    const globalLoading = ref(false)
    const globalError = ref(null)
    const isMobile = ref(window.innerWidth < 768)
    const navVisible = ref(false)

    // 全局错误处理
    const handleGlobalError = (error) => {
      console.error('全局错误:', error)
      globalError.value = error.message || '发生未知错误'
      ElMessage.error(globalError.value)
    }

    // 页面重载
    const reloadPage = () => {
      globalError.value = null
      router.go(0)
    }

    // 错误信息复制
    const copyError = () => {
      navigator.clipboard.writeText(globalError.value)
      ElMessage.success('错误信息已复制到剪贴板')
    }

    // 导航切换
    const toggleNav = () => {
      navVisible.value = !navVisible.value
    }

    // 响应式处理
    const updateResponsive = debounce(() => {
      isMobile.value = window.innerWidth < 768
      if (!isMobile.value) navVisible.value = false
    }, 300)

    // 路由守卫
    const setupRouteGuards = () => {
      router.beforeEach(() => {
        globalLoading.value = true
      })
      router.afterEach(() => {
        globalLoading.value = false
      })
    }

    onMounted(() => {
      // 初始化路由守卫
      setupRouteGuards()

      // 添加全局错误监听
      router.onError(handleGlobalError)

      // 添加窗口大小监听器
      window.addEventListener('resize', updateResponsive)
    })

    onUnmounted(() => {
      window.removeEventListener('resize', updateResponsive)
    })

    return {
      globalLoading,
      globalError,
      reloadPage,
      copyError,
      isDark,
      toggleDark,
      isMobile,
      navVisible,
      toggleNav
    }
  }
}
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background-color: var(--el-color-primary);
  color: var(--el-text-color-primary);
  transition: background-color 0.3s ease;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.logo-container {
  flex-shrink: 0;
  padding: 10px 0;
}


.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  color: inherit;
  text-decoration: none;
}

.logo h1 {
  color: inherit;
  margin: 0;
  font-size: 1.5rem;
}

.nav-links {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;

  a {
    position: relative;
    padding: 8px 0;
    color: inherit;
    text-decoration: none;
    font-weight: 500;

    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      width: 0;
      height: 2px;
      background: currentColor;
      transition: width 0.3s ease;
    }

    &:hover::after {
      width: 100%;
    }
  }
}

.menu-button {
  display: none;
}

.app-main {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

.app-footer {
  background-color: var(--el-bg-color-overlay);
  color: var(--el-text-color-secondary);
  text-align: center;
  padding: 15px 0;
  border-top: 1px solid var(--el-border-color);
}

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 40px 0;
}

.error-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

/* 路由切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<style>
/* 全局样式 */
body {
  margin: 0;
  padding: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: var(--el-bg-color-overlay);
  transition: background-color 0.3s ease;
}

/* 暗色模式样式 */
.dark body {
  background-color: #1a1a1a;
  color: #ffffff;
}

.dark .app-header {
  background-color: #1a1a1a;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    padding: 10px 0;
  }

  .nav-links {
    margin-top: 10px;
  }

  .app-main {
    padding: 15px;
  }

  .menu-button {
    display: block;
  }
}
</style>
