<template>
  <div class="sidebar-wrapper">
    <nav
      class="sidebar"
      :class="{
        'sidebar-collapsed': navigationStore.sidebarCollapsed,
        'sidebar-mobile-open': navigationStore.mobileSidebarOpen,
      }"
    >
      <!-- Sidebar Header -->
      <div class="sidebar-header">
        <router-link to="/" class="sidebar-brand">
          <!-- <i class="fas fa-cube brand-icon"></i> -->
          <span class="brand-text" v-show="!navigationStore.sidebarCollapsed"
            >Quickbalance</span
          >
        </router-link>
        <button
          class="btn btn-link sidebar-toggle d-lg-none"
          @click="navigationStore.closeMobileSidebar"
        >
          <i class="fas fa-times"></i>
        </button>
      </div>

      <!-- User Profile Section -->
      <div class="sidebar-profile" v-show="!navigationStore.sidebarCollapsed">
        <div class="profile-avatar">
          <img
            :src="authStore.userAvatar"
            :alt="authStore.userName"
            class="avatar-img"
          />
          <div class="status-indicator status-online"></div>
        </div>
        <div class="profile-info">
          <h6 class="profile-name">{{ authStore.userName }}</h6>
          <small class="profile-role">{{
            formatRole(authStore.userRole)
          }}</small>
        </div>
      </div>

      <!-- Sidebar Content -->
      <div class="sidebar-content">
        <ul class="sidebar-nav">
          <!-- Dashboard Section -->
          <li class="nav-section">
            <span
              class="nav-section-title"
              v-show="!navigationStore.sidebarCollapsed"
              >Dashboard</span
            >
          </li>
          <li class="nav-item">
            <router-link
              to="/dashboard"
              class="nav-link"
              :class="{ active: $route.name === 'Dashboard' }"
              @click="handleMenuClick"
            >
              <i class="nav-icon fas fa-tachometer-alt"></i>
              <span class="nav-text" v-show="!navigationStore.sidebarCollapsed"
                >Dashboard</span
              >
            </router-link>
          </li>
          <li class="nav-item">
            <router-link
              to="/analytics"
              class="nav-link"
              :class="{ active: $route.name === 'Analytics' }"
              @click="handleMenuClick"
            >
              <i class="nav-icon fas fa-chart-line"></i>
              <span class="nav-text" v-show="!navigationStore.sidebarCollapsed"
                >Analytics</span
              >
              <span class="nav-badge" v-show="!navigationStore.sidebarCollapsed"
                >New</span
              >
            </router-link>
          </li>

          <!-- Management Section -->
          <li
            class="nav-section"
            v-if="authStore.hasRole(['admin', 'manager'])"
          >
            <span
              class="nav-section-title"
              v-show="!navigationStore.sidebarCollapsed"
              >Management</span
            >
          </li>
          <li class="nav-item" v-if="authStore.hasRole(['admin', 'manager'])">
            <router-link
              to="/users"
              class="nav-link"
              :class="{
                active:
                  $route.name === 'Users' || $route.name === 'UserProfile',
              }"
              @click="handleMenuClick"
            >
              <i class="nav-icon fas fa-users"></i>
              <span class="nav-text" v-show="!navigationStore.sidebarCollapsed"
                >Users</span
              >
              <span
                class="nav-count"
                v-show="!navigationStore.sidebarCollapsed"
                >{{ userCount }}</span
              >
            </router-link>
          </li>

          <!-- Projects Submenu -->
          <li
            class="nav-item"
            :class="{ 'nav-item-expanded': projectsExpanded }"
          >
            <a
              href="#"
              class="nav-link nav-link-submenu"
              :class="{ active: $route.path.startsWith('/projects') }"
              @click.prevent="toggleSubmenu('projects')"
            >
              <i class="nav-icon fas fa-project-diagram"></i>
              <span class="nav-text" v-show="!navigationStore.sidebarCollapsed"
                >Projects</span
              >
              <i
                class="nav-arrow fas fa-chevron-right"
                v-show="!navigationStore.sidebarCollapsed"
              ></i>
            </a>
            <ul
              class="nav-submenu"
              v-show="projectsExpanded && !navigationStore.sidebarCollapsed"
            >
              <li>
                <router-link
                  to="/projects"
                  class="nav-link"
                  :class="{ active: $route.name === 'Projects' }"
                  @click="handleMenuClick"
                >
                  <span class="nav-text">All Projects</span>
                </router-link>
              </li>
              <li>
                <router-link
                  to="/projects/create"
                  class="nav-link"
                  :class="{ active: $route.name === 'CreateProject' }"
                  @click="handleMenuClick"
                >
                  <span class="nav-text">Create Project</span>
                </router-link>
              </li>
            </ul>
          </li>

          <li class="nav-item">
            <router-link
              to="/reports"
              class="nav-link"
              :class="{ active: $route.name === 'Reports' }"
              @click="handleMenuClick"
            >
              <i class="nav-icon fas fa-chart-bar"></i>
              <span class="nav-text" v-show="!navigationStore.sidebarCollapsed"
                >Reports</span
              >
            </router-link>
          </li>

          <!-- Tools Section -->
          <li class="nav-section">
            <span
              class="nav-section-title"
              v-show="!navigationStore.sidebarCollapsed"
              >Tools</span
            >
          </li>
          <li class="nav-item">
            <router-link
              to="/calendar"
              class="nav-link"
              :class="{ active: $route.name === 'Calendar' }"
              @click="handleMenuClick"
            >
              <i class="nav-icon fas fa-calendar"></i>
              <span class="nav-text" v-show="!navigationStore.sidebarCollapsed"
                >Calendar</span
              >
            </router-link>
          </li>
          <li class="nav-item">
            <router-link
              to="/messages"
              class="nav-link"
              :class="{ active: $route.name === 'Messages' }"
              @click="handleMenuClick"
            >
              <i class="nav-icon fas fa-envelope"></i>
              <span class="nav-text" v-show="!navigationStore.sidebarCollapsed"
                >Messages</span
              >
              <span
                class="nav-badge badge-danger"
                v-show="!navigationStore.sidebarCollapsed && unreadMessages > 0"
              >
                {{ unreadMessages }}
              </span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link
              to="/settings"
              class="nav-link"
              :class="{ active: $route.name === 'Settings' }"
              @click="handleMenuClick"
            >
              <i class="nav-icon fas fa-cog"></i>
              <span class="nav-text" v-show="!navigationStore.sidebarCollapsed"
                >Settings</span
              >
            </router-link>
          </li>
        </ul>
      </div>

      <!-- Sidebar Footer -->
      <div class="sidebar-footer">
        <div class="sidebar-stats" v-show="!navigationStore.sidebarCollapsed">
          <div class="stat-item">
            <small class="text-muted">Storage Used</small>
            <div class="progress progress-sm mt-1">
              <div
                class="progress-bar bg-primary"
                :style="{ width: storageUsed + '%' }"
              ></div>
            </div>
            <small class="text-muted">{{ storageUsed }}% of 10 GB</small>
          </div>
        </div>

        <button
          class="btn btn-link sidebar-collapse-btn"
          @click="navigationStore.toggleSidebar"
          :title="
            navigationStore.sidebarCollapsed
              ? 'Expand Sidebar'
              : 'Collapse Sidebar'
          "
        >
          <i
            class="fas"
            :class="
              navigationStore.sidebarCollapsed
                ? 'fa-chevron-right'
                : 'fa-chevron-left'
            "
          ></i>
        </button>
      </div>
    </nav>

    <!-- Sidebar Overlay for Mobile -->
    <div
      class="sidebar-overlay d-lg-none"
      :class="{ show: navigationStore.mobileSidebarOpen }"
      @click="navigationStore.closeMobileSidebar"
    ></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { useAuthStore } from "../../stores/auth";
