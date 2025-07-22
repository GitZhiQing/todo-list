<template>
  <div class="app-container">
    <el-container>
      <el-main>
        <app-title />
        <app-sections />
      </el-main>
    </el-container>
  </div>
</template>
<script setup>
import AppTitle from './components/AppTitle.vue';
import AppSections from './components/AppSections.vue';
import { useTodoStore } from '@/store/todo';
import { onMounted } from 'vue';

const store = useTodoStore();

onMounted(() => {
  store.fetchTodos(); // 组件挂载时获取初始数据
});
</script>
<style>
.app-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
</style>
