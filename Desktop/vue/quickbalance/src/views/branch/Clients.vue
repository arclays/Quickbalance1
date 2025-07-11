<template>
  <div class="container-fluid">
    <div class="row mb-4">
      <div class="col">
        <h1 class="h3 mb-0">Client Management</h1>
        <p class="text-muted">Manage client information and memberships</p>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary" @click="showAddClient = true">
          <i class="fas fa-plus me-2"></i>
          Add Client
        </button>
      </div>
    </div>

    <!-- Search and Filters -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-4">
            <label class="form-label">Search Clients</label>
            <div class="input-group">
              <span class="input-group-text">
                <i class="fas fa-search"></i>
              </span>
              <input
                type="text"
                class="form-control"
                placeholder="Search by name, ID, or phone"
                v-model="searchQuery"
              />
            </div>
          </div>
          <div class="col-md-3">
            <label class="form-label">Status</label>
            <select class="form-select" v-model="statusFilter">
              <option value="">All Status</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
              <option value="suspended">Suspended</option>
            </select>
          </div>
          <div class="col-md-3">
            <label class="form-label">Membership Type</label>
            <select class="form-select" v-model="membershipFilter">
              <option value="">All Types</option>
              <option value="regular">Regular</option>
              <option value="premium">Premium</option>
              <option value="corporate">Corporate</option>
            </select>
          </div>
          <div class="col-md-2">
            <label class="form-label">&nbsp;</label>
            <button
              class="btn btn-outline-secondary w-100"
              @click="clearFilters"
            >
              Clear Filters
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Client List -->
    <ClientList
      :clients="filteredClients"
      @edit="editClient"
      @view="viewClient"
      @delete="deleteClient"
    />

    <!-- Add/Edit Client Modal -->
    <ClientForm
      v-if="showAddClient || editingClient"
      :client="editingClient"
      @save="saveClient"
      @cancel="cancelClientForm"
    />

    <!-- Client Details Modal -->
    <MembershipDetails
      v-if="viewingClient"
      :client="viewingClient"
      @close="viewingClient = null"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import ClientList from "../../components/branch/ClientManagement/ClientList.vue";
import ClientForm from "../../components/branch/ClientManagement/ClientForm.vue";
import MembershipDetails from "../../components/branch/ClientManagement/MembershipDetails.vue";

const searchQuery = ref("");
const statusFilter = ref("");
const membershipFilter = ref("");
const showAddClient = ref(false);
const editingClient = ref(null);
const viewingClient = ref(null);

const clients = ref([
  {
    id: 1,
    clientId: "CL001",
    firstName: "John",
    lastName: "Doe",
    email: "john.doe@email.com",
    phone: "+1234567890",
    address: "123 Main St, City",
    status: "active",
    membershipType: "regular",
    joinDate: "2023-01-15",
    totalSavings: 15000,
    activeLoans: 2,
    creditScore: 750,
  },
  {
    id: 2,
    clientId: "CL002",
    firstName: "Jane",
    lastName: "Smith",
    email: "jane.smith@email.com",
    phone: "+1234567891",
    address: "456 Oak Ave, City",
    status: "active",
    membershipType: "premium",
    joinDate: "2023-02-20",
    totalSavings: 25000,
    activeLoans: 1,
    creditScore: 800,
  },
]);

const filteredClients = computed(() => {
  let filtered = clients.value;

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (client) =>
        client.firstName.toLowerCase().includes(query) ||
        client.lastName.toLowerCase().includes(query) ||
        client.clientId.toLowerCase().includes(query) ||
        client.phone.includes(query)
    );
  }

  if (statusFilter.value) {
    filtered = filtered.filter(
      (client) => client.status === statusFilter.value
    );
  }

  if (membershipFilter.value) {
    filtered = filtered.filter(
      (client) => client.membershipType === membershipFilter.value
    );
  }

  return filtered;
});

const editClient = (client) => {
  editingClient.value = { ...client };
};

const viewClient = (client) => {
  viewingClient.value = client;
};

const deleteClient = (clientId) => {
  if (confirm("Are you sure you want to delete this client?")) {
    clients.value = clients.value.filter((c) => c.id !== clientId);
  }
};

const saveClient = (clientData) => {
  if (editingClient.value) {
    // Update existing client
    const index = clients.value.findIndex(
      (c) => c.id === editingClient.value.id
    );
    if (index !== -1) {
      clients.value[index] = { ...clientData, id: editingClient.value.id };
    }
  } else {
    // Add new client
    const newClient = {
      ...clientData,
      id: Date.now(),
      clientId: `CL${String(clients.value.length + 1).padStart(3, "0")}`,
      joinDate: new Date().toISOString().split("T")[0],
      totalSavings: 0,
      activeLoans: 0,
      creditScore: 650,
    };
    clients.value.push(newClient);
  }

  cancelClientForm();
};

const cancelClientForm = () => {
  showAddClient.value = false;
  editingClient.value = null;
};

const clearFilters = () => {
  searchQuery.value = "";
  statusFilter.value = "";
  membershipFilter.value = "";
};

onMounted(() => {
  // Load clients data
});
</script>
