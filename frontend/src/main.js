import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import "element-plus/dist/index.css";
import ElementPlus from "element-plus";

const pinia = createPinia();
const app = createApp(App);

app.use(ElementPlus);
app.use(pinia);
app.mount("#app");
