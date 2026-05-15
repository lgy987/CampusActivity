<!-- AppPageContainer.vue -->
<script setup lang="ts">
import { computed } from 'vue'
import { cn } from '@/lib/utils'

interface Props {
  // 背景变体
  variant?: 'light' | 'dark' | 'gradient' | 'particle' | 'wave'
  
  // 是否显示网格背景
  showGrid?: boolean
  
  // 是否显示光晕效果
  showGlow?: boolean
  
  // 内边距大小
  padding?: 'none' | 'sm' | 'md' | 'lg' | 'xl'
  
  // 最大宽度限制
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full'
  
  // 是否居中内容
  centered?: boolean
  
  // 是否显示滚动指示器
  showScrollIndicator?: boolean
  
  // 自定义类名
  class?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'gradient',
  showGrid: true,
  showGlow: true,
  padding: 'lg',
  maxWidth: '2xl',
  centered: true,
  showScrollIndicator: false
})

// 内边距类
const paddingClass = computed(() => {
  const map = {
    none: 'p-0',
    sm: 'p-4 sm:p-6',
    md: 'p-6 sm:p-8',
    lg: 'p-8 sm:p-10',
    xl: 'p-10 sm:p-12'
  }
  return map[props.padding]
})

// 最大宽度类
const maxWidthClass = computed(() => {
  const map = {
    sm: 'max-w-screen-sm',
    md: 'max-w-screen-md',
    lg: 'max-w-screen-lg',
    xl: 'max-w-screen-xl',
    '2xl': 'max-w-screen-2xl',
    full: 'max-w-full'
  }
  return map[props.maxWidth]
})

// 背景变体类
const variantClass = computed(() => {
  const map = {
    light: 'bg-gradient-to-br from-blue-50 to-indigo-100',
    dark: 'bg-gradient-to-br from-blue-900 to-indigo-950',
    gradient: 'bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800',
    particle: 'bg-gradient-to-br from-blue-500 to-purple-700',
    wave: 'bg-gradient-to-br from-cyan-500 via-blue-600 to-indigo-700'
  }
  return map[props.variant]
})

// 文字颜色
const textColorClass = computed(() => {
  if (props.variant === 'light') return 'text-gray-900'
  return 'text-white'
})
</script>

