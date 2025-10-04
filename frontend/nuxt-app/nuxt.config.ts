// https://nuxt.com/docs/api/configuration/nuxt-config
// Updated for Render deployment - Oct 4, 2025
export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },

  modules: [
    "@nuxt/eslint",
    "@nuxt/fonts",
    "@nuxt/icon",
    "@nuxt/image",
    "@nuxtjs/tailwindcss",
  ],

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "https://gps-tracking-systeam.onrender.com/api",
    },
  },

  ssr: false, // Enable SPA mode for better API integration
});
