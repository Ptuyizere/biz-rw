<template>
  <div class="min-h-screen bg-gray-50 py-10">
    <div class="page-container">
      <div class="flex items-center gap-4 mb-8">
        <RouterLink to="/dashboard" class="btn-ghost text-sm"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg> Dashboard</RouterLink>
        <h1 class="font-display text-2xl font-bold text-rw-dark">Analytics</h1>
      </div>

      <div v-if="loading" class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div v-for="i in 4" :key="i" class="h-28 rounded-2xl skeleton"></div>
      </div>

      <template v-else-if="analytics">
        <!-- Stats Grid -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div class="card p-5" v-for="stat in statCards" :key="stat.label">
            <p class="text-sm font-medium text-gray-500 mb-1">{{ stat.label }}</p>
            <p class="font-display text-4xl font-bold" :class="stat.color">{{ stat.value }}</p>
            <p v-if="stat.sub" class="text-xs text-gray-400 mt-1">{{ stat.sub }}</p>
          </div>
        </div>

        <!-- Recent Bookings Table -->
        <div class="card p-6 mb-6">
          <h2 class="font-display text-xl font-semibold mb-5">Recent Booking Requests</h2>
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="border-b border-gray-100">
                  <th class="text-left py-3 px-2 text-gray-500 font-semibold">Name</th>
                  <th class="text-left py-3 px-2 text-gray-500 font-semibold">Email</th>
                  <th class="text-left py-3 px-2 text-gray-500 font-semibold">Date</th>
                  <th class="text-left py-3 px-2 text-gray-500 font-semibold">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="b in analytics.recent_bookings" :key="b.id" class="border-b border-gray-50 hover:bg-gray-50">
                  <td class="py-3 px-2 font-medium text-rw-dark">{{ b.visitor_name }}</td>
                  <td class="py-3 px-2 text-gray-500">{{ b.email }}</td>
                  <td class="py-3 px-2 text-gray-500">{{ b.preferred_date || '—' }}</td>
                  <td class="py-3 px-2">
                    <span class="badge text-xs" :class="statusBadge(b.status)">{{ b.status }}</span>
                  </td>
                </tr>
                <tr v-if="!analytics.recent_bookings.length">
                  <td colspan="4" class="text-center py-8 text-gray-400">No bookings yet.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Recent Reviews -->
        <div class="card p-6">
          <h2 class="font-display text-xl font-semibold mb-5">Recent Reviews</h2>
          <div class="space-y-4">
            <div v-for="f in analytics.recent_feedback" :key="f.id" class="flex gap-4 py-4 border-b border-gray-50 last:border-0">
              <div class="w-10 h-10 bg-rw-green-50 rounded-full flex items-center justify-center font-display font-bold text-rw-green-700 flex-shrink-0">
                {{ f.visitor_name[0].toUpperCase() }}
              </div>
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-1">
                  <span class="font-semibold text-sm">{{ f.visitor_name }}</span>
                  <span class="text-rw-gold-400 text-sm">{{ '★'.repeat(f.rating) }}{{ '☆'.repeat(5-f.rating) }}</span>
                </div>
                <p class="text-sm text-gray-500">{{ f.comment || 'No comment.' }}</p>
              </div>
            </div>
            <div v-if="!analytics.recent_feedback.length" class="text-center py-8 text-gray-400">No reviews yet.</div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { businessApi, analyticsApi } from '@/api'

const analytics = ref(null)
const loading = ref(true)
const slug = ref('')

const statCards = computed(() => analytics.value ? [
  { label: 'Total Views', value: analytics.value.total_views, color: 'text-blue-600' },
  { label: 'Total Bookings', value: analytics.value.total_bookings, color: 'text-rw-green-700', sub: `${analytics.value.pending_bookings} pending` },
  { label: 'Reviews', value: analytics.value.total_feedback, color: 'text-rw-gold-600', sub: analytics.value.avg_rating ? `★ ${analytics.value.avg_rating} avg` : null },
  { label: 'Unread', value: analytics.value.unread_bookings, color: 'text-orange-500' },
] : [])

function statusBadge(status) {
  return { pending: 'bg-yellow-100 text-yellow-700', confirmed: 'bg-green-100 text-green-700', cancelled: 'bg-red-100 text-red-700' }[status] || 'badge-gray'
}

onMounted(async () => {
  try {
    const { data: biz } = await businessApi.getMyBusiness()
    slug.value = biz.slug
    const { data } = await analyticsApi.get(biz.slug)
    analytics.value = data
  } finally {
    loading.value = false
  }
})
</script>
