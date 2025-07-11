<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
    <div class="container-fluid">
      <!-- Mobile Menu Toggle -->
      <button
        class="btn btn-link navbar-toggler d-lg-none me-3"
        @click="navigationStore.toggleMobileSidebar"
      >
        <i class="fas fa-bars"></i>
      </button>

      <!-- Breadcrumb Navigation -->
      <nav aria-label="breadcrumb" class="d-none d-md-block">
        <ol class="breadcrumb mb-0">
          <li class="breadcrumb-item">
            <router-link to="/" class="text-decoration-none">
              <i class="fas fa-home me-1"></i>
              Home
            </router-link>
          </li>
          <li
            v-for="(crumb, index) in breadcrumbs"
            :key="index"
            class="breadcrumb-item"
            :class="{ active: index === breadcrumbs.length - 1 }"
          >
            <router-link
              v-if="crumb.to && index !== breadcrumbs.length - 1"
              :to="crumb.to"
              class="text-decoration-none"
            >
              {{ crumb.text }}
            </router-link>
            <span v-else>{{ crumb.text }}</span>
          </li>
        </ol>
      </nav>

      <!-- Right Side Navigation -->
      <div class="navbar-nav ms-auto d-flex flex-row align-items-center">
        <!-- Search -->
        <div class="nav-item me-3">
          <div class="search-container">
            <div class="input-group">
              <input
                type="text"
                class="form-control search-input"
                placeholder="Search..."
                v-model="searchQuery"
                @keyup.enter="performSearch"
                @focus="showSearchResults = true"
                @blur="hideSearchResults"
              />
              <button class="btn btn-outline-secondary" @click="performSearch">
                <i class="fas fa-search"></i>
              </button>
            </div>

            <!-- Search Results Dropdown -->
            <div
              v-if="showSearchResults && searchResults.length > 0"
              class="search-results"
            >
              <div class="search-results-header">
                <small class="text-muted">Recent searches</small>
              </div>
              <div
                v-for="result in searchResults"
                :key="result.id"
                class="search-result-item"
                @click="selectSearchResult(result)"
              >
                <div class="search-result-icon">
                  <i :class="result.icon"></i>
                </div>
                <div class="search-result-content">
                  <div class="search-result-title">{{ result.title }}</div>
                  <div class="search-result-subtitle">
                    {{ result.subtitle }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="nav-item dropdown me-3">
          <button
            class="btn btn-link nav-link dropdown-toggle position-relative"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            <i class="fas fa-plus-circle fa-lg"></i>
          </button>
          <ul class="dropdown-menu dropdown-menu-end">
            <li class="dropdown-header">Quick Actions</li>
            <li>
              <router-link class="dropdown-item" to="/projects/create">
                <i class="fas fa-project-diagram me-2"></i>
                New Project
              </router-link>
            </li>
            <li v-if="authStore.hasRole(['admin', 'manager'])">
              <a
                class="dropdown-item"
                href="#"
                @click.prevent="quickAction('new-user')"
              >
                <i class="fas fa-user-plus me-2"></i>
                Add User
              </a>
            </li>
            <li>
              <router-link class="dropdown-item" to="/reports">
                <i class="fas fa-chart-bar me-2"></i>
                View Reports
              </router-link>
            </li>
            <li><hr class="dropdown-divider" /></li>
            <li>
              <a
                class="dropdown-item"
                href="#"
                @click.prevent="quickAction('import')"
              >
                <i class="fas fa-upload me-2"></i>
                Import Data
              </a>
            </li>
          </ul>
        </div>

        <!-- Notifications -->
        <div class="nav-item dropdown me-3">
          <button
            class="btn btn-link nav-link position-relative"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            <i class="fas fa-bell fa-lg"></i>
            <!-- <span
              v-if="notificationStore.unreadCount > 0"
              class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
            >
              {{
                notificationStore.unreadCount > 99
                  ? "99+"
                  : notificationStore.unreadCount
              }}
            </span> -->
          </button>
          <div class="dropdown-menu dropdown-menu-end notification-dropdown">
            <div
              class="dropdown-header d-flex justify-content-between align-items-center"
            >
              <span>Notifications</span>
              <button class="btn btn-sm btn-link p-0">Mark all as read</button>
              <!-- @click="notificationStore.markAllAsRead -->
            </div>
            <!-- <div class="notification-list">
              <div
                v-for="notification in notificationStore.notifications"
                :key="notification.id"
                class="notification-item"
                :class="{ 'notification-unread': !notification.read }"
                @click="notificationStore.markAsRead(notification.id)"
              >
                <div
                  class="notification-icon"
                  :class="getNotificationIconClass(notification.type)"
                >
                  <i :class="getNotificationIcon(notification.type)"></i>
                </div>
                <div class="notification-content">
                  <div class="notification-title">{{ notification.title }}</div>
                  <div class="notification-message">
                    {{ notification.message }}
                  </div>
                  <div class="notification-time">
                    {{ formatNotificationTime(notification.timestamp) }}
                  </div>
                </div>
              </div>
            </div> -->
            <div class="dropdown-footer">
              <router-link
                to="/notifications"
                class="btn btn-sm btn-primary w-100"
              >
                View All Notifications
              </router-link>
            </div>
          </div>
        </div>

        <!-- Theme Toggle -->
        <div class="nav-item me-3">
          <button
            class="btn btn-link nav-link"
            @click="toggleTheme"
            :title="
              themeStore.isDarkMode
                ? 'Switch to Light Mode'
                : 'Switch to Dark Mode'
            "
          >
            <i
              class="fas"
              :class="themeStore.isDarkMode ? 'fa-sun' : 'fa-moon'"
            ></i>
          </button>
        </div>

        <!-- User Profile Dropdown -->
        <div class="nav-item dropdown">
          <button
            class="btn btn-link nav-link dropdown-toggle d-flex align-items-center"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            <img
              :src="authStore.userAvatar"
              :alt="authStore.userName"
              class="user-avatar me-2"
            />
            <div class="user-info d-none d-md-block text-start">
              <div class="user-name">{{ authStore.userName }}</div>
              <div class="user-role">{{ formatRole(authStore.userRole) }}</div>
            </div>
          </button>
          <ul class="dropdown-menu dropdown-menu-end user-dropdown">
            <li class="dropdown-header">
              <div class="user-profile-header">
                <img
                  :src="authStore.userAvatar"
                  :alt="authStore.userName"
                  class="profile-avatar"
                />
                <div class="profile-info">
                  <div class="profile-name">{{ authStore.userName }}</div>
                  <div class="profile-email">{{ authStore.userEmail }}</div>
                  <div class="profile-status">
                    <span class="status-dot status-online"></span>
                    Online
                  </div>
                </div>
              </div>
            </li>
            <li><hr class="dropdown-divider" /></li>
            <li>
              <router-link class="dropdown-item" to="/profile">
                <i class="fas fa-user me-2"></i>
                My Profile
              </router-link>
            </li>
            <li>
              <router-link class="dropdown-item" to="/settings">
                <i class="fas fa-cog me-2"></i>
                Account Settings
              </router-link>
            </li>
            <li v-if="authStore.hasRole('admin')">
              <router-link class="dropdown-item" to="/admin">
                <i class="fas fa-shield-alt me-2"></i>
                Admin Panel
              </router-link>
            </li>
            <li>
              <a class="dropdown-item" href="#" @click.prevent="openHelp">
                <i class="fas fa-question-circle me-2"></i>
                Help & Support
              </a>
            </li>
            <li><hr class="dropdown-divider" /></li>
            <li>
              <a
                class="dropdown-item text-danger"
                href="#"
                @click.prevent="logout"
              >
                <i class="fas fa-sign-out-alt me-2"></i>
                Sign Out
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
// import { useThemeStore } from "../stores/themestore";
import { useAuthStore } from "../../stores/auth";
import { useNavigationStore } from "../../stores/navigation";
// import { useNotificationStore } from "../../stores/notification";
import { useThemeStore } from "../../stores/themeStore";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const navigationStore = useNavigationStore();
// const notificationStore = useNotificationStore();
const themeStore = useThemeStore();

// onMounted(() => {
//   notificationStore.fetchNotifications();
// });

// Reactive data
const searchQuery = ref("");
const showSearchResults = ref(false);

// Computed
const breadcrumbs = computed(() => route.meta.breadcrumb || []);

// Search results (would typically come from API)
const searchResults = ref([
  {
    id: 1,
    title: "Project Alpha",
    subtitle: "Active project",
    icon: "fas fa-project-diagram text-primary",
    route: "/projects/1",
  },
  {
    id: 2,
    title: "User Management",
    subtitle: "System settings",
    icon: "fas fa-users text-success",
    route: "/users",
  },
]);

// Methods
const performSearch = async () => {
  if (!searchQuery.value.trim()) return;

  // Here you would typically call an API
  console.log("Searching for:", searchQuery.value);
  showSearchResults.value = true;
};

const hideSearchResults = () => {
  setTimeout(() => {
    showSearchResults.value = false;
  }, 200);
};

const selectSearchResult = (result) => {
  searchQuery.value = result.title;
  showSearchResults.value = false;
  if (result.route) {
    router.push(result.route);
  }
};
const quickAction = (action) => {
  switch (action) {
    case "new-user":
      // Open user creation modal or navigate to user creation page
      console.log("Creating new user...");
      break;
    case "import":
      // Open import dialog
      console.log("Opening import dialog...");
      break;
  }
};

const toggleTheme = () => {
  themeStore.toggleTheme();
};

const formatRole = (role) => {
  const roleMap = {
    admin: "Administrator",
    manager: "Manager",
    user: "User",
  };
  return roleMap[role] || role;
};

// const getNotificationIcon = (type) => {
//   const iconMap = {
//     success: "fas fa-check-circle",
//     warning: "fas fa-exclamation-triangle",
//     info: "fas fa-info-circle",
//     error: "fas fa-exclamation-circle",
//   };
//   return iconMap[type] || "fas fa-bell";
// };

// const getNotificationIconClass = (type) => {
//   const classMap = {
//     success: "notification-icon-success",
//     warning: "notification-icon-warning",
//     info: "notification-icon-info",
//     error: "notification-icon-error",
//   };
//   return classMap[type] || "notification-icon-default";
// };

// const formatNotificationTime = (timestamp) => {
//   const now = new Date();
//   const diff = now - new Date(timestamp);
//   const minutes = Math.floor(diff / 60000);
//   const hours = Math.floor(diff / 3600000);

//   if (minutes < 1) return "Just now";
//   if (minutes < 60) return `${minutes}m ago`;
//   if (hours < 24) return `${hours}h ago`;
//   return new Date(timestamp).toLocaleDateString();
// };

const openHelp = () => {
  // Open help modal or navigate to help page
  console.log("Opening help...");
};

const logout = async () => {
  if (confirm("Are you sure you want to sign out?")) {
    await authStore.logout();
    router.push("/auth/Userlogin");
  }
};

// onMounted(() => {
//   // Initialize notifications
//   notificationStore.fetchNotifications();
// });
</script>

<style scoped>
/* Same styles as before with router-link specific styles */
.navbar {
  transition: all 0.3s ease;
  border-bottom: 1px solid #e9ecef;
  z-index: 999;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
}

.navbar-toggler {
  border: none;
  color: #6c757d;
  font-size: 1.2rem;
}

.breadcrumb {
  background: none;
  padding: 0;
  margin: 0;
}

.breadcrumb-item + .breadcrumb-item::before {
  content: "›";
  color: #6c757d;
}

.breadcrumb-item a {
  color: #007bff;
  transition: color 0.3s ease;
}

.breadcrumb-item a:hover {
  color: #0056b3;
}

.nav-link {
  color: #6c757d !important;
  border: none;
  background: none;
  padding: 0.5rem;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #007bff !important;
}

.dropdown-item {
  transition: all 0.3s ease;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
  transform: translateX(2px);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid #e9ecef;
}

.user-info {
  line-height: 1.2;
}

.user-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #495057;
}

