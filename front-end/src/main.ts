import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
// Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './styles/base.css'

//注册库组件
import TypeNav from '@/components/type-nav/TypeNav.vue'
import Carousel from '@/components/carousel/Carousel.vue'

//创建pinia对象
const pinia = createPinia()
const app = createApp(App)

app.use(ElementPlus)
app.use(router)
app.use(pinia)
app.component('type-nav', TypeNav)
app.component('my-carousel', Carousel)
.mount('#app')
