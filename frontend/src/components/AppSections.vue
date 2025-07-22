<template>
  <div>
    <app-sections-list headline="未完成"
                       :do-child="filters.beforeDo">
    </app-sections-list>
    <app-sections-list headline="已完成"
                       :do-child="filters.afterDo">
    </app-sections-list>
    <app-sections-form @add="fatherAdd"></app-sections-form>
  </div>
</template>

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
