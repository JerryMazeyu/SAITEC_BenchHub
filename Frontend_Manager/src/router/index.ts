import { createRouter, createWebHistory } from 'vue-router'
import Login from "../views/Login.vue"
import Layout from "../components/Layout.vue"

const routes= [
     {
        path: '/login',
        name: 'Login',
        component: Login,
      },
      {
        path:'/',
        name:'Layout',
        component:Layout,
        children:[

        ]
      },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
  });
  
export default router