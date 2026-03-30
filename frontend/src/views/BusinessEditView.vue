<template>
  <div class="min-h-screen bg-gray-50 py-10">
    <div class="page-container max-w-4xl">
      <div class="flex items-center gap-4 mb-8">
        <RouterLink to="/dashboard" class="btn-ghost text-sm gap-1">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
          Dashboard
        </RouterLink>
        <h1 class="font-display text-2xl font-bold text-rw-dark">Edit Business Profile</h1>
      </div>

      <div v-if="loading" class="space-y-4">
        <div v-for="i in 3" :key="i" class="h-40 rounded-2xl skeleton"></div>
      </div>

      <div v-else-if="business">
        <!-- Tabs -->
        <div class="flex gap-1 bg-white rounded-2xl p-1 border border-gray-100 shadow-sm mb-8 overflow-x-auto">
          <button v-for="tab in tabs" :key="tab.key" @click="activeTab = tab.key"
            class="flex-1 min-w-fit px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 whitespace-nowrap"
            :class="activeTab === tab.key ? 'bg-rw-green-700 text-white shadow' : 'text-gray-500 hover:text-rw-dark'"
          >
            {{ tab.label }}
          </button>
        </div>

        <!-- Tab: Profile -->
        <div v-if="activeTab === 'profile'">
          <!-- Images -->
          <div class="card p-6 mb-6">
            <h2 class="font-display text-lg font-semibold text-rw-dark mb-5">Images</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Logo -->
              <div>
                <label class="input-label mb-3">Logo</label>
                <div class="flex items-center gap-4">
                  <div class="w-20 h-20 rounded-2xl bg-gray-100 border-2 border-dashed border-gray-300 overflow-hidden flex items-center justify-center">
                    <img v-if="business.logo_url" :src="business.logo_url" alt="Logo" class="w-full h-full object-cover" />
                    <svg v-else class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                  </div>
                  <div>
                    <label class="btn-secondary text-sm cursor-pointer">
                      <input type="file" accept="image/*" class="hidden" @change="uploadLogo" :disabled="uploadingLogo" />
                      {{ uploadingLogo ? 'Uploading…' : 'Upload Logo' }}
                    </label>
                    <p class="text-xs text-gray-400 mt-1">JPG, PNG, max 5MB</p>
                  </div>
                </div>
              </div>
              <!-- Cover -->
              <div>
                <label class="input-label mb-3">Cover Image</label>
                <div class="h-24 rounded-2xl bg-gray-100 border-2 border-dashed border-gray-300 overflow-hidden relative flex items-center justify-center">
                  <img v-if="business.cover_url" :src="business.cover_url" alt="Cover" class="w-full h-full object-cover" />
                  <div v-else class="text-center">
                    <svg class="w-8 h-8 text-gray-400 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                  </div>
                  <label class="absolute inset-0 flex items-end justify-end p-2 cursor-pointer">
                    <input type="file" accept="image/*" class="hidden" @change="uploadCover" :disabled="uploadingCover" />
                    <span class="btn-primary text-xs py-1.5 px-3">{{ uploadingCover ? 'Uploading…' : 'Upload Cover' }}</span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Business Info Form -->
          <div class="card p-6 mb-6">
            <h2 class="font-display text-lg font-semibold text-rw-dark mb-5">Business Information</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div class="md:col-span-2"><label class="input-label">Business Name</label><input v-model="form.name" class="input-field" /></div>
              <div class="md:col-span-2"><label class="input-label">Tagline</label><input v-model="form.tagline" class="input-field" maxlength="120" /></div>
              <div class="md:col-span-2"><label class="input-label">Description</label><textarea v-model="form.description" rows="4" class="input-field resize-none"></textarea></div>
              <div>
                <label class="input-label">Category</label>
                <select v-model="form.category" class="input-field">
                  <option value="service">🛠 Service</option>
                  <option value="product">📦 Product</option>
                </select>
              </div>
              <div>
                <label class="input-label">Template</label>
                <select v-model="form.template" class="input-field">
                  <option value="modern">⚡ Modern</option>
                  <option value="classic">🏛 Classic</option>
                  <option value="bold">🔥 Bold</option>
                </select>
              </div>
              <div><label class="input-label">Email</label><input v-model="form.email" type="email" class="input-field" /></div>
              <div><label class="input-label">Phone</label><input v-model="form.phone" type="tel" class="input-field" /></div>
              <div><label class="input-label">City</label><input v-model="form.city" class="input-field" /></div>
              <div><label class="input-label">Address</label><input v-model="form.address" class="input-field" /></div>
              <div class="md:col-span-2"><label class="input-label">Website</label><input v-model="form.website" type="url" class="input-field" /></div>
              <div><label class="input-label">Facebook</label><input v-model="form.facebook" type="url" class="input-field" placeholder="https://facebook.com/..." /></div>
              <div><label class="input-label">Instagram</label><input v-model="form.instagram" type="url" class="input-field" placeholder="https://instagram.com/..." /></div>
              <div><label class="input-label">Twitter / X</label><input v-model="form.twitter" type="url" class="input-field" placeholder="https://twitter.com/..." /></div>
              <div><label class="input-label">WhatsApp</label><input v-model="form.whatsapp" type="tel" class="input-field" placeholder="+250 7XX XXX XXX" /></div>
            </div>
            <div class="flex justify-end mt-6 pt-5 border-t border-gray-100">
              <button @click="saveProfile" :disabled="saving" class="btn-primary">
                <svg v-if="saving" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
                {{ saving ? 'Saving…' : 'Save Changes' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Tab: Products/Services -->
        <div v-if="activeTab === 'items'">
          <div class="card p-6">
            <div class="flex items-center justify-between mb-6">
              <h2 class="font-display text-lg font-semibold text-rw-dark">
                {{ business.category === 'product' ? 'Products' : 'Services' }}
              </h2>
              <button @click="showItemForm = true" class="btn-primary text-sm">+ Add {{ business.category === 'product' ? 'Product' : 'Service' }}</button>
            </div>

            <!-- Add Item Form -->
            <div v-if="showItemForm" class="bg-gray-50 rounded-2xl p-5 mb-6 border border-gray-200">
              <h3 class="font-semibold text-rw-dark mb-4">New {{ business.category === 'product' ? 'Product' : 'Service' }}</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="md:col-span-2"><label class="input-label">Name *</label><input v-model="itemForm.name" class="input-field" placeholder="Item name" /></div>
                <div class="md:col-span-2"><label class="input-label">Description</label><textarea v-model="itemForm.description" rows="2" class="input-field resize-none" placeholder="Brief description"></textarea></div>
                <div><label class="input-label">Price</label><input v-model.number="itemForm.price" type="number" class="input-field" placeholder="0" /></div>
                <div><label class="input-label">Currency</label><select v-model="itemForm.currency" class="input-field"><option>RWF</option><option>USD</option><option>EUR</option></select></div>
              </div>
              <div class="flex gap-3 justify-end mt-4">
                <button @click="showItemForm = false; resetItemForm()" class="btn-ghost text-sm">Cancel</button>
                <button @click="createItem" :disabled="savingItem" class="btn-primary text-sm">{{ savingItem ? 'Saving…' : 'Save Item' }}</button>
              </div>
            </div>

            <!-- Items list -->
            <div class="space-y-3">
              <div v-for="item in items" :key="item.id" class="flex items-center gap-4 p-4 bg-gray-50 rounded-xl border border-gray-100">
                <div class="w-12 h-12 rounded-xl bg-gray-200 overflow-hidden flex-shrink-0">
                  <img v-if="item.image_url" :src="item.image_url" :alt="item.name" class="w-full h-full object-cover" />
                  <div v-else class="w-full h-full flex items-center justify-center text-gray-400 text-lg">📦</div>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="font-semibold text-sm text-rw-dark truncate">{{ item.name }}</p>
                  <p class="text-xs text-gray-400">{{ item.price ? `${item.price.toLocaleString()} ${item.currency}` : 'Price not set' }}</p>
                </div>
                <div class="flex items-center gap-2">
                  <label class="text-xs btn-secondary py-1.5 px-2 cursor-pointer">
                    <input type="file" accept="image/*" class="hidden" @change="(e) => uploadItemImage(item.id, e)" />
                    📷
                  </label>
                  <button @click="deleteItem(item.id)" class="text-red-400 hover:text-red-600 p-1.5 rounded-lg hover:bg-red-50 transition-colors">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                  </button>
                </div>
              </div>
              <div v-if="!items.length" class="text-center py-10 text-gray-400 text-sm">No items yet. Add your first one!</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { businessApi, itemsApi } from '@/api'
import { useToastStore } from '@/stores/toast'
import { getErrorMessage } from '@/api/axios'

const toast = useToastStore()
const business = ref(null)
const loading = ref(true)
const saving = ref(false)
const uploadingLogo = ref(false)
const uploadingCover = ref(false)
const activeTab = ref('profile')
const showItemForm = ref(false)
const savingItem = ref(false)
const items = ref([])

const tabs = [
  { key: 'profile', label: '🏢 Profile Info' },
  { key: 'items', label: '📦 Products / Services' },
]

const form = ref({})
const itemForm = ref({ name: '', description: '', price: null, currency: 'RWF', is_available: true })

function resetItemForm() {
  itemForm.value = { name: '', description: '', price: null, currency: 'RWF', is_available: true }
}

onMounted(async () => {
  try {
    const { data } = await businessApi.getMyBusiness()
    business.value = data
    items.value = data.products_services || []
    form.value = {
      name: data.name, tagline: data.tagline, description: data.description,
      category: data.category, template: data.template, email: data.email,
      phone: data.phone, address: data.address, city: data.city, website: data.website,
      facebook: data.facebook, instagram: data.instagram, twitter: data.twitter, whatsapp: data.whatsapp,
    }
  } finally {
    loading.value = false
  }
})

async function saveProfile() {
  saving.value = true
  try {
    const { data } = await businessApi.update(business.value.slug, form.value)
    business.value = data
    toast.success('Profile updated successfully!')
  } catch (err) {
    toast.error(getErrorMessage(err))
  } finally {
    saving.value = false
  }
}

async function uploadLogo(e) {
  const file = e.target.files[0]
  if (!file) return
  uploadingLogo.value = true
  try {
    const { data } = await businessApi.uploadLogo(business.value.slug, file)
    business.value.logo_url = data.logo_url
    toast.success('Logo updated!')
  } catch (err) {
    toast.error(getErrorMessage(err))
  } finally {
    uploadingLogo.value = false
  }
}

async function uploadCover(e) {
  const file = e.target.files[0]
  if (!file) return
  uploadingCover.value = true
  try {
    const { data } = await businessApi.uploadCover(business.value.slug, file)
    business.value.cover_url = data.cover_url
    toast.success('Cover updated!')
  } catch (err) {
    toast.error(getErrorMessage(err))
  } finally {
    uploadingCover.value = false
  }
}

async function createItem() {
  if (!itemForm.value.name.trim()) return
  savingItem.value = true
  try {
    const { data } = await itemsApi.create(business.value.slug, itemForm.value)
    items.value.push(data)
    showItemForm.value = false
    resetItemForm()
    toast.success('Item added!')
  } catch (err) {
    toast.error(getErrorMessage(err))
  } finally {
    savingItem.value = false
  }
}

async function deleteItem(id) {
  if (!confirm('Delete this item?')) return
  try {
    await itemsApi.delete(business.value.slug, id)
    items.value = items.value.filter(i => i.id !== id)
    toast.success('Item removed.')
  } catch (err) {
    toast.error(getErrorMessage(err))
  }
}

async function uploadItemImage(id, e) {
  const file = e.target.files[0]
  if (!file) return
  try {
    const { data } = await itemsApi.uploadImage(business.value.slug, id, file)
    const idx = items.value.findIndex(i => i.id === id)
    if (idx !== -1) items.value[idx].image_url = data.image_url
    toast.success('Image updated!')
  } catch (err) {
    toast.error(getErrorMessage(err))
  }
}
</script>
