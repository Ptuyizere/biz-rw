<template>
  <div class="fixed bottom-6 right-6 z-[100] flex flex-col gap-3 pointer-events-none" style="max-width: 380px;">
    <TransitionGroup name="toast-list" tag="div" class="flex flex-col gap-3">
      <div
        v-for="toast in toastStore.toasts"
        :key="toast.id"
        class="toast pointer-events-auto flex items-start gap-3 px-4 py-3.5 rounded-2xl shadow-card-hover backdrop-blur-sm border text-sm font-medium"
        :class="typeClass(toast.type)"
      >
        <span class="flex-shrink-0 mt-0.5" v-html="icon(toast.type)"></span>
        <p class="flex-1 leading-relaxed">{{ toast.message }}</p>
        <button
          @click="toastStore.dismiss(toast.id)"
          class="flex-shrink-0 opacity-60 hover:opacity-100 transition-opacity"
        >
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { useToastStore } from '@/stores/toast'

const toastStore = useToastStore()

function typeClass(type) {
  return {
    success: 'bg-white border-green-200 text-green-800',
    error: 'bg-white border-red-200 text-red-800',
    info: 'bg-white border-blue-200 text-blue-800',
    warning: 'bg-white border-yellow-200 text-yellow-800',
  }[type] || 'bg-white border-gray-200 text-gray-800'
}

function icon(type) {
  const icons = {
    success: '<svg class="w-5 h-5 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
    error: '<svg class="w-5 h-5 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
    info: '<svg class="w-5 h-5 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
    warning: '<svg class="w-5 h-5 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>',
  }
  return icons[type] || icons.info
}
</script>

<style scoped>
.toast-list-enter-active,
.toast-list-leave-active {
  transition: all 0.3s ease;
}
.toast-list-enter-from {
  opacity: 0;
  transform: translateX(100%);
}
.toast-list-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
.toast-list-move {
  transition: transform 0.3s ease;
}
</style>
