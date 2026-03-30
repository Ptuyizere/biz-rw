import api from './axios'

// ─── Auth ─────────────────────────────────────────────────────────────────
export const authApi = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  me: () => api.get('/auth/me'),
  updateMe: (data) => api.put('/auth/me', data),
}

// ─── Businesses ───────────────────────────────────────────────────────────
export const businessApi = {
  list: (params) => api.get('/businesses', { params }),
  create: (data) => api.post('/businesses', data),
  getBySlug: (slug) => api.get(`/businesses/${slug}`),
  getMyBusiness: () => api.get('/businesses/my'),
  update: (slug, data) => api.put(`/businesses/${slug}`, data),
  delete: (slug) => api.delete(`/businesses/${slug}`),
  uploadLogo: (slug, file) => {
    const fd = new FormData()
    fd.append('file', file)
    return api.post(`/businesses/${slug}/logo`, fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  uploadCover: (slug, file) => {
    const fd = new FormData()
    fd.append('file', file)
    return api.post(`/businesses/${slug}/cover`, fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}

// ─── Feedback ─────────────────────────────────────────────────────────────
export const feedbackApi = {
  list: (slug) => api.get(`/businesses/${slug}/feedback`),
  create: (slug, data) => api.post(`/businesses/${slug}/feedback`, data),
  toggleHide: (slug, id) => api.patch(`/businesses/${slug}/feedback/${id}/hide`),
}

// ─── Bookings ─────────────────────────────────────────────────────────────
export const bookingApi = {
  list: (slug) => api.get(`/businesses/${slug}/bookings`),
  create: (slug, data) => api.post(`/businesses/${slug}/bookings`, data),
  updateStatus: (slug, id, status) =>
    api.patch(`/businesses/${slug}/bookings/${id}/status`, null, { params: { new_status: status } }),
}

// ─── Products / Services ───────────────────────────────────────────────────
export const itemsApi = {
  list: (slug) => api.get(`/businesses/${slug}/items`),
  create: (slug, data) => api.post(`/businesses/${slug}/items`, data),
  update: (slug, id, data) => api.put(`/businesses/${slug}/items/${id}`, data),
  delete: (slug, id) => api.delete(`/businesses/${slug}/items/${id}`),
  uploadImage: (slug, id, file) => {
    const fd = new FormData()
    fd.append('file', file)
    return api.post(`/businesses/${slug}/items/${id}/image`, fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}

// ─── Analytics ────────────────────────────────────────────────────────────
export const analyticsApi = {
  get: (slug) => api.get(`/analytics/${slug}`),
}

// ─── Admin ────────────────────────────────────────────────────────────────
export const adminApi = {
  stats: () => api.get('/admin/stats'),
  listUsers: (params) => api.get('/admin/users', { params }),
  toggleUserActive: (id) => api.patch(`/admin/users/${id}/toggle-active`),
  makeAdmin: (id) => api.patch(`/admin/users/${id}/make-admin`),
  listBusinesses: (params) => api.get('/admin/businesses', { params }),
  toggleBusinessActive: (slug) => api.patch(`/admin/businesses/${slug}/toggle-active`),
  toggleBusinessFeatured: (slug) => api.patch(`/admin/businesses/${slug}/toggle-featured`),
  listFeedback: (params) => api.get('/admin/feedback', { params }),
  toggleFeedbackHide: (id) => api.patch(`/admin/feedback/${id}/toggle-hide`),
}
