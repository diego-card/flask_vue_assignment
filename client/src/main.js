/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'
import axios from 'axios'

// Set Axios base URL to Flask API
axios.defaults.baseURL = 'http://localhost:5000/api'

const app = createApp(App)

registerPlugins(app)

app.config.globalProperties.$axios = axios

app.mount('#app')
