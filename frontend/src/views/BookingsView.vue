<template>
  <div class="min-h-screen bg-gray-50 py-10">
    <div class="page-container">
      <div class="flex items-center gap-4 mb-8">
        <RouterLink to="/dashboard" class="btn-ghost text-sm"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg> Dashboard</RouterLink>
        <h1 class="font-display text-2xl font-bold text-rw-dark">Booking Requests</h1>
      </div>

      <!-- Filter tabs -->
      <div class="flex gap-2 mb-6">
        <button v-for="f in filters" :key="f.value" @click="activeFilter = f.value"
          class="px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 border"
          :class="activeFilter === f.value ? 'bg-rw-green-700 text-white border-rw-green-700' : 'bg-white text-gray-600 border-gray-200 hover:border-rw-green-400'"
        >
          {{ f.label }}
          <span v-if="f.count !== undefined" class="ml-1.5 bg-current/20 rounded-full px-1.5 py-0.5 text-xs">{{ f.count }}</span>
        </button>
      </div>

      <div v-if="loading" class="space-y-3">
        <div v-for="i in 5" :key="i" class="h-20 rounded-2xl skeleton"></div>
      </div>

      <div v-else-if="filteredBookings.length" class="space-y-3">
        <div v-for="b in filteredBookings" :key="b.id"
          class="card p-5 flex flex-col sm:flex-row sm:items-center gap-4"
          :class="{ 'border-l-4 border-rw-gold-400': !b.is_read }"
        >
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <p class="font-semibold text-rw-dark">{{ b.visitor_name }}</p>
              <span v-if="!b.is_read" class="badge bg-rw-gold-50 text-rw-gold-600 text-xs">New</span>
              <span class="badge text-xs" :class="statusBadge(b.status)">{{ b.status }}</span>
            </div>
            <div class="flex flex-wrap gap-3 text-xs text-gray-500">
              <span class="flex items-center gap-1"><svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>{{ b.email }}</span>
              <span v-if="b.phone" class="flex items-center gap-1"><svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>{{ b.phone }}</span>
              <span v-if="b.preferred_date" class="flex items-center gap-1"><svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>{{ b.preferred_date }}</span>
            </div>
            <p v-if="b.message" class="text-xs text-gray-400 mt-2 line-clamp-2 italic">"{{ b.message }}"</p>
          </div>
          <div class="flex gap-2 flex-shrink-0">
            <button @click="updateStatus(b, 'confirmed')" v-if="b.status === 'pending'"
              class="px-3 py-1.5 bg-green-600 text-white text-xs font-semibold rounded-lg hover:bg-green-700 transition-colors">
              ✓ Confirm
            </button>
            <button @click="updateStatus(b, 'cancelled')" v-if="b.status === 'pending'"
              class="px-3 py-1.5 bg-red-500 text-white text-xs font-semibold rounded-lg hover:bg-red-600 transition-colors">
              ✕ Cancel
            </button>
            <button @click="updateStatus(b, 'pending')" v-if="b.status !== 'pending'"
              class="px-3 py-1.5 bg-gray-200 text-gray-700 text-xs font-semibold rounded-lg hover:bg-gray-300 transition-colors">
              Reset
            </button>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-20 text-gray-400">
        <div class="text-5xl mb-4">📭</div>
        <p class="font-semibold text-rw-dark mb-2">No bookings found</p>
        <p class="text-sm">Bookings from your public page will appear here.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { businessApi, bookingApi } from '@/api'
import { useToastStore } from '@/stores/toast'

const toast = useToastStore()
const bookings = ref([])
const loading = ref(true)
const slug = ref('')
const activeFilter = ref('all')

const filters = computed(() => [
  { value: 'all', label: 'All', count: bookings.value.length },
  { value: 'pending', label: 'Pending', count: bookings.value.filter(b => b.status === 'pending').length },
  { value: 'confirmed', label: 'Confirmed', count: bookings.value.filter(b => b.status === 'confirmed').length },
  { value: 'cancelled', label: 'Cancelled', count: bookings.value.filter(b => b.status === 'cancelled').length },
])

const filteredBookings = computed(() => {
  if (activeFilter.value === 'all') return bookings.value
  return bookings.value.filter(b => b.status === activeFilter.value)
})

function statusBadge(status) {
  return { pending: 'bg-yellow-100 text-yellow-700', confirmed: 'bg-green-100 text-green-700', cancelled: 'bg-red-100 text-red-700' }[status] || 'badge-gray'
}

async function updateStatus(booking, status) {
  try {
    const { data } = await bookingApi.updateStatus(slug.value, booking.id, status)
    const idx = bookings.value.findIndex(b => b.id === booking.id)
    if (idx !== -1) bookings.value[idx] = data
    toast.success(`Booking ${status}!`)
  } catch {
    toast.error('Could not update booking status.')
  }
}

onMounted(async () => {
  try {
    const { data: biz } = await businessApi.getMyBusiness()
    slug.value = biz.slug
    const { data } = await bookingApi.list(biz.slug)
    bookings.value = data
  } finally {
    loading.value = false
  }
})
</script>
