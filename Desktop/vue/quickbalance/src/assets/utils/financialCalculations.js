/**
 * Financial calculation utilities for QuickBalance
 */

// Calculate loan payment using PMT formula
export function calculateLoanPayment(principal, rate, periods) {
  if (rate === 0) return principal / periods;

  const monthlyRate = rate / 100 / 12;
  const payment =
    (principal * (monthlyRate * Math.pow(1 + monthlyRate, periods))) /
    (Math.pow(1 + monthlyRate, periods) - 1);

  return Math.round(payment * 100) / 100;
}

// Calculate compound interest
export function calculateCompoundInterest(
  principal,
  rate,
  periods,
  compoundingFrequency = 12
) {
  const r = rate / 100;
  const n = compoundingFrequency;
  const t = periods / 12;

  const amount = principal * Math.pow(1 + r / n, n * t);
  return Math.round(amount * 100) / 100;
}

// Calculate simple interest
export function calculateSimpleInterest(principal, rate, time) {
  const interest = (principal * rate * time) / 100;
  return Math.round(interest * 100) / 100;
}

// Calculate loan amortization schedule
export function generateAmortizationSchedule(principal, rate, periods) {
  const monthlyPayment = calculateLoanPayment(principal, rate, periods);
  const monthlyRate = rate / 100 / 12;
  let balance = principal;
  const schedule = [];

  for (let i = 1; i <= periods; i++) {
    const interestPayment = balance * monthlyRate;
    const principalPayment = monthlyPayment - interestPayment;
    balance -= principalPayment;

    schedule.push({
      period: i,
      payment: Math.round(monthlyPayment * 100) / 100,
      principal: Math.round(principalPayment * 100) / 100,
      interest: Math.round(interestPayment * 100) / 100,
      balance: Math.round(Math.max(0, balance) * 100) / 100,
    });
  }

  return schedule;
}

// Calculate debt-to-income ratio
export function calculateDebtToIncomeRatio(monthlyDebt, monthlyIncome) {
  if (monthlyIncome === 0) return 0;
  return Math.round((monthlyDebt / monthlyIncome) * 100 * 100) / 100;
}

// Calculate loan-to-value ratio
export function calculateLoanToValueRatio(loanAmount, assetValue) {
  if (assetValue === 0) return 0;
  return Math.round((loanAmount / assetValue) * 100 * 100) / 100;
}

// Calculate effective annual rate
export function calculateEffectiveAnnualRate(nominalRate, compoundingPeriods) {
  const r = nominalRate / 100;
  const n = compoundingPeriods;
  const ear = Math.pow(1 + r / n, n) - 1;
  return Math.round(ear * 100 * 100) / 100;
}

// Calculate present value
export function calculatePresentValue(futureValue, rate, periods) {
  const r = rate / 100;
  const pv = futureValue / Math.pow(1 + r, periods);
  return Math.round(pv * 100) / 100;
}

// Calculate future value
export function calculateFutureValue(presentValue, rate, periods) {
  const r = rate / 100;
  const fv = presentValue * Math.pow(1 + r, periods);
  return Math.round(fv * 100) / 100;
}

// Calculate break-even point
export function calculateBreakEvenPoint(
  fixedCosts,
  variableCostPerUnit,
  pricePerUnit
) {
  const contributionMargin = pricePerUnit - variableCostPerUnit;
  if (contributionMargin <= 0) return 0;
  return Math.round(fixedCosts / contributionMargin);
}

// Calculate return on investment
export function calculateROI(gain, cost) {
  if (cost === 0) return 0;
  return Math.round(((gain - cost) / cost) * 100 * 100) / 100;
}

// Validate financial inputs
export function validateFinancialInput(
  value,
  min = 0,
  max = Number.POSITIVE_INFINITY
) {
  const num = Number.parseFloat(value);
  return !isNaN(num) && num >= min && num <= max;
}

// Format percentage
export function formatPercentage(value, decimals = 2) {
  return `${value.toFixed(decimals)}%`;
}

// Calculate age from date of birth
export function calculateAge(dateOfBirth) {
  const today = new Date();
  const birthDate = new Date(dateOfBirth);
  let age = today.getFullYear() - birthDate.getFullYear();
  const monthDiff = today.getMonth() - birthDate.getMonth();

  if (
    monthDiff < 0 ||
    (monthDiff === 0 && today.getDate() < birthDate.getDate())
  ) {
    age--;
  }

  return age;
}
