import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useNavigationStore = defineStore("navigation", () => {
  // State
  const sidebarCollapsed = ref(false);
  const mobileSidebarOpen = ref(false);
  const activeMenu = ref("dashboard");
  const breadcrumbs = ref([]);
  const pageTitle = ref("Dashboard");

  // 👇 Add submenu expanded states
  const submenus = ref({
    loanActions: false,
  });
  // Getters
  const isMobile = computed(() => {
    if (typeof window !== "undefined") {
      return window.innerWidth < 992;
    }
    return false;
  });
  // Actions
  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value;
    if (typeof window !== "undefined") {
      localStorage.setItem(
        "sidebar-collapsed",
        sidebarCollapsed.value.toString()
      );
    }
  };

  const toggleMobileSidebar = () => {
    mobileSidebarOpen.value = !mobileSidebarOpen.value;
  };

  const closeMobileSidebar = () => {
    mobileSidebarOpen.value = false;
  };

  const setActiveMenu = (menu) => {
    activeMenu.value = menu;
  };

  const setBreadcrumbs = (crumbs) => {
    breadcrumbs.value = crumbs;
  };

  const setPageTitle = (title) => {
    pageTitle.value = title;
  };

  const initializeSidebar = () => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("sidebar-collapsed");
      if (saved !== null) {
        sidebarCollapsed.value = saved === "true";
      }
    }
  };

  // 👇 Submenu toggle
  const toggleSubmenu = (menuKey) => {
    submenus.value[menuKey] = !submenus.value[menuKey];
  };

  const closeAllSubmenus = () => {
    for (const key in submenus.value) {
      submenus.value[key] = false;
    }
  };

  return {
    // State
    sidebarCollapsed,
    mobileSidebarOpen,
    activeMenu,
    breadcrumbs,
    pageTitle,
    submenus,

    // Getters
    isMobile,

    // Actions
    toggleSidebar,
    toggleMobileSidebar,
    closeMobileSidebar,
    setActiveMenu,
    setBreadcrumbs,
    setPageTitle,
    initializeSidebar,
    toggleSubmenu,
    closeAllSubmenus,
  };
});
