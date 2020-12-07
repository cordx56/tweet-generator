import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTwitter } from '@fortawesome/free-brands-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import VueMeta from 'vue-meta'

Vue.use(VueMeta)

Vue.prototype.$axios = axios
Vue.use(BootstrapVue)

library.add(faTwitter)
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
  created() {
    const html = document.documentElement
    html.setAttribute('lang', 'ja')
  }
}).$mount('#app')
