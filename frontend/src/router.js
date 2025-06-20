import { createRouter, createWebHistory } from 'vue-router'
import Login from './components/Login.vue'
import AdminView from './components/AdminView.vue'
import EmployeeView from './components/EmployeeView.vue'

const routes = [
  { 
    path: '/', 
    component: Login,
    meta: { public: true }
  },
  {
    path: '/login',
    component: Login
  },
  {
    path: '/admin',
    component: AdminView
  },
  {
    path: '/employee',
    component: EmployeeView
  }
]

// router.beforeEach((to, from, next) => {
//   const isAuthenticated = localStorage.getItem('token') !== null
  
//   if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
//     next('/login')
//   } else if (to.matched.some(record => record.meta.public) && isAuthenticated) {
//     next('/home')
//   } else {
//     next()
//   }
// })

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router