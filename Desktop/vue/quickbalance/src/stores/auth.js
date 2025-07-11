import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "../services/api";

export const useAuthStore = defineStore("auth", () => {
  // State
  const user = ref(null);
  const token = ref(localStorage.getItem("token"));
  const loading = ref(false);
  const error = ref(null);

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value);
  const userRole = computed(() => user.value?.role || null);
  const userName = computed(() => user.value?.name || "");
  const userEmail = computed(() => user.value?.email || "");
  const userAvatar = computed(() => {
    if (user.value?.avatar) return user.value.avatar;
    return `https://ui-avatars.com/api/?name=${encodeURIComponent(
      userName.value
    )}&background=007bff&color=fff&size=40`;
  });

  // Actions
  const login = async (credentials) => {
    loading.value = true;
    error.value = null;

    try {
      const response = await api.post("/auth/login", credentials);
      const { user: userData, token: authToken } = response.data;

      user.value = userData;
      token.value = authToken;
      localStorage.setItem("token", authToken);

      return { success: true };
    } catch (err) {
      error.value = err.response?.data?.message || "Login failed";
      return { success: false, error: error.value };
    } finally {
      loading.value = false;
    }
  };

  const register = async (userData) => {
    loading.value = true;
    error.value = null;

    try {
      const response = await api.post("/auth/register", userData);
      const { user: newUser, token: authToken } = response.data;

      user.value = newUser;
      token.value = authToken;
      localStorage.setItem("token", authToken);

      return { success: true };
    } catch (err) {
      error.value = err.response?.data?.message || "Registration failed";
      return { success: false, error: error.value };
    } finally {
      loading.value = false;
    }
  };

  const logout = async () => {
    try {
      await api.post("/auth/logout");
    } catch (err) {
      console.error("Logout error:", err);
    } finally {
      user.value = null;
      token.value = null;
      localStorage.removeItem("token");
    }
  };

  const fetchUser = async () => {
    if (!token.value) return;

    try {
      const response = await api.get("/auth/me");
      user.value = response.data;
    } catch (err) {
      console.error("Fetch user error:", err);
      logout();
    }
  };

  const updateProfile = async (profileData) => {
    loading.value = true;
    error.value = null;

    try {
      const response = await api.put("/auth/profile", profileData);
      user.value = { ...user.value, ...response.data };
      return { success: true };
    } catch (err) {
      error.value = err.response?.data?.message || "Update failed";
      return { success: false, error: error.value };
    } finally {
      loading.value = false;
    }
  };

  const hasRole = (roles) => {
    if (!user.value) return false;
    if (typeof roles === "string") return user.value.role === roles;
    if (Array.isArray(roles)) return roles.includes(user.value.role);
    return false;
  };

  const hasPermission = (permission) => {
    if (!user.value?.permissions) return false;
    return user.value.permissions.includes(permission);
  };

  return {
    // State
    user,
    token,
    loading,
    error,

    // Getters
    isAuthenticated,
    userRole,
    userName,
    userEmail,
    userAvatar,

    // Actions
    login,
    register,
    logout,
    fetchUser,
    updateProfile,
    hasRole,
    hasPermission,
  };
});
