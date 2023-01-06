import accountRoutes from './account.routes'

const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/AnalyticsPageg.vue') }]
  },
  { ...accountRoutes },
  {
    path: '/books',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/BooksPage.vue') }]
  },
  {
    path: '/analytics',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/AnalyticsPage.vue') }]
  },
  {
    path: '/counter',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/CounterPage.vue') }]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
