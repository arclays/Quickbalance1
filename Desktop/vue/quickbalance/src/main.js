import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";

// Bootstrap CSS and JS
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";

// Font Awesome
import "@fortawesome/fontawesome-free/css/all.min.css";

// app.use(store);

const app = createApp(App);
app.use(router);
app.use(createPinia());
app.mount("#app");
