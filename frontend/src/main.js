import { createApp } from "vue"

import App from "./App.vue"

import router from "./router"

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap/dist/js/bootstrap.bundle.min.js"

document.documentElement.setAttribute("data-bs-theme", "dark")

createApp(App).use(router).mount("#app")
