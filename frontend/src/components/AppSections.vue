<template>
  <div class="sections-container">
    <div class="section-column">
      <app-sections-list headline="未完成"
                         :do-child="filters.beforeDo"
                         :collapsed="collapsedStatus.beforeDo"
                         @toggle-collapse="toggleCollapse('beforeDo')" />
    </div>
    <div class="section-column">
      <app-sections-list headline="已完成"
                         :do-child="filters.afterDo"
                         :collapsed="collapsedStatus.afterDo"
                         @toggle-collapse="toggleCollapse('afterDo')" />
    </div>
    <div class="form-container">
      <app-sections-form @add="fatherAdd" />
    </div>
  </div>
</template>

<script setup>
import { computed, reactive } from 'vue';
import AppSectionsList from './AppSectionsList.vue';
import AppSectionsForm from './AppSectionsForm.vue';
import { useTodoStore } from '@/store/todo';
import { ElMessage } from 'element-plus';

const store = useTodoStore();

// 折叠状态管理
const collapsedStatus = reactive({
  beforeDo: false,
  afterDo: false
});

const toggleCollapse = (type) => {
  collapsedStatus[type] = !collapsedStatus[type];
};

const fatherAdd = async (todoData) => {
  try {
    await store.createTodo(todoData);
    ElMessage.success('添加成功');
  } catch (error) {
    ElMessage.error(`添加失败: ${error.message}`);
  }
};
// 不再需要修改 filters 计算属性
const filters = computed(() => {
  return {
    beforeDo: store.todos.filter(item => !item.completed),
    afterDo: store.todos.filter(item => item.completed)
  };
});
</script>

<style scoped>
.sections-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-column {
  display: flex;
  flex-direction: column;
}
</style>
