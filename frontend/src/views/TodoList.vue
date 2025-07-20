<template>
  <div class="todo-list">
    <el-empty v-if="todos.length === 0"
              description="暂无数据" />

    <div v-else>
      <TodoCard v-for="todo in todos"
                :key="todo.id"
                :todo="todo"
                @edit="editTodo"
                @delete="deleteTodo" />

      <el-pagination background
                     layout="prev, pager, next"
                     :total="pagination.total"
                     :page-size="pagination.size"
                     :current-page="pagination.page"
                     @current-change="handlePageChange" />
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useTodoStore } from '@/store/todo'
import TodoCard from '@/components/TodoCard.vue'
import { ElMessageBox } from 'element-plus' // 新增导入

export default {
  components: { TodoCard },
  setup() {
    const router = useRouter()
    const todoStore = useTodoStore()

    // 初始化加载数据
    todoStore.fetchTodos()

    const todos = computed(() => todoStore.todos)
    const pagination = computed(() => todoStore.pagination)

    const goToCreate = () => router.push({ name: 'todo-create' })
    const editTodo = (todo) => router.push({
      name: 'todo-edit',
      params: { id: todo.id }
    })

    const deleteTodo = async (id) => {
      await ElMessageBox.confirm('确定删除该 Todo?', '警告', { // 直接使用导入的组件
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      todoStore.deleteTodo(id)
    }

    const handlePageChange = (page) => {
      todoStore.pagination.page = page
      todoStore.fetchTodos()
    }

    return {
      todos,
      pagination,
      goToCreate,
      editTodo,
      deleteTodo,
      handlePageChange
    }
  }
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>
