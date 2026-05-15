<template>
  <!-- variant: primary/secondary/outline/ghost/destructive/link/blue -->
  <!-- content -->
  <Button
    :variant="variant"
    :size="size"
    :disabled="disabled || loading"
    :as="as"
    :as-child="asChild"
    :class="buttonClass"
  >

    <span
      class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-75"
    >
      <span
        class="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-700 ease-out bg-gradient-to-r from-transparent via-white/25 to-transparent"
      />
    </span>

    <!-- content -->
    <span class="relative flex items-center justify-center gap-2">
      <Loader2
        v-if="loading"
        class="h-4 w-4 animate-spin"
      />

      <component
        :is="icon"
        v-else-if="icon && iconPosition === 'left'"
        class="h-4 w-4 transition-transform duration-200 group-hover:rotate-6"
      />

      <slot />

      <component
        :is="icon"
        v-if="icon && iconPosition === 'right' && !loading"
        class="h-4 w-4 transition-transform duration-200 group-hover:translate-x-1"
      />
    </span>
  </Button>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Loader2 } from '@lucide/vue'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import type { ButtonVariants } from '@/components/ui/button'

interface Props {
  variant?: ButtonVariants['variant'] | 'blue'  // 添加 'blue' 类型
  size?: ButtonVariants['size']
  as?: string
  asChild?: boolean

  loading?: boolean
  disabled?: boolean
  fullWidth?: boolean

  icon?: any
  iconPosition?: 'left' | 'right'

  rounded?: 'none' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full'

  glow?: boolean
  glass?: boolean
  animated?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  size: 'default',
  loading: false,
  disabled: false,
  fullWidth: false,
  iconPosition: 'left',
  rounded: '2xl',
  glow: false,
  glass: false,
  animated: true
})

const roundedClass = computed(() => {
  const map = {
    none: 'rounded-none',
    sm: 'rounded-sm',
    md: 'rounded-md',
    lg: 'rounded-lg',
    xl: 'rounded-xl',
    '2xl': 'rounded-2xl',
    full: 'rounded-full'
  }
  return map[props.rounded]
})

const widthClass = computed(() => {
  return props.fullWidth ? 'w-full' : ''
})

const buttonClass = computed(() => {
  return cn(
    'group relative overflow-hidden',
    roundedClass.value,
    widthClass.value,

    // base
    'font-medium tracking-wide',
    'transition-all duration-200 ease-out',
    'select-none',

    // interaction
    props.animated && [
      'hover:-translate-y-0.5',
      'hover:scale-[1.02]',
      'active:scale-[0.97]',
    ],

    // focus
    'focus-visible:outline-none',
    'focus-visible:ring-2',
    'focus-visible:ring-primary/50',
    'focus-visible:ring-offset-2',

    // disabled
    (props.disabled || props.loading) &&
      'cursor-not-allowed opacity-60',

    // glow
    props.glow &&
      !props.disabled &&
      'shadow-[0_0_25px_rgba(59,130,246,0.35)] hover:shadow-[0_0_35px_rgba(59,130,246,0.5)]',

    // glass
    props.glass && [
      'backdrop-blur-xl',
      'bg-white/10',
      'border border-white/20',
      'hover:bg-white/20',
      'hover:border-white/30'
    ],

    // blue variant
    props.variant === 'blue' && [
      'bg-gradient-to-r',
      'from-blue-600',
      'to-blue-500',
      'hover:from-blue-700',
      'hover:to-blue-600',
      'text-white',
      'shadow-md',
      'hover:shadow-lg',
      'hover:brightness-105',
      'border-none'
    ],

    // default variant enhancement
    props.variant === 'default' &&
      !props.glass && [
        'bg-gradient-to-r',
        'from-primary',
        'to-primary/80',
        'hover:brightness-105',
        'shadow-md',
        'hover:shadow-lg'
      ],

    // outline variant hover enhancement
    props.variant === 'outline' && [
      'hover:bg-primary/5',
      'hover:border-primary/50'
    ],

    // ghost variant hover enhancement
    props.variant === 'ghost' && [
      'hover:bg-primary/5'
    ]
  )
})
</script>