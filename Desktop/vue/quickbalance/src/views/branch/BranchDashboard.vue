<template>
  <div class="container-fluid">
    <!-- Page Header -->
    <div class="row mb-4 align-items-center">
      <div class="col">
        <h1 class="h3 mb-0">Branch Dashboard</h1>
        <p class="text-muted">{{ currentBranch }} Branch - {{ currentDate }}</p>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">
          <!-- @click="refreshData -->
          <i class="fas fa-sync-alt me-2"></i>
          Refresh
        </button>
      </div>
    </div>

    <!-- Key Metrics Cards -->
    <div class="row mb-4">
      <div v-for="(metric, index) in metrics" :key="index" class="col-md-3">
        <div :class="['card', 'text-white', metric.bgClass]">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h6 class="card-title">{{ metric.title }}</h6>
                <h3 class="mb-0">{{ metric.value }}</h3>
              </div>
              <div class="align-self-center">
                <i :class="[metric.icon, 'fa-2x', 'opacity-75']"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Cash Status Section -->
    <div class="row">
      <div class="col-md-4 mb-4" v-for="i in 3" :key="i">
        <CashStatus :cashData="cashStatus" />
      </div>
    </div>

    <!-- Recent Transactions -->
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">Recent Transactions</h5>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Time</th>
                    <th>Type</th>
                    <th>Client</th>
                    <th>Amount</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="transaction in recentTransactions"
                    :key="transaction.id"
                  >
                    <td>{{ formatTime(transaction.timestamp) }}</td>
                    <td>
                      <span
                        :class="[
                          'badge',
                          getTransactionTypeClass(transaction.type),
                        ]"
                      >
                        {{ transaction.type }}
                      </span>
                    </td>
                    <td>{{ transaction.clientName }}</td>
                    <td>{{ formatCurrency(transaction.amount) }}</td>
                    <td>
                      <span
                        :class="['badge', getStatusClass(transaction.status)]"
                      >
                        {{ transaction.status }}
                      </span>
                    </td>
                    <td>
                      <button
                        class="btn btn-sm btn-outline-primary me-1"
                        @click="viewTransaction(transaction)"
                      >
                        <i class="fas fa-eye"></i>
                      </button>
                      <button
                        class="btn btn-sm btn-outline-secondary"
                        @click="printReceipt(transaction)"
                      >
                        <i class="fas fa-print"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
// import { useStore } from "vuex";
import CashStatus from "../../components/branch/BranchDashboard/CashStatus.vue";
import { useAuthStore } from "../../stores/auth";

const authStore = useAuthStore();

// ✅ Access state or getters directly
const currentUser = computed(() => authStore.user); // or `authStore.currentUser` if that's a getter
const currentBranch = computed(() => currentUser.value?.branch || "Main");
const currentDate = computed(() => new Date().toLocaleDateString());

const cashStatus = ref({
  totalCash: 125000,
  cashIn: 45000,
  cashOut: 32000,
  vaultBalance: 98000,
});

const dailySummary = ref({
  activeLoans: 156,
  savingsAccounts: 342,
  todayTransactions: 87,
});

const metrics = computed(() => [
  {
    title: "Total Cash",
    value: formatCurrency(cashStatus.value.totalCash),
    bgClass: "bg-primary",
    icon: "fas fa-money-bill-wave",
  },
  {
    title: "Active Loans",
    value: dailySummary.value.activeLoans,
    bgClass: "bg-success",
    icon: "fas fa-hand-holding-usd",
  },
  {
    title: "Savings Accounts",
    value: dailySummary.value.savingsAccounts,
    bgClass: "bg-info",
    icon: "fas fa-piggy-bank",
  },
  {
    title: "Today's Transactions",
    value: dailySummary.value.todayTransactions,
    bgClass: "bg-warning",
    icon: "fas fa-exchange-alt",
  },
]);

const recentTransactions = ref([
  {
    id: 1,
    timestamp: new Date(),
    type: "Loan Payment",
    clientName: "John Doe",
    amount: 5000,
    status: "Completed",
  },
  {
    id: 2,
    timestamp: new Date(Date.now() - 300000),
    type: "Savings Deposit",
    clientName: "Jane Smith",
    amount: 2500,
    status: "Completed",
  },
  {
    id: 3,
    timestamp: new Date(Date.now() - 600000),
    type: "Withdrawal",
    clientName: "Bob Johnson",
    amount: 1000,
    status: "Pending",
  },
]);

const formatCurrency = (amount) => {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(amount);
};

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString();
};

const getTransactionTypeClass = (type) => {
  return (
    {
      "Loan Payment": "bg-success",
      "Savings Deposit": "bg-primary",
      Withdrawal: "bg-warning",
      Transfer: "bg-info",
    }[type] || "bg-secondary"
  );
};

const getStatusClass = (status) => {
  return (
    {
      Completed: "bg-success",
      Pending: "bg-warning",
      Failed: "bg-danger",
    }[status] || "bg-secondary"
  );
};

// const refreshData = () => {
//   store.dispatch("setLoading", true);
//   setTimeout(() => {
//     store.dispatch("setLoading", false);
//     store.dispatch("showNotification", {
//       type: "success",
//       message: "Dashboard data refreshed successfully",
//     });
//   }, 1000);
// };

const viewTransaction = (transaction) => {
  console.log("Viewing transaction:", transaction);
};

const printReceipt = (transaction) => {
  console.log("Printing receipt for:", transaction);
};

// onMounted(() => {
//   refreshData();
// });
</script>
