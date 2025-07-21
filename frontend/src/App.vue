<template>
  <app-title />
  <app-sections />
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
