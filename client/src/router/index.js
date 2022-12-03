import { createRouter, createWebHistory } from 'vue-router';
import Ping from '@/components/Ping.vue';
import Books from '@/components/Book-List.vue';

const routes = [
  {
    path: '/',
    name: 'Book-List',
    component: Books,
  },
  {
    path: '/ping',
    name: 'Ping-Component',
    component: Ping,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
