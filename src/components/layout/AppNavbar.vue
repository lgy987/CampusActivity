<!-- AppNavbar.vue -->
<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Menu, X } from '@lucide/vue'
import { cn } from '@/lib/utils'

interface NavItem {
  label: string
  href?: string
  icon?: any
  children?: NavItem[]
  open?: boolean // 移动端下拉菜单状态
}

interface Props {
  // 品牌名称
  brandName?: string
  // Logo URL
  logoUrl?: string
  // Logo 替代文本
  logoAlt?: string
  // 导航项
  navItems?: NavItem[]
  // 是否固定顶部
  fixed?: boolean
  // 背景变体
  variant?: 'default' | 'glass' | 'transparent' | 'gradient'
  // 是否显示阴影
  shadow?: boolean
  // 是否显示边框
  border?: boolean
  // 响应式断点（移动端菜单显示）
  mobileBreakpoint?: 'sm' | 'md' | 'lg'
  // 主题色
  theme?: 'light' | 'dark' | 'auto'
}

const props = withDefaults(defineProps<Props>(), {
  brandName: 'Brand',
  logoUrl: '/src/assets/logo.png',
  logoAlt: 'Logo',
  navItems: () => [],
  fixed: true,
  variant: 'glass',
  shadow: true,
  border: false,
  mobileBreakpoint: 'md',
  theme: 'auto'
})

const emit = defineEmits<{
  'nav-click': [item: NavItem]
  'logo-click': []
}>()

// 移动端菜单状态
const mobileMenuOpen = ref(false)

// 滚动状态（用于改变样式）
const scrolled = ref(false)

// 主题检测
const isDark = computed(() => {
  if (props.theme === 'auto') {
    return window.matchMedia('(prefers-color-scheme: dark)').matches
  }
  return props.theme === 'dark'
})

// 变体样式
const variantClass = computed(() => {
  const map = {
    default: 'bg-background',
    glass: 'bg-background/80 backdrop-blur-xl',
    transparent: 'bg-transparent',
    gradient: 'bg-gradient-to-r from-primary/90 to-primary/60 backdrop-blur-sm'
  }
  return map[props.variant]
})

// 移动端断点
const mobileBreakpointClass = computed(() => {
  const map = {
    sm: 'sm:hidden',
    md: 'md:hidden',
    lg: 'lg:hidden'
  }
  return map[props.mobileBreakpoint]
})

const desktopBreakpointClass = computed(() => {
  const map = {
    sm: 'hidden sm:flex',
    md: 'hidden md:flex',
    lg: 'hidden lg:flex'
  }
  return map[props.mobileBreakpoint]
})

// 处理滚动
const handleScroll = () => {
  scrolled.value = window.scrollY > 10
}

// 监听滚动
onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

// 处理导航点击
const handleNavClick = (item: NavItem) => {
  emit('nav-click', item)
  if (item.href) {
    // 平滑滚动到锚点
    if (item.href.startsWith('#')) {
      const element = document.querySelector(item.href)
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' })
      }
    } else {
      window.location.href = item.href
    }
  }
  mobileMenuOpen.value = false
}

