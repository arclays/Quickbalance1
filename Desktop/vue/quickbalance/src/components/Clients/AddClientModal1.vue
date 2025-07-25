<script setup>
import { reactive, ref } from "vue";

const creditOfficers = ref([
  { id: 1, name: "John Mwangi" },
  { id: 2, name: "Grace Nansubuga" },
  { id: 3, name: "Peter Okello" },
]);

const form = reactive({
  fullName: "",
  address: "",
  gender: "",
  phone: "",
  nin: "",
  businessName: "",
  creditOfficer: "",
  accountNumber: "",
  creditLimit: "",
});

const errors = reactive({});
const submitting = ref(false);
const successMessage = ref("");
const errorMessage = ref("");
const isModalOpen = ref(false);

function validate() {
  errors.fullName = !form.fullName.trim() ? "Full Name is required." : "";
  errors.address = !form.address.trim() ? "Address is required." : "";
  errors.gender = !form.gender ? "Please select a gender." : "";
  errors.phone = !form.phone.trim() ? "Phone Number is required." : "";
  errors.nin = !form.nin.trim() ? "National ID / NIN is required." : "";
  errors.creditOfficer = !form.creditOfficer
    ? "Please select a credit officer."
    : "";

  if (form.phone && !/^\+?[\d\s-]{7,15}$/.test(form.phone)) {
    errors.phone = "Please enter a valid phone number (7–15 digits)";
  }

  return !Object.values(errors).some((error) => error);
}

function saveClient() {
  return new Promise((resolve) => {
    setTimeout(() => resolve({ success: true }), 1500);
  });
}

async function handleSubmit() {
  successMessage.value = "";
  errorMessage.value = "";

  if (!validate()) return;

  submitting.value = true;
  try {
    const response = await saveClient();
    if (response.success) {
      successMessage.value = "Client created successfully!";
      for (const key in form) form[key] = "";
      setTimeout(() => {
        isModalOpen.value = false;
        successMessage.value = "";
      }, 2000);
    } else {
      errorMessage.value = "Failed to create client.";
    }
  } catch (err) {
    errorMessage.value = "An unexpected error occurred.";
  } finally {
    submitting.value = false;
  }
}

function openModal() {
  isModalOpen.value = true;
  successMessage.value = "";
  errorMessage.value = "";
  for (const key in errors) errors[key] = "";
}

function closeModal() {
  isModalOpen.value = false;
  for (const key in form) form[key] = "";
  for (const key in errors) errors[key] = "";
  successMessage.value = "";
  errorMessage.value = "";
}
</script>

<template>
  <div>
    <!-- Modal -->
    <div class="modal" :class="{ show: isModalOpen }">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">
              <i class="fas fa-user-plus"></i> Client Registration
            </h4>
            <button class="close-btn" @click="closeModal">
              <i class="fas fa-times"></i>
            </button>
          </div>

          <div class="modal-body">
            <form @submit.prevent="handleSubmit" novalidate>
              <h5 class="section-title">
                <i class="fas fa-user-circle"></i> Personal Information
              </h5>

              <div class="form-grid">
                <!-- Full Name -->
                <div class="form-group">
                  <label for="fullName" class="form-label">
                    Full Name <span class="text-danger">*</span>
                  </label>
                  <input
                    type="text"
                    id="fullName"
                    class="form-control"
                    v-model="form.fullName"
                    :class="{ 'is-invalid': errors.fullName }"
                    placeholder="Enter full name"
                    required
                  />
                  <div v-if="errors.fullName" class="invalid-feedback">
                    {{ errors.fullName }}
                  </div>
                </div>

                <!-- Address -->
                <div class="form-group">
                  <label for="address" class="form-label">
                    Address <span class="text-danger">*</span>
                  </label>
                  <textarea
                    id="address"
                    class="form-control"
                    v-model="form.address"
                    :class="{ 'is-invalid': errors.address }"
                    placeholder="Enter client address"
                    required
                  ></textarea>
                  <div v-if="errors.address" class="invalid-feedback">
                    {{ errors.address }}
                  </div>
                </div>

                <!-- Gender -->
                <div class="form-group">
                  <label for="gender" class="form-label">
                    Gender <span class="text-danger">*</span>
                  </label>
                  <select
                    id="gender"
                    class="form-select"
                    v-model="form.gender"
                    :class="{ 'is-invalid': errors.gender }"
                    required
                  >
                    <option value="" disabled>Select gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                  <div v-if="errors.gender" class="invalid-feedback">
                    {{ errors.gender }}
                  </div>
                </div>

                <!-- Phone -->
                <div class="form-group">
                  <label for="phone" class="form-label">
                    Phone Number <span class="text-danger">*</span>
                  </label>
                  <input
                    type="tel"
                    id="phone"
                    class="form-control"
                    v-model="form.phone"
                    :class="{ 'is-invalid': errors.phone }"
                    placeholder="+256 700 000000"
                    required
                  />
                  <div v-if="errors.phone" class="invalid-feedback">
                    {{ errors.phone }}
                  </div>
                </div>

                <!-- NIN -->
                <div class="form-group">
                  <label for="nin" class="form-label">
                    National ID / NIN <span class="text-danger">*</span>
                  </label>
                  <input
                    type="text"
                    id="nin"
                    class="form-control"
                    v-model="form.nin"
                    :class="{ 'is-invalid': errors.nin }"
                    placeholder="Enter National ID or NIN"
                    required
                  />
                  <div v-if="errors.nin" class="invalid-feedback">
                    {{ errors.nin }}
                  </div>
                </div>

                <!-- Business Info -->
                <h5 class="section-title">
                  <i class="fas fa-briefcase"></i> Business Information
                </h5>

                <!-- Business Name -->
                <div class="form-group">
                  <label for="businessName" class="form-label"
                    >Business Name</label
                  >
                  <input
                    type="text"
                    id="businessName"
                    class="form-control"
                    v-model="form.businessName"
                    placeholder="Client's business name (optional)"
                  />
                </div>

                <!-- Financial Info -->
                <h5 class="section-title">
                  <i class="fas fa-chart-line"></i> Financial Information
                </h5>

                <!-- Credit Officer -->
                <div class="form-group">
                  <label for="creditOfficer" class="form-label">
                    Credit Officer <span class="text-danger">*</span>
                  </label>
                  <select
                    id="creditOfficer"
                    class="form-select"
                    v-model="form.creditOfficer"
                    :class="{ 'is-invalid': errors.creditOfficer }"
                    required
                  >
                    <option value="" disabled>Select credit officer</option>
                    <option
                      v-for="officer in creditOfficers"
                      :key="officer.id"
                      :value="officer.name"
                    >
                      {{ officer.name }}
                    </option>
                  </select>
                  <div v-if="errors.creditOfficer" class="invalid-feedback">
                    {{ errors.creditOfficer }}
                  </div>
                </div>

                <!-- Account Number -->
                <div class="form-group">
                  <label for="accountNumber" class="form-label"
                    >Account Number</label
                  >
                  <input
                    type="text"
                    id="accountNumber"
                    class="form-control"
                    v-model="form.accountNumber"
                    placeholder="Client account number (optional)"
                  />
                </div>

                <!-- Credit Limit -->
                <div class="form-group">
                  <label for="creditLimit" class="form-label"
                    >Credit Limit</label
                  >
                  <input
                    type="number"
                    id="creditLimit"
                    class="form-control"
                    v-model="form.creditLimit"
                    placeholder="Enter credit limit (optional)"
                    min="0"
                    step="0.01"
                  />
                </div>
              </div>

              <!-- Alerts -->
              <div v-if="successMessage" class="alert alert-success mt-3">
                {{ successMessage }}
              </div>
              <div v-if="errorMessage" class="alert alert-danger mt-3">
                {{ errorMessage }}
              </div>
            </form>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeModal()">
              Cancel
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="submitting"
              @click="handleSubmit"
            >
              {{ submitting ? "Saving..." : "Create Client" }}
            </button>
          </div>
        </div>
      </div>

      <!-- Modal Overlay -->
      <div class="modal-overlay" @click="closeModal"></div>
    </div>
  </div>
