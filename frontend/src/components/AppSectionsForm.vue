<template>
  <el-form @submit.prevent="add"
           class="todo-form">
    <el-form-item>
      <el-input v-model="newTodoTitle"
                placeholder="待办标题"
                maxlength="50"
                show-word-limit
                clearable />
    </el-form-item>
    <el-form-item>
      <el-input v-model="newTodoDescription"
                placeholder="待办描述"
                maxlength="200"
                style="width: 100%;"
                :autosize="{ minRows: 3, maxRows: 6 }"
                show-word-limit
                type="textarea"
                resize="none" />
    </el-form-item>
    <el-form-item>
      <el-row style="width: 100%">
        <el-col :span="12">
          <el-date-picker v-model="newTodoDeadline"
                          type="datetime"
                          placeholder="截止时间（可选）"
                          :disabled-date="disabledDate"
                          :shortcuts="shortcuts"
                          style="width: 100%" />
        </el-col>
        <el-col :span="12"
                style="text-align: right;">
          <el-button type="primary"
                     native-type="submit">添加</el-button>
        </el-col>
      </el-row>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref } from 'vue';
import { ElMessage } from 'element-plus'; // 导入 ElMessage

const newTodoTitle = ref('');
const newTodoDescription = ref('');
const newTodoDeadline = ref(null); // 新增 deadline 字
const emit = defineEmits(['add']);

// 禁用今天之前的日期
const disabledDate = (time) => {
  return time.getTime() < Date.now() - 86400000;
};

const shortcuts = [
  {
    text: '1小时后',
    value: () => {
      const date = new Date();
      date.setTime(date.getTime() + 3600 * 1000);
      return date;
    },
  },
  {
    text: '1天后',
    value: () => {
      const date = new Date();
      date.setTime(date.getTime() + 3600 * 1000 * 24);
      return date;
    },
  },
  {
    text: '1周后',
    value: () => {
      const date = new Date();
      date.setTime(date.getTime() + 3600 * 1000 * 24 * 7);
      return date;
    },
  }
];

function add() {
  if (!newTodoTitle.value.trim() || !newTodoDescription.value.trim()) {
    ElMessage.warning({
      message: '请填写标题和描述',
      duration: 2000 // 2秒后自动消失
    });
    return;
  }
  emit('add', {
    title: newTodoTitle.value,
    description: newTodoDescription.value,
    completed: false,
    deadline: newTodoDeadline.value ? Math.floor(newTodoDeadline.value.getTime() / 1000) : null // 转为时间戳
  });

  newTodoTitle.value = '';
  newTodoDescription.value = '';
  newTodoDeadline.value = null;
}
</script>

<style scoped></style>
