import { createRouter, createWebHistory } from 'vue-router';
import Login from "../views/Login.vue";
import Layout from "../components/Layout.vue";
import Paper from "../views/Paper.vue";
import QA from "../views/QA.vue";

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/paper', // 默认重定向到 /home
    children: [
      {
        path: '/paper', // 子路由直接匹配 /home
        name: 'Paper',
        component: Paper,
      },
      {
        path: '/qa', // 子路由直接匹配 /home
        name: 'QA',
        component: QA,
      },
    ],
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router