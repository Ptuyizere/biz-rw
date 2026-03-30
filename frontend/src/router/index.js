import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    component: () => import('@/views/HomeView.vue'),
    name: 'home',
  },
  {
    path: '/explore',
    component: () => import('@/views/ExploreView.vue'),
    name: 'explore',
  },
  {
    path: '/login',
    component: () => import('@/views/LoginView.vue'),
    name: 'login',
    meta: { guestOnly: true },
  },
  {
    path: '/register',
    component: () => import('@/views/RegisterView.vue'),
    name: 'register',
    meta: { guestOnly: true },
  },
  {
    path: '/dashboard',
    component: () => import('@/views/DashboardView.vue'),
    name: 'dashboard',
    meta: { requiresAuth: true },
  },
  {
    path: '/dashboard/setup',
    component: () => import('@/views/BusinessSetupView.vue'),
    name: 'business-setup',
    meta: { requiresAuth: true },
  },
  {
    path: '/dashboard/edit',
    component: () => import('@/views/BusinessEditView.vue'),
    name: 'business-edit',
    meta: { requiresAuth: true },
  },
  {
    path: '/dashboard/analytics',
    component: () => import('@/views/AnalyticsView.vue'),
    name: 'analytics',
    meta: { requiresAuth: true },
  },
  {
    path: '/dashboard/bookings',
    component: () => import('@/views/BookingsView.vue'),
    name: 'bookings',
    meta: { requiresAuth: true },
  },
  {
    path: '/admin',
    component: () => import('@/views/admin/AdminLayout.vue'),
    meta: { requiresAdmin: true },
    children: [
      {
        path: '',
        component: () => import('@/views/admin/AdminDashboard.vue'),
        name: 'admin',
      },
      {
        path: 'users',
        component: () => import('@/views/admin/AdminUsers.vue'),
        name: 'admin-users',
      },
      {
        path: 'businesses',
        component: () => import('@/views/admin/AdminBusinesses.vue'),
        name: 'admin-businesses',
      },
      {
        path: 'feedback',
        component: () => import('@/views/admin/AdminFeedback.vue'),
        name: 'admin-feedback',
      },
    ],
  },
  {
    path: '/b/:slug',
    component: () => import('@/views/BusinessPublicView.vue'),
    name: 'business-public',
  },
  {
    path: '/:pathMatch(.*)*',
    component: () => import('@/views/NotFoundView.vue'),
    name: 'not-found',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return { top: 0, behavior: 'smooth' }
  },
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAdmin && !auth.isAdmin) {
    return next(auth.isLoggedIn ? '/' : '/login')
  }
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return next({ name: 'login', query: { redirect: to.fullPath } })
  }
  if (to.meta.guestOnly && auth.isLoggedIn) {
    return next('/dashboard')
  }
  next()
})

export default router
