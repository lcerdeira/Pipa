import Vue from 'vue'
import axios from 'axios'

// Set default timeout to 30 seconds for uploads
axios.defaults.timeout = 30000

Vue.prototype.$axios = axios
