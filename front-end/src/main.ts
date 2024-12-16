import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
// Element Plus
import ElementPlus from 'element-plus'
// import 'element-plus/dist/index.css'
import './styles/base.css'
import piniaPersistedState from 'pinia-plugin-persist'


//注册库组件
// if (process.env.NODE_ENV === 'development') {
//     import('./mock/user'); // 动态引入
//   }

  
//创建pinia对象
const pinia = createPinia()
const app = createApp(App)
pinia.use(piniaPersistedState)
app.use(ElementPlus)
app.use(router)
app.use(pinia)
.mount('#app')
