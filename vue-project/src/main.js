import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import './assets/main.css'

// ✅ создаём app отдельно
const app = createApp(App);

// ✅ подключаем pinia
app.use(createPinia());

// ✅ подключаем router
app.use(router);

// ✅ монтируем в самом конце
app.mount("#app");