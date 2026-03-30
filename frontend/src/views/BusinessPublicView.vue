<template>
  <div>
    <!-- Loading -->
    <div v-if="loading" class="min-h-screen flex items-center justify-center">
      <div class="flex flex-col items-center gap-4">
        <div class="w-12 h-12 border-4 border-rw-green-700 border-t-transparent rounded-full animate-spin"></div>
        <p class="text-gray-500 text-sm">Loading business…</p>
      </div>
    </div>

    <!-- 404 -->
    <div v-else-if="!business" class="min-h-screen flex items-center justify-center text-center px-4">
      <div>
        <div class="text-7xl mb-6">🏚</div>
        <h1 class="font-display text-3xl font-bold text-rw-dark mb-3">Business not found</h1>
        <p class="text-gray-500 mb-6">This business page doesn't exist or has been removed.</p>
        <RouterLink to="/explore" class="btn-primary">Browse Businesses</RouterLink>
      </div>
    </div>

    <!-- ══════════════════════ MODERN TEMPLATE ══════════════════════ -->
    <div v-else-if="business.template === 'modern'" class="min-h-screen bg-gray-50">
      <!-- Mini nav -->
      <nav class="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-gray-100 shadow-sm">
        <div class="page-container h-14 flex items-center justify-between">
          <RouterLink to="/explore" class="flex items-center gap-2 text-sm font-medium text-gray-500 hover:text-rw-green-700 transition-colors">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
            Explore
          </RouterLink>
          <RouterLink to="/" class="flex items-center gap-1.5">
            <div class="w-6 h-6 rounded bg-rw-green-700 flex items-center justify-center"><span class="text-rw-gold-400 font-display font-bold text-xs">B</span></div>
            <span class="font-display font-bold text-rw-dark text-sm">biz<span class="text-rw-green-700">.rw</span></span>
          </RouterLink>
          <div class="flex items-center gap-3">
            <RouterLink v-if="!auth.isLoggedIn" to="/register" class="btn-primary text-xs py-1.5 px-3">Get Started</RouterLink>
            <RouterLink v-else to="/dashboard" class="text-sm font-medium text-rw-green-700 hover:underline">Dashboard</RouterLink>
          </div>
        </div>
      </nav>
      <!-- Hero -->
      <div class="relative h-72 md:h-96 bg-gradient-to-br from-rw-green-700 via-rw-green-800 to-rw-green-900 overflow-hidden">
        <img v-if="business.cover_url" :src="business.cover_url" alt="cover" class="absolute inset-0 w-full h-full object-cover mix-blend-overlay opacity-40" />
        <div class="absolute inset-0 hero-pattern opacity-30"></div>
        <div class="absolute top-4 right-4 w-32 h-32 bg-rw-gold-400/20 rounded-full blur-2xl"></div>
        <div class="absolute inset-0 flex flex-col justify-end p-8 md:p-14">
          <div class="flex items-end gap-6">
            <div class="w-20 h-20 md:w-24 md:h-24 rounded-2xl bg-white shadow-luxury border-4 border-white overflow-hidden flex-shrink-0">
              <img v-if="business.logo_url" :src="business.logo_url" :alt="business.name" class="w-full h-full object-cover" />
              <div v-else class="w-full h-full flex items-center justify-center bg-rw-green-50">
                <span class="font-display font-bold text-3xl text-rw-green-700">{{ business.name[0] }}</span>
              </div>
            </div>
            <div class="pb-1">
              <div class="flex items-center gap-3 flex-wrap mb-2">
                <span class="badge bg-white/20 text-white backdrop-blur-sm text-xs">{{ business.category === 'product' ? '📦 Products' : '🛠 Services' }}</span>
                <span v-if="business.city" class="text-white/70 text-sm flex items-center gap-1">
                  <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /></svg>
                  {{ business.city }}
                </span>
              </div>
              <h1 class="font-display text-3xl md:text-4xl font-bold text-white drop-shadow-lg">{{ business.name }}</h1>
              <p v-if="business.tagline" class="text-white/75 text-sm mt-1">{{ business.tagline }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Rating bar -->
      <div class="bg-white border-b border-gray-100 shadow-sm">
        <div class="page-container py-4 flex flex-wrap items-center justify-between gap-4">
          <div class="flex items-center gap-6">
            <div v-if="avgRating" class="flex items-center gap-2">
              <div class="flex gap-0.5">
                <span v-for="i in 5" :key="i" class="text-lg" :class="i <= Math.round(avgRating) ? 'text-rw-gold-400' : 'text-gray-200'">★</span>
              </div>
              <span class="font-bold text-rw-dark">{{ avgRating }}</span>
              <span class="text-gray-400 text-sm">({{ visibleFeedback.length }} reviews)</span>
            </div>
            <div class="flex items-center gap-1.5 text-gray-400 text-sm">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
              {{ business.view_count }} views
            </div>
          </div>
          <!-- Social icons -->
          <div class="flex gap-3">
            <a v-if="business.facebook" :href="business.facebook" target="_blank" class="social-pill bg-blue-600 text-white">f</a>
            <a v-if="business.instagram" :href="business.instagram" target="_blank" class="social-pill bg-gradient-to-br from-pink-500 to-orange-400 text-white">ig</a>
            <a v-if="business.twitter" :href="business.twitter" target="_blank" class="social-pill bg-sky-500 text-white">𝕏</a>
            <a v-if="business.whatsapp" :href="`https://wa.me/${business.whatsapp}`" target="_blank" class="social-pill bg-green-500 text-white">wa</a>
          </div>
        </div>
      </div>

      <!-- Body -->
      <div class="page-container py-12">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Main content -->
          <div class="lg:col-span-2 space-y-8">
            <!-- About -->
            <div v-if="business.description" class="card p-6">
              <h2 class="font-display text-2xl font-semibold text-rw-dark mb-4">About</h2>
              <p class="text-gray-600 leading-relaxed whitespace-pre-line">{{ business.description }}</p>
            </div>

            <!-- Products/Services -->
            <div v-if="business.products_services?.length" class="card p-6">
              <h2 class="font-display text-2xl font-semibold text-rw-dark mb-6">
                {{ business.category === 'product' ? 'Our Products' : 'Our Services' }}
              </h2>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div v-for="item in business.products_services.filter(i => i.is_available)" :key="item.id"
                  class="group rounded-2xl border border-gray-100 overflow-hidden hover:shadow-card transition-all duration-300">
                  <div v-if="item.image_url" class="h-40 overflow-hidden bg-gray-100">
                    <img :src="item.image_url" :alt="item.name" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                  </div>
                  <div class="p-4">
                    <h3 class="font-semibold text-rw-dark">{{ item.name }}</h3>
                    <p v-if="item.description" class="text-sm text-gray-500 mt-1 line-clamp-2">{{ item.description }}</p>
                    <p v-if="item.price" class="text-rw-green-700 font-bold mt-2">{{ item.price.toLocaleString() }} {{ item.currency }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Reviews Section -->
            <div class="card p-6">
              <h2 class="font-display text-2xl font-semibold text-rw-dark mb-6">Customer Reviews</h2>
              <div v-if="visibleFeedback.length" class="space-y-4 mb-8">
                <div v-for="f in visibleFeedback.slice(0, showAllReviews ? 999 : 3)" :key="f.id" class="flex gap-4 py-4 border-b border-gray-50 last:border-0">
                  <div class="w-10 h-10 rounded-full bg-rw-green-50 flex items-center justify-center font-display font-bold text-rw-green-700 text-sm flex-shrink-0">
                    {{ f.visitor_name[0].toUpperCase() }}
                  </div>
                  <div class="flex-1">
                    <div class="flex items-center gap-2 mb-1">
                      <span class="font-semibold text-sm">{{ f.visitor_name }}</span>
                      <div class="text-rw-gold-400 text-sm">{{ '★'.repeat(f.rating) }}{{ '☆'.repeat(5-f.rating) }}</div>
                    </div>
                    <p class="text-sm text-gray-500">{{ f.comment }}</p>
                  </div>
                </div>
                <button v-if="visibleFeedback.length > 3" @click="showAllReviews = !showAllReviews" class="btn-ghost text-sm mt-2">
                  {{ showAllReviews ? 'Show less' : `Show all ${visibleFeedback.length} reviews` }}
                </button>
              </div>
              <div v-else class="text-gray-400 text-sm mb-6">No reviews yet. Be the first!</div>
              <!-- Leave review form -->
              <div class="bg-gray-50 rounded-2xl p-5 border border-gray-100">
                <h3 class="font-semibold text-rw-dark mb-4">Leave a Review</h3>
                <div class="flex gap-2 mb-4">
                  <span v-for="i in 5" :key="i" class="star-interactive text-2xl" :class="{ active: i <= feedbackForm.rating }" @click="feedbackForm.rating = i">★</span>
                </div>
                <div class="space-y-3">
                  <input v-model="feedbackForm.visitor_name" type="text" placeholder="Your name *" class="input-field" />
                  <textarea v-model="feedbackForm.comment" rows="3" placeholder="Share your experience…" class="input-field resize-none"></textarea>
                  <button @click="submitFeedback" :disabled="submittingFeedback" class="btn-primary w-full">
                    {{ submittingFeedback ? 'Submitting…' : 'Submit Review' }}
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Sidebar -->
          <div class="space-y-6">
            <!-- Contact info -->
            <div class="card p-5">
              <h3 class="font-display font-semibold text-lg text-rw-dark mb-4">Contact</h3>
              <div class="space-y-3 text-sm">
                <a v-if="business.email" :href="`mailto:${business.email}`" class="contact-row">
                  <svg class="w-4 h-4 text-rw-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
                  {{ business.email }}
                </a>
                <a v-if="business.phone" :href="`tel:${business.phone}`" class="contact-row">
                  <svg class="w-4 h-4 text-rw-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>
                  {{ business.phone }}
                </a>
                <div v-if="business.address" class="contact-row cursor-default">
                  <svg class="w-4 h-4 text-rw-green-600 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /></svg>
                  {{ business.address }}
                </div>
                <a v-if="business.website" :href="business.website" target="_blank" class="contact-row">
                  <svg class="w-4 h-4 text-rw-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" /></svg>
                  Visit Website
                </a>
              </div>
            </div>

            <!-- Booking form -->
            <div class="card p-5 border-rw-green-200 bg-rw-green-50/50">
              <h3 class="font-display font-semibold text-lg text-rw-dark mb-1">Book / Inquire</h3>
              <p class="text-xs text-gray-500 mb-4">Send a request directly to this business.</p>
              <div v-if="bookingSuccess" class="p-4 bg-green-100 rounded-xl text-green-700 text-sm font-medium">
                ✅ Request sent! They'll contact you soon.
              </div>
              <div v-else class="space-y-3">
                <input v-model="bookingForm.visitor_name" type="text" placeholder="Your name *" class="input-field text-sm" />
                <input v-model="bookingForm.email" type="email" placeholder="Email address *" class="input-field text-sm" />
                <input v-model="bookingForm.phone" type="tel" placeholder="Phone number" class="input-field text-sm" />
                <input v-model="bookingForm.preferred_date" type="date" class="input-field text-sm" />
                <textarea v-model="bookingForm.message" rows="3" placeholder="Your message or inquiry…" class="input-field text-sm resize-none"></textarea>
                <button @click="submitBooking" :disabled="submittingBooking" class="btn-primary w-full text-sm">
                  {{ submittingBooking ? 'Sending…' : 'Send Request' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ══════════════════════ CLASSIC TEMPLATE ══════════════════════ -->
    <div v-else-if="business.template === 'classic'" class="min-h-screen" style="background: #F5F0E8; color: #1A1A2E; font-family: 'Playfair Display', serif;">
      <!-- Top bar -->
      <div style="background: #1A1A2E; padding: 10px 0;">
        <div class="page-container flex justify-between items-center text-xs" style="color: #D4A853;">
          <span v-if="business.city">📍 {{ business.city }}, Rwanda</span>
          <div class="flex gap-4">
            <a v-if="business.email" :href="`mailto:${business.email}`" style="color: #D4A853;">{{ business.email }}</a>
            <a v-if="business.phone" :href="`tel:${business.phone}`" style="color: #D4A853;">{{ business.phone }}</a>
          </div>
        </div>
      </div>

      <!-- Header -->
      <header class="py-12 text-center border-b-4" style="border-color: #D4A853; background: #1A1A2E;">
        <div class="page-container">
          <div class="flex justify-center mb-6">
            <div class="w-24 h-24 rounded-full border-4 overflow-hidden" style="border-color: #D4A853;">
              <img v-if="business.logo_url" :src="business.logo_url" alt="logo" class="w-full h-full object-cover" />
              <div v-else class="w-full h-full flex items-center justify-center text-4xl font-bold" style="background: #D4A853; color: #1A1A2E;">{{ business.name[0] }}</div>
            </div>
          </div>
          <h1 class="text-4xl md:text-5xl font-bold mb-3" style="color: #fff; letter-spacing: -1px;">{{ business.name }}</h1>
          <p v-if="business.tagline" class="text-lg mb-4" style="color: #D4A853; font-style: italic;">{{ business.tagline }}</p>
          <div class="flex justify-center gap-4 flex-wrap">
            <a v-if="business.facebook" :href="business.facebook" target="_blank" class="classic-social">Facebook</a>
            <a v-if="business.instagram" :href="business.instagram" target="_blank" class="classic-social">Instagram</a>
            <a v-if="business.twitter" :href="business.twitter" target="_blank" class="classic-social">Twitter</a>
          </div>
        </div>
      </header>

      <!-- Nav -->
      <nav class="sticky top-0 z-40 py-3 shadow-sm" style="background: #F5F0E8; border-bottom: 1px solid #d4c098;">
        <div class="page-container flex gap-8 justify-center text-sm font-semibold" style="font-family: 'DM Sans', sans-serif; color: #1A1A2E; letter-spacing: 0.05em; text-transform: uppercase;">
          <a href="#about">About</a>
          <a href="#offerings">{{ business.category === 'product' ? 'Products' : 'Services' }}</a>
          <a href="#reviews">Reviews</a>
          <a href="#contact">Contact</a>
        </div>
      </nav>

      <div class="page-container py-16 max-w-5xl">
        <!-- About -->
        <section id="about" class="mb-16 text-center" v-if="business.description">
          <h2 class="text-3xl font-bold mb-2" style="color: #1A1A2E;">About Us</h2>
          <div class="w-24 h-1 mx-auto mb-6" style="background: #D4A853;"></div>
          <p class="text-lg leading-relaxed max-w-2xl mx-auto" style="color: #4a4a4a; font-family: 'DM Sans', sans-serif;">{{ business.description }}</p>
        </section>

        <!-- Products/Services -->
        <section id="offerings" class="mb-16" v-if="business.products_services?.length">
          <h2 class="text-3xl font-bold mb-2 text-center" style="color: #1A1A2E;">{{ business.category === 'product' ? 'Our Products' : 'Our Services' }}</h2>
          <div class="w-24 h-1 mx-auto mb-10" style="background: #D4A853;"></div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div v-for="item in business.products_services.filter(i => i.is_available)" :key="item.id"
              class="text-center rounded-2xl overflow-hidden shadow-md" style="background: #fff; border: 1px solid #e8dfc8;">
              <div v-if="item.image_url" class="h-44 overflow-hidden">
                <img :src="item.image_url" :alt="item.name" class="w-full h-full object-cover" />
              </div>
              <div class="p-5">
                <h3 class="text-xl font-bold mb-2" style="color: #1A1A2E;">{{ item.name }}</h3>
                <p v-if="item.description" class="text-sm mb-3" style="color: #666; font-family: 'DM Sans', sans-serif;">{{ item.description }}</p>
                <p v-if="item.price" class="font-bold text-lg" style="color: #D4A853;">{{ item.price.toLocaleString() }} {{ item.currency }}</p>
              </div>
            </div>
          </div>
        </section>

        <!-- Reviews -->
        <section id="reviews" class="mb-16">
          <h2 class="text-3xl font-bold mb-2 text-center" style="color: #1A1A2E;">What Clients Say</h2>
          <div class="w-24 h-1 mx-auto mb-10" style="background: #D4A853;"></div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
            <div v-for="f in visibleFeedback.slice(0,4)" :key="f.id" class="p-5 rounded-2xl italic" style="background: #fff; border: 1px solid #e8dfc8; font-family: 'DM Sans', sans-serif;">
              <div class="text-rw-gold-400 mb-2 text-lg">{{ '★'.repeat(f.rating) }}{{ '☆'.repeat(5-f.rating) }}</div>
              <p class="text-sm mb-3" style="color: #555;">"{{ f.comment || 'Great experience!' }}"</p>
              <p class="font-semibold text-xs" style="color: #1A1A2E;">— {{ f.visitor_name }}</p>
            </div>
          </div>
          <!-- Leave review -->
          <div class="rounded-2xl p-6" style="background: #1A1A2E;">
            <h3 class="text-xl font-bold mb-4" style="color: #D4A853;">Share Your Experience</h3>
            <div class="flex gap-2 mb-4">
              <span v-for="i in 5" :key="i" class="star-interactive" :class="{ active: i <= feedbackForm.rating }" @click="feedbackForm.rating = i" style="font-size: 1.8rem;">★</span>
            </div>
            <div class="space-y-3">
              <input v-model="feedbackForm.visitor_name" type="text" placeholder="Your name *" class="w-full px-4 py-3 rounded-xl text-sm" style="background: rgba(255,255,255,0.1); border: 1px solid rgba(212,168,83,0.3); color: #fff; outline: none;" />
              <textarea v-model="feedbackForm.comment" rows="3" placeholder="Your feedback…" class="w-full px-4 py-3 rounded-xl text-sm resize-none" style="background: rgba(255,255,255,0.1); border: 1px solid rgba(212,168,83,0.3); color: #fff; outline: none;"></textarea>
              <button @click="submitFeedback" :disabled="submittingFeedback" class="w-full py-3 rounded-xl font-semibold text-sm transition-all" style="background: #D4A853; color: #1A1A2E; font-family: 'DM Sans', sans-serif;">
                {{ submittingFeedback ? 'Submitting…' : 'Submit Review' }}
              </button>
            </div>
          </div>
        </section>

        <!-- Contact + Booking -->
        <section id="contact" class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div class="rounded-2xl p-6" style="background: #1A1A2E; color: #fff;">
            <h3 class="text-2xl font-bold mb-6" style="color: #D4A853;">Get In Touch</h3>
            <div class="space-y-4 text-sm" style="font-family: 'DM Sans', sans-serif;">
              <div v-if="business.email" class="flex items-center gap-3"><span style="color: #D4A853;">✉</span> {{ business.email }}</div>
              <div v-if="business.phone" class="flex items-center gap-3"><span style="color: #D4A853;">☎</span> {{ business.phone }}</div>
              <div v-if="business.address" class="flex items-center gap-3"><span style="color: #D4A853;">📍</span> {{ business.address }}</div>
            </div>
          </div>
          <div class="rounded-2xl p-6" style="background: #fff; border: 1px solid #e8dfc8;">
            <h3 class="text-2xl font-bold mb-4" style="color: #1A1A2E;">Send a Request</h3>
            <div v-if="bookingSuccess" class="p-4 rounded-xl text-sm font-medium" style="background: #d4edda; color: #155724;">Request sent!</div>
            <div v-else class="space-y-3" style="font-family: 'DM Sans', sans-serif;">
              <input v-model="bookingForm.visitor_name" type="text" placeholder="Your name *" class="w-full px-4 py-2.5 rounded-xl border text-sm focus:outline-none" style="border-color: #d4c098;" />
              <input v-model="bookingForm.email" type="email" placeholder="Email *" class="w-full px-4 py-2.5 rounded-xl border text-sm focus:outline-none" style="border-color: #d4c098;" />
              <input v-model="bookingForm.phone" type="tel" placeholder="Phone" class="w-full px-4 py-2.5 rounded-xl border text-sm focus:outline-none" style="border-color: #d4c098;" />
              <input v-model="bookingForm.preferred_date" type="date" class="w-full px-4 py-2.5 rounded-xl border text-sm focus:outline-none" style="border-color: #d4c098;" />
              <textarea v-model="bookingForm.message" rows="3" placeholder="Your message…" class="w-full px-4 py-2.5 rounded-xl border text-sm resize-none focus:outline-none" style="border-color: #d4c098;"></textarea>
              <button @click="submitBooking" :disabled="submittingBooking" class="w-full py-3 rounded-xl font-bold text-sm transition-all" style="background: #1A1A2E; color: #D4A853;">
                {{ submittingBooking ? 'Sending…' : 'Send Request' }}
              </button>
            </div>
          </div>
        </section>
      </div>
    </div>

    <!-- ══════════════════════ BOLD TEMPLATE ══════════════════════ -->
    <div v-else-if="business.template === 'bold'" class="min-h-screen" style="background: #0D0D0D; color: #fff;">
      <!-- Full-height hero -->
      <div class="relative h-screen flex flex-col justify-center overflow-hidden">
        <img v-if="business.cover_url" :src="business.cover_url" alt="cover" class="absolute inset-0 w-full h-full object-cover opacity-20" />
        <div class="absolute inset-0" style="background: linear-gradient(135deg, rgba(212,168,83,0.15) 0%, rgba(0,0,0,0) 60%)"></div>

        <div class="page-container relative z-10">
          <div class="flex items-center gap-3 mb-8">
            <div class="w-16 h-16 rounded-2xl overflow-hidden border-2" style="border-color: #D4A853;">
              <img v-if="business.logo_url" :src="business.logo_url" :alt="business.name" class="w-full h-full object-cover" />
              <div v-else class="w-full h-full flex items-center justify-center text-2xl font-bold" style="background: #D4A853; color: #0D0D0D;">{{ business.name[0] }}</div>
            </div>
            <div>
              <span class="text-xs uppercase tracking-widest font-semibold" style="color: #D4A853;">{{ business.city || 'Rwanda' }}</span>
              <div class="flex gap-2 mt-1">
                <span class="text-xs px-2 py-0.5 rounded-full border" style="border-color: rgba(212,168,83,0.4); color: #D4A853;">{{ business.category === 'product' ? 'Products' : 'Services' }}</span>
              </div>
            </div>
          </div>
          <h1 class="font-display font-bold leading-none mb-4" style="font-size: clamp(3rem, 10vw, 7rem); letter-spacing: -3px;">
            {{ business.name }}
          </h1>
          <p v-if="business.tagline" class="text-xl mb-8" style="color: rgba(255,255,255,0.6); max-width: 500px; font-family: 'DM Sans', sans-serif;">{{ business.tagline }}</p>
          <div class="flex gap-4 flex-wrap">
            <a href="#booking" class="px-8 py-4 font-bold rounded-xl transition-all hover:scale-105 text-sm uppercase tracking-wider" style="background: #D4A853; color: #0D0D0D;">Book Now</a>
            <a href="#about" class="px-8 py-4 font-bold rounded-xl border text-sm uppercase tracking-wider hover:bg-white/10 transition-all" style="border-color: rgba(255,255,255,0.3); color: #fff;">Learn More</a>
          </div>
          <!-- Rating -->
          <div v-if="avgRating" class="flex items-center gap-2 mt-8">
            <div class="text-lg" style="color: #D4A853;">{{ '★'.repeat(Math.round(avgRating)) }}{{ '☆'.repeat(5 - Math.round(avgRating)) }}</div>
            <span class="text-sm" style="color: rgba(255,255,255,0.5);">{{ avgRating }}/5 · {{ visibleFeedback.length }} reviews</span>
          </div>
        </div>

        <!-- Scroll indicator -->
        <div class="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 animate-bounce" style="color: rgba(255,255,255,0.3);">
          <span class="text-xs uppercase tracking-widest">Scroll</span>
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
        </div>
      </div>

      <!-- Content sections -->
      <div class="page-container py-20 space-y-20">
        <!-- About -->
        <section id="about" v-if="business.description">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div>
              <p class="text-xs uppercase tracking-widest mb-4" style="color: #D4A853; font-family: 'DM Sans', sans-serif;">Our Story</p>
              <h2 class="font-display text-4xl font-bold mb-6" style="color: #fff;">Who We Are</h2>
              <p class="text-lg leading-relaxed" style="color: rgba(255,255,255,0.65); font-family: 'DM Sans', sans-serif;">{{ business.description }}</p>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div class="rounded-2xl p-5 text-center" style="background: rgba(212,168,83,0.1); border: 1px solid rgba(212,168,83,0.2);">
                <p class="font-display text-3xl font-bold" style="color: #D4A853;">{{ business.view_count }}+</p>
                <p class="text-xs mt-1 uppercase tracking-wider" style="color: rgba(255,255,255,0.5); font-family: 'DM Sans', sans-serif;">Profile Views</p>
              </div>
              <div class="rounded-2xl p-5 text-center" style="background: rgba(212,168,83,0.1); border: 1px solid rgba(212,168,83,0.2);">
                <p class="font-display text-3xl font-bold" style="color: #D4A853;">{{ visibleFeedback.length }}</p>
                <p class="text-xs mt-1 uppercase tracking-wider" style="color: rgba(255,255,255,0.5); font-family: 'DM Sans', sans-serif;">Reviews</p>
              </div>
            </div>
          </div>
        </section>

        <!-- Products/Services -->
        <section v-if="business.products_services?.length">
          <p class="text-xs uppercase tracking-widest mb-3" style="color: #D4A853; font-family: 'DM Sans', sans-serif;">What We Offer</p>
          <h2 class="font-display text-4xl font-bold mb-12">{{ business.category === 'product' ? 'Products' : 'Services' }}</h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="item in business.products_services.filter(i => i.is_available)" :key="item.id"
              class="group rounded-2xl overflow-hidden transition-all duration-300 hover:scale-[1.02]"
              style="background: #1a1a1a; border: 1px solid rgba(255,255,255,0.08);">
              <div v-if="item.image_url" class="h-48 overflow-hidden">
                <img :src="item.image_url" :alt="item.name" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500 opacity-80 group-hover:opacity-100" />
              </div>
              <div class="p-5">
                <h3 class="font-display text-xl font-bold mb-2">{{ item.name }}</h3>
                <p v-if="item.description" class="text-sm mb-4" style="color: rgba(255,255,255,0.55); font-family: 'DM Sans', sans-serif;">{{ item.description }}</p>
                <p v-if="item.price" class="font-bold text-lg" style="color: #D4A853;">{{ item.price.toLocaleString() }} {{ item.currency }}</p>
              </div>
            </div>
          </div>
        </section>

        <!-- Reviews + Booking side by side -->
        <section class="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <!-- Reviews -->
          <div>
            <p class="text-xs uppercase tracking-widest mb-3" style="color: #D4A853; font-family: 'DM Sans', sans-serif;">Testimonials</p>
            <h2 class="font-display text-3xl font-bold mb-8">What They Say</h2>
            <div class="space-y-4 mb-6">
              <div v-for="f in visibleFeedback.slice(0,3)" :key="f.id" class="rounded-xl p-5" style="background: #1a1a1a; border: 1px solid rgba(255,255,255,0.08);">
                <div style="color: #D4A853;" class="mb-2">{{ '★'.repeat(f.rating) }}{{ '☆'.repeat(5-f.rating) }}</div>
                <p class="text-sm mb-3" style="color: rgba(255,255,255,0.65); font-family: 'DM Sans', sans-serif; font-style: italic;">"{{ f.comment || 'Great experience!' }}"</p>
                <p class="text-xs font-bold" style="color: rgba(255,255,255,0.4);">— {{ f.visitor_name }}</p>
              </div>
              <div v-if="!visibleFeedback.length" class="text-sm" style="color: rgba(255,255,255,0.4); font-family: 'DM Sans', sans-serif;">No reviews yet.</div>
            </div>
            <!-- Leave review -->
            <div class="rounded-2xl p-5" style="background: rgba(212,168,83,0.08); border: 1px solid rgba(212,168,83,0.2);">
              <p class="font-bold mb-3" style="color: #D4A853;">Leave a Review</p>
              <div class="flex gap-2 mb-3">
                <span v-for="i in 5" :key="i" class="star-interactive" :class="{ active: i <= feedbackForm.rating }" @click="feedbackForm.rating = i" style="font-size: 1.6rem;">★</span>
              </div>
              <div class="space-y-2">
                <input v-model="feedbackForm.visitor_name" type="text" placeholder="Your name *" class="w-full px-3 py-2 rounded-lg text-sm" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1); color: #fff; outline:none;" />
                <textarea v-model="feedbackForm.comment" rows="2" placeholder="Your experience…" class="w-full px-3 py-2 rounded-lg text-sm resize-none" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1); color: #fff; outline:none;"></textarea>
                <button @click="submitFeedback" :disabled="submittingFeedback" class="w-full py-2.5 rounded-lg font-bold text-sm" style="background: #D4A853; color: #0D0D0D;">
                  {{ submittingFeedback ? 'Submitting…' : 'Submit' }}
                </button>
              </div>
            </div>
          </div>

          <!-- Booking -->
          <div id="booking">
            <p class="text-xs uppercase tracking-widest mb-3" style="color: #D4A853; font-family: 'DM Sans', sans-serif;">Connect</p>
            <h2 class="font-display text-3xl font-bold mb-8">Make a Booking</h2>
            <div v-if="business.email || business.phone || business.address" class="space-y-3 mb-8" style="font-family: 'DM Sans', sans-serif; font-size: 0.9rem; color: rgba(255,255,255,0.6);">
              <div v-if="business.email" class="flex items-center gap-3"><span style="color: #D4A853;">✉</span> {{ business.email }}</div>
              <div v-if="business.phone" class="flex items-center gap-3"><span style="color: #D4A853;">☎</span> {{ business.phone }}</div>
              <div v-if="business.address" class="flex items-center gap-3"><span style="color: #D4A853;">📍</span> {{ business.address }}</div>
            </div>
            <div v-if="bookingSuccess" class="p-4 rounded-xl text-sm font-medium mb-4" style="background: rgba(26,158,113,0.2); color: #1a9e71;">✅ Request sent! They'll contact you soon.</div>
            <div v-else class="space-y-3" style="font-family: 'DM Sans', sans-serif;">
              <input v-model="bookingForm.visitor_name" type="text" placeholder="Your name *" class="w-full px-4 py-3 rounded-xl text-sm" style="background: #1a1a1a; border: 1px solid rgba(255,255,255,0.1); color: #fff; outline:none;" />
              <input v-model="bookingForm.email" type="email" placeholder="Email *" class="w-full px-4 py-3 rounded-xl text-sm" style="background: #1a1a1a; border: 1px solid rgba(255,255,255,0.1); color: #fff; outline:none;" />
              <input v-model="bookingForm.phone" type="tel" placeholder="Phone" class="w-full px-4 py-3 rounded-xl text-sm" style="background: #1a1a1a; border: 1px solid rgba(255,255,255,0.1); color: #fff; outline:none;" />
              <input v-model="bookingForm.preferred_date" type="date" class="w-full px-4 py-3 rounded-xl text-sm" style="background: #1a1a1a; border: 1px solid rgba(255,255,255,0.1); color: #fff; outline:none;" />
              <textarea v-model="bookingForm.message" rows="4" placeholder="Your message or inquiry…" class="w-full px-4 py-3 rounded-xl text-sm resize-none" style="background: #1a1a1a; border: 1px solid rgba(255,255,255,0.1); color: #fff; outline:none;"></textarea>
              <button @click="submitBooking" :disabled="submittingBooking" class="w-full py-4 rounded-xl font-bold text-sm uppercase tracking-wider transition-all hover:scale-[1.02]" style="background: #D4A853; color: #0D0D0D;">
                {{ submittingBooking ? 'Sending…' : 'Send Request' }}
              </button>
            </div>
          </div>
        </section>
      </div>

      <!-- Footer strip -->
      <div class="py-8 text-center text-xs uppercase tracking-widest" style="border-top: 1px solid rgba(255,255,255,0.08); color: rgba(255,255,255,0.3); font-family: 'DM Sans', sans-serif; background: #0a0a0a;">
        {{ business.name }} · Powered by <RouterLink to="/" style="color: #D4A853;">biz.rw</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { businessApi, feedbackApi, bookingApi } from '@/api'
import { useToastStore } from '@/stores/toast'
import { useAuthStore } from '@/stores/auth'
import { getErrorMessage } from '@/api/axios'

const route = useRoute()
const toast = useToastStore()
const auth = useAuthStore()

const business = ref(null)
const loading = ref(true)
const showAllReviews = ref(false)

const feedbackForm = ref({ visitor_name: '', rating: 0, comment: '' })
const submittingFeedback = ref(false)

const bookingForm = ref({ visitor_name: '', email: '', phone: '', preferred_date: '', message: '' })
const submittingBooking = ref(false)
const bookingSuccess = ref(false)

const visibleFeedback = computed(() =>
  (business.value?.feedback || []).filter(f => !f.is_hidden)
)

const avgRating = computed(() => {
  const fb = visibleFeedback.value
  if (!fb.length) return null
  return (fb.reduce((s, f) => s + f.rating, 0) / fb.length).toFixed(1)
})

onMounted(async () => {
  try {
    const { data } = await businessApi.getBySlug(route.params.slug)
    business.value = data
    document.title = `${data.name} — biz.rw`
  } catch {
    business.value = null
  } finally {
    loading.value = false
  }
})

async function submitFeedback() {
  if (!feedbackForm.value.visitor_name.trim()) { toast.error('Please enter your name.'); return }
  if (!feedbackForm.value.rating) { toast.error('Please select a rating.'); return }
  submittingFeedback.value = true
  try {
    const { data } = await feedbackApi.create(business.value.slug, feedbackForm.value)
    business.value.feedback.push(data)
    feedbackForm.value = { visitor_name: '', rating: 0, comment: '' }
    toast.success('Thank you for your review!')
  } catch (err) {
    toast.error(getErrorMessage(err))
  } finally {
    submittingFeedback.value = false
  }
}

async function submitBooking() {
  if (!bookingForm.value.visitor_name.trim() || !bookingForm.value.email.trim()) {
    toast.error('Please fill in your name and email.')
    return
  }
  submittingBooking.value = true
  try {
    await bookingApi.create(business.value.slug, bookingForm.value)
    bookingSuccess.value = true
    toast.success('Booking request sent!')
  } catch (err) {
    toast.error(getErrorMessage(err))
  } finally {
    submittingBooking.value = false
  }
}
</script>

<style scoped>
.social-pill {
  @apply inline-flex items-center justify-center w-8 h-8 rounded-lg text-xs font-bold transition-all hover:scale-110;
}
.contact-row {
  @apply flex items-center gap-2 text-gray-600 hover:text-rw-green-700 transition-colors;
}
.classic-social {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  padding: 4px 12px;
  border: 1px solid rgba(212,168,83,0.4);
  border-radius: 999px;
  color: #D4A853;
  transition: all 0.2s;
}
.classic-social:hover {
  background: rgba(212,168,83,0.15);
}
</style>
