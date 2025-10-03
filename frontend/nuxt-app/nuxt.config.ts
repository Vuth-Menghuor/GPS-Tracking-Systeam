// https://nuxt.com/docs/api/configuration/nuxt-config
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
      apiBase: "http://127.0.0.1:8000/api",
    },
  },

  ssr: false, // Enable SPA mode for better API integration
});
