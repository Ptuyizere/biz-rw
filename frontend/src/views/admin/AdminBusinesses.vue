<template>
  <div class="p-8">
    <h1 class="font-display text-3xl font-bold text-rw-dark mb-8">Manage Businesses</h1>
    <div v-if="loading" class="space-y-3"><div v-for="i in 5" :key="i" class="h-14 rounded-xl skeleton"></div></div>
    <div v-else class="card overflow-x-auto">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-100">
          <tr>
            <th class="text-left py-3 px-4 text-gray-500 font-semibold">Business</th>
            <th class="text-left py-3 px-4 text-gray-500 font-semibold">Category</th>
            <th class="text-left py-3 px-4 text-gray-500 font-semibold">City</th>
            <th class="text-left py-3 px-4 text-gray-500 font-semibold">Status</th>
            <th class="text-left py-3 px-4 text-gray-500 font-semibold">Featured</th>
            <th class="text-left py-3 px-4 text-gray-500 font-semibold">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="b in businesses" :key="b.id" class="border-b border-gray-50 hover:bg-gray-50">
            <td class="py-3 px-4">
              <RouterLink :to="`/b/${b.slug}`" target="_blank" class="font-semibold text-rw-green-700 hover:underline">{{ b.name }}</RouterLink>
              <p class="text-xs text-gray-400">{{ b.slug }}</p>
            </td>
            <td class="py-3 px-4 text-gray-500">{{ b.category }}</td>
            <td class="py-3 px-4 text-gray-500">{{ b.city || '—' }}</td>
            <td class="py-3 px-4">
              <span class="badge" :class="b.is_active ? 'badge-green' : 'bg-red-100 text-red-700'">
                {{ b.is_active ? 'Active' : 'Hidden' }}
              </span>
            </td>
            <td class="py-3 px-4">
              <span class="badge" :class="b.is_featured ? 'badge-gold' : 'badge-gray'">
                {{ b.is_featured ? '⭐ Yes' : 'No' }}
              </span>
            </td>
            <td class="py-3 px-4">
              <div class="flex gap-2">
                <button @click="toggleActive(b)" class="text-xs px-2 py-1 rounded-lg transition-colors" :class="b.is_active ? 'bg-red-50 text-red-600 hover:bg-red-100' : 'bg-green-50 text-green-700 hover:bg-green-100'">
                  {{ b.is_active ? 'Hide' : 'Show' }}
                </button>
                <button @click="toggleFeatured(b)" class="text-xs px-2 py-1 rounded-lg bg-yellow-50 text-yellow-700 hover:bg-yellow-100 transition-colors">
                  {{ b.is_featured ? 'Unfeature' : 'Feature' }}
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api'
import { useToastStore } from '@/stores/toast'

const toast = useToastStore()
const businesses = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await adminApi.listBusinesses()
    businesses.value = data
  } finally {
    loading.value = false
  }
})

async function toggleActive(b) {
  try {
    const { data } = await adminApi.toggleBusinessActive(b.slug)
    const idx = businesses.value.findIndex(x => x.slug === b.slug)
    if (idx !== -1) businesses.value[idx].is_active = data.is_active
    toast.success('Updated.')
  } catch { toast.error('Failed.') }
}

async function toggleFeatured(b) {
  try {
    const { data } = await adminApi.toggleBusinessFeatured(b.slug)
    const idx = businesses.value.findIndex(x => x.slug === b.slug)
    if (idx !== -1) businesses.value[idx].is_featured = data.is_featured
    toast.success('Updated.')
  } catch { toast.error('Failed.') }
}
</script>
