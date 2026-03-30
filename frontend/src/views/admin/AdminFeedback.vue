<template>
  <div class="p-8">
    <h1 class="font-display text-3xl font-bold text-rw-dark mb-8">Moderate Reviews</h1>
    <div v-if="loading" class="space-y-3"><div v-for="i in 5" :key="i" class="h-14 rounded-xl skeleton"></div></div>
    <div v-else class="space-y-3">
      <div v-for="f in feedback" :key="f.id" class="card p-4 flex items-start gap-4" :class="{ 'opacity-50': f.is_hidden }">
        <div class="w-10 h-10 rounded-full bg-rw-green-50 flex items-center justify-center font-display font-bold text-rw-green-700 flex-shrink-0">
          {{ f.visitor_name[0].toUpperCase() }}
        </div>
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 mb-1">
            <span class="font-semibold text-sm">{{ f.visitor_name }}</span>
            <span class="text-rw-gold-400 text-sm">{{ '★'.repeat(f.rating) }}{{ '☆'.repeat(5 - f.rating) }}</span>
            <span v-if="f.is_hidden" class="badge bg-red-100 text-red-600 text-xs">Hidden</span>
          </div>
          <p class="text-sm text-gray-500">{{ f.comment || 'No comment.' }}</p>
        </div>
        <button @click="toggleHide(f)" class="flex-shrink-0 text-xs px-3 py-1.5 rounded-lg transition-colors" :class="f.is_hidden ? 'bg-green-50 text-green-700 hover:bg-green-100' : 'bg-red-50 text-red-600 hover:bg-red-100'">
          {{ f.is_hidden ? 'Show' : 'Hide' }}
        </button>
      </div>
      <div v-if="!feedback.length" class="text-center py-16 text-gray-400">No reviews yet.</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api'
import { useToastStore } from '@/stores/toast'

const toast = useToastStore()
const feedback = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await adminApi.listFeedback()
    feedback.value = data
  } finally {
    loading.value = false
  }
})

async function toggleHide(f) {
  try {
    const { data } = await adminApi.toggleFeedbackHide(f.id)
    const idx = feedback.value.findIndex(x => x.id === f.id)
    if (idx !== -1) feedback.value[idx] = data
    toast.success(data.is_hidden ? 'Review hidden.' : 'Review visible.')
  } catch { toast.error('Failed.') }
}
</script>
