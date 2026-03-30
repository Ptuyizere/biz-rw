<template>
  <nav class="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-gray-100 shadow-sm">
    <div class="page-container">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center gap-2 group">
          <div class="w-8 h-8 rounded-lg bg-rw-green-700 flex items-center justify-center shadow-luxury group-hover:scale-105 transition-transform">
            <span class="text-rw-gold-400 font-display font-bold text-sm">B</span>
          </div>
          <span class="font-display font-bold text-xl text-rw-dark">
            biz<span class="text-rw-green-700">.rw</span>
          </span>
        </RouterLink>

        <!-- Desktop Nav -->
        <div class="hidden md:flex items-center gap-6">
          <RouterLink to="/explore" class="nav-link" :class="{ 'nav-link-active': $route.name === 'explore' }">
            Explore Businesses
          </RouterLink>
          <template v-if="auth.isLoggedIn">
            <RouterLink to="/dashboard" class="nav-link" :class="{ 'nav-link-active': $route.path.startsWith('/dashboard') }">
              Dashboard
            </RouterLink>
            <RouterLink v-if="auth.isAdmin" to="/admin" class="nav-link text-rw-gold-600">
              Admin
            </RouterLink>
          </template>
        </div>

        <!-- Right actions -->
        <div class="flex items-center gap-3">
          <template v-if="!auth.isLoggedIn">
            <RouterLink to="/login" class="btn-ghost hidden sm:inline-flex text-sm">Sign In</RouterLink>
            <RouterLink to="/register" class="btn-primary text-sm py-2 px-4">
              Get Started
            </RouterLink>
          </template>
          <template v-else>
            <div class="relative" ref="dropdownRef">
              <button
                @click="dropdownOpen = !dropdownOpen"
                class="flex items-center gap-2 px-3 py-2 rounded-xl hover:bg-gray-50 transition-colors"
              >
                <div class="w-8 h-8 bg-rw-green-700 rounded-full flex items-center justify-center text-white font-semibold text-sm">
                  {{ auth.user?.full_name?.[0]?.toUpperCase() }}
                </div>
                <span class="hidden sm:block text-sm font-medium text-rw-dark max-w-[120px] truncate">
                  {{ auth.user?.full_name }}
                </span>
                <svg class="w-4 h-4 text-gray-400 transition-transform" :class="{ 'rotate-180': dropdownOpen }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <Transition name="slide-up">
                <div v-if="dropdownOpen" class="absolute right-0 mt-2 w-52 bg-white rounded-2xl shadow-card-hover border border-gray-100 py-2 z-50">
                  <RouterLink to="/dashboard" @click="dropdownOpen = false" class="dropdown-item">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
                    Dashboard
                  </RouterLink>
                  <RouterLink to="/dashboard/analytics" @click="dropdownOpen = false" class="dropdown-item">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
                    Analytics
                  </RouterLink>
                  <RouterLink to="/dashboard/bookings" @click="dropdownOpen = false" class="dropdown-item">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                    Bookings
                  </RouterLink>
                  <div class="border-t border-gray-100 my-2"></div>
                  <button @click="handleLogout" class="dropdown-item text-red-600 w-full text-left">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
                    Sign Out
                  </button>
                </div>
              </Transition>
            </div>
          </template>

          <!-- Mobile menu button -->
          <button @click="mobileOpen = !mobileOpen" class="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path v-if="!mobileOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile menu -->
      <Transition name="slide-up">
        <div v-if="mobileOpen" class="md:hidden py-4 border-t border-gray-100">
          <div class="flex flex-col gap-1">
            <RouterLink to="/explore" @click="mobileOpen = false" class="mobile-nav-item">Explore Businesses</RouterLink>
            <template v-if="auth.isLoggedIn">
              <RouterLink to="/dashboard" @click="mobileOpen = false" class="mobile-nav-item">Dashboard</RouterLink>
              <RouterLink to="/dashboard/analytics" @click="mobileOpen = false" class="mobile-nav-item">Analytics</RouterLink>
              <RouterLink to="/dashboard/bookings" @click="mobileOpen = false" class="mobile-nav-item">Bookings</RouterLink>
              <RouterLink v-if="auth.isAdmin" to="/admin" @click="mobileOpen = false" class="mobile-nav-item text-rw-gold-600">Admin Panel</RouterLink>
              <button @click="handleLogout" class="mobile-nav-item text-red-600 text-left">Sign Out</button>
            </template>
            <template v-else>
              <RouterLink to="/login" @click="mobileOpen = false" class="mobile-nav-item">Sign In</RouterLink>
              <RouterLink to="/register" @click="mobileOpen = false" class="mobile-nav-item font-semibold text-rw-green-700">Get Started</RouterLink>
            </template>
          </div>
        </div>
      </Transition>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { onClickOutside } from '@vueuse/core'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'

const auth = useAuthStore()
const toast = useToastStore()
const router = useRouter()

const dropdownOpen = ref(false)
const mobileOpen = ref(false)
const dropdownRef = ref(null)

onClickOutside(dropdownRef, () => { dropdownOpen.value = false })

function handleLogout() {
  auth.logout()
  dropdownOpen.value = false
  mobileOpen.value = false
  toast.success('You have been signed out.')
  router.push('/')
}
</script>

<style scoped>
.dropdown-item {
  @apply flex items-center gap-2 px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 transition-colors cursor-pointer font-medium;
}
.mobile-nav-item {
  @apply px-3 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 rounded-lg transition-colors;
}
</style>
