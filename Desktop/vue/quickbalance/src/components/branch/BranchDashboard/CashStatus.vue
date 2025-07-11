<template>
  <div class="card h-100">
    <div class="card-header">
      <h6 class="card-title mb-0">
        <i class="fas fa-cash-register me-2"></i>
        Cash Status
      </h6>
    </div>
    <div class="card-body">
      <div class="row g-3">
        <div class="col-6">
          <div class="text-center p-3 bg-light rounded">
            <i class="fas fa-arrow-down text-success fa-2x mb-2"></i>
            <h6 class="mb-1">Cash In</h6>
            <h5 class="text-success mb-0">
              {{ formatCurrency(cashData.cashIn) }}
            </h5>
          </div>
        </div>
        <div class="col-6">
          <div class="text-center p-3 bg-light rounded">
            <i class="fas fa-arrow-up text-danger fa-2x mb-2"></i>
            <h6 class="mb-1">Cash Out</h6>
            <h5 class="text-danger mb-0">
              {{ formatCurrency(cashData.cashOut) }}
            </h5>
          </div>
        </div>
        <div class="col-12">
          <div class="text-center p-3 bg-primary text-white rounded">
            <i class="fas fa-university fa-2x mb-2"></i>
            <h6 class="mb-1">Vault Balance</h6>
            <h4 class="mb-0">{{ formatCurrency(cashData.vaultBalance) }}</h4>
          </div>
        </div>
      </div>

      <div class="mt-3">
        <div class="d-flex justify-content-between align-items-center mb-2">
          <small class="text-muted">Cash Flow Today</small>
          <small class="text-muted">{{ cashFlowPercentage }}%</small>
        </div>
        <div class="progress">
          <div
            class="progress-bar"
            :class="cashFlowPercentage > 0 ? 'bg-success' : 'bg-danger'"
            :style="{ width: Math.abs(cashFlowPercentage) + '%' }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { computed, defineProps } from "vue";
const props = defineProps({
  cashData: {
    type: Object,
    required: true,
  },
});

const formatCurrency = (amount) => {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(amount);
};

const cashFlowPercentage = computed(() => {
  const netFlow = props.cashData.cashIn - props.cashData.cashOut;
  const totalFlow = props.cashData.cashIn + props.cashData.cashOut;
  return totalFlow > 0 ? Math.round((netFlow / totalFlow) * 100) : 0;
});
</script>
