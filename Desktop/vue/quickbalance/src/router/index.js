import { createRouter, createWebHistory } from "vue-router";

// Layouts
import MainLayout from "@/components/Layouts/MainLayout.vue";
import AuthLayout from "@/components//Layouts/AuthLayout.vue";
// src/router/index.js or wherever your router is defined
import AddClients from "@/views/branch/AddClients.vue";
// Views
import Login from "../views/auth/UserLogin.vue";
import Register from "../views/auth/UserRegister.vue";
import BranchDashboard from "../views/branch/BranchDashboard.vue";
import NotFound from "../views/NotFound.vue";

const routes = [
  {
    path: "/auth",
    component: AuthLayout,
    children: [
      {
        path: "",
        redirect: "Userlogin",
      },
      {
        path: "Userlogin",
        name: "Login",
        component: Login,
        meta: {
          // requiresGuest: true,
          title: "Login",
        },
      },

      {
        path: "UserRegister",
        name: "Register",
        component: Register,
        meta: {
          requiresGuest: true,
          title: "Register",
        },
      },
    ],
  },

  {
    path: "/",
    component: MainLayout,
    redirect: "/BranchDashboard",
    // meta: { requiresAuth: true },
    children: [
      // Dashboard
      {
        path: "BranchDashboard",
        name: "BranchDashboard",
        component: BranchDashboard,
        meta: {
          title: "Dashboard",
          breadcrumb: [{ text: "Home", to: "/" }, { text: "BranchDashboard" }],
        },
      },

      {
        path: "/AddClients",
        name: "AddClients",
        component: AddClients,
      },
    ],
  },

  // Catch All
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: NotFound,
    meta: { title: "Page Not Found" },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 };
  },
});

router.beforeEach(async (to, from, next) => {
  const { useAuthStore } = await import("../stores/auth");
  const authStore = useAuthStore();
  document.title = to.meta.title
    ? `${to.meta.title} - Quickbalance`
    : "Quickbalance";

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next("/auth/Userlogin");
  }
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    return next("/");
  }
  if (to.meta.requiresRole && !authStore.hasRole(to.meta.requiresRole)) {
    return next("/BranchDashboard");
  }
  next();
});
export default router;