.user-role {
  font-size: 0.75rem;
  color: #6c757d;
}

.user-dropdown {
  min-width: 280px;
}

.user-profile-header {
  display: flex;
  align-items: center;
  padding: 0.5rem 0;
}

.profile-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  margin-right: 0.75rem;
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-weight: 600;
  color: #495057;
  margin-bottom: 0.25rem;
}

.profile-email {
  font-size: 0.875rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
}

.profile-status {
  font-size: 0.75rem;
  color: #28a745;
  display: flex;
  align-items: center;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 0.5rem;
}

.status-online {
  background-color: #28a745;
}

.search-container {
  position: relative;
}

.search-input {
  width: 300px;
  border-radius: 20px;
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
}

.search-input:focus {
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
  border-color: #007bff;
  width: 350px;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  z-index: 1000;
  max-height: 300px;
  overflow-y: auto;
  margin-top: 0.25rem;
}

.search-results-header {
  padding: 0.5rem 1rem;
  border-bottom: 1px solid #f8f9fa;
}

.search-result-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  cursor: pointer;
  border-bottom: 1px solid #f8f9fa;
  transition: background-color 0.2s ease;
}

.search-result-item:hover {
  background: #f8f9fa;
}

.search-result-item:last-child {
  border-bottom: none;
}

