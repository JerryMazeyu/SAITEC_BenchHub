import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import BenchMarks from "@/views/BenchMarks.vue"
import QuestionAnswer from "@/views/QuestionAnswer.vue"
import Papers from "@/views/Papers.vue"

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
  },
  {
    path: '/papers',
    name: 'Papers',
    component: Papers,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router