<script setup lang="ts">
import { AppButton } from '@/components/common'

import { ref } from 'vue'
import { Settings, ArrowRight } from '@lucide/vue'

const isSubmitting = ref(false)
const saving = ref(false)

const someAsyncTask = () => {
  return new Promise(resolve => setTimeout(resolve, 3000))
}

const handleSubmit = async () => {
  isSubmitting.value = true
  await someAsyncTask()
  isSubmitting.value = false
}

const handleNavClick = (item: { href?: string }) => {
  console.log('导航点击:', item)
  // 你的自定义逻辑
}
</script>

<template>
  <!-- 按钮 -->
  <!-- 页面标题 -->
  <div class="min-h-screen p-8">
  <div class="mx-auto max-w-7xl">
  <div class="mb-8 text-center">
    <h1 class="text-4xl font-bold mb-2">AppButton 组件演示</h1>
  </div>
   
  <section class="mb-12">
  <p class="text-lg font-semibold mb-3"> 1. 基础用法 </p>
  <p>&ltAppButton&gt</p>
  <AppButton>按钮</AppButton>
  </section>

  <section class="mb-12">
  <p class="text-lg font-semibold mb-3"> 2. Loading 状态 </p>
  <p>&ltAppButton :loading = false&gt点击变为loading=true</p>
  <AppButton :loading="isSubmitting" @click="handleSubmit">
    登录
  </AppButton>
  </section>

  <section class="mb-12">
  <p class="text-lg font-semibold mb-3"> 3. 不同变体 </p>
  <p>&ltAppButton variant="..."&gt</p>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
  <div><p>blue</p><AppButton variant="blue">蓝色按钮</AppButton></div>
  <div><p>link</p><AppButton variant="link">链接</AppButton></div>
  <div><p>destructive</p><AppButton variant="destructive">删除</AppButton></div>
  <div><p>outline</p><AppButton variant="outline">取消</AppButton></div>
  <div><p>ghost</p><AppButton variant="ghost">更多</AppButton></div>
  <div><p>secondary</p><AppButton variant="secondary">草稿</AppButton></div>
  </div>
  </section>

  <section class="mb-12">
  <p class="text-lg font-semibold mb-3"> 4. 不同尺寸 </p>
  <p>&ltAppButton size="..."&gt</p>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
    <div>
      <p>sm</p>
      <AppButton size="sm">小按钮</AppButton>
    </div>
    <div>
      <p>lg</p>
      <AppButton size="lg">大按钮</AppButton>
    </div>
    <div>
      <p>icon</p>
      <AppButton size="icon">
        <Settings class="h-4 w-4" />
      </AppButton>
    </div>
  </div>
  </section>

  <section class="mb-12">
  <p class="text-lg font-semibold mb-3"> 5. 完整宽度 </p>
  <p>&ltAppButton fullWidth&gt</p>
  <AppButton fullWidth>提交订单</AppButton>
  </section>

  <section class="mb-12">
  <p class="text-lg font-semibold mb-3"> 6. 带图标 </p>
  <p>&ltAppButton :icon="..."&gt icon来自lucide库</p>
  <AppButton 
    :icon="ArrowRight" 
    icon-position="right"
  >
    下一步
  </AppButton>
  </section>

  <section class="mb-12">
  <p class="text-lg font-semibold mb-3"> 7. 不同圆角 </p>
  <p>&ltAppButton rounded="..."&gt</p>
  <p>none</p>
  <AppButton rounded="none">方角按钮</AppButton>
  <p>full</p>
  <AppButton rounded="full">圆形按钮</AppButton>
  </section>

  </div>
  </div>

</template>