.search-result-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-radius: 50%;
  margin-right: 0.75rem;
}

.search-result-content {
  flex: 1;
}

.search-result-title {
  font-weight: 600;
  color: #495057;
  margin-bottom: 0.25rem;
}

.search-result-subtitle {
  font-size: 0.875rem;
  color: #6c757d;
}

.notification-dropdown {
  min-width: 380px;
  max-height: 500px;
}

.notification-list {
  max-height: 350px;
  overflow-y: auto;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  padding: 1rem;
  cursor: pointer;
  border-bottom: 1px solid #f8f9fa;
  transition: background-color 0.2s ease;
}

.notification-item:hover {
  background: #f8f9fa;
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-unread {
  background: #f0f8ff;
  border-left: 4px solid #007bff;
}

.notification-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin-right: 0.75rem;
  flex-shrink: 0;
}

.notification-icon-success {
  background: #d4edda;
  color: #155724;
}
.notification-icon-warning {
  background: #fff3cd;
  color: #856404;
}
.notification-icon-info {
  background: #d1ecf1;
  color: #0c5460;
}
.notification-icon-error {
  background: #f8d7da;
  color: #721c24;
}
.notification-icon-default {
  background: #f8f9fa;
  color: #6c757d;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-title {
  font-weight: 600;
  color: #495057;
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
}

.notification-message {
  color: #6c757d;
  font-size: 0.85rem;
  margin-bottom: 0.25rem;
  line-height: 1.4;
}

.notification-time {
  color: #adb5bd;
  font-size: 0.75rem;
}

.dropdown-footer {
  padding: 0.75rem;
  border-top: 1px solid #e9ecef;
}

@media (max-width: 768px) {
  .search-input {
    width: 200px;
  }

  .search-input:focus {
    width: 250px;
  }

  .user-info {
    display: none !important;
  }
}
</style>
