<template>
  <RouterLink
    :to="`/b/${business.slug}`"
    class="group block bg-white rounded-2xl overflow-hidden border border-gray-100 shadow-card hover:shadow-card-hover transition-all duration-300 hover:-translate-y-1"
  >
    <!-- Cover Image -->
    <div class="relative h-44 bg-gradient-to-br from-rw-green-700 to-rw-green-900 overflow-hidden">
      <img
        v-if="business.cover_url"
        :src="business.cover_url"
        :alt="business.name"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
      />
      <div v-else class="absolute inset-0 hero-pattern opacity-20"></div>

      <!-- Badges -->
      <div class="absolute top-3 left-3 flex gap-2">
        <span v-if="business.is_featured" class="badge bg-rw-gold-400 text-white">
          ⭐ Featured
        </span>
        <span class="badge" :class="business.category === 'product' ? 'bg-blue-500 text-white' : 'bg-rw-green-600 text-white'">
          {{ business.category === 'product' ? '📦 Products' : '🛠 Services' }}
        </span>
      </div>

      <!-- Logo -->
      <div class="absolute -bottom-5 left-4">
        <div class="w-12 h-12 rounded-xl bg-white shadow-card border-2 border-white overflow-hidden">
          <img v-if="business.logo_url" :src="business.logo_url" :alt="business.name" class="w-full h-full object-cover" />
          <div v-else class="w-full h-full flex items-center justify-center bg-rw-green-50">
            <span class="text-rw-green-700 font-display font-bold text-lg">{{ business.name[0] }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="pt-8 px-4 pb-4">
      <div class="flex items-start justify-between gap-2 mb-1">
        <h3 class="font-display font-semibold text-rw-dark text-lg leading-tight group-hover:text-rw-green-700 transition-colors line-clamp-1">
          {{ business.name }}
        </h3>
        <div v-if="business.avg_rating" class="flex items-center gap-1 flex-shrink-0">
          <span class="text-rw-gold-400 text-sm">★</span>
          <span class="text-sm font-semibold text-rw-dark">{{ business.avg_rating }}</span>
          <span class="text-xs text-gray-400">({{ business.feedback_count }})</span>
        </div>
      </div>

      <p v-if="business.city" class="text-xs text-gray-400 mb-2 flex items-center gap-1">
        <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
        {{ business.city }}
      </p>

      <p class="text-sm text-gray-500 line-clamp-2 leading-relaxed">
        {{ business.description || business.tagline || 'No description provided.' }}
      </p>

      <div class="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
        <div class="flex items-center gap-1 text-xs text-gray-400">
          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
          {{ business.view_count }} views
        </div>
        <span class="text-xs font-semibold text-rw-green-700 group-hover:underline">
          View profile →
        </span>
      </div>
    </div>
  </RouterLink>
</template>

<script setup>
defineProps({
  business: { type: Object, required: true },
})
</script>