// 处理 Logo 点击
const handleLogoClick = () => {
  emit('logo-click')
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 切换移动端下拉菜单
const toggleMobileDropdown = (item: NavItem) => {
  item.open = !item.open
}

// 关闭移动端菜单
const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

// 监听窗口大小变化，自动关闭移动端菜单
const handleResize = () => {
  if (window.innerWidth >= 768) {
    mobileMenuOpen.value = false
  }
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <nav
    :class="cn(
      'w-full z-50 transition-all duration-300',
      variantClass,
      {
        'fixed top-0 left-0 right-0': props.fixed,
        'shadow-lg': props.shadow && scrolled,
        'shadow-md': props.shadow && !scrolled,
        'border-b': props.border,
        'border-b-border': props.border,
        'backdrop-blur-xl': props.variant === 'glass',
        'py-2': !scrolled,
        'py-1': scrolled,
      }
    )"
  >
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between">
        <!-- Logo 区域 -->
        <div 
          class="flex items-center gap-2 cursor-pointer group"
          @click="handleLogoClick"
        >
          <img 
            :src="props.logoUrl" 
            :alt="props.logoAlt"
            class="h-8 w-8 sm:h-10 sm:w-10 object-contain transition-transform duration-300 group-hover:scale-105"
          />
          <span 
            class="text-lg sm:text-xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent"
          >
            {{ props.brandName }}
          </span>
        </div>

        <!-- 桌面端导航 -->
        <div :class="cn('items-center gap-6', desktopBreakpointClass)">
          <template v-for="item in props.navItems" :key="item.label">
            <!-- 普通导航项 -->
            <div v-if="!item.children" class="relative group">
              <button
                @click="handleNavClick(item)"
                class="px-3 py-2 text-sm font-medium transition-all duration-200 rounded-lg hover:bg-primary/10 hover:text-primary"
              >
                <div class="flex items-center gap-2">
                  <component :is="item.icon" v-if="item.icon" class="h-4 w-4" />
                  {{ item.label }}
                </div>
              </button>
              <!-- 下划线动画 -->
              <div class="absolute bottom-0 left-0 w-0 h-0.5 bg-primary transition-all duration-300 group-hover:w-full" />
            </div>

            <!-- 带下拉菜单的导航项 -->
            <div v-else class="relative group">
              <button class="px-3 py-2 text-sm font-medium transition-all duration-200 rounded-lg hover:bg-primary/10">
                <div class="flex items-center gap-1">
                  {{ item.label }}
                  <svg class="w-4 h-4 transition-transform duration-200 group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </button>
              <div class="absolute top-full left-0 mt-2 w-48 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 transform -translate-y-2 group-hover:translate-y-0">
                <div class="bg-popover rounded-lg shadow-lg border overflow-hidden">
                  <button
                    v-for="child in item.children"
                    :key="child.label"
                    @click="handleNavClick(child)"
                    class="w-full text-left px-4 py-2 text-sm hover:bg-muted transition-colors flex items-center gap-2"
                  >
                    <component :is="child.icon" v-if="child.icon" class="h-4 w-4" />
                    {{ child.label }}
                  </button>
                </div>
              </div>
            </div>
          </template>
        </div>

        <!-- 右侧区域（插槽） -->
        <div class="hidden md:flex items-center gap-4">
          <slot name="right" />
        </div>

        <!-- 移动端菜单按钮 -->
        <button
          @click="mobileMenuOpen = !mobileMenuOpen"
          :class="cn(
            'p-2 rounded-lg transition-colors',
            mobileBreakpointClass,
            'hover:bg-primary/10'
          )"
        >
          <Menu v-if="!mobileMenuOpen" class="h-5 w-5" />
          <X v-else class="h-5 w-5" />
        </button>
      </div>

      <!-- 移动端菜单 -->
      <div
        v-if="mobileMenuOpen"
        :class="cn(
          'fixed inset-x-0 top-[57px] bg-background/95 backdrop-blur-xl z-40',
          'border-t shadow-lg'
        )"
      >
        <div class="container mx-auto px-4 py-4 space-y-2">
          <template v-for="item in props.navItems" :key="item.label">
            <!-- 普通导航项 -->
            <button
              v-if="!item.children"
              @click="handleNavClick(item)"
              class="w-full text-left px-4 py-3 text-base font-medium rounded-lg hover:bg-primary/10 transition-colors flex items-center gap-3"
            >
              <component :is="item.icon" v-if="item.icon" class="h-5 w-5" />
              {{ item.label }}
            </button>

            <!-- 带下拉菜单的导航项（移动端） -->
            <div v-else>
              <button
                @click="toggleMobileDropdown(item)"
                class="w-full text-left px-4 py-3 text-base font-medium rounded-lg hover:bg-primary/10 transition-colors flex items-center justify-between"
              >
                <span class="flex items-center gap-3">
                  <component :is="item.icon" v-if="item.icon" class="h-5 w-5" />
                  {{ item.label }}
                </span>
                <svg 
                  class="w-4 h-4 transition-transform" 
                  :class="{ 'rotate-180': item.open }" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              
              <!-- 下拉子菜单 -->
              <div v-if="item.open" class="ml-6 space-y-1 mt-2">
                <button
                  v-for="child in item.children"
                  :key="child.label"
                  @click="handleNavClick(child)"
                  class="w-full text-left px-4 py-2 text-sm rounded-lg hover:bg-primary/10 transition-colors flex items-center gap-3"
                >
                  <component :is="child.icon" v-if="child.icon" class="h-4 w-4" />
                  {{ child.label }}
                </button>
              </div>
            </div>
          </template>
          
          <!-- 移动端右侧插槽内容 -->
          <div class="pt-4 border-t">
            <slot name="mobile-right" />
          </div>
        </div>
      </div>
    </div>
  </nav>

  <!-- 占位元素（fixed 导航需要） -->
  <div v-if="props.fixed" class="h-16" />
</template>