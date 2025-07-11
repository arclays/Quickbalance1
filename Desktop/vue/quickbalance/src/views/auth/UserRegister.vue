<template>
  <div class="register-form">
    <form @submit.prevent="handleRegister">
      <div class="row">
        <div class="col-md-6 mb-3">
          <label for="firstName" class="form-label">First Name</label>
          <div class="input-group">
            <span class="input-group-text">
              <i class="fas fa-user"></i>
            </span>
            <input
              type="text"
              class="form-control"
              id="firstName"
              v-model="formData.firstName"
              required
              :class="{ 'is-invalid': errors.firstName }"
              placeholder="First name"
            />
          </div>
          <div class="invalid-feedback" v-if="errors.firstName">
            {{ errors.firstName }}
          </div>
        </div>

        <div class="col-md-6 mb-3">
          <label for="lastName" class="form-label">Last Name</label>
          <div class="input-group">
            <span class="input-group-text">
              <i class="fas fa-user"></i>
            </span>
            <input
              type="text"
              class="form-control"
              id="lastName"
              v-model="formData.lastName"
              required
              :class="{ 'is-invalid': errors.lastName }"
              placeholder="Last name"
            />
          </div>
          <div class="invalid-feedback" v-if="errors.lastName">
            {{ errors.lastName }}
          </div>
        </div>
      </div>

      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <div class="input-group">
          <span class="input-group-text">
            <i class="fas fa-at"></i>
          </span>
          <input
            type="text"
            class="form-control"
            id="username"
            v-model="formData.username"
            required
            :class="{ 'is-invalid': errors.username }"
            placeholder="Choose a username"
          />
        </div>
        <div class="invalid-feedback" v-if="errors.username">
          {{ errors.username }}
        </div>
      </div>

      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <div class="input-group">
          <span class="input-group-text">
            <i class="fas fa-envelope"></i>
          </span>
          <input
            type="email"
            class="form-control"
            id="email"
            v-model="formData.email"
            required
            :class="{ 'is-invalid': errors.email }"
            placeholder="your@email.com"
          />
        </div>
        <div class="invalid-feedback" v-if="errors.email">
          {{ errors.email }}
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
            v-model="formData.password"
            required
            :class="{ 'is-invalid': errors.password }"
            placeholder="Create a password"
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
        <div class="form-text">Password must be at least 8 characters long</div>
      </div>

      <div class="mb-3">
        <label for="confirmPassword" class="form-label">Confirm Password</label>
        <div class="input-group">
          <span class="input-group-text">
            <i class="fas fa-lock"></i>
          </span>
          <input
            :type="showConfirmPassword ? 'text' : 'password'"
            class="form-control"
            id="confirmPassword"
            v-model="formData.confirmPassword"
            required
            :class="{ 'is-invalid': errors.confirmPassword }"
            placeholder="Confirm your password"
          />

          <button
            class="btn btn-outline-secondary"
            type="button"
            @click="showConfirmPassword = !showConfirmPassword"
          >
            <i
              class="fas"
              :class="showConfirmPassword ? 'fa-eye-slash' : 'fa-eye'"
            ></i>
          </button>
        </div>
        <div class="invalid-feedback" v-if="errors.confirmPassword">
          {{ errors.confirmPassword }}
        </div>
      </div>

      <div class="mb-3 form-check">
        <input
          type="checkbox"
          class="form-check-input"
          id="terms"
          v-model="formData.acceptTerms"
          required
          :class="{ 'is-invalid': errors.acceptTerms }"
        />
        <label class="form-check-label" for="terms">
          I agree to the
          <a href="#" class="text-primary">Terms of Service</a> and
          <a href="#" class="text-primary">Privacy Policy</a>
        </label>
        <div class="invalid-feedback" v-if="errors.acceptTerms">
          {{ errors.acceptTerms }}
        </div>
      </div>

      <div class="alert alert-danger" v-if="registerError">
        <i class="fas fa-exclamation-circle me-2"></i>
        {{ registerError }}
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
        <i v-else class="fas fa-user-plus me-2"></i>
        {{ authStore.loading ? "Creating Account..." : "Create Account" }}
      </button>

      <div class="text-center">
        <p class="mb-2">Already have an account?</p>
        <router-link to="/auth/UserLogin" class="btn btn-outline-primary">
          Sign In
        </router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const showPassword = ref(false);
const showConfirmPassword = ref(false);
const registerError = ref("");
const errors = reactive({});

const formData = reactive({
  firstName: "",
  lastName: "",
  username: "",
  email: "",
  password: "",
  confirmPassword: "",
  acceptTerms: false,
});

const validateForm = () => {
  Object.keys(errors).forEach((key) => delete errors[key]);

  if (!formData.firstName.trim()) {
    errors.firstName = "First name is required";
  }
  if (!formData.lastName.trim()) {
    errors.lastName = "Last name is required";
  }
  if (!formData.username.trim()) {
    errors.username = "Username is required";
  } else if (formData.username.length < 3) {
    errors.username = "Username must be at least 3 characters";
  }
  if (!formData.email.trim()) {
    errors.email = "Email is required";
  } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
    errors.email = "Please enter a valid email";
  }
  if (!formData.password) {
    errors.password = "Password is required";
  } else if (formData.password.length < 8) {
    errors.password = "Password must be at least 8 characters";
  }
  if (!formData.confirmPassword) {
    errors.confirmPassword = "Please confirm your password";
  } else if (formData.password !== formData.confirmPassword) {
    errors.confirmPassword = "Passwords do not match";
  }
  if (!formData.acceptTerms) {
    errors.acceptTerms = "You must accept the terms and conditions";
  }
  return Object.keys(errors).length === 0;
};

const handleRegister = async () => {
  registerError.value = "";

  if (!validateForm()) {
    return handleRegister;
  }
  try {
    const result = await authStore.register({
      name: `${formData.firstName} ${formData.lastName}`,
      username: formData.username,
      email: formData.email,
      password: formData.password,
    });

    if (result.success) {
      router.push("/BoardDashboard");
    } else {
      registerError.value = result.error;
    }
  } catch (error) {
    registerError.value = "An unexpected error occurred";
    console.error("Registration error:", error);
  }
};
</script>

<style scoped>
.register-form {
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
  border-color: #667eea;
  color: #667eea;
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: #667eea;
}

.alert {
  border-radius: 10px;
  border: none;
}

.form-check-input:checked {
  background-color: #667eea;
  border-color: #667eea;
}

.text-primary {
  color: #667eea !important;
}

.text-primary:hover {
  color: #764ba2 !important;
}
</style>
