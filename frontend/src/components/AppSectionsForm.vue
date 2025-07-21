<template>
  <form @submit.prevent="add">
    <input type="text"
           placeholder="任务标题"
           v-model="newTodoTitle">
    <input type="text"
           placeholder="任务描述"
           v-model="newTodoDescription">
    <button type="submit">添加</button>
  </form>
</template>

<script setup>
import { ref } from 'vue';

const newTodoTitle = ref('');
const newTodoDescription = ref('');
const emit = defineEmits(['add']);

function add() {
  if (!newTodoTitle.value.trim() || !newTodoDescription.value.trim()) {
    alert('请填写标题和描述');
    return;
  }
  emit('add', {
    title: newTodoTitle.value,
    description: newTodoDescription.value,
    completed: false // 确保新增项有默认状态
  });
  newTodoTitle.value = '';
  newTodoDescription.value = '';
}
</script>
