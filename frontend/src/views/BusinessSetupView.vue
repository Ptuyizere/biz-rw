<template>
  <div class="min-h-screen bg-gray-50 py-12">
    <div class="page-container max-w-3xl">
      <!-- Header -->
      <div class="text-center mb-10">
        <div class="inline-flex items-center gap-2 bg-rw-green-50 text-rw-green-700 rounded-full px-4 py-2 text-sm font-semibold mb-4">
          Step 1 of 1
        </div>
        <h1 class="font-display text-4xl font-bold text-rw-dark mb-3">Create your business profile</h1>
        <p class="text-gray-500">Fill in the details below. You can always update them later.</p>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-8">
        <!-- Basic Info -->
        <div class="card p-6 md:p-8">
          <h2 class="font-display text-xl font-semibold text-rw-dark mb-6 pb-4 border-b border-gray-100">Basic Information</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div class="md:col-span-2">
              <label class="input-label">Business Name *</label>
              <input v-model="form.name" type="text" placeholder="e.g. Kigali Fresh Bakery" class="input-field" required />
            </div>
            <div class="md:col-span-2">
              <label class="input-label">Tagline</label>
              <input v-model="form.tagline" type="text" placeholder="A short, catchy description" class="input-field" maxlength="120" />
            </div>
            <div class="md:col-span-2">
              <label class="input-label">Description</label>
              <textarea v-model="form.description" rows="4" placeholder="Tell customers about your business..." class="input-field resize-none"></textarea>
            </div>
            <div>
              <label class="input-label">Business Type *</label>
              <select v-model="form.category" class="input-field">
                <option value="service">🛠 Service Business</option>
                <option value="product">📦 Product Business</option>
              </select>
            </div>
            <div>
              <label class="input-label">City</label>
              <input v-model="form.city" type="text" placeholder="e.g. Kigali" class="input-field" />
            </div>
          </div>
        </div>

        <!-- Template Selection -->
        <div class="card p-6 md:p-8">
          <h2 class="font-display text-xl font-semibold text-rw-dark mb-2">Choose Your Template *</h2>
          <p class="text-sm text-gray-500 mb-6">Select a page style that matches your brand.</p>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <button
              v-for="tpl in templates"
              :key="tpl.value"
              type="button"
              @click="form.template = tpl.value"
              class="relative rounded-2xl overflow-hidden border-2 transition-all duration-200 text-left"
              :class="form.template === tpl.value ? 'border-rw-green-700 shadow-luxury scale-[1.02]' : 'border-gray-200 hover:border-rw-green-300'"
            >
              <div class="h-28 flex items-center justify-center text-4xl" :style="{ background: tpl.bg }">
                {{ tpl.emoji }}
              </div>
              <div class="p-3 bg-white">
                <div class="flex items-center justify-between">
                  <p class="font-semibold text-sm text-rw-dark">{{ tpl.label }}</p>
                  <div v-if="form.template === tpl.value" class="w-5 h-5 bg-rw-green-700 rounded-full flex items-center justify-center">
                    <svg class="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" /></svg>
                  </div>
                </div>
                <p class="text-xs text-gray-400 mt-0.5">{{ tpl.desc }}</p>
              </div>
            </button>
          </div>
        </div>

        <!-- Contact Info -->
        <div class="card p-6 md:p-8">
          <h2 class="font-display text-xl font-semibold text-rw-dark mb-6 pb-4 border-b border-gray-100">Contact Details</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div>
              <label class="input-label">Business Email</label>
              <input v-model="form.email" type="email" placeholder="business@email.com" class="input-field" />
            </div>
            <div>
              <label class="input-label">Phone Number</label>
              <input v-model="form.phone" type="tel" placeholder="+250 7XX XXX XXX" class="input-field" />
            </div>
            <div class="md:col-span-2">
              <label class="input-label">Address</label>
              <input v-model="form.address" type="text" placeholder="Street address" class="input-field" />
            </div>
            <div class="md:col-span-2">
              <label class="input-label">Website (optional)</label>
              <input v-model="form.website" type="url" placeholder="https://yourwebsite.com" class="input-field" />
            </div>
          </div>
        </div>

        <!-- Social Media -->
        <div class="card p-6 md:p-8">
          <h2 class="font-display text-xl font-semibold text-rw-dark mb-6 pb-4 border-b border-gray-100">Social Media</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M18.77 7.46H14.5v-1.9c0-.9.6-1.1 1-1.1h3V.5h-4.33C10.24.5 9.5 3.44 9.5 5.32v2.15h-3v4h3v12h5v-12h3.85l.42-4z"/></svg>
              </div>
              <input v-model="form.facebook" type="url" placeholder="Facebook page URL" class="input-field" />
            </div>
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-gradient-to-br from-pink-500 to-orange-400 rounded-xl flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
              </div>
              <input v-model="form.instagram" type="url" placeholder="Instagram page URL" class="input-field" />
            </div>
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-sky-400 rounded-xl flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/></svg>
              </div>
              <input v-model="form.twitter" type="url" placeholder="Twitter / X profile URL" class="input-field" />
            </div>
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-green-500 rounded-xl flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
              </div>
              <input v-model="form.whatsapp" type="tel" placeholder="+250 7XX XXX XXX" class="input-field" />
            </div>
          </div>
        </div>

        <div v-if="errorMsg" class="p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">{{ errorMsg }}</div>

        <div class="flex gap-4 justify-end">
          <RouterLink to="/dashboard" class="btn-secondary">Cancel</RouterLink>
          <button type="submit" :disabled="submitting" class="btn-primary min-w-[180px]">
            <svg v-if="submitting" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
            {{ submitting ? 'Creating…' : 'Create Business Profile' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { businessApi } from '@/api'
import { useToastStore } from '@/stores/toast'
import { getErrorMessage } from '@/api/axios'

const router = useRouter()
const toast = useToastStore()
const submitting = ref(false)
const errorMsg = ref('')

const form = ref({
  name: '', tagline: '', description: '', category: 'service', template: 'modern',
  email: '', phone: '', address: '', city: '', website: '',
  facebook: '', instagram: '', twitter: '', whatsapp: '',
})

const templates = [
  { value: 'modern', label: 'Modern', emoji: '⚡', bg: 'linear-gradient(135deg, #0A4F3A, #1a9e71)', desc: 'Clean & bold' },
  { value: 'classic', label: 'Classic', emoji: '🏛', bg: 'linear-gradient(135deg, #1A1A2E, #2d2d4e)', desc: 'Timeless elegance' },
  { value: 'bold', label: 'Bold', emoji: '🔥', bg: 'linear-gradient(135deg, #D4A853, #c8892a)', desc: 'High-impact' },
]

async function handleSubmit() {
  submitting.value = true
  errorMsg.value = ''
  try {
    const { data } = await businessApi.create(form.value)
    toast.success('Business profile created! 🎉')
    router.push(`/dashboard/edit`)
  } catch (err) {
    errorMsg.value = getErrorMessage(err)
  } finally {
    submitting.value = false
  }
}
</script>
