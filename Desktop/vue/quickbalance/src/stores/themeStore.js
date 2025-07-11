import { defineStore } from "pinia";

export const useThemeStore = defineStore("theme", {
  state: () => ({
    isDarkMode: false,
  }),
  actions: {
    initializeTheme() {
      // Implement theme initialization
      this.isDarkMode = localStorage.getItem("darkMode") === "true";
    },
  },
});
