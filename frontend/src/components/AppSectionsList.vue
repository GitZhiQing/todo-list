<template>
  <el-card class="section-card"
           v-if="doChild.length">
    <template #header>
      <h2>{{ headline }}</h2>
    </template>
    <el-checkbox-group>
      <div v-for="todo in doChild"
           :key="todo.id"
           class="todo-item">
        <el-checkbox v-model="todo.completed"
                     @change="(val) => handleToggleDone(todo, val)"
                     :label="todo.title"
                     :disabled="isUpdating"
                     :loading="isUpdating">
          <span :class="{ completed: todo.completed }">
            {{ todo.description }}
            <el-tag size="small"
                    type="info">
              {{ formatTimestamp(todo.created_at) }}
            </el-tag>
          </span>
        </el-checkbox>
        <el-button size="small"
                   type="danger"
                   @click="deleteTodo(todo.id)"
                   icon="Delete"
                   circle
                   :disabled="isUpdating" />
      </div>
    </el-checkbox-group>
  </el-card>
</template>

<script setup>
import { ref } from 'vue';
import { useTodoStore } from '@/store/todo';
import { ElMessage, ElMessageBox } from 'element-plus';

const store = useTodoStore();
const isUpdating = ref(false);

defineProps({
  headline: String,
  doChild: Array
});

function formatTimestamp(timestamp) {
  if (!timestamp) return '未知时间';
  const date = new Date(timestamp * 1000);
  return date.toLocaleString();
}

async function handleToggleDone(todo) {
  let originalStatus; // 提升作用域到函数顶部
  try {
    isUpdating.value = true;
    const targetStatus = !todo.completed;
    originalStatus = todo.completed; // 保存原始状态
    todo.completed = targetStatus;

    const updateData = {
      completed: targetStatus,
      updated_at: Math.floor(Date.now() / 1000)
    };

    await store.updateTodo(todo.id, updateData);
    await store.fetchTodos();
    ElMessage.success(`任务已${targetStatus ? '完成' : '重新激活'}`);
  } catch (error) {
    console.error('状态更新失败:', error);
    todo.completed = originalStatus; // 使用保存的原始状态回滚
    ElMessage.error(`状态更新失败: ${error.message}`);
  } finally {
    isUpdating.value = false;
  }
}

// 删除确认优化
async function deleteTodo(id) {
  try {
    await ElMessageBox.confirm('确定要删除这条待办事项吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await store.deleteTodo(id)
    ElMessage.success('删除成功')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败: ' + error.message)
    }
  }
}
</script>

<style scoped>
.section-card {
  margin-bottom: 20px;
}

.todo-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.completed {
  text-decoration: line-through;
  color: #999;
}

/* 优化复选框样式 */
.el-checkbox {
  margin-right: 10px;
}
</style>
