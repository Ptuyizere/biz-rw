<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Left panel (decorative) -->
    <div class="hidden lg:flex lg:w-1/2 gradient-hero hero-pattern flex-col justify-between p-16 relative overflow-hidden">
      <div class="absolute top-20 right-10 w-72 h-72 bg-rw-gold-400/10 rounded-full blur-3xl"></div>
      <RouterLink to="/" class="flex items-center gap-2">
        <div class="w-9 h-9 rounded-xl bg-white/10 border border-white/20 flex items-center justify-center">
          <span class="text-rw-gold-400 font-display font-bold text-base">B</span>
        </div>
        <span class="font-display font-bold text-2xl text-white">biz<span class="text-rw-gold-400">.rw</span></span>
      </RouterLink>

      <div>
        <h2 class="font-display text-4xl font-bold text-white mb-6 leading-tight">
          Welcome back to<br />Rwanda's business<br />platform.
        </h2>
        <div class="space-y-4">
          <div v-for="item in benefits" :key="item" class="flex items-center gap-3 text-white/80">
            <svg class="w-5 h-5 text-rw-gold-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <span class="text-sm">{{ item }}</span>
          </div>
        </div>
      </div>

      <p class="text-white/40 text-xs">© 2024 biz.rw</p>
    </div>

    <!-- Right panel (form) -->
    <div class="flex-1 flex items-center justify-center p-6 lg:p-16">
      <div class="w-full max-w-md">
        <div class="mb-8">
          <RouterLink to="/" class="flex items-center gap-2 mb-8 lg:hidden">
            <div class="w-8 h-8 rounded-lg bg-rw-green-700 flex items-center justify-center">
              <span class="text-rw-gold-400 font-display font-bold text-sm">B</span>
            </div>
            <span class="font-display font-bold text-xl text-rw-dark">biz<span class="text-rw-green-700">.rw</span></span>
          </RouterLink>
          <h1 class="font-display text-3xl font-bold text-rw-dark mb-2">Sign in</h1>
          <p class="text-gray-500">New to biz.rw? <RouterLink to="/register" class="text-rw-green-700 font-semibold hover:underline">Create an account</RouterLink></p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label class="input-label">Email address</label>
            <input v-model="form.email" type="email" placeholder="you@example.com" class="input-field" required />
          </div>
          <div>
            <label class="input-label">Password</label>
            <div class="relative">
              <input v-model="form.password" :type="showPwd ? 'text' : 'password'" placeholder="••••••••" class="input-field pr-12" required />
              <button type="button" @click="showPwd = !showPwd" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                <svg v-if="showPwd" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" /></svg>
                <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
              </button>
            </div>
          </div>

          <div v-if="errorMsg" class="p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm flex items-center gap-2">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            {{ errorMsg }}
          </div>

          <button type="submit" :disabled="auth.loading" class="btn-primary w-full text-base py-3.5">
            <svg v-if="auth.loading" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
            <span>{{ auth.loading ? 'Signing in…' : 'Sign In' }}</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'

const auth = useAuthStore()
const toast = useToastStore()
const router = useRouter()
const route = useRoute()

const form = ref({ email: '', password: '' })
const showPwd = ref(false)
const errorMsg = ref('')

const benefits = [
  'Manage your business profile anytime',
  'Track bookings and customer inquiries',
  'View analytics and grow your reach',
  'Respond to customer reviews',
]

async function handleLogin() {
  errorMsg.value = ''
  const result = await auth.login(form.value)
  if (result.success) {
    toast.success('Welcome back!')
    const redirect = route.query.redirect || '/dashboard'
    router.push(redirect)
  } else {
    errorMsg.value = result.error
  }
}
</script>
