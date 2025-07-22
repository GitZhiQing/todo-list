<template>
  <el-container class="root-container">
    <el-header class="fixed-header">
      <div class="header-inner">
        <app-title />
      </div>
    </el-header>
    <el-main class="main-content">
      <app-sections />
    </el-main>
  </el-container>
</template>

<script setup>
import AppTitle from './components/AppTitle.vue'
import AppSections from './components/AppSections.vue'
import { useTodoStore } from '@/store/todo'
import { onMounted } from 'vue'

const store = useTodoStore()
onMounted(() => store.fetchTodos())
</script>

<style scoped>
.fixed-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  height: 60px;
  line-height: 60px;
  background: #019587;
  color: #fafdfd;
  border-bottom: 1px solid var(--el-border-color-light);
}

.header-inner {
  max-width: 100%;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
}

.main-content {
  padding-top: 60px;
  width: 60%;
  max-width: 800px;
  margin: 0 auto;
}
</style>
