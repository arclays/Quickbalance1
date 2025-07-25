// src/stores/clients.js
import { defineStore } from "pinia";

export const useClientsStore = defineStore("clients", {
  state: () => ({
    clients: [],
  }),
  actions: {
    addClient(client) {
      this.clients.push(client);
    },
    deleteClient(id) {
      this.clients = this.clients.filter((c) => c.id !== id);
    },
  },
});
