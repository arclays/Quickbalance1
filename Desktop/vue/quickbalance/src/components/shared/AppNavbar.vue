<template>
  <nav
    class="navbar navbar-expand-lg navbar-light bg-white shadow-sm"
    :class="{ shifted: !sidebarCollapsed }"
  >
    <div class="container-fluid">
      <!-- Mobile Menu Toggle -->
      <button
        class="btn btn-link navbar-toggler d-lg-none me-3"
        @click="navigationStore.toggleMobileSidebar"
        aria-label="Toggle navigation"
      >
        <i class="fas fa-bars"></i>
      </button>

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
                aria-label="Search"
              />
              <button
                class="btn btn-outline-secondary"
                @click="performSearch"
                aria-label="Search"
              >
                <i class="fas fa-search"></i>
              </button>
            </div>
            <div
              v-if="showSearchResults && searchResults.length"
              class="search-results"
            >
              <div class="search-results-header">Search Results</div>
              <div
                v-for="(result, index) in searchResults"
                :key="index"
                class="search-result-item"
                @mousedown="selectSearchResult(result)"
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
            aria-label="Quick actions"
          >
            <i class="fas fa-plus-circle fa-lg"></i>
          </button>
          <ul class="dropdown-menu dropdown-menu-end">
            <li class="dropdown-header">Quick Actions</li>
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
            aria-label="Toggle theme"
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
            aria-label="User menu"
          >
            <img
              :src="authStore.userAvatar"
              :alt="authStore.userName"
              class="user-avatar me-2"
              width="40"
              height="40"
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
                  width="48"
                  height="48"
                />
                <div class="profile-info">
                  <div class="profile-name">{{ authStore.userName }}</div>
                  <div class="profile-email">{{ authStore.userEmail }}</div>
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
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth";
import { useNavigationStore } from "../../stores/navigation";
import { useThemeStore } from "../../stores/themeStore";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const navigationStore = useNavigationStore();
const themeStore = useThemeStore();

const searchQuery = ref("");
const showSearchResults = ref(false);
const searchResults = ref([]);
const sidebarCollapsed = ref(false);

// Methods
const performSearch = async () => {
  if (!searchQuery.value.trim()) {
    searchResults.value = [];
    return;
  }

  try {
    // Here you would typically call an API
    console.log("Searching for:", searchQuery.value);
    // Mock search results for demonstration
    searchResults.value = [
      {
        title: "User Profile",
        subtitle: "View user details",
        icon: "fas fa-user",
        route: "/profile",
      },
      {
        title: "Settings",
        subtitle: "Account configuration",
        icon: "fas fa-cog",
        route: "/settings",
      },
    ];
    showSearchResults.value = true;
  } catch (error) {
    console.error("Search failed:", error);
    searchResults.value = [];
  }
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
      router.push("/users/new");
      break;
    case "import":
      console.log("Opening import dialog...");
      // Implement import functionality
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

const formatTime = (time) => {
  return time;
};

const openHelp = () => {
  router.push("/help");
};

const logout = async () => {
  if (confirm("Are you sure you want to sign out?")) {
    try {
      await authStore.logout();
      router.push("/auth/login");
    } catch (error) {
      console.error("Logout failed:", error);
    }
  }
};

// Keyboard navigation for search results
const handleKeyDown = (e) => {
  if (e.key === "Escape") {
    showSearchResults.value = false;
  }
};

onUnmounted(() => {
  document.removeEventListener("keydown", handleKeyDown);
});
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 280px;
  right: 0;
  height: 60px;
  z-index: 1030;
  transition: all 0.3s ease;
  background: white;
}

.navbar.shifted {
  left: 200px;
}

.navbar:not(.shifted) {
  left: 80px;
}

@media (max-width: 991.98px) {
  .navbar {
    left: 0 !important;
  }
}

.navbar-toggler {
  border: none;
  color: var(--bs-gray-600);
  font-size: 1.2rem;
}

