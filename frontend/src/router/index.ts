import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    // ✅ 新增：根路径直接重定向到登录页
    { path: '/', redirect: '/login' },

    // 公开路由
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { guest: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/user/RegisterView.vue'),
      meta: { guest: true },
    },
    // 组织者注册（公开）—— 已修正组件路径
    {
      path: '/organizer/register',
      name: 'organizer-register',
      component: () => import('@/views/organizer/Register.vue'),
      meta: { guest: true },
    },
    // 学生端布局（需要登录）
    {
      path: '/',
      component: () => import('@/layouts/AppLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '', redirect: '/activities' },
        {
          path: 'activities',
          name: 'activities',
          meta: { title: '活动查询' },
          component: () => import('@/views/user/ActivitiesView.vue'),
        },
        {
          path: 'activities/:id',
          name: 'activity-detail',
          meta: { title: '活动详情' },
          component: () => import('@/views/user/ActivityDetailView.vue'),
        },
        {
          path: 'profile',
          name: 'profile',
          meta: { title: '个人主页' },
          component: () => import('@/views/user/ProfileView.vue'),
        },
        {
          path: 'my/history',
          name: 'my-history',
          meta: { title: '活动历史' },
          component: () => import('@/views/user/MyHistoryView.vue'),
        },
        {
          path: 'notifications',
          name: 'notifications',
          meta: { title: '通知与公告' },
          component: () => import('@/views/user/NotificationsView.vue'),
        },
        {
          path: 'achievement',
          name: 'achievement',
          meta: { title: '统计排行' },
          component: () => import('@/views/user/AchievementView.vue'),
        },
      ],
    },
    // 组织者独立页面（需要登录，但不使用 AppLayout）
    {
      path: '/organizer/activities',
      name: 'organizer-activities',
      component: () => import('@/views/organizer/ActivityList.vue'),
      meta: { requiresAuth: true, role: 'organizer' },
    },
    {
      path: '/organizer/activity',
      name: 'organizer-activity-form',
      component: () => import('@/views/organizer/ActivityDetail.vue'),
      meta: { requiresAuth: true, role: 'organizer' },
    },
    {
      path: '/organizer/registrations',
      name: 'organizer-registrations',
      component: () => import('@/views/organizer/RegistrationList.vue'),
      meta: { requiresAuth: true, role: 'organizer' },
    },
    {
      path: '/organizer/signs',
      name: 'organizer-signs',
      component: () => import('@/views/organizer/SignList.vue'),
      meta: { requiresAuth: true, role: 'organizer' },
    },
    {
      path: '/organizer/stats',
      name: 'organizer-stats',
      component: () => import('@/views/organizer/Stats.vue'),
      meta: { requiresAuth: true, role: 'organizer' },
    },
    {
      path: '/organizer/notice',
      name: 'organizer-notice',
      component: () => import('@/views/organizer/NoticeCenter.vue'),
      meta: { requiresAuth: true, role: 'organizer' },
    },
    {
      path: '/organizer/profile',
      name: 'organizer-profile',
      component: () => import('@/views/organizer/Profile.vue'),
      meta: { requiresAuth: true, role: 'organizer' },
    },
    // 管理员独立页面（需要登录）
    {
      path: '/admin/audit',
      name: 'admin-audit',
      component: () => import('@/views/admin/ActivityAudit.vue'),
      meta: { requiresAuth: true, role: 'admin' },
    },
    {
      path: '/admin/audit/:id',
      name: 'admin-audit-detail',
      component: () => import('@/views/admin/ActivityAuditDetail.vue'),
      meta: { requiresAuth: true, role: 'admin' },
    },
    {
      path: '/admin/users',
      name: 'admin-users',
      component: () => import('@/views/admin/UserManagement.vue'),
      meta: { requiresAuth: true, role: 'admin' },
    },
    {
      path: '/admin/announcements',
      name: 'admin-announcements',
      component: () => import('@/views/admin/Announcement.vue'),
      meta: { requiresAuth: true, role: 'admin' },
    },
    {
      path: '/admin/statistics',
      name: 'admin-statistics',
      component: () => import('@/views/admin/Statistics.vue'),
      meta: { requiresAuth: true, role: 'admin' },
    },
    {
      path: '/admin/profile',
      name: 'admin-profile',
      component: () => import('@/views/admin/Profile.vue'),
      meta: { requiresAuth: true, role: 'admin' },
    },
    // 404 重定向
    { path: '/:pathMatch(.*)*', redirect: '/activities' },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  // 需要登录但未登录
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  // 已登录用户访问 guest 页面，跳转到默认首页
  if (to.meta.guest && auth.isLoggedIn) {
    // 根据角色跳转
    if (auth.role === 'organizer') return '/organizer/activities'
    if (auth.role === 'admin') return '/admin/audit'
    return '/activities'
  }
  // 角色权限检查（可选）
  if (to.meta.role && auth.role !== to.meta.role) {
    if (auth.role === 'organizer') return '/organizer/activities'
    if (auth.role === 'admin') return '/admin/audit'
    return '/activities'
  }
  return true
})

export default router