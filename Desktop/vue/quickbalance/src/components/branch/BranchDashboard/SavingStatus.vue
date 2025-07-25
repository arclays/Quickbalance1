<template>
  <div class="card h-100">
    <div class="card-header">
      <h6 class="card-title mb-0">
        <i class="fas fa-piggy-bank me-2"></i>
        Saving Status
      </h6>
    </div>
    <div class="card-body">
      <div class="row g-3">
        <div class="col-6">
          <div class="text-center p-3 bg-light rounded">
            <i class="fas fa-arrow-down text-success fa-2x mb-2"></i>
            <h6 class="mb-1">Deposits</h6>
            <h5 class="text-success mb-0">
              {{ formatCurrency() }}
            </h5>
          </div>
        </div>
        <div class="col-6">
          <div class="text-center p-3 bg-light rounded">
            <i class="fas fa-arrow-up text-danger fa-2x mb-2"></i>
            <h6 class="mb-1">Withdrawals</h6>
            <h5 class="text-danger mb-0">
              {{ formatCurrency() }}
            </h5>
          </div>
        </div>
        <div class="col-12">
          <div class="text-center p-3 bg-info text-white rounded">
            <i class="fas fa-wallet fa-2x opacity-75 mb-2"></i>
            <h6 class="mb-1">Savings Balance</h6>
            <h4 class="mb-0">{{ formatCurrency() }}</h4>
          </div>
        </div>
      </div>

      <div class="mt-3">
        <div class="d-flex justify-content-between align-items-center mb-2">
          <small class="text-muted">Saving Flow Today</small>
          <small class="text-muted">{{ savingFlowPercentage }}%</small>
        </div>
        <div class="progress">
          <div
            class="progress-bar"
            :class="savingFlowPercentage > 0 ? 'bg-success' : 'bg-danger'"
            :style="{ width: Math.abs(savingFlowPercentage) + '%' }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineProps } from "vue";

const props = defineProps({
  savingData: {
    type: Object,
    required: true,
  },
});

// Dummy fetch simulation (optional)
// const savingStatus = ref(null);
// setTimeout(() => {
//   savingStatus.value = {
//     cashIn: 100000,
//     cashOut: 50000,
//   };
// }, 1000);

// Format amount as UGX
const formatCurrency = (amount) => {
  return new Intl.NumberFormat("en-UG", {
    style: "currency",
    currency: "UGX",
    minimumFractionDigits: 0,
  }).format(amount);
};

// const savingFlowPercentage = computed(() => {
//   const deposits = props.savingData.deposits || 0;
//   const withdrawals = props.savingData.withdrawals || 0;
//   const netFlow = deposits - withdrawals;
//   const totalFlow = deposits + withdrawals;
//   return totalFlow > 0 ? Math.round((netFlow / totalFlow) * 100) : 0;
// });
const cashFlowPercentage = computed(() => {
  const netFlow = props.cashData.cashIn - props.cashData.cashOut;
  const totalFlow = props.cashData.cashIn + props.cashData.cashOut;
  return totalFlow > 0 ? Math.round((netFlow / totalFlow) * 100) : 0;
});
</script>
