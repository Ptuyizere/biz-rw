<template>
  <div class="min-h-screen bg-gray-50">
    <AppNav v-if="showChrome" />
    <main>
      <RouterView v-slot="{ Component }">
        <Transition name="fade" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>
    <AppFooter v-if="showChrome" />
    <ToastContainer />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppNav from '@/components/AppNav.vue'
import AppFooter from '@/components/AppFooter.vue'
import ToastContainer from '@/components/ToastContainer.vue'

const route = useRoute()

// Hide the shared nav/footer for pages that provide their own full-page layout
const BARE_ROUTES = ['business-public', 'admin', 'admin-users', 'admin-businesses', 'admin-feedback']
const showChrome = computed(() => !BARE_ROUTES.includes(route.name))
</script>