<template>
  <div 
    :class="cn(
      'relative min-h-screen w-full overflow-hidden',
      variantClass,
      textColorClass,
      props.class
    )"
  >
    <!-- 动态网格背景 -->
    <div 
      v-if="props.showGrid" 
      class="absolute inset-0"
      :class="{
        'bg-grid-white/10': props.variant !== 'light',
        'bg-grid-gray-900/10': props.variant === 'light'
      }"
    >
      <div class="absolute inset-0 bg-gradient-to-t from-transparent via-transparent to-black/20" />
    </div>

    <!-- 动态光晕效果 -->
    <div 
      v-if="props.showGlow" 
      class="absolute inset-0 overflow-hidden"
    >
      <div class="absolute -top-40 -right-40 h-80 w-80 rounded-full bg-blue-400/30 blur-3xl animate-pulse" />
      <div class="absolute -bottom-40 -left-40 h-80 w-80 rounded-full bg-indigo-400/30 blur-3xl animate-pulse delay-1000" />
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-96 w-96 rounded-full bg-cyan-400/20 blur-3xl animate-pulse delay-700" />
    </div>

    <!-- 运动粒子效果（仅在 particle 变体时显示） -->
    <div 
      v-if="props.variant === 'particle'" 
      class="absolute inset-0 overflow-hidden"
    >
      <div 
        v-for="i in 20" 
        :key="i"
        class="absolute h-1 w-1 rounded-full bg-white/40 animate-float"
        :style="{
          left: `${Math.random() * 100}%`,
          top: `${Math.random() * 100}%`,
          animationDelay: `${Math.random() * 5}s`,
          animationDuration: `${3 + Math.random() * 4}s`
        }"
      />
    </div>

    <!-- 波浪效果（仅在 wave 变体时显示） -->
    <div 
      v-if="props.variant === 'wave'" 
      class="absolute bottom-0 left-0 w-full overflow-hidden leading-[0]"
    >
      <svg
        class="relative block w-full h-[60px] sm:h-[100px]"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 1200 120"
        preserveAspectRatio="none"
      >
        <path 
          d="M0,64L80,69C160,75,320,85,480,80C640,75,800,53,960,48C1120,43,1280,53,1360,58.7L1440,64L1440,120L1360,120C1280,120,1120,120,960,120C800,120,640,120,480,120C320,120,160,120,80,120L0,120Z"
          fill="rgba(255,255,255,0.1)"
          class="animate-wave"
        />
        <path 
          d="M0,96L80,101.3C160,107,320,117,480,112C640,107,800,85,960,80C1120,75,1280,85,1360,90.7L1440,96L1440,120L1360,120C1280,120,1120,120,960,120C800,120,640,120,480,120C320,120,160,120,80,120L0,120Z"
          fill="rgba(255,255,255,0.15)"
          class="animate-wave-delay"
        />
      </svg>
    </div>

    <!-- 动态浮动圆点（装饰） -->
    <div class="absolute top-20 left-10 h-2 w-2 rounded-full bg-white/30 animate-float-delay" />
    <div class="absolute bottom-20 right-10 h-3 w-3 rounded-full bg-white/20 animate-float" />
    <div class="absolute top-1/3 right-1/4 h-1.5 w-1.5 rounded-full bg-white/40 animate-float-delay" />

    <!-- 主要内容容器 -->
    <div 
      :class="cn(
        'relative z-10 mx-auto',
        maxWidthClass,
        paddingClass,
        {
          'flex flex-col items-center justify-center min-h-screen': props.centered
        }
      )"
    >
      <!-- 可选的头部装饰 -->
      <div v-if="$slots.header" class="mb-8">
        <slot name="header" />
      </div>

      <!-- 主要内容 -->
      <slot />

      <!-- 可选的底部装饰 -->
      <div v-if="$slots.footer" class="mt-8">
        <slot name="footer" />
      </div>
    </div>

    <!-- 滚动指示器（可选） -->
    <div 
      v-if="props.showScrollIndicator" 
      class="absolute bottom-8 left-1/2 -translate-x-1/2 z-10 animate-bounce"
    >
      <div class="h-10 w-6 rounded-full border-2 border-white/50 flex justify-center">
        <div class="h-2 w-1 rounded-full bg-white/70 mt-1 animate-scroll" />
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 网格背景 */
.bg-grid-white\/10 {
  background-image: linear-gradient(to right, rgba(255,255,255,0.1) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(255,255,255,0.1) 1px, transparent 1px);
  background-size: 50px 50px;
}

.bg-grid-gray-900\/10 {
  background-image: linear-gradient(to right, rgba(0,0,0,0.05) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(0,0,0,0.05) 1px, transparent 1px);
  background-size: 50px 50px;
}

/* 动画效果 */
@keyframes float {
  0%, 100% {
    transform: translateY(0px) translateX(0px);
    opacity: 0;
  }
  50% {
    transform: translateY(-20px) translateX(10px);
    opacity: 0.8;
  }
}

@keyframes float-delay {
  0%, 100% {
    transform: translateY(0px) translateX(0px);
    opacity: 0;
  }
  50% {
    transform: translateY(-15px) translateX(-10px);
    opacity: 0.6;
  }
}

@keyframes wave {
  0% {
    transform: translateX(0) translateY(0);
  }
  50% {
    transform: translateX(-10%) translateY(3px);
  }
  100% {
    transform: translateX(0) translateY(0);
  }
}

@keyframes wave-delay {
  0% {
    transform: translateX(0) translateY(0);
  }
  50% {
    transform: translateX(10%) translateY(-3px);
  }
  100% {
    transform: translateX(0) translateY(0);
  }
}

@keyframes scroll {
  0% {
    transform: translateY(0);
    opacity: 1;
  }
  100% {
    transform: translateY(20px);
    opacity: 0;
  }
}

.animate-float {
  animation: float 4s ease-in-out infinite;
}

.animate-float-delay {
  animation: float-delay 5s ease-in-out infinite;
}

.animate-wave {
  animation: wave 8s ease-in-out infinite;
}

.animate-wave-delay {
  animation: wave-delay 8s ease-in-out infinite;
}

.animate-scroll {
  animation: scroll 1.5s ease-in-out infinite;
}

/* 脉冲动画优化 */
@keyframes pulse {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(1.05);
  }
}

.animate-pulse {
  animation: pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.delay-1000 {
  animation-delay: 1s;
}

.delay-700 {
  animation-delay: 0.7s;
}
</style>