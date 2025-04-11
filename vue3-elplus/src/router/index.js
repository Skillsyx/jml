import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Usage from '../views/Usage.vue'
import Preview from '../views/Preview.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: Login },
  { path: '/usage', name: 'Usage', component: Usage },
  { path: '/preview', name: 'Preview', component: Preview }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局路由守卫
router.beforeEach((to, from, next) => {
    // 假设我们在 localStorage 存储了 "isAuthenticated" 标志表示已登录
    const isAuthenticated = localStorage.getItem('isAuthenticated')
    
    if (to.name !== 'Login' && !isAuthenticated) {
      // 如果目标不是登录页且未认证，则重定向到登录页
      next({ name: 'Login' })
    } else {
      next()
    }
  })
  

export default router
