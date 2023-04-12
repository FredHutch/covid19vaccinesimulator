import { createApp } from 'vue';
import { createPinia } from 'pinia';
import ToastService from 'primevue/toastservice';
import App from './App.vue';
import router from './router';
import { createHead } from "@unhead/vue"
import PrimeVue from 'primevue/config';

import VueGtag from "vue-gtag";


const app = createApp(App);
//app.config.globalProperties.$systemName = 'Vaccine Allocator';

const head = createHead()
app.use(head)


app.use(createPinia());
app.use(router);



app.use(PrimeVue);

app.use(ToastService);

app.use(VueGtag, {
    config: { 
      id: "G-8F3QSHJHXW",
    },
  }, router); // <----- add your router here

app.mount('#app');
