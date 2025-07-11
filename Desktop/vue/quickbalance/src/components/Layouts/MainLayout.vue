<template>
  <div class="main-layout" :class="{ 'dark-mode': themeStore.isDarkMode }">
    <!-- Sidebar -->
    <AppSidebar />

    <!-- Main Content Area -->
    <div
      class="main-content"
      :class="{ 'content-shifted': !navigationStore.sidebarCollapsed }"
    >
      <!-- Navbar -->
      <AppNarbar />

      <!-- Page Content -->
      <main class="page-content">
        <router-view />
      </main>
    </div>
    <!-- footer -->
    <AppFooter />
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
<script setup>
import { computed, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useNavigationStore } from "@/stores/navigation";
import { useThemeStore } from "../../stores/themeStore";
import AppSidebar from "@/components/shared/AppSidebar.vue";
import AppNarbar from "@/components/shared/AppNarbar.vue";
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

<style scoped>
.main-layout {
  min-height: 100vh;
  background: #f8f9fa;
  transition: all 0.3s ease;
}

.main-content {
  transition: margin-left 0.3s ease;
  min-height: 100vh;
}

.content-shifted {
  margin-left: 280px;
}

@media (max-width: 991.98px) {
  .content-shifted {
    margin-left: 0;
  }
}

.page-content {
  padding-top: 80px;
  padding-bottom: 2rem;
  min-height: calc(100vh - 80px);
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-spinner {
  text-align: center;
}

.loading-text {
  color: #6c757d;
  font-weight: 500;
}

.dark-mode {
  background: #1a1a1a;
  color: #ffffff;
}
</style>