.nav-link {
  color: var(--bs-gray-600) !important;
  border: none;
  background: none;
  padding: 0.5rem;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: var(--bs-primary) !important;
}

.dropdown-item {
  transition: all 0.3s ease;
  padding: 0.5rem 1rem;
}

.dropdown-item:hover {
  background-color: var(--bs-light);
  transform: translateX(2px);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid var(--bs-border-color);
  object-fit: cover;
}

.user-info {
  line-height: 1.2;
}

.user-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--bs-gray-800);
}

.user-role {
  font-size: 0.75rem;
  color: var(--bs-gray-600);
}

.user-dropdown {
  min-width: 280px;
  padding: 0.5rem 0;
}

.user-profile-header {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
}

.profile-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  margin-right: 0.75rem;
  object-fit: cover;
}

.profile-info {
  flex: 1;
  overflow: hidden;
}

.profile-name {
  font-weight: 600;
  color: var(--bs-gray-800);
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.profile-email {
  font-size: 0.875rem;
  color: var(--bs-gray-600);
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.search-container {
  position: relative;
}

.search-input {
  width: 300px;
  border-radius: 20px;
  border: 1px solid var(--bs-border-color);
  transition: all 0.3s ease;
  padding: 0.375rem 1rem;
}

.search-input:focus {
  box-shadow: 0 0 0 0.2rem rgba(var(--bs-primary-rgb), 0.25);
  border-color: var(--bs-primary);
  width: 350px;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid var(--bs-border-color);
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  z-index: 1050;
  max-height: 300px;
  overflow-y: auto;
  margin-top: 0.25rem;
}

.search-results-header {
  padding: 0.5rem 1rem;
  border-bottom: 1px solid var(--bs-border-color);
  font-weight: 600;
  background-color: var(--bs-light);
}

.search-result-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  cursor: pointer;
  border-bottom: 1px solid var(--bs-border-color);
  transition: background-color 0.2s ease;
}

.search-result-item:hover {
  background: var(--bs-light);
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
  background: var(--bs-light);
  border-radius: 50%;
  margin-right: 0.75rem;
  color: var(--bs-primary);
}

.search-result-content {
  flex: 1;
  min-width: 0;
}

.search-result-title {
  font-weight: 600;
  color: var(--bs-gray-800);
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.search-result-subtitle {
  font-size: 0.875rem;
  color: var(--bs-gray-600);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.notification-dropdown {
  min-width: 380px;
  max-height: 500px;
  display: flex;
  flex-direction: column;
}

.notification-list {
  max-height: 350px;
  overflow-y: auto;
  flex: 1;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  padding: 1rem;
  cursor: pointer;
  border-bottom: 1px solid var(--bs-border-color);
  transition: background-color 0.2s ease;
}

.notification-item:hover {
  background: var(--bs-light);
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-unread {
  background: rgba(var(--bs-primary-rgb), 0.05);
  border-left: 4px solid var(--bs-primary);
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
  background: var(--bs-success-bg-subtle);
  color: var(--bs-success-text);
}
.notification-icon-warning {
  background: var(--bs-warning-bg-subtle);
  color: var(--bs-warning-text);
}
.notification-icon-info {
  background: var(--bs-info-bg-subtle);
  color: var(--bs-info-text);
}
.notification-icon-error {
  background: var(--bs-danger-bg-subtle);
  color: var(--bs-danger-text);
}
.notification-icon-default {
  background: var(--bs-light);
  color: var(--bs-gray-600);
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-title {
  font-weight: 600;
  color: var(--bs-gray-800);
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
}

.notification-message {
  color: var(--bs-gray-600);
  font-size: 0.85rem;
  margin-bottom: 0.25rem;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.notification-time {
  color: var(--bs-gray-500);
  font-size: 0.75rem;
}

.dropdown-footer {
  padding: 0.75rem;
  border-top: 1px solid var(--bs-border-color);
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

  .notification-dropdown {
    min-width: 300px;
    width: 300px;
  }
}
</style>
