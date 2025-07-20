<template>
  <div class="todo-form">
    <h1>{{ isEditMode ? '编辑 Todo' : '创建 Todo' }}</h1>

    <el-form :model="form"
             label-width="80px"
             style="max-width: 600px;"
             ref="formRef">
      <el-form-item label="标题"
                    prop="title"
                    required>
        <el-input v-model="form.title"
                  placeholder="请输入标题" />
      </el-form-item>

      <el-form-item label="描述"
                    prop="description">
        <el-input v-model="form.description"
                  type="textarea"
                  placeholder="请输入描述"
                  :rows="4" />
      </el-form-item>

      <el-form-item v-if="isEditMode"
                    label="完成状态">
        <el-switch v-model="form.completed" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary"
                   @click="submitForm">提交</el-button>
        <el-button @click="cancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTodoStore } from '@/store/todo'
import { ElMessage } from 'element-plus'

export default {
  setup() {
    const route = useRoute()
    const router = useRouter()
    const todoStore = useTodoStore()
    const formRef = ref(null)

    const isEditMode = computed(() => route.name === 'todo-edit')
    const todoId = computed(() => route.params.id)

    // 表单数据
    const form = reactive({
      title: '',
      description: '',
      completed: false
    })

    // 如果是编辑模式，加载数据
    if (isEditMode.value) {
      onMounted(async () => {
        await todoStore.fetchTodo(todoId.value)
        Object.assign(form, todoStore.currentTodo)
      })
    }

    const submitForm = async () => {
      try {
        if (isEditMode.value) {
          await todoStore.updateTodo(todoId.value, form)
          ElMessage.success('更新成功')
        } else {
          await todoStore.createTodo(form)
          ElMessage.success('创建成功')
        }
        router.push({ name: 'todo-list' })
      } catch (error) {
        ElMessage.error('操作失败: ' + error.message)
      }
    }

    const cancel = () => router.go(-1)

    return {
      isEditMode,
      form,
      formRef,
      submitForm,
      cancel
    }
  }
}
</script>
