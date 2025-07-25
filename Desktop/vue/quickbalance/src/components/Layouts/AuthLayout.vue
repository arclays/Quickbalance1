<template>
  <div class="auth-layout">
    <div class="auth-container">
      <div class="auth-background">
        <div class="auth-overlay"></div>
        <div class="auth-pattern"></div>
      </div>
      <div class="auth-content">
        <div class="container">
          <div class="row justify-content-center align-items-center min-vh-100">
            <div class="col-md-6 col-lg-5 col-xl-4">
              <div class="auth-card">
                <div class="auth-header text-center mb-4">
                  <div class="auth-logo">
                    <!-- <img
                      class="img-fluid"
                      src="../../assets/utils/images/qbc.jpg"
                      alt
                    /> -->
                    <!-- <img src="@/utils/images/image.png" alt="Description" /> -->
                    <i class="fas fa-cube fa-3x text-primary mb-3"></i>
                    <h2 class="auth-title">Quickbalance</h2>
                    <p class="auth-subtitle text-muted">Welcome back</p>
                  </div>
                </div>

                <router-view />

                <div class="auth-footer text-center mt-4">
                  <small class="text-muted">
                    © 2025 Quickbalance. All rights reserved.
                  </small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";

onMounted(() => {
  document.body.classList.add("auth-body");

  return () => {
    document.body.classList.remove("auth-body");
  };
});
</script>

<style scoped>
.auth-layout {
  display: flex;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}
.auth-container {
  position: relative;
  z-index: 2;
  display: flex;
  width: 100%;
  min-height: 100vh;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.auth-card {
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  width: 100%;
  max-width: 420px;
  padding: 2.5rem;
  border: 1px solid rgba(255, 255, 255, 0.6);
  transform: translateY(0);
  transition: var(--transition);
  position: relative;
  overflow: hidden;
}

.auth-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #4346f0 0%, #3d94f8 100%);
  z-index: 1;
}

.auth-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.1);
}

.auth-pattern {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: radial-gradient(
      circle at 25% 25%,
      rgba(255, 255, 255, 0.1) 0%,
      transparent 50%
    ),
    radial-gradient(
      circle at 75% 75%,
      rgba(255, 255, 255, 0.1) 0%,
      transparent 50%
    );
  background-size: 100px 100px;
}

.auth-content {
  position: relative;
  z-index: 2;
  width: 100%;
}

/* .auth-card {
  background: white;
  padding: 1rem 1rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
} */

.auth-header {
  margin-bottom: 2rem;
}

.auth-logo i {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.auth-title {
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.auth-subtitle {
  font-size: 1rem;
  color: #718096;
}
.auth-footer {
  text-align: center;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

/* Global auth body styles */
:global(.auth-body) {
  background: #f7fafc;
}

@media (max-width: 768px) {
  .auth-card {
    margin: 1rem;
    padding: 2rem 1.5rem;
  }
}
</style>
