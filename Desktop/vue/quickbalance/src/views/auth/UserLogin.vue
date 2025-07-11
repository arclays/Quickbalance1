<template>
  <div class="login-form">
    <form @submit.prevent="handleLogin">
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <div class="input-group">
          <span class="input-group-text">
            <i class="fas fa-user"></i>
          </span>
          <input
            type="text"
            class="form-control"
            id="username"
            v-model="credentials.username"
            required
            :class="{ 'is-invalid': errors.username }"
            placeholder="Enter your username"
          />
        </div>
        <div class="invalid-feedback" v-if="errors.username">
          {{ errors.username }}
        </div>
      </div>

      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <div class="input-group">
          <span class="input-group-text">
            <i class="fas fa-lock"></i>
          </span>
          <input
            :type="showPassword ? 'text' : 'password'"
            class="form-control"
            id="password"
            v-model="credentials.password"
            required
            :class="{ 'is-invalid': errors.password }"
            placeholder="Enter your password"
          />
          <button
            class="btn btn-outline-secondary"
            type="button"
            @click="showPassword = !showPassword"
          >
            <i
              class="fas"
              :class="showPassword ? 'fa-eye-slash' : 'fa-eye'"
            ></i>
          </button>
        </div>
        <div class="invalid-feedback" v-if="errors.password">
          {{ errors.password }}
        </div>
      </div>

      <div class="mb-3 form-check">
        <input
          type="checkbox"
          class="form-check-input"
          id="remember"
          v-model="credentials.remember"
        />
        <label class="form-check-label" for="remember"> Remember me </label>
      </div>

      <div class="alert alert-danger" v-if="loginError">
        <i class="fas fa-exclamation-circle me-2"></i>{{ loginError }}
      </div>

      <button
        type="submit"
        class="btn btn-primary w-100 mb-3"
        :disabled="authStore.loading"
      >
        <span
          v-if="authStore.loading"
          class="spinner-border spinner-border-sm me-2"
        ></span>
        <i v-else class="fas fa-sign-in-alt me-2"></i>
        {{ authStore.loading ? "Signing In..." : "Sign In" }}
      </button>

      <div class="text-center">
        <p class="mb-2">Don't have an account?</p>
        <router-link to="/auth/UserRegister" class="btn btn-outline-primary">
          Create Account
        </router-link>
      </div>
    </form>
    <!-- 
    <div class="demo-credentials mt-4">
      <div class="card bg-light">
        <div class="card-body">
          <h6 class="card-title">
            <i class="fas fa-info-circle me-2"></i>
            Demo Credentials
          </h6>
          <div class="row">
            <div class="col-4">
              <strong>Admin:</strong><br />
              <small>admin / admin123</small>
            </div>
            <div class="col-4">
              <strong>Manager:</strong><br />
              <small>manager / manager123</small>
            </div>
            <div class="col-4">
              <strong>User:</strong><br />
              <small>user / user123</small>
            </div>
          </div>
        </div>
      </div>
    </div> -->
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const showPassword = ref(false);
const loginError = ref("");
const errors = reactive({});

const credentials = reactive({
  username: "",
  password: "",
  remember: false,
});

const handleLogin = async () => {
  loginError.value = "";
  Object.keys(errors).forEach((key) => delete errors[key]);

  // Basic validation
  if (!credentials.username.trim()) {
    errors.username = "Username is required";
    return;
  }

  if (!credentials.password.trim()) {
    errors.password = "Password is required";
    return;
  }

  try {
    const result = await authStore.login({
      username: credentials.username,
      password: credentials.password,
    });

    if (result.success) {
      // Redirect based on user role
      const user = authStore.user;
      if (user.role === "admin") {
        router.push("/admin/dashboard");
      } else {
        router.push("/dashboard");
      }
    } else {
      loginError.value = result.error;
    }
  } catch (error) {
    loginError.value = "An unexpected error occurred";
    console.error("Login error:", error);
  }
};
</script>

<style scoped>
.login-form {
  max-width: 100%;
}

.input-group-text {
  background: #f8f9fa;
  border-right: none;
  color: #6c757d;
}

.form-control {
  border-left: none;
}

.form-control:focus {
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
  border-color: #007bff;
}

.btn-primary {
  background: linear-gradient(135deg, #3255f3 0%, #41379e 100%);
  border: none;
  padding: 0.75rem 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.btn-outline-primary {
  border-color: #4159c0;
  color: #384a97;
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  background: linear-gradient(135deg, #193ddb 0%, #4d1ebb 100%);
  border-color: #3354e7;
}

.demo-credentials {
  border-top: 1px solid #e9ecef;
  padding-top: 1rem;
}

.demo-credentials .card {
  border: none;
  box-shadow: none;
}

.demo-credentials .card-body {
  padding: 1rem;
}

.alert {
  border-radius: 10px;
  border: none;
}

.form-check-input:checked {
  background-color: #667eea;
  border-color: #667eea;
}
</style>