</template>

<style scoped>
:root {
  --primary: #4361ee;
  --secondary: #5f77ff;
  --accent: #4895ef;
}

/* Add Client Button */
.add-client-btn {
  background: linear-gradient(
    90deg,
    var(--primary, #4361ee),
    var(--secondary, #5f77ff)
  );
  border: none;
  padding: 12px 20px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.add-client-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(67, 97, 238, 0.4);
}

/* Modal Styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1050;
  display: none;
  overflow: auto;
}

.modal.show {
  display: block;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1040;
}

.modal-dialog {
  position: relative;
  max-width: 800px;
  margin: 2rem auto;
  z-index: 1050;
}

.modal-content {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.modal-header {
  background: linear-gradient(
    90deg,
    var(--primary, #4361ee),
    var(--secondary, #5f77ff)
  );
  color: #fff;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
}

.close-btn {
  background: none;
  border: none;
  color: #fff;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.5rem;
}

.modal-body {
  padding: 2rem;
  max-height: 60vh;
  overflow-y: auto;
}

.modal-footer {
  padding: 1rem;
  border-top: 1px solid #e9ecef;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* Form Styles */
.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--primary, #4361ee);
  border-bottom: 2px solid var(--accent, #4895ef);
  padding-bottom: 8px;
  margin: 1.5rem 0 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .modal-dialog {
    margin: 1rem;
    max-width: 95%;
  }
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-label {
  display: block;
  font-weight: 500;
  color: #495057;
  margin-bottom: 0.5rem;
}

.form-control,
.form-select {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border: 2px solid #e1e5eb;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.form-control:focus,
.form-select:focus {
  border-color: var(--accent, #4895ef);
  box-shadow: 0 0 0 0.25rem rgba(67, 97, 238, 0.2);
}

.form-control.is-invalid,
.form-select.is-invalid {
  border-color: #dc3545;
}

.invalid-feedback {
  font-size: 0.875rem;
  color: #dc3545;
  margin-top: 0.25rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
}

.btn-primary {
  background: linear-gradient(
    90deg,
    var(--primary, #4361ee),
    var(--secondary, #5f77ff)
  );
  border: none;
  color: #fff;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(67, 97, 238, 0.4);
}

.btn-primary:disabled {
  background: linear-gradient(90deg, #a0a8d0, #8a8fc5);
  transform: none;
  box-shadow: none;
  cursor: not-allowed;
}

.btn-secondary {
  background: #6c757d;
  border: none;
  color: #fff;
}

.btn-secondary:hover {
  background: #5a6268;
}

.alert {
  font-weight: 500;
  margin-top: 1rem;
}

/* Scrollbar Styling */
.modal-body::-webkit-scrollbar {
  width: 6px;
}

.modal-body::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.modal-body::-webkit-scrollbar-thumb {
  background: var(--accent, #4895ef);
  border-radius: 3px;
}
</style>
```
