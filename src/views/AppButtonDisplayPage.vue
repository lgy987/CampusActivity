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
  <div class="mb-8 text-center">
    <h1 class="text-4xl font-bold mb-2">AppButton 组件演示</h1>
  </div>
   
  <p> 1. 基础用法 </p>
  <p>&ltAppButton&gt</p>
  <AppButton>按钮</AppButton>

  <p> 2. Loading 状态 </p>
  <p>&ltAppButton :loading = false&gt点击变为loading=true</p>
  <AppButton :loading="isSubmitting" @click="handleSubmit">
    登录
  </AppButton>

  <p> 3. 不同变体 </p>
  <p>&ltAppButton variant="..."&gt</p>
  <p>blue</p><AppButton variant="blue">蓝色按钮</AppButton>
  <p>link</p><AppButton variant="link">链接</AppButton>
  <p>destructive</p><AppButton variant="destructive">删除</AppButton>
  <p>outline</p><AppButton variant="outline">取消</AppButton>
  <p>ghost</p><AppButton variant="ghost">更多</AppButton>
  <p>secondary</p><AppButton variant="secondary">草稿</AppButton>

  <p> 4. 不同尺寸 </p>
  <p>&ltAppButton size="..."&gt</p>
  <p>sm</p>
  <AppButton size="sm">小按钮</AppButton>
  <p>lg</p>
  <AppButton size="lg">大按钮</AppButton>
  <p>icon</p>
  <AppButton size="icon">
    <Settings class="h-4 w-4" />
  </AppButton>

  <p> 5. 完整宽度 </p>
  <p>&ltAppButton fullWidth&gt</p>
  <AppButton fullWidth>提交订单</AppButton>

  <p> 6. 带图标 </p>
  <p>&ltAppButton :icon="..."&gt icon来自lucide库</p>
  <AppButton 
    :icon="ArrowRight" 
    icon-position="right"
  >
    下一步
  </AppButton>

  <p> 7. 不同圆角 </p>
  <p>&ltAppButton rounded="..."&gt</p>
  <p>none</p>
  <AppButton rounded="none">方角按钮</AppButton>
  <p>full</p>
  <AppButton rounded="full">圆形按钮</AppButton>

</template>