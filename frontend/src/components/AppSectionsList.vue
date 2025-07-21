<template>
  <section v-if="doChild.length">
    <h2>{{ headline }}</h2>
    <ul>
      <li v-for="todo in doChild"
          :key="todo.id"
          :class="{ completed: todo.completed }">
        <label>
          <input type="checkbox"
                 v-model="todo.completed"
                 @change="toggleDone(todo)">
          <span>{{ todo.title }} - {{ todo.description }}</span>
          <small><span class="create-time">{{ formatTimestamp(todo.created_at) }}</span></small>
        </label>
        <button @click="deleteTodo(todo.id)">删除</button>
      </li>
    </ul>
  </section>
</template>

<script setup>
import { useTodoStore } from '@/store/todo';

const store = useTodoStore();
defineProps({
  headline: String,
  doChild: Array
});
function formatTimestamp(timestamp) {
  if (!timestamp) return '未知时间';
  const date = new Date(timestamp * 1000); // 注意：Unix 时间戳需要乘以1000
  return date.toLocaleString(); // 使用本地化格式，如：2023/5/15 14:30:00
}
async function toggleDone(todo) {
  const updateData = {
    completed: todo.completed // 使用正确的字段
  };
  await store.updateTodo(todo.id, updateData);
}

async function deleteTodo(id) {
  if (!confirm('确定要删除这条待办事项吗？')) return;
  try {
    await store.deleteTodo(id);
  } catch (error) {
    console.error(error);
    alert('删除失败，请重试');
  }
}
</script>
<style scoped>
.completed {
  text-decoration: line-through;
  color: #999;
  background-color: #f0f0f0;
}
</style>
