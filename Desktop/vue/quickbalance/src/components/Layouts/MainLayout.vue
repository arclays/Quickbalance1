<script setup>
import { computed, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useNavigationStore } from "@/stores/navigation";
import { useThemeStore } from "../../stores/themeStore";
import AppSidebar from "@/components/shared/AppSidebar.vue";
import AppNavbar from "@/components/shared/AppNavbar.vue";
import AppFooter from "@/components/AppFooter.vue";

const authStore = useAuthStore();
const navigationStore = useNavigationStore();
const themeStore = useThemeStore();

const loading = computed(() => authStore.loading);

onMounted(async () => {
  navigationStore.initializeSidebar();
  themeStore.initializeTheme();

  if (authStore.token) {
    await authStore.fetchUser();
  }
});
</script>

<template>
  <div class="main-layout" :class="{ 'dark-mode': themeStore.isDarkMode }">
    <!-- Sidebar -->
    <AppSidebar />

    <!-- Main Content -->
    <div
      class="main-content-wrapper"
      :class="{ collapsed: navigationStore.sidebarCollapsed }"
    >
      <!-- Navbar -->
      <AppNavbar :sidebar-collapsed="navigationStore.sidebarCollapsed" />

      <!-- Main Content -->
      <div class="main-content">
        <!-- Page Content -->
        <main class="page-content">
          <router-view />
        </main>

        <!-- Footer -->
        <AppFooter />
      </div>
    </div>

    <!-- Global Loading Spinner -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <div class="loading-text mt-3">Loading...</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.main-layout {
  display: flex;
  min-height: 100vh;
  /* background: #1d7ad8; */
  transition: background 0.3s ease;
  position: relative;
}

.main-content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  margin-left: 210px;
  transition: margin-left 0.3s ease;
  width: calc(100% - 280px);
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding-top: 60px;
}
.main-content-wrapper {
  margin-left: 200px;
  transition: margin-left 0.3s ease;
}

.main-content-wrapper.collapsed {
  margin-left: 80px;
}

@media (max-width: 991.98px) {
  .main-content-wrapper,
  .main-content-wrapper.collapsed {
    margin-left: 0;
  }
}
.loading-overlay {
  position: fixed;
  inset: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}

.loading-spinner {
  text-align: center;
}

.loading-text {
  color: #6c757d;
  font-weight: 500;
}

/* Dark Mode */
.dark-mode {
  background: #121212;
  color: #f1f1f1;
}

.dark-mode .loading-overlay {
  background: rgba(0, 0, 0, 0.8);
}
</style>
