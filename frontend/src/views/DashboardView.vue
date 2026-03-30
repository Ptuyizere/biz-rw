<template>
  <div class="min-h-screen bg-gray-50 py-10">
    <div class="page-container">
      <!-- Welcome header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-10">
        <div>
          <h1 class="font-display text-3xl font-bold text-rw-dark">
            Good {{ greeting }}, {{ auth.user?.full_name?.split(' ')[0] }} 👋
          </h1>
          <p class="text-gray-500 mt-1">Here's an overview of your business.</p>
        </div>
        <RouterLink v-if="business" :to="`/b/${business.slug}`" target="_blank" class="btn-secondary text-sm gap-2">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
          View Public Page
        </RouterLink>
      </div>

      <!-- No business setup prompt -->
      <div v-if="!loading && !business" class="card p-12 text-center max-w-2xl mx-auto">
        <div class="w-20 h-20 bg-rw-green-50 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-10 h-10 text-rw-green-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        </div>
        <h2 class="font-display text-2xl font-bold text-rw-dark mb-3">Set up your business profile</h2>
        <p class="text-gray-500 mb-8 leading-relaxed">
          You don't have a business profile yet. Create one now to get your biz.rw page and start reaching customers.
        </p>
        <RouterLink to="/dashboard/setup" class="btn-primary text-base px-8 py-3.5">
          Create My Business Profile →
        </RouterLink>
      </div>

      <!-- Dashboard with business -->
      <template v-else-if="business">
        <!-- Stats cards -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div class="card p-5">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm font-medium text-gray-500">Profile Views</p>
              <div class="w-9 h-9 bg-blue-50 rounded-xl flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
              </div>
            </div>
            <p class="font-display text-3xl font-bold text-rw-dark">{{ analytics?.total_views ?? business.view_count }}</p>
          </div>
          <div class="card p-5">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm font-medium text-gray-500">Bookings</p>
              <div class="w-9 h-9 bg-rw-green-50 rounded-xl flex items-center justify-center">
                <svg class="w-5 h-5 text-rw-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
              </div>
            </div>
            <p class="font-display text-3xl font-bold text-rw-dark">{{ analytics?.total_bookings ?? 0 }}</p>
            <p v-if="analytics?.unread_bookings" class="text-xs text-rw-gold-600 font-semibold mt-1">{{ analytics.unread_bookings }} unread</p>
          </div>
          <div class="card p-5">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm font-medium text-gray-500">Reviews</p>
              <div class="w-9 h-9 bg-rw-gold-50 rounded-xl flex items-center justify-center">
                <svg class="w-5 h-5 text-rw-gold-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" /></svg>
              </div>
            </div>
            <p class="font-display text-3xl font-bold text-rw-dark">{{ analytics?.total_feedback ?? 0 }}</p>
            <p v-if="analytics?.avg_rating" class="text-xs text-rw-gold-600 font-semibold mt-1">★ {{ analytics.avg_rating }} avg</p>
          </div>
          <div class="card p-5">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm font-medium text-gray-500">Pending</p>
              <div class="w-9 h-9 bg-orange-50 rounded-xl flex items-center justify-center">
                <svg class="w-5 h-5 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              </div>
            </div>
            <p class="font-display text-3xl font-bold text-rw-dark">{{ analytics?.pending_bookings ?? 0 }}</p>
            <p class="text-xs text-gray-400 mt-1">Awaiting response</p>
          </div>
        </div>

        <!-- Quick actions -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <RouterLink to="/dashboard/edit" class="card p-5 flex items-center gap-4 hover:border-rw-green-400 group">
            <div class="w-11 h-11 bg-rw-green-50 rounded-xl flex items-center justify-center group-hover:bg-rw-green-100 transition-colors">
              <svg class="w-6 h-6 text-rw-green-700" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
            </div>
            <div>
              <p class="font-semibold text-rw-dark">Edit Profile</p>
              <p class="text-xs text-gray-400">Update your info & template</p>
            </div>
            <svg class="w-5 h-5 text-gray-300 ml-auto group-hover:text-rw-green-700 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
          </RouterLink>

          <RouterLink to="/dashboard/bookings" class="card p-5 flex items-center gap-4 hover:border-rw-green-400 group">
            <div class="w-11 h-11 bg-blue-50 rounded-xl flex items-center justify-center group-hover:bg-blue-100 transition-colors">
              <svg class="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
            </div>
            <div>
              <p class="font-semibold text-rw-dark">Manage Bookings</p>
              <p class="text-xs text-gray-400">Confirm or cancel requests</p>
            </div>
            <svg class="w-5 h-5 text-gray-300 ml-auto group-hover:text-rw-green-700 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
          </RouterLink>

          <RouterLink to="/dashboard/analytics" class="card p-5 flex items-center gap-4 hover:border-rw-green-400 group">
            <div class="w-11 h-11 bg-purple-50 rounded-xl flex items-center justify-center group-hover:bg-purple-100 transition-colors">
              <svg class="w-6 h-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
            </div>
            <div>
              <p class="font-semibold text-rw-dark">View Analytics</p>
              <p class="text-xs text-gray-400">Insights & performance</p>
            </div>
            <svg class="w-5 h-5 text-gray-300 ml-auto group-hover:text-rw-green-700 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
          </RouterLink>
        </div>

        <!-- Recent activity -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Recent bookings -->
          <div class="card p-6">
            <div class="flex items-center justify-between mb-5">
              <h3 class="font-display font-semibold text-lg text-rw-dark">Recent Bookings</h3>
              <RouterLink to="/dashboard/bookings" class="text-xs text-rw-green-700 font-semibold hover:underline">View all →</RouterLink>
            </div>
            <div v-if="analytics?.recent_bookings?.length" class="space-y-3">
              <div v-for="b in analytics.recent_bookings.slice(0,5)" :key="b.id" class="flex items-center justify-between py-3 border-b border-gray-50 last:border-0">
                <div>
                  <p class="font-medium text-sm text-rw-dark">{{ b.visitor_name }}</p>
                  <p class="text-xs text-gray-400">{{ b.email }}</p>
                </div>
                <span class="badge text-xs" :class="statusBadge(b.status)">{{ b.status }}</span>
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-400 text-sm">No bookings yet.</div>
          </div>

          <!-- Recent reviews -->
          <div class="card p-6">
            <div class="flex items-center justify-between mb-5">
              <h3 class="font-display font-semibold text-lg text-rw-dark">Recent Reviews</h3>
            </div>
            <div v-if="analytics?.recent_feedback?.length" class="space-y-3">
              <div v-for="f in analytics.recent_feedback.slice(0,5)" :key="f.id" class="py-3 border-b border-gray-50 last:border-0">
                <div class="flex items-center justify-between mb-1">
                  <p class="font-medium text-sm text-rw-dark">{{ f.visitor_name }}</p>
                  <div class="text-rw-gold-400 text-sm">{{ '★'.repeat(f.rating) }}{{ '☆'.repeat(5 - f.rating) }}</div>
                </div>
                <p class="text-xs text-gray-500 line-clamp-2">{{ f.comment || 'No comment left.' }}</p>
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-400 text-sm">No reviews yet.</div>
          </div>
        </div>
      </template>

      <!-- Loading -->
      <div v-else class="space-y-4">
        <div class="grid grid-cols-4 gap-4">
          <div v-for="i in 4" :key="i" class="h-28 rounded-2xl skeleton"></div>
        </div>
        <div class="h-64 rounded-2xl skeleton"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { businessApi, analyticsApi } from '@/api'

const auth = useAuthStore()
const business = ref(null)
const analytics = ref(null)
const loading = ref(true)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'morning'
  if (h < 17) return 'afternoon'
  return 'evening'
})

function statusBadge(status) {
  return {
    pending: 'bg-yellow-100 text-yellow-700',
    confirmed: 'bg-green-100 text-green-700',
    cancelled: 'bg-red-100 text-red-700',
  }[status] || 'badge-gray'
}

onMounted(async () => {
  try {
    const { data } = await businessApi.getMyBusiness()
    business.value = data
    const { data: an } = await analyticsApi.get(data.slug)
    analytics.value = an
  } catch {
    // no business yet
  } finally {
    loading.value = false
  }
})
</script>
