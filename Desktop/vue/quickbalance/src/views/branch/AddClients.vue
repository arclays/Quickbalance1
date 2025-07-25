<script setup>
import { ref, computed } from "vue";
// import AddClientModal from '@/components/Clients/AddClientModal.vue';
import DataTable from "datatables.net-vue3";
import DataTablesCore from "datatables.net-bs5";
import AddClientModal from "@/components/Clients/AddClientModal.vue";

DataTable.use(DataTablesCore);
const isModalOpen = ref(false);
const modalMode = ref("create"); // 'create' or 'edit'
const selectedClient = ref({});
// Sample mock client data

const clients = ref([
  {
    id: 1,
    fullName: "Jane Doe",
    address: "123 Kampala Rd",
    gender: "Female",
    phone: "+256 700000001",
    nin: "CF12345678BDE",
    businessName: "Jane's Boutique",
    creditOfficer: "John Mwangi",
    accountNumber: "00123",
    creditLimit: 2000,
  },
  {
    id: 2,
    fullName: "David Okello",
    address: "Plot 45, Ntinda",
    gender: "Male",
    phone: "+256 700000002",
    nin: "CF87654321XYZ",
    businessName: "Okello Electronics",
    creditOfficer: "Grace Nansubuga",
    accountNumber: "00456",
    creditLimit: 5000,
  },
]);

const totalClients = computed(() => clients.value.length);

function openModal() {
  // isModalOpen.value = true;
}

function deleteClient(id) {
  if (confirm("Are you sure you want to delete this client?")) {
    clients.value = clients.value.filter((c) => c.id !== id);
  }
}

function viewClient(client) {
  alert(`Client Info:\n\n${JSON.stringify(client, null, 2)}`);
}

function editClient(client) {
  alert(
    `Editing client: ${client.fullName} (You can link this to a real edit page)`
  );
}

function closeModal() {
  // isModalOpen.value = false;
  // for (const key in form) form[key] = "";
  // for (const key in errors) errors[key] = "";
  // successMessage.value = "";
  // errorMessage.value = "";
}

function openCreateModal() {
  modalMode.value = "create";
  selectedClient.value = {};
  isModalOpen.value = true;
}

// Open modal for editing client
function openEditModal(client) {
  modalMode.value = "edit";
  selectedClient.value = { ...client };
  isModalOpen.value = true;
}
function handleCloseModal() {
  isModalOpen.value = false;
}

// Optional: Refresh client list after saving
function handleSavedClient() {
  console.log("Client was saved");
  isModalOpen.value = false;
  // refreshClients(); // if needed
}
</script>

<template>
  <section class="client-section">
    <div class="header">
      <h2><i class="fas fa-users"></i> Clients</h2>
      <div class="actions">
        <span class="total">Total: {{ totalClients }}</span>
        <!-- <button class="btn btn-primary" @click="openModal">
          <i class="fas fa-user-plus"></i> Add Client
        </button> -->
        <button class="btn btn-dark" @click="openCreateModal">
          Add New Client
        </button>
      </div>
    </div>

    <!-- Client Table -->
    <div class="table-container">
      <!-- <table class="client-table"> -->
      <DataTable class="table table-striped table-bordered w-100 display">
        <thead>
          <tr>
            <th style="width: 40px">No</th>
            <th style="min-width: 150px">Full Name</th>
            <th style="min-width: 150px">Phone</th>
            <th style="min-width: 150px">NIN</th>
            <th style="min-width: 150px">Business</th>
            <th style="min-width: 150px">Credit Officer</th>
            <th style="min-width: 100px">Limit</th>
            <th style="width: 150px">Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="(client, index) in clients" :key="client.id">
            <td>{{ index + 1 }}</td>
            <td>{{ client.fullName }}</td>
            <td>{{ client.phone }}</td>
            <td>{{ client.nin }}</td>
            <td>{{ client.businessName }}</td>
            <td>{{ client.creditOfficer }}</td>
            <td>{{ client.creditLimit }}</td>
            <td class="action-buttons">
              <button class="btn btn-info" @click="viewClient(client)">
                <i class="fas fa-eye"></i>
              </button>
              <button class="btn btn-warning" @click="editClient(client)">
                <i class="fas fa-edit"></i>
              </button>
              <button class="btn btn-danger" @click="deleteClient(client.id)">
                <i class="fas fa-trash-alt"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </DataTable>
      <!-- </table> -->
    </div>
    <!-- Modal -->
    <!-- <AddClientModal  /> -->
    <AddClientModal
      v-if="isModalOpen"
      :mode="modalMode"
      :client="selectedClient"
      @close="handleCloseModal"
      @saved="handleSavedClient"
    />

    <!-- <AddClientModal v-if="isModalOpen" @close="isModalOpen = false" /> -->
  </section>
</template>

<style scoped>
.client-section {
  padding: 2rem;
}
.action-buttons {
  display: flex;
  gap: 5px;
  justify-content: center;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.header h2 {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #2d2d2d;
}

.total {
  margin-right: 1rem;
  font-weight: bold;
}

.actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.table-container {
  overflow-x: auto;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.05);
}

.client-table {
  width: 100%;
  border-collapse: collapse;
}

.client-table th,
.client-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.client-table th {
  background-color: #f1f3f5;
  color: #333;
}

.action-buttons button {
  margin-right: 5px;
  padding: 6px 10px;
  font-size: 0.9rem;
}

.btn-info {
  background-color: #17a2b8;
  color: white;
}

.btn-warning {
  background-color: #ffc107;
  color: black;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}
</style>
