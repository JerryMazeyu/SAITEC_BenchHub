import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import BenchMarks from "@/views/BenchMarks.vue"



const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/benchmarks',
    name: 'Benchmarks',
    component: BenchMarks,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router