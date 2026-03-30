<template>
  <div class="p-8">
    <h1 class="font-display text-3xl font-bold text-rw-dark mb-8">Manage Users</h1>
    <div v-if="loading" class="space-y-3"><div v-for="i in 5" :key="i" class="h-14 rounded-xl skeleton"></div></div>
    <div v-else class="card overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-100">
          <tr>
            <th class="text-left py-3 px-4 text-gray-500 font-semibold">Name</th>
            <th class="text-left py-3 px-4 text-gray-500 font-semibold">Email</th>
            <th class="text-left py-3 px-4 text-gray-500 font-semibold">Role</th>
            <th class="text-left py-3 px-4 text-gray-500 font-semibold">Status</th>
            <th class="text-left py-3 px-4 text-gray-500 font-semibold">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in users" :key="u.id" class="border-b border-gray-50 hover:bg-gray-50">
            <td class="py-3 px-4 font-medium text-rw-dark">{{ u.full_name }}</td>
            <td class="py-3 px-4 text-gray-500">{{ u.email }}</td>
            <td class="py-3 px-4">
              <span class="badge" :class="u.is_admin ? 'bg-purple-100 text-purple-700' : 'badge-gray'">
                {{ u.is_admin ? 'Admin' : 'User' }}
              </span>
            </td>
            <td class="py-3 px-4">
              <span class="badge" :class="u.is_active ? 'badge-green' : 'bg-red-100 text-red-700'">
                {{ u.is_active ? 'Active' : 'Disabled' }}
              </span>
            </td>
            <td class="py-3 px-4">
              <div class="flex gap-2">
                <button @click="toggleActive(u)" class="text-xs px-2 py-1 rounded-lg transition-colors" :class="u.is_active ? 'bg-red-50 text-red-600 hover:bg-red-100' : 'bg-green-50 text-green-700 hover:bg-green-100'">
                  {{ u.is_active ? 'Disable' : 'Enable' }}
                </button>
                <button @click="toggleAdmin(u)" class="text-xs px-2 py-1 rounded-lg bg-purple-50 text-purple-700 hover:bg-purple-100 transition-colors">
                  {{ u.is_admin ? 'Remove Admin' : 'Make Admin' }}
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
const users = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await adminApi.listUsers()
    users.value = data
  } finally {
    loading.value = false
  }
})

async function toggleActive(u) {
  try {
    const { data } = await adminApi.toggleUserActive(u.id)
    const idx = users.value.findIndex(x => x.id === u.id)
    if (idx !== -1) users.value[idx] = data
    toast.success(`User ${data.is_active ? 'enabled' : 'disabled'}.`)
  } catch { toast.error('Failed to update user.') }
}

async function toggleAdmin(u) {
  try {
    const { data } = await adminApi.makeAdmin(u.id)
    const idx = users.value.findIndex(x => x.id === u.id)
    if (idx !== -1) users.value[idx] = data
    toast.success(`Admin status updated.`)
  } catch { toast.error('Failed to update user.') }
}
</script>
