<template>
  <div class="overflow-hidden">
    <!-- Hero Section -->
    <section class="gradient-hero hero-pattern relative min-h-[92vh] flex items-center">
      <!-- Decorative blobs -->
      <div class="absolute top-20 right-10 w-72 h-72 bg-rw-gold-400/10 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute bottom-10 left-10 w-96 h-96 bg-rw-green-900/30 rounded-full blur-3xl pointer-events-none"></div>

      <div class="page-container relative py-24">
        <div class="max-w-3xl">
          <div class="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-4 py-2 mb-8">
            <span class="w-2 h-2 bg-rw-gold-400 rounded-full animate-pulse-slow"></span>
            <span class="text-white/90 text-sm font-medium">Rwanda's #1 Business Platform</span>
          </div>

          <h1 class="font-display text-5xl md:text-6xl lg:text-7xl font-bold text-white leading-tight mb-6">
            Your Business,<br />
            <span class="text-rw-gold-400">Online & Thriving.</span>
          </h1>

          <p class="text-white/75 text-lg md:text-xl leading-relaxed max-w-xl mb-10">
            Join thousands of Rwandan entrepreneurs who've built their digital presence with biz.rw — the fastest way to get found, get bookings, and grow.
          </p>

          <div class="flex flex-wrap gap-4">
            <RouterLink to="/register" class="inline-flex items-center gap-2 px-8 py-4 bg-rw-gold-400 hover:bg-rw-gold-500 text-white font-semibold rounded-2xl shadow-gold transition-all duration-200 hover:scale-105 text-lg">
              Start for Free
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
            </RouterLink>
            <RouterLink to="/explore" class="inline-flex items-center gap-2 px-8 py-4 bg-white/10 hover:bg-white/20 border border-white/30 text-white font-semibold rounded-2xl transition-all duration-200 text-lg backdrop-blur-sm">
              Explore Businesses
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- Scroll indicator -->
      <div class="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-white/40 animate-bounce">
        <span class="text-xs">Scroll</span>
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-24 bg-white">
      <div class="page-container">
        <div class="text-center mb-16">
          <p class="text-rw-green-700 font-semibold text-sm uppercase tracking-widest mb-3">Everything you need</p>
          <h2 class="section-heading">Built for Rwandan businesses</h2>
          <p class="section-subheading max-w-xl mx-auto">
            From street-side shops to professional services — create your page in minutes and start getting customers.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="(feat, i) in features" :key="i" class="group p-6 rounded-2xl border border-gray-100 hover:border-rw-green-200 hover:bg-rw-green-50/30 transition-all duration-300">
            <div class="w-12 h-12 rounded-2xl flex items-center justify-center mb-5 text-2xl" :class="feat.bg">
              {{ feat.icon }}
            </div>
            <h3 class="font-display font-semibold text-xl text-rw-dark mb-2">{{ feat.title }}</h3>
            <p class="text-gray-500 text-sm leading-relaxed">{{ feat.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Templates Showcase -->
    <section class="py-24 bg-gray-50">
      <div class="page-container">
        <div class="text-center mb-16">
          <p class="text-rw-green-700 font-semibold text-sm uppercase tracking-widest mb-3">Stunning designs</p>
          <h2 class="section-heading">3 Beautiful Templates</h2>
          <p class="section-subheading max-w-xl mx-auto">
            Choose a style that matches your brand. Each template is fully responsive and customizable.
          </p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div v-for="tpl in templates" :key="tpl.name" class="group rounded-2xl overflow-hidden border border-gray-200 hover:border-rw-green-400 shadow-card hover:shadow-card-hover transition-all duration-300 hover:-translate-y-1 bg-white">
            <div class="h-48 relative overflow-hidden" :style="{ background: tpl.gradient }">
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-5xl opacity-30">{{ tpl.emoji }}</span>
              </div>
              <div class="absolute bottom-4 left-4">
                <span class="badge bg-white/90 text-rw-dark font-semibold">{{ tpl.name }}</span>
              </div>
            </div>
            <div class="p-5">
              <h3 class="font-display font-semibold text-lg mb-2">{{ tpl.name }} Template</h3>
              <p class="text-gray-500 text-sm">{{ tpl.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Businesses -->
    <section class="py-24 bg-white">
      <div class="page-container">
        <div class="flex items-end justify-between mb-12">
          <div>
            <p class="text-rw-green-700 font-semibold text-sm uppercase tracking-widest mb-3">Discover</p>
            <h2 class="section-heading">Featured Businesses</h2>
          </div>
          <RouterLink to="/explore" class="btn-secondary text-sm hidden md:inline-flex">
            View All →
          </RouterLink>
        </div>

        <div v-if="loadingBiz" class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div v-for="i in 3" :key="i" class="rounded-2xl overflow-hidden bg-gray-100 animate-pulse h-72"></div>
        </div>

        <div v-else-if="featuredBiz.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <BusinessCard v-for="b in featuredBiz" :key="b.id" :business="b" />
        </div>

        <div v-else class="text-center py-16 text-gray-400">
          <p class="text-4xl mb-4">🏪</p>
          <p>No businesses listed yet. Be the first!</p>
        </div>

        <div class="text-center mt-8 md:hidden">
          <RouterLink to="/explore" class="btn-secondary">View All Businesses →</RouterLink>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-24 gradient-hero hero-pattern relative overflow-hidden">
      <div class="absolute top-0 right-0 w-96 h-96 bg-rw-gold-400/10 rounded-full blur-3xl"></div>
      <div class="page-container relative text-center">
        <h2 class="font-display text-4xl md:text-5xl font-bold text-white mb-6">
          Ready to go digital?
        </h2>
        <p class="text-white/70 text-lg mb-10 max-w-lg mx-auto">
          Create your free business profile in under 5 minutes and reach customers across Rwanda and beyond.
        </p>
        <RouterLink to="/register" class="inline-flex items-center gap-2 px-10 py-4 bg-rw-gold-400 hover:bg-rw-gold-500 text-white font-bold rounded-2xl shadow-gold transition-all duration-200 hover:scale-105 text-lg">
          Create Your Free Profile
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import BusinessCard from '@/components/BusinessCard.vue'
import { businessApi } from '@/api'

const featuredBiz = ref([])
const loadingBiz = ref(true)

const stats = [
  { value: '500+', label: 'Businesses listed' },
  { value: '10K+', label: 'Monthly visitors' },
  { value: '98%', label: 'Owner satisfaction' },
]

const features = [
  { icon: '🌐', bg: 'bg-rw-green-50', title: 'Instant Web Presence', desc: 'Get a beautiful public page with your unique biz.rw URL in minutes — no coding required.' },
  { icon: '📅', bg: 'bg-blue-50', title: 'Booking & Inquiries', desc: 'Accept booking requests and customer inquiries directly from your public profile.' },
  { icon: '⭐', bg: 'bg-rw-gold-50', title: 'Ratings & Reviews', desc: 'Build trust with verified customer reviews and ratings displayed on your page.' },
  { icon: '📊', bg: 'bg-purple-50', title: 'Analytics Dashboard', desc: 'Track profile views, booking trends, and customer engagement — all in one place.' },
  { icon: '📱', bg: 'bg-orange-50', title: 'Social Media Links', desc: 'Connect all your social media profiles and make it easy for customers to follow you.' },
  { icon: '📧', bg: 'bg-pink-50', title: 'Email Notifications', desc: 'Receive instant email alerts for every new booking request and customer review.' },
]

const templates = [
  { name: 'Modern', emoji: '⚡', gradient: 'linear-gradient(135deg, #0A4F3A, #1a9e71)', desc: 'Clean lines, bold typography, perfect for tech-forward services and modern brands.' },
  { name: 'Classic', emoji: '🏛', gradient: 'linear-gradient(135deg, #1A1A2E, #2d2d4e)', desc: 'Timeless elegance with warm tones — ideal for established businesses and professional services.' },
  { name: 'Bold', emoji: '🔥', gradient: 'linear-gradient(135deg, #D4A853, #c8892a)', desc: 'High-impact visual design with striking contrasts — perfect for retail and product businesses.' },
]

onMounted(async () => {
  try {
    const { data } = await businessApi.list({ per_page: 6 })
    featuredBiz.value = data
  } catch {
    // silently fail
  } finally {
    loadingBiz.value = false
  }
})
</script>
