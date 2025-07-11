<template>
  <div class="not-found">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 text-center">
          <div class="error-content">
            <h1 class="error-code">404</h1>
            <h2 class="error-title">Page Not Found</h2>
            <p class="error-message">
              The page you are looking for doesn't exist or has been moved.
            </p>
            <div class="error-actions">
              <router-link to="/" class="btn btn-primary me-3">
                <i class="fas fa-home me-2"></i>
                Go Home
              </router-link>
              <button @click="$router.go(-1)" class="btn btn-outline-secondary">
                <i class="fas fa-arrow-left me-2"></i>
                Go Back
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Component logic here
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
}

.error-content {
  padding: 2rem;
}

.error-code {
  font-size: 8rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 1rem;
  line-height: 1;
}

.error-title {
  font-size: 2rem;
  color: #2d3748;
  margin-bottom: 1rem;
}

.error-message {
  font-size: 1.1rem;
  color: #718096;
  margin-bottom: 2rem;
}

.error-actions {
  margin-top: 2rem;
}

.btn {
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
}
</style>
