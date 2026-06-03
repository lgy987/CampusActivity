<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import {
  User,
  Home,
  Trophy,
  CalendarCheck,
  Bell,
  Search,
  LogOut,
  ChevronDown,
} from 'lucide-vue-next'
import { cn } from '@/utils'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import { logout } from '@/api/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const userStore = useUserStore()

const personalOpen = ref(true)

const navItems = [
  {
    label: '个人中心',
    icon: User,
    children: [
      { label: '个人主页', icon: Home, to: '/profile' },
      { label: '统计排行', icon: Trophy, to: '/achievement' },
      { label: '我的活动历史', icon: CalendarCheck, to: '/my/history' },
    ],
  },
  { label: '活动查询', icon: Search, to: '/activities' },
  { label: '通知与公告', icon: Bell, to: '/notifications' },
]

//const displayName = computed(() => userStore.profile?.username || '学生用户')
const displayName = computed(() => userStore.userInfo?.username || '学生用户')

function isActive(path: string) {
  if (path === '/activities') {
    return route.path === '/activities' || route.path.startsWith('/activities/')
  }
  return route.path.startsWith(path)
}

async function handleLogout() {
  try {
    await logout()
  } catch {
    /* ignore */
  }
  auth.clearAuth()
  userStore.clearProfile()
  router.push('/login')
}

onMounted(() => {
//  if (auth.isLoggedIn && !userStore.profile) {
  if (auth.isLoggedIn && !userStore.userInfo) {
    userStore.fetchProfile().catch(() => {})
  }
})
</script>

<template>
  <aside class="flex w-56 shrink-0 flex-col border-r bg-white">
    <div class="border-b px-4 py-4">
      <p class="text-sm font-bold text-[var(--proto-blue)]">BIT 校园活动</p>
    </div>

    <nav class="flex-1 overflow-y-auto py-3">
      <ul class="space-y-0.5 px-2">
        <li v-for="item in navItems" :key="item.label">
          <template v-if="item.children">
            <button
              type="button"
              class="flex w-full items-center gap-2 rounded-md px-3 py-2.5 text-sm text-foreground hover:bg-blue-50"
              @click="personalOpen = !personalOpen"
            >
              <component :is="item.icon" class="h-4 w-4 shrink-0 text-gray-500" />
              <span class="flex-1 text-left">{{ item.label }}</span>
              <ChevronDown
                class="h-4 w-4 text-gray-400 transition-transform"
                :class="{ 'rotate-180': personalOpen }"
              />
            </button>
            <ul v-show="personalOpen" class="ml-2 mt-0.5 space-y-0.5 border-l border-gray-100 pl-2">
              <li v-for="child in item.children" :key="child.to">
                <RouterLink
                  :to="child.to"
                  :class="
                    cn(
                      'flex items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors',
                      isActive(child.to) ? 'sidebar-active font-medium' : 'text-gray-600 hover:bg-blue-50',
                    )
                  "
                >
                  <component :is="child.icon" class="h-4 w-4 shrink-0" />
                  {{ child.label }}
                </RouterLink>
              </li>
            </ul>
          </template>

          <RouterLink
            v-else
            :to="item.to!"
            :class="
              cn(
                'flex items-center gap-2 rounded-md px-3 py-2.5 text-sm transition-colors',
                isActive(item.to!) ? 'sidebar-active font-medium' : 'text-gray-600 hover:bg-blue-50',
              )
            "
          >
            <component :is="item.icon" class="h-4 w-4 shrink-0" />
            {{ item.label }}
          </RouterLink>
        </li>
      </ul>
    </nav>

    <div class="border-t p-3">
      <div class="mb-2 flex items-center gap-2 rounded-lg bg-blue-50 px-3 py-2">
        <div
          class="flex h-9 w-9 items-center justify-center rounded-full bg-blue-100 text-sm font-bold text-blue-600"
        >
          {{ displayName.charAt(0) }}
        </div>
        <p class="truncate text-sm font-medium">{{ displayName }}</p>
      </div>
      <button
        type="button"
        class="flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-gray-600 hover:bg-red-50 hover:text-red-600"
        @click="handleLogout"
      >
        <LogOut class="h-4 w-4" />
        退出登录
      </button>
    </div>
  </aside>
</template>
