<template>
  <div class="min-h-screen flex items-center justify-center text-center px-4 bg-gray-50">
    <div>
      <div class="font-display text-9xl font-bold text-rw-green-700/20 mb-4">404</div>
      <h1 class="font-display text-3xl font-bold text-rw-dark mb-3">Page not found</h1>
      <p class="text-gray-500 mb-8">The page you're looking for doesn't exist or has been moved.</p>
      <div class="flex gap-4 justify-center">
        <RouterLink to="/" class="btn-primary">Go Home</RouterLink>
        <RouterLink to="/explore" class="btn-secondary">Explore Businesses</RouterLink>
      </div>
    </div>
  </div>
</template>
