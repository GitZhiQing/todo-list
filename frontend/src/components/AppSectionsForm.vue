<template>
  <el-form @submit.prevent="add"
           class="todo-form">
    <el-form-item>
      <el-input v-model="newTodoTitle"
                placeholder="任务标题"
                clearable />
    </el-form-item>
    <el-form-item>
      <el-input v-model="newTodoDescription"
                placeholder="任务描述"
                clearable
                type="textarea"
                :rows="2" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary"
                 native-type="submit">添加</el-button>
    </el-form-item>
  </el-form>
</template>

<style scoped>
.todo-form {
  margin: 20px 0;
  padding: 20px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>
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
