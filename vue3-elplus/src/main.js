import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './style.css'
import axios from 'axios';


const app = createApp(App)

// 注册 Vue Router 插件
app.use(router)
// 注册 Element Plus 插件
app.use(ElementPlus)

app.mount('#app')
