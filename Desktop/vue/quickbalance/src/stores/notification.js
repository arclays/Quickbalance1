// // src/stores/notification.js
// import { defineStore } from "pinia";

// export const useNotificationStore = defineStore("notification", {
//   state: () => ({
//     notifications: [],
//     unreadCount: 0,
//   }),

//   actions: {
//     addNotification(notification) {
//       this.notifications.push(notification);
//       this.unreadCount++;
//     },

//     markAsRead(id) {
//       const index = this.notifications.findIndex((n) => n.id === id);
//       if (index !== -1 && !this.notifications[index].read) {
//         this.notifications[index].read = true;
//         this.unreadCount--;
//       }
//     },

//     markAllAsRead() {
//       this.notifications.forEach((n) => {
//         n.read = true;
//       });
//       this.unreadCount = 0;
//     },

//     clearNotifications() {
//       this.notifications = [];
//       this.unreadCount = 0;
//     },

//     async fetchNotifications() {
//       try {
//         const response = await fetch("http://localhost:8000/api/notifications");

//         if (!response.ok) {
//           throw new Error(`Failed to fetch: ${response.status}`);
//         }

//         const data = await response.json();

//         // assuming API returns an array of notifications with {id, title, message, type, timestamp, read}
//         this.notifications = data;
//         this.unreadCount = data.filter((n) => !n.read).length;
//       } catch (error) {
//         console.error("Failed to fetch notifications:", error.message);
//       }
//     },
//   },
// });
