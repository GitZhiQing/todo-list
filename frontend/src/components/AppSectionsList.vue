<template>
  <el-card class="section-card"
           v-if="doChild.length"
           :shadow="'never'"
           :body-style="{ padding: '0' }">
    <template #header>
      <div class="section-title"
           @click="$emit('toggle-collapse')">
        {{ headline }} ({{ doChild.length }})
        <el-icon :class="['collapse-icon', { rotated: collapsed }]">
          <ArrowDown />
        </el-icon>
      </div>
    </template>

    <el-checkbox-group v-show="!collapsed">
      <transition-group name="slide-fade"
                        tag="div">
        <div v-for="todo in doChild"
             :key="todo.id"
             class="todo-item"
             @click.self="openDrawer(todo)">
          <!-- checkbox 部分 -->
          <el-checkbox v-model="todo.completed"
                       :disabled="isUpdating"
                       @change="handleToggleDone(todo)"
                       @click.stop>
            <!-- 阻止冒泡，避免触发抽屉 -->
            <span :class="{ completed: todo.completed }">
              {{ todo.title }}
            </span>
          </el-checkbox>

          <div class="tag-wrapper">
            <el-tag v-if="todo.deadline"
                    :type="deadlineStatus(todo)"
                    size="small">
              {{ formatDeadline(todo.deadline) }}
            </el-tag>
          </div>

          <el-button type="danger"
                     :icon="Delete"
                     link
                     :disabled="isUpdating"
                     @click="deleteTodo(todo.id)" />
        </div>
      </transition-group>
    </el-checkbox-group>
  </el-card>

  <el-drawer v-model="drawerVisible"
             title="待办详情"
             direction="rtl"
             size="400px"
             :before-close="handleClose">
    <el-form ref="editFormRef"
             :model="editForm"
             label-position="top"
             @submit.prevent="handleSave">
      <el-form-item label="标题">
        <el-input v-model="editForm.title" />
      </el-form-item>

      <el-form-item label="详情">
        <el-input v-model="editForm.description"
                  style="width: 100%"
                  :autosize="{ minRows: 6, maxRows: 12 }"
                  maxlength="200"
                  show-word-limit
                  type="textarea" />
      </el-form-item>

      <el-form-item label="截止时间">
        <el-date-picker v-model="editForm.deadline"
                        type="datetime"
                        placeholder="选择时间"
                        value-format="x"
                        style="width:100%" />
      </el-form-item>

      <div style="margin-bottom:16px;">
        <el-switch v-model="editForm.completed"
                   :active-value="true"
                   :inactive-value="false"
                   active-text="已完成"
                   inactive-text="未完成">
        </el-switch>
      </div>

      <el-form-item>
        <el-button type="primary"
                   native-type="submit">保存</el-button>
        <el-button @click="drawerVisible = false">取消</el-button>
      </el-form-item>
    </el-form>
  </el-drawer>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useTodoStore } from '@/store/todo';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Delete, ArrowDown } from '@element-plus/icons-vue' // 轮廓图标

const store = useTodoStore();
const isUpdating = ref(false);
const drawerVisible = ref(false);
const editFormRef = ref();
const editForm = reactive({
  id: null,
  title: '',
  description: '',
  deadline: null
});
defineProps({
  headline: String,
  doChild: Array,
  collapsed: Boolean
});
const rawForm = reactive({});
// 打开抽屉
function openDrawer(todo) {
  // 1. 填充表单
  Object.assign(editForm, {
    id: todo.id,
    title: todo.title,
    description: todo.description,
    deadline: todo.deadline ? todo.deadline * 1000 : null,
    completed: todo.completed
  });
  // 2. 深拷贝一份原始值作对比
  Object.assign(rawForm, JSON.parse(JSON.stringify(editForm)));

  drawerVisible.value = true;
}
function isFormDirty() {
  return (
    editForm.title !== rawForm.title ||
    editForm.description !== rawForm.description ||
    editForm.deadline !== rawForm.deadline ||
    editForm.completed !== rawForm.completed
  );
}
async function handleClose(done) {
  if (!isFormDirty()) {
    // 没改动，直接关
    done();
    return;
  }
  try {
    await ElMessageBox.confirm(
      '有未保存的修改，确定关闭吗？',
      '提示',
      { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
    );
    done(); // 用户点「确定」
  } catch {
    // 用户点「取消」，什么都不做
  }
}

async function handleSave() {
  try {
    isUpdating.value = true;
    await store.updateTodo(editForm.id, {
      title: editForm.title,
      description: editForm.description,
      deadline: editForm.deadline ? Math.floor(editForm.deadline / 1000) : null,
      completed: editForm.completed,          // ← 加这一行
      updated_at: Math.floor(Date.now() / 1000)
    });
    await store.fetchTodos();
    ElMessage.success('已更新');
    drawerVisible.value = false;
  } catch (e) {
    ElMessage.error(`更新失败：${e.message}`);
  } finally {
    isUpdating.value = false;
  }
}
defineEmits(['toggle-collapse']);
const formatDeadline = (timestamp) => {
  return new Date(timestamp * 1000).toLocaleString();
};
const deadlineStatus = (todo) => {
  if (!todo.deadline) return 'info';
  const now = Math.floor(Date.now() / 1000);
  if (todo.completed) return 'success';
  return todo.deadline < now ? 'danger' : 'warning';
};
const handleToggleDone = async (todo) => {
  const originalStatus = todo.completed;
  try {
    isUpdating.value = true;
    todo.completed = !originalStatus;

    await store.updateTodo(todo.id, {
      completed: todo.completed,
      updated_at: Math.floor(Date.now() / 1000)
    });

    await store.fetchTodos();
    ElMessage.success(`任务 ${todo.title} 已${todo.completed ? '完成' : '重新激活'}`);
  } catch (error) {
    todo.completed = originalStatus;
    ElMessage.error(`状态更新失败: ${error.message}`);
  } finally {
    isUpdating.value = false;
  }
};

const deleteTodo = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这条待办事项吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });
    await store.deleteTodo(id);
    ElMessage.success('删除成功');
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(`删除失败: ${error.message}`);
    }
  }
};
</script>

<style scoped>
.section-card {
  margin-bottom: 20px;
}

.section-title {
  font-size: 1rem;
  font-weight: bold;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}

.collapse-icon {
  transition: transform 0.3s;
}

.collapse-icon.rotated {
  transform: rotate(-90deg);
}

.todo-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.2rem 1rem;
  border: 0.5px solid var(--el-border-color-extra-light);
  cursor: pointer;
}

.todo-item:hover {
  border-color: var(--el-border-color-hover);
}

.tag-wrapper {
  font-family: monospace;
  margin-left: auto;
  margin-right: 1rem;
}

.completed {
  text-decoration: line-through;
  color: var(--el-text-color-secondary);
}
</style>
