<template>
  <div class="p-8">
    <h1 class="font-display text-3xl font-bold text-rw-dark mb-8">Admin Overview</h1>
    <div v-if="loading" class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div v-for="i in 4" :key="i" class="h-28 rounded-2xl skeleton"></div>
    </div>
    <div v-else class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      <div class="card p-5" v-for="s in statCards" :key="s.label">
        <p class="text-sm text-gray-500 mb-1">{{ s.label }}</p>
        <p class="font-display text-4xl font-bold" :class="s.color">{{ s.value }}</p>
      </div>
    </div>
    <div class="card p-6">
      <p class="text-gray-500 text-sm">Use the sidebar to manage users, businesses, and moderate content.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { adminApi } from '@/api'

const stats = ref(null)
const loading = ref(true)

const statCards = computed(() => stats.value ? [
  { label: 'Total Users', value: stats.value.total_users, color: 'text-blue-600' },
  { label: 'Businesses', value: stats.value.total_businesses, color: 'text-rw-green-700' },
  { label: 'Total Bookings', value: stats.value.total_bookings, color: 'text-orange-500' },
  { label: 'Reviews', value: stats.value.total_feedback, color: 'text-rw-gold-600' },
] : [])

onMounted(async () => {
  try {
    const { data } = await adminApi.stats()
    stats.value = data
  } finally {
    loading.value = false
  }
})
</script>
