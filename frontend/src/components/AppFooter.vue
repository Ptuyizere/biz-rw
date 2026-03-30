<template>
  <footer class="bg-rw-dark text-white mt-20">
    <div class="page-container py-16">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-10">
        <!-- Brand -->
        <div class="md:col-span-2">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-9 h-9 rounded-xl bg-rw-green-700 flex items-center justify-center">
              <span class="text-rw-gold-400 font-display font-bold text-base">B</span>
            </div>
            <span class="font-display font-bold text-2xl">
              biz<span class="text-rw-gold-400">.rw</span>
            </span>
          </div>
          <p class="text-gray-400 text-sm leading-relaxed max-w-sm">
            Empowering Rwandan small and medium enterprises with the tools to create a powerful online presence and grow their businesses.
          </p>
          <div class="flex gap-3 mt-6">
            <a href="#" class="social-icon" aria-label="Facebook">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M18.77 7.46H14.5v-1.9c0-.9.6-1.1 1-1.1h3V.5h-4.33C10.24.5 9.5 3.44 9.5 5.32v2.15h-3v4h3v12h5v-12h3.85l.42-4z"/></svg>
            </a>
            <a href="#" class="social-icon" aria-label="Twitter">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/></svg>
            </a>
            <a href="#" class="social-icon" aria-label="Instagram">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
            </a>
          </div>
        </div>

        <!-- Links -->
        <div>
          <h4 class="font-semibold text-white mb-4 text-sm uppercase tracking-wider">Platform</h4>
          <ul class="space-y-3">
            <li><RouterLink to="/explore" class="footer-link">Explore Businesses</RouterLink></li>
            <li><RouterLink to="/register" class="footer-link">List Your Business</RouterLink></li>
            <li><RouterLink to="/login" class="footer-link">Sign In</RouterLink></li>
          </ul>
        </div>

        <div>
          <h4 class="font-semibold text-white mb-4 text-sm uppercase tracking-wider">Company</h4>
          <ul class="space-y-3">
            <li><a href="#" class="footer-link">About Us</a></li>
            <li><a href="#" class="footer-link">Contact</a></li>
          </ul>
        </div>
      </div>

      <div class="border-t border-gray-800 mt-12 pt-8 flex flex-col sm:flex-row justify-between items-center gap-4">
        <p class="text-gray-500 text-sm">
          © {{ new Date().getFullYear() }} biz.rw · Empowering Rwandan SMEs
        </p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer-link {
  @apply text-gray-400 text-sm hover:text-rw-gold-400 transition-colors;
}
.social-icon {
  @apply w-8 h-8 bg-gray-800 hover:bg-rw-green-700 rounded-lg flex items-center justify-center text-gray-400 hover:text-white transition-all duration-200;
}
</style>
