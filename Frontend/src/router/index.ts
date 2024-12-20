import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
// import BenchmarkPage from '@/components/BenchmarkPage.vue'



const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
//   {
//     path: '/benchmarks',
//     name: 'Benchmarks',
//     component: BenchmarkPage,
//   },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router