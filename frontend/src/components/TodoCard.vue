<template>
  <el-card shadow="hover"
           class="todo-card">
    <template #header>
      <div class="card-header">
        <el-tag :type="todo.completed ? 'success' : 'danger'">
          {{ todo.completed ? '完成' : '未完成' }}
        </el-tag>
        <h3>{{ todo.title }}</h3>
      </div>
    </template>

    <p>{{ todo.description || '暂无描述' }}</p>

    <div class="card-footer">
      <small>创建时间: {{ formatDate(todo.created_at) }}</small>
      <div>
        <el-button size="small"
                   @click="$emit('edit', todo)">编辑</el-button>
        <el-button size="small"
                   type="danger"
                   @click="$emit('delete', todo.id)">删除</el-button>
      </div>
    </div>
  </el-card>
</template>

<script>
export default {
  props: ['todo'],
  methods: {
    formatDate(timestamp) {
      return new Date(timestamp * 1000).toLocaleString()
    }
  }
}
</script>

<style scoped>
.todo-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
}
</style>
