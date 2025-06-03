import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('../views/layout/Layout.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('../views/home/Index.vue'),
        meta: { title: '首页' }
      },
      {
        path: 'documents',
        name: 'Documents',
        component: () => import('../views/documents/Index.vue'),
        meta: { title: '文档管理' }
      },
      {
        path: 'templates',
        name: 'Templates',
        component: () => import('../views/templates/Index.vue'),
        meta: { title: '模板管理' }
      },
      {
        path: 'knowledge',
        name: 'Knowledge',
        component: () => import('../views/knowledge/Index.vue'),
        meta: { title: '知识图谱' }
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('../views/users/Index.vue'),
        meta: { title: '用户管理' }
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/login/Index.vue'),
    meta: { title: '登录' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 