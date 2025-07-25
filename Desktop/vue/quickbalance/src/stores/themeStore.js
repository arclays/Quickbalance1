// stores/themeStore.js
import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useThemeStore = defineStore("theme", () => {
  // State
  const isDarkMode = ref(false);
  const themeColor = ref("#3b82f6"); // Default blue color

  // Initialize from localStorage or system preference
  const initializeTheme = () => {
    const savedTheme = localStorage.getItem("theme");
    const savedColor = localStorage.getItem("themeColor");

    if (savedTheme) {
      isDarkMode.value = savedTheme === "dark";
    } else {
      // Use system preference if no saved theme
      isDarkMode.value = window.matchMedia(
        "(prefers-color-scheme: dark)"
      ).matches;
    }

    if (savedColor) {
      themeColor.value = savedColor;
    }

    applyTheme();
  };

  // Computed properties
  const currentTheme = computed(() => (isDarkMode.value ? "dark" : "light"));
  const themeIcon = computed(() => (isDarkMode.value ? "fa-sun" : "fa-moon"));
  const themeTitle = computed(() =>
    isDarkMode.value ? "Light Mode" : "Dark Mode"
  );

  // Actions
  const toggleTheme = () => {
    isDarkMode.value = !isDarkMode.value;
    localStorage.setItem("theme", currentTheme.value);
    applyTheme();
  };

  const setThemeColor = (color) => {
    themeColor.value = color;
    localStorage.setItem("themeColor", color);
    applyTheme();
  };

  const applyTheme = () => {
    if (isDarkMode.value) {
      document.documentElement.classList.add("dark");
      document.documentElement.setAttribute("data-bs-theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      document.documentElement.setAttribute("data-bs-theme", "light");
    }

    // Apply theme color
    document.documentElement.style.setProperty(
      "--bs-primary",
      themeColor.value
    );
  };

  // Initialize theme when store is created
  initializeTheme();

  // Watch for system theme changes
  const systemThemeWatcher = window.matchMedia("(prefers-color-scheme: dark)");
  systemThemeWatcher.addEventListener("change", (e) => {
    if (!localStorage.getItem("theme")) {
      isDarkMode.value = e.matches;
      applyTheme();
    }
  });

  return {
    // State
    isDarkMode,
    themeColor,

    // Computed
    currentTheme,
    themeIcon,
    themeTitle,

    // Actions
    toggleTheme,
    setThemeColor,
    initializeTheme,
  };
});
