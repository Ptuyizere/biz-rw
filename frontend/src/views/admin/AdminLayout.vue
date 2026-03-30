<template>
  <div class="min-h-screen flex bg-gray-50">
    <!-- Sidebar -->
    <aside class="w-56 bg-rw-dark flex-shrink-0 flex flex-col py-6 px-3 min-h-screen">
      <RouterLink to="/" class="flex items-center gap-2 px-3 mb-8">
        <div class="w-8 h-8 rounded-lg bg-rw-green-700 flex items-center justify-center">
          <span class="text-rw-gold-400 font-display font-bold text-sm">B</span>
        </div>
        <span class="font-display font-bold text-white text-lg">biz<span class="text-rw-gold-400">.rw</span></span>
      </RouterLink>
      <p class="px-3 text-xs uppercase tracking-widest text-gray-500 font-semibold mb-3">Admin Panel</p>
      <nav class="flex flex-col gap-1 flex-1">
        <RouterLink v-for="link in links" :key="link.to" :to="link.to"
          class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200"
          :class="$route.path === link.to || $route.path.startsWith(link.to + '/') ? 'bg-rw-green-700 text-white' : 'text-gray-400 hover:bg-white/10 hover:text-white'"
        >
          <span v-html="link.icon" class="w-4 h-4 flex-shrink-0"></span>
          {{ link.label }}
        </RouterLink>
      </nav>
      <div class="border-t border-gray-700 pt-4">
        <RouterLink to="/dashboard" class="flex items-center gap-3 px-3 py-2 rounded-xl text-sm text-gray-400 hover:text-white hover:bg-white/10 transition-all">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
          Back to Dashboard
        </RouterLink>
      </div>
    </aside>

    <!-- Main -->
    <main class="flex-1 overflow-auto">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
const links = [
  { to: '/admin', label: 'Overview', icon: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>' },
  { to: '/admin/users', label: 'Users', icon: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" /></svg>' },
  { to: '/admin/businesses', label: 'Businesses', icon: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5" /></svg>' },
  { to: '/admin/feedback', label: 'Feedback', icon: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" /></svg>' },
]
</script>
