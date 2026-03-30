<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Page Header -->
    <div class="gradient-hero hero-pattern py-16">
      <div class="page-container text-center">
        <h1 class="font-display text-4xl md:text-5xl font-bold text-white mb-4">
          Discover Rwandan Businesses
        </h1>
        <p class="text-white/70 text-lg mb-8 max-w-xl mx-auto">
          Find services and products from local entrepreneurs across Rwanda.
        </p>
        <!-- Search bar -->
        <div class="max-w-2xl mx-auto relative">
          <div class="flex gap-2 bg-white rounded-2xl p-2 shadow-luxury">
            <div class="flex-1 relative">
              <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                v-model="searchQuery"
                @keyup.enter="doSearch"
                type="text"
                placeholder="Search businesses, services, products..."
                class="w-full pl-10 pr-4 py-2.5 text-gray-800 focus:outline-none text-sm font-medium placeholder-gray-400"
              />
            </div>
            <button @click="doSearch" class="btn-primary rounded-xl py-2.5 px-6 text-sm">
              Search
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters + Results -->
    <div class="page-container py-10">
      <!-- Filter row -->
      <div class="flex flex-wrap items-center gap-3 mb-8">
        <span class="text-sm font-semibold text-gray-500">Filter:</span>
        <button
          v-for="cat in categories"
          :key="cat.value"
          @click="toggleCategory(cat.value)"
          class="px-4 py-2 rounded-full text-sm font-medium border transition-all duration-200"
          :class="activeCategory === cat.value
            ? 'bg-rw-green-700 text-white border-rw-green-700 shadow-luxury'
            : 'bg-white text-gray-600 border-gray-200 hover:border-rw-green-400 hover:text-rw-green-700'"
        >
          {{ cat.label }}
        </button>

        <div class="ml-auto flex items-center gap-2">
          <label class="text-sm text-gray-500">City:</label>
          <input
            v-model="cityFilter"
            @input="debouncedSearch"
            type="text"
            placeholder="Any city"
            class="px-3 py-2 rounded-xl border border-gray-200 text-sm focus:outline-none focus:border-rw-green-500 w-32"
          />
        </div>
      </div>

      <!-- Result count -->
      <div class="flex items-center justify-between mb-6">
        <p class="text-sm text-gray-500">
          <span v-if="!loading">Showing <span class="font-semibold text-rw-dark">{{ businesses.length }}</span> businesses</span>
          <span v-else>Loading…</span>
        </p>
        <div class="flex gap-2">
          <button
            v-for="view in ['grid', 'list']"
            :key="view"
            @click="viewMode = view"
            class="p-2 rounded-lg transition-colors"
            :class="viewMode === view ? 'bg-rw-green-700 text-white' : 'bg-white text-gray-400 hover:text-rw-green-700'"
          >
            <svg v-if="view === 'grid'" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
            <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" /></svg>
          </button>
        </div>
      </div>

      <!-- Loading skeleton -->
      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="i in 6" :key="i" class="rounded-2xl bg-gray-200 animate-pulse h-64"></div>
      </div>

      <!-- Grid view -->
      <div v-else-if="viewMode === 'grid' && businesses.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <BusinessCard v-for="b in businesses" :key="b.id" :business="b" />
      </div>

      <!-- List view -->
      <div v-else-if="viewMode === 'list' && businesses.length" class="flex flex-col gap-4">
        <RouterLink
          v-for="b in businesses"
          :key="b.id"
          :to="`/b/${b.slug}`"
          class="group bg-white rounded-2xl border border-gray-100 shadow-card hover:shadow-card-hover p-5 flex items-center gap-5 transition-all duration-300 hover:-translate-x-1"
        >
          <div class="w-16 h-16 rounded-xl bg-rw-green-50 flex-shrink-0 overflow-hidden border border-gray-100">
            <img v-if="b.logo_url" :src="b.logo_url" :alt="b.name" class="w-full h-full object-cover" />
            <div v-else class="w-full h-full flex items-center justify-center">
              <span class="font-display font-bold text-2xl text-rw-green-700">{{ b.name[0] }}</span>
            </div>
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-0.5">
              <h3 class="font-display font-semibold text-rw-dark group-hover:text-rw-green-700 transition-colors">{{ b.name }}</h3>
              <span v-if="b.is_featured" class="badge bg-rw-gold-50 text-rw-gold-600 text-xs">⭐ Featured</span>
            </div>
            <p class="text-sm text-gray-400 mb-2">{{ b.city }} · {{ b.category }}</p>
            <p class="text-sm text-gray-500 line-clamp-1">{{ b.description || b.tagline }}</p>
          </div>
          <div class="text-right flex-shrink-0">
            <div v-if="b.avg_rating" class="text-rw-gold-400 font-bold">★ {{ b.avg_rating }}</div>
            <div class="text-xs text-gray-400 mt-1">{{ b.view_count }} views</div>
          </div>
        </RouterLink>
      </div>

      <!-- Empty -->
      <div v-else-if="!loading" class="text-center py-24">
        <div class="text-6xl mb-4">🔍</div>
        <h3 class="font-display text-2xl font-semibold text-rw-dark mb-2">No businesses found</h3>
        <p class="text-gray-500 mb-6">Try adjusting your search or filters.</p>
        <button @click="resetFilters" class="btn-secondary">Clear Filters</button>
      </div>

      <!-- Load More -->
      <div v-if="businesses.length && !loading && hasMore" class="text-center mt-10">
        <button @click="loadMore" :disabled="loadingMore" class="btn-secondary min-w-[160px]">
          <span v-if="loadingMore" class="flex items-center gap-2">
            <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
            Loading…
          </span>
          <span v-else>Load More</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import BusinessCard from '@/components/BusinessCard.vue'
import { businessApi } from '@/api'

const businesses = ref([])
const loading = ref(true)
const loadingMore = ref(false)
const searchQuery = ref('')
const activeCategory = ref('')
const cityFilter = ref('')
const viewMode = ref('grid')
const page = ref(1)
const perPage = 12
const hasMore = ref(true)

const categories = [
  { value: '', label: 'All' },
  { value: 'service', label: '🛠 Services' },
  { value: 'product', label: '📦 Products' },
]

let debounceTimer = null
function debouncedSearch() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(doSearch, 500)
}

function toggleCategory(val) {
  activeCategory.value = activeCategory.value === val ? '' : val
  doSearch()
}

async function fetchBusinesses(reset = true) {
  if (reset) {
    loading.value = true
    page.value = 1
  } else {
    loadingMore.value = true
  }
  try {
    const params = {
      page: page.value,
      per_page: perPage,
    }
    if (searchQuery.value.trim()) params.search = searchQuery.value.trim()
    if (activeCategory.value) params.category = activeCategory.value
    if (cityFilter.value.trim()) params.city = cityFilter.value.trim()

    const { data } = await businessApi.list(params)
    if (reset) {
      businesses.value = data
    } else {
      businesses.value.push(...data)
    }
    hasMore.value = data.length === perPage
  } catch {
    // fail silently
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

function doSearch() {
  fetchBusinesses(true)
}

async function loadMore() {
  page.value++
  await fetchBusinesses(false)
}

function resetFilters() {
  searchQuery.value = ''
  activeCategory.value = ''
  cityFilter.value = ''
  doSearch()
}

onMounted(() => fetchBusinesses())
</script>
