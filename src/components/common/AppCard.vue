<!-- AppCard.vue -->
<script setup lang="ts">
import { computed } from 'vue'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { cn } from '@/lib/utils'

interface Props {
  // 卡片变体
  variant?: 'default' | 'glass' | 'outline' | 'elevated'
  
  // 圆角大小
  rounded?: 'none' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl'
  
  // 内边距大小
  padding?: 'none' | 'sm' | 'md' | 'lg' | 'xl'
  
  // 是否显示边框
  border?: boolean
  
  // 是否可悬停（hover 效果）
  hoverable?: boolean
  
  // 是否可点击
  clickable?: boolean
  
  // 加载状态
  loading?: boolean
  
  // 头部区域（可选）
  title?: string
  description?: string
  
  // 自定义类名
  class?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  rounded: '2xl',
  padding: 'md',
  border: false,
  hoverable: false,
  clickable: false,
  loading: false,
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

// 圆角类映射
const roundedClass = computed(() => {
  const map = {
    none: 'rounded-none',
    sm: 'rounded-sm',
    md: 'rounded-md',
    lg: 'rounded-lg',
    xl: 'rounded-xl',
    '2xl': 'rounded-2xl',
    '3xl': 'rounded-3xl'
  }
  return map[props.rounded]
})

// 内边距类映射
const paddingClass = computed(() => {
  const map = {
    none: 'p-0',
    sm: 'p-3',
    md: 'p-6',
    lg: 'p-8',
    xl: 'p-10'
  }
  return map[props.padding]
})

// 变体样式
const variantClass = computed(() => {
  const map = {
    default: 'bg-card shadow-md',
    glass: 'bg-white/10 backdrop-blur-xl shadow-lg',
    outline: 'bg-transparent border-2',
    elevated: 'bg-card shadow-xl hover:shadow-2xl transition-shadow'
  }
  return map[props.variant]
})

// 卡片主类
const cardClass = computed(() => {
  return cn(
    'relative', // 添加相对定位
    'transition-all duration-200',
    roundedClass.value,
    variantClass.value,
    {
      'border': props.border,
      'border-border': props.border,
      'border-none': !props.border,
      'cursor-pointer transition-all duration-200 hover:-translate-y-1 hover:shadow-xl': props.hoverable,
      'cursor-pointer active:scale-98': props.clickable,
    },
    props.class
  )
})

// 内容加载状态
const contentClass = computed(() => {
  return cn(
    paddingClass.value,
    {
      'opacity-50 pointer-events-none': props.loading
    }
  )
})

// 处理点击
const handleClick = (event: MouseEvent) => {
  if (props.clickable && !props.loading) {
    emit('click', event)
  }
}
</script>

<template>
  <Card 
    :class="cardClass"
    @click="handleClick"
  >
    <!-- 加载遮罩 -->
    <div 
      v-if="loading" 
      class="absolute inset-0 flex items-center justify-center bg-background/50 z-10"
      :class="roundedClass"
    >
      <div class="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
    </div>

    <!-- 头部（如果提供了 title 或 description） -->
    <CardHeader v-if="title || description" :class="paddingClass">
      <CardTitle v-if="title" class="text-xl font-semibold">
        {{ title }}
      </CardTitle>
      <CardDescription v-if="description" class="text-sm text-muted-foreground">
        {{ description }}
      </CardDescription>
    </CardHeader>

    <!-- 主要内容 -->
    <CardContent :class="contentClass">
      <slot />
    </CardContent>

    <!-- 底部插槽 -->
    <CardFooter v-if="$slots.footer" :class="paddingClass">
      <slot name="footer" />
    </CardFooter>
  </Card>
</template>