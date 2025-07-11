<template>
  <div class="container-fluid">
    <div class="row mb-4">
      <div class="col">
        <h1 class="h3 mb-0">Dashboard</h1>
        <p class="text-muted">Welcome back, {{ authStore.userName }}!</p>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">
      <div class="col-md-3 mb-3">
        <div class="card stats-card">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h6 class="card-title text-muted">Total Projects</h6>
                <h3 class="mb-0">24</h3>
                <small class="text-success">
                  <i class="fas fa-arrow-up"></i> +12% from last month
                </small>
              </div>
              <div class="stats-icon">
                <i class="fas fa-project-diagram"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-3 mb-3">
        <div class="card stats-card">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h6 class="card-title text-muted">Active Users</h6>
                <h3 class="mb-0">1,247</h3>
                <small class="text-success">
                  <i class="fas fa-arrow-up"></i> +5% from last week
                </small>
              </div>
              <div class="stats-icon">
                <i class="fas fa-users"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-3 mb-3">
        <div class="card stats-card">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h6 class="card-title text-muted">Pending Tasks</h6>
                <h3 class="mb-0">18</h3>
                <small class="text-warning">
                  <i class="fas fa-clock"></i> 3 due today
                </small>
              </div>
              <div class="stats-icon">
                <i class="fas fa-tasks"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-3 mb-3">
        <div class="card stats-card">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h6 class="card-title text-muted">Revenue</h6>
                <h3 class="mb-0">$45,280</h3>
                <small class="text-success">
                  <i class="fas fa-arrow-up"></i> +8% from last month
                </small>
              </div>
              <div class="stats-icon">
                <i class="fas fa-dollar-sign"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">Recent Activity</h5>
          </div>
          <div class="card-body">
            <p>Your dashboard content goes here...</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from "../stores/auth";

const authStore = useAuthStore();
</script>

<style scoped>
.stats-card {
  border: none;
  border-radius: 12px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stats-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.stats-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 123, 255, 0.1);
  color: #007bff;
  font-size: 1.5rem;
}

.card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}
</style>
