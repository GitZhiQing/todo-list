<template>
  <div class="sections-container">
    <div class="section-column">
      <app-sections-list headline="未完成" :do-child="filters.beforeDo">
      </app-sections-list>
    </div>
    <div class="section-column">
      <app-sections-list headline="已完成" :do-child="filters.afterDo">
      </app-sections-list>
    </div>
    <div class="form-container">
      <app-sections-form @add="fatherAdd"></app-sections-form>
    </div>
  </div>
</template>

<style scoped>
.sections-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
  margin-bottom: 20px;
}

.section-column {
  display: flex;
  flex-direction: column;
}

.form-container {
  position: sticky;
  bottom: 0;
  background: white;
  padding: 15px;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  z-index: 10;
}
</style>

<script setup>
import { computed } from 'vue';
import AppSectionsList from './AppSectionsList.vue';
import AppSectionsForm from './AppSectionsForm.vue';
import { useTodoStore } from '@/store/todo';

const store = useTodoStore();

const filters = computed(() => {
  return {
    beforeDo: store.todos.filter(item => !item.completed),
    afterDo: store.todos.filter(item => item.completed)
  };
});

// 添加新 Todo
async function fatherAdd(todo) {
  await store.createTodo(todo);
}
</script>