import { useNavigationStore } from "../../stores/navigation";

const route = useRoute();
const authStore = useAuthStore();
const navigationStore = useNavigationStore();

// Reactive data
const projectsExpanded = ref(false);
const userCount = ref(1247);
const unreadMessages = ref(5);
const storageUsed = ref(65);

// Methods
const toggleSubmenu = (menu) => {
  if (menu === "projects") {
    projectsExpanded.value = !projectsExpanded.value;
  }
};

const handleMenuClick = () => {
  // Close mobile sidebar when menu item is clicked
  if (window.innerWidth < 992) {
    navigationStore.closeMobileSidebar();
  }
};

const formatRole = (role) => {
  const roleMap = {
    admin: "Administrator",
    manager: "Manager",
    user: "User",
  };
  return roleMap[role] || role;
};

// Watch route changes to expand appropriate submenus
watch(
  route,
  (newRoute) => {
    if (newRoute.path.startsWith("/projects")) {
      projectsExpanded.value = true;
    }
  },
  { immediate: true }
);

onMounted(() => {
  navigationStore.initializeSidebar();
});
</script>

<style scoped>
/* Same styles as before, but with router-link specific styles */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 200px;
  background: linear-gradient(135deg, #162dff 0%, #162dff 100%);
  color: white;
  transition: all 0.3s ease;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  transform: translateX(-100%);
}

