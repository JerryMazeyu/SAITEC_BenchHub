import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import BenchMarks from "@/views/BenchMarks.vue"
import QuestionAnswer from "@/views/QuestionAnswer.vue"

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
  },
  {
    path: '/questionAnswer',
    name: 'QuestionAnswer',
    component: QuestionAnswer,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router