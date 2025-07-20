<template>
  <div class="todo-detail"
       v-if="todo">
    <h1>{{ todo.title }}</h1>

    <el-tag :type="todo.completed ? 'success' : 'danger'"
            size="large">
      {{ todo.completed ? '已完成' : '未完成' }}
    </el-tag>

    <div class="content">
      <p>{{ todo.description || '暂无描述' }}</p>

      <div class="meta">
        <div>创建时间: {{ formatDate(todo.created_at) }}</div>
        <div>更新时间: {{ formatDate(todo.updated_at) }}</div>
      </div>
    </div>

    <div class="actions">
      <el-button type="primary"
                 @click="editTodo">编辑</el-button>
      <el-button @click="goBack">返回列表</el-button>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTodoStore } from '@/store/todo'

export default {
  setup() {
    const route = useRoute()
    const router = useRouter()
    const todoStore = useTodoStore()

    // 加载数据
    todoStore.fetchTodo(route.params.id)

    const todo = computed(() => todoStore.currentTodo)

    const formatDate = (timestamp) => {
      return new Date(timestamp * 1000).toLocaleString()
    }

    const editTodo = () => {
      router.push({
        name: 'todo-edit',
        params: { id: route.params.id }
      })
    }

    const goBack = () => router.push({ name: 'todo-list' })

    return {
      todo,
      formatDate,
      editTodo,
      goBack
    }
  }
}
</script>

<style scoped>
.content {
  margin: 20px 0;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 4px;
}

.meta div {
  margin: 5px 0;
  color: #888;
  font-size: 14px;
}

.actions {
  margin-top: 20px;
}
</style>
