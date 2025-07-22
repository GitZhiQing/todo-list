<template>
  <el-card class="section-card" v-if="doChild.length" :shadow="headline === '未完成' ? 'hover' : 'never'"
    :style="{ '--header-bg': headline === '未完成' ? '#f0f7ff' : '#f8f9fa' }">
    <template #header>
      <h2 :style="{ background: 'var(--header-bg)', padding: '10px', borderRadius: '4px' }">
        {{ headline }} ({{ doChild.length }})
      </h2>
    </template>
    <el-checkbox-group>
      <transition-group name="slide-fade" tag="div">
        <div v-for="todo in doChild" :key="todo.id" class="todo-item">
          <el-checkbox v-model="todo.completed" @change="(val) => handleToggleDone(todo, val)" :label="todo.title"
            :disabled="isUpdating" :loading="isUpdating">
            <span :class="{ completed: todo.completed }">
              <el-icon v-if="todo.completed" style="color: #67c23a; margin-right: 5px;">
                <Check />
              </el-icon>
              {{ todo.description }}
              <el-tag size="small" type="info" style="margin-left: 8px;">
                {{ formatTimestamp(todo.created_at) }}
              </el-tag>
            </span>
          </el-checkbox>
          <el-button size="small" type="danger" @click="deleteTodo(todo.id)" :icon="Delete" circle
            :disabled="isUpdating" />
        </div>
      </transition-group>
    </el-checkbox-group>
  </el-card>
</template>

<script setup>
import { ref } from 'vue';
import { useTodoStore } from '@/store/todo';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Check, Delete } from '@element-plus/icons-vue';

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
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.section-card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.todo-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 8px;
  transition: all 0.3s ease;
}

.todo-item:hover {
  background-color: #f9f9f9;
  transform: translateY(-2px);
}

.completed {
  text-decoration: line-through;
  color: #999;
}

/* 过渡动画 */
.slide-fade-enter-active {
  transition: all 0.3s ease;
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
