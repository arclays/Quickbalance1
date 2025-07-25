<template>
  <div id="app">
    <nav
      class="navbar navbar-expand-lg navbar-dark bg-primary"
      v-if="isAuthenticated"
    >
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">
          <i class="fas fa-balance-scale me-2"></i>
          QuickBalance
        </router-link>

        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item dropdown" v-if="userRole === 'admin'">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
              >
                Admin</a
              >
              <ul class="dropdown-menu">
                <li>
                  <router-link class="dropdown-item" to="/admin/dashboard"
                    >Dashboard</router-link
                  >
                </li>
                <li>
                  <router-link class="dropdown-item" to="/admin/branches"
                    >Branches</router-link
                  >
                </li>
                <li>
                  <router-link class="dropdown-item" to="/admin/users"
                    >Users</router-link
                  >
                </li>
                <li>
                  <router-link class="dropdown-item" to="/admin/settings"
                    >Settings</router-link
                  >
                </li>
              </ul>
            </li>

            <li
              class="nav-item dropdown"
              v-if="userRole === 'branch_manager' || userRole === 'teller'"
            >
              <a
                class="nav-link dropdown-toggle"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
              >
                Branch
              </a>

              <ul class="dropdown-menu">
                <li>
                  <router-link class="dropdown-item" to="/branch/dashboard"
                    >Dashboard</router-link
                  >
                </li>
                <li>
                  <router-link class="dropdown-item" to="/branch/clients"
                    >Clients</router-link
                  >
                </li>
                <li>
                  <router-link class="dropdown-item" to="/branch/loans"
                    >Loans</router-link
                  >
                </li>
                <li>
                  <router-link class="dropdown-item" to="/branch/savings"
                    >Savings</router-link
                  >
                </li>
                <li>
                  <router-link class="dropdown-item" to="/branch/reports"
                    >Reports</router-link
                  >
                </li>
              </ul>
            </li>

            <li class="nav-item" v-if="userRole === 'admin'">
              <router-link class="nav-link" to="/global/overview"
                >Global Overview</router-link
              >
            </li>
          </ul>

          <ul class="navbar-nav">
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
              >
                <i class="fas fa-user me-1"></i>
                {{ currentUser?.name || "User" }}
              </a>
              <ul class="dropdown-menu">
                <li>
                  <a class="dropdown-item" href="#" @click="logout">Logout</a>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <main class="container-fluid mt-3" v-if="isAuthenticated">
      <router-view />
    </main>

    <router-view v-else />

    <!-- Loading Spinner -->
    <div
      v-if="loading"
      class="position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center"
      style="background: rgba(0, 0, 0, 0.5); z-index: 9999"
    >
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth";
import { computed, onMounted } from "vue";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

const isAuthenticated = computed(() => authStore.isAuthenticated);
const currentUser = computed(() => authStore.user);
const userRole = computed(() => authStore.userRole);

const logout = async () => {
  await authStore.logout();
  router.push("/auth/userlogin");
};

onMounted(() => {
  authStore.fetchUser();
});
</script>

<style>
#app {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.navbar-brand {
  font-weight: bold;
  font-size: 1.5rem;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border: 1px solid rgba(0, 0, 0, 0.125);
}

.btn {
  border-radius: 0.375rem;
}

.table {
  border-radius: 0.375rem;
  overflow: hidden;
}

.form-control,
.form-select {
  border-radius: 0.375rem;
}

.alert {
  border-radius: 0.375rem;
}
</style>