.sidebar-collapsed {
  width: 70px;
}

.sidebar-mobile-open {
  transform: translateX(0);
}

@media (min-width: 992px) {
  .sidebar {
    transform: translateX(0);
  }
}

.sidebar-header {
  padding: 1.5rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 80px;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
  transition: color 0.3s ease;
}

.sidebar-brand:hover {
  color: rgba(255, 255, 255, 0.8);
}

.brand-icon {
  margin-right: 0.75rem;
  font-size: 1.75rem;
}

.brand-text {
  transition: opacity 0.3s ease;
}

.sidebar-toggle {
  color: white;
  border: none;
  background: none;
  font-size: 1.2rem;
  padding: 0.5rem;
}

.sidebar-profile {
  padding: 1.5rem 1rem;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 1rem;
}

.profile-avatar {
  position: relative;
  display: inline-block;
  margin-bottom: 1rem;
}

.avatar-img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 3px solid rgba(255, 255, 255, 0.3);
}

.status-indicator {
  position: absolute;
  bottom: 5px;
  right: 5px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 3px solid white;
}

.status-online {
  background-color: #28a745;
}

.profile-info h6 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.profile-role {
  opacity: 0.8;
  font-size: 0.875rem;
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 0;
}

.sidebar-nav {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-section {
  padding: 1rem 1rem 0.5rem;
  margin-top: 1rem;
}

.nav-section:first-child {
  margin-top: 0;
}

.nav-section-title {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  opacity: 0.7;
  font-weight: 600;
}

.nav-item {
  margin: 0.25rem 0;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 0.875rem 1rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s ease;
  border-radius: 0 25px 25px 0;
  margin-right: 1rem;
  position: relative;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  transform: translateX(5px);
}

.nav-link.active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-weight: 600;
}

.nav-link.active::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: #fff;
  border-radius: 0 2px 2px 0;
}

.nav-icon {
  width: 20px;
  text-align: center;
  margin-right: 0.875rem;
  font-size: 1.1rem;
}

.nav-text {
  flex: 1;
  font-size: 0.9rem;
}

.nav-badge {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 0.7rem;
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
  margin-left: auto;
}

.nav-badge.badge-danger {
  background: #dc3545;
}

.nav-count {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  font-size: 0.75rem;
  padding: 0.2rem 0.5rem;
  border-radius: 8px;
  margin-left: auto;
}

.nav-arrow {
  margin-left: auto;
  font-size: 0.8rem;
  transition: transform 0.3s ease;
}

.nav-item-expanded .nav-arrow {
  transform: rotate(90deg);
}

.nav-submenu {
  list-style: none;
  padding: 0;
  margin: 0;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 0 15px 15px 0;
  margin-right: 1rem;
  overflow: hidden;
}

.nav-submenu .nav-link {
  padding: 0.625rem 1rem 0.625rem 3.5rem;
  font-size: 0.85rem;
  margin-right: 0;
  border-radius: 0;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-stats {
  margin-bottom: 1rem;
}

.stat-item {
  text-align: center;
}

.progress-sm {
  height: 4px;
}

.sidebar-collapse-btn {
  width: 100%;
  color: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.1);
  padding: 0.75rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.sidebar-collapse-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.sidebar-overlay.show {
  opacity: 1;
  visibility: visible;
}

/* Scrollbar Styling */
.sidebar-content::-webkit-scrollbar {
  width: 4px;
}

.sidebar-content::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
}

.sidebar-content::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
}

.sidebar-content::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>
