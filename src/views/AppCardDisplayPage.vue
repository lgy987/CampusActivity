<!-- AppCardDisplayPage.vue - 完整展示页面 -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-950 p-8">
    <div class="mx-auto max-w-7xl">
      <!-- 页面标题 -->
      <div class="mb-8 text-center">
        <h1 class="text-4xl font-bold mb-2">AppCard 组件演示</h1>
      </div>

      <!-- 1. 基础用法 -->
      <section class="mb-12">
        <p class="text-lg font-semibold mb-3">1. 基础用法</p>
        <p class="text-sm text-muted-foreground mb-4">&lt;AppCard&gt;</p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <AppCard>
            <div class="text-center py-6">
              <div class="text-4xl mb-2">📝</div>
              <h3 class="font-semibold mb-1">基础卡片</h3>
              <p class="text-sm text-muted-foreground">最简单的使用方式</p>
            </div>
          </AppCard>

          <AppCard variant="outline">
            <div class="text-center py-6">
              <div class="text-4xl mb-2">🎨</div>
              <h3 class="font-semibold mb-1">边框卡片</h3>
              <p class="text-sm text-muted-foreground">带边框样式</p>
            </div>
          </AppCard>

          <AppCard variant="glass">
            <div class="text-center py-6">
              <div class="text-4xl mb-2">✨</div>
              <h3 class="font-semibold mb-1">毛玻璃卡片</h3>
              <p class="text-sm text-muted-foreground">现代化毛玻璃效果</p>
            </div>
          </AppCard>
        </div>
      </section>

      <!-- 2. 不同圆角 -->
      <section class="mb-12">
        <p class="text-lg font-semibold mb-3">2. 不同圆角</p>
        <p class="text-sm text-muted-foreground mb-4">&lt;AppCard rounded="..."&gt;</p>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div>
            <p class="text-sm text-muted-foreground mb-2">none</p>
            <AppCard rounded="none">
              <div class="text-center py-4 text-sm">rounded-none</div>
            </AppCard>
          </div>
          <div>
            <p class="text-sm text-muted-foreground mb-2">md</p>
            <AppCard rounded="md">
              <div class="text-center py-4 text-sm">rounded-md</div>
            </AppCard>
          </div>
          <div>
            <p class="text-sm text-muted-foreground mb-2">2xl</p>
            <AppCard rounded="2xl">
              <div class="text-center py-4 text-sm">rounded-2xl</div>
            </AppCard>
          </div>
          <div>
            <p class="text-sm text-muted-foreground mb-2">3xl</p>
            <AppCard rounded="3xl">
              <div class="text-center py-4 text-sm">rounded-3xl</div>
            </AppCard>
          </div>
        </div>
      </section>

      <!-- 3. 悬停效果 -->
      <section class="mb-12">
        <p class="text-lg font-semibold mb-3">3. 悬停效果</p>
        <p class="text-sm text-muted-foreground mb-4">&lt;AppCard hoverable&gt;</p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <AppCard hoverable>
            <div class="text-center py-6">
              <div class="text-3xl mb-2">🖱️</div>
              <h3 class="font-semibold">悬停上浮</h3>
              <p class="text-sm text-muted-foreground mt-1">鼠标悬停时卡片上浮</p>
            </div>
          </AppCard>

          <AppCard variant="elevated">
            <div class="text-center py-6">
              <div class="text-3xl mb-2">📦</div>
              <h3 class="font-semibold">高级阴影</h3>
              <p class="text-sm text-muted-foreground mt-1">自带阴影增强效果</p>
            </div>
          </AppCard>

          <AppCard clickable @click="handleCardClick">
            <div class="text-center py-6">
              <div class="text-3xl mb-2">👆</div>
              <h3 class="font-semibold">可点击卡片</h3>
              <p class="text-sm text-muted-foreground mt-1">点击触发事件</p>
            </div>
          </AppCard>
        </div>
      </section>

      <!-- 4. 带标题和描述 -->
      <section class="mb-12">
        <p class="text-lg font-semibold mb-3">4. 带标题和描述</p>
        <p class="text-sm text-muted-foreground mb-4">&lt;AppCard title="..." description="..."&gt;</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <AppCard 
            title="用户信息" 
            description="查看和编辑个人资料"
          >
            <div class="space-y-3">
              <div class="flex items-center justify-between py-2 border-b">
                <span class="text-sm text-muted-foreground">用户名</span>
                <span class="font-medium">张三</span>
              </div>
              <div class="flex items-center justify-between py-2 border-b">
                <span class="text-sm text-muted-foreground">邮箱</span>
                <span class="font-medium">zhangsan@example.com</span>
              </div>
              <div class="flex items-center justify-between py-2">
                <span class="text-sm text-muted-foreground">角色</span>
                <span class="font-medium">管理员</span>
              </div>
            </div>
          </AppCard>

          <AppCard 
            title="最近活动" 
            description="过去7天的数据统计"
          >
            <div class="space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-sm">页面访问量</span>
                <span class="font-semibold text-primary">12,345</span>
              </div>
              <div class="h-2 bg-secondary rounded-full overflow-hidden">
                <div class="h-full w-3/4 bg-primary rounded-full"></div>
              </div>
              <div class="flex justify-between items-center mt-3">
                <span class="text-sm">新增用户</span>
                <span class="font-semibold text-primary">+128</span>
              </div>
              <div class="h-2 bg-secondary rounded-full overflow-hidden">
                <div class="h-full w-1/2 bg-primary rounded-full"></div>
              </div>
            </div>
          </AppCard>
        </div>
      </section>

      <!-- 5. 加载状态 -->
      <section class="mb-12">
        <p class="text-lg font-semibold mb-3">5. 加载状态</p>
        <p class="text-sm text-muted-foreground mb-4">&lt;AppCard loading&gt;</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <AppCard loading>
            <div class="text-center py-8">
              <p class="text-muted-foreground">内容加载中...</p>
            </div>
          </AppCard>

          <AppCard :loading="isLoading">
            <div class="text-center py-8">
              <div v-if="!isLoading">
                <p class="mb-3 text-muted-foreground">点击下方按钮体验加载效果</p>
                <p class="text-sm text-muted-foreground mb-3">加载时内容会被遮盖</p>
              </div>
              <AppButton size="sm" @click="toggleLoading">
                {{ isLoading ? '加载中...' : '开始加载' }}
              </AppButton>
            </div>
          </AppCard>
        </div>
      </section>

      <!-- 6. 复杂内容展示 -->
      <section class="mb-12">
        <p class="text-lg font-semibold mb-3">6. 复杂内容展示</p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- 用户卡片 -->
          <AppCard hoverable class="text-center">
            <div class="flex flex-col items-center py-4">
              <div class="w-20 h-20 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white text-2xl mb-3">
                👤
              </div>
              <h3 class="font-semibold text-lg">Alex Johnson</h3>
              <p class="text-sm text-muted-foreground">产品设计师</p>
              <div class="flex gap-2 mt-3">
                <span class="px-2 py-1 bg-secondary rounded-full text-xs">UI/UX</span>
                <span class="px-2 py-1 bg-secondary rounded-full text-xs">Figma</span>
              </div>
            </div>
          </AppCard>

          <!-- 统计数据卡片 -->
          <AppCard variant="elevated">
            <div class="flex items-center justify-between py-2">
              <div>
                <p class="text-sm text-muted-foreground">总收入</p>
                <p class="text-2xl font-bold">$48,293</p>
                <p class="text-xs text-green-600 mt-1">↑ 14% 较上周</p>
              </div>
              <div class="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center text-xl">
                💰
              </div>
            </div>
          </AppCard>

          <!-- 带底部按钮的卡片 -->
          <AppCard hoverable>
            <div class="space-y-3 py-2">
              <h3 class="font-semibold">升级到专业版</h3>
              <p class="text-sm text-muted-foreground">
                解锁所有高级功能，获得更好的使用体验。
              </p>
              <AppButton size="sm" fullWidth>立即升级</AppButton>
            </div>
          </AppCard>
        </div>
      </section>

      <!-- 7. 带底部插槽 -->
      <section class="mb-12">
        <p class="text-lg font-semibold mb-3">7. 带底部插槽</p>
        <p class="text-sm text-muted-foreground mb-4">&lt;template #footer&gt;...&lt;/template&gt;</p>
        <AppCard>
          <div class="space-y-2 py-2">
            <p class="text-sm">这是卡片的主要内容区域</p>
            <p class="text-xs text-muted-foreground">你可以在这里放置任何内容</p>
          </div>
          <template #footer>
            <div class="flex justify-between items-center pt-3 border-t">
              <span class="text-xs text-muted-foreground">更新于 2 分钟前</span>
              <AppButton size="sm" variant="outline">查看详情</AppButton>
            </div>
          </template>
        </AppCard>
      </section>

      <!-- 8. 组合展示 -->
      <section>
        <p class="text-lg font-semibold mb-3">8. 组合展示 - 仪表板风格</p>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <AppCard class="text-center" hoverable>
            <div class="py-4">
              <div class="text-2xl font-bold text-primary">1,234</div>
              <div class="text-sm text-muted-foreground">总用户数</div>
            </div>
          </AppCard>
          <AppCard class="text-center" hoverable>
            <div class="py-4">
              <div class="text-2xl font-bold text-green-600">+23%</div>
              <div class="text-sm text-muted-foreground">增长率</div>
            </div>
          </AppCard>
          <AppCard class="text-center" hoverable>
            <div class="py-4">
              <div class="text-2xl font-bold text-blue-600">$12.4k</div>
              <div class="text-sm text-muted-foreground">总收入</div>
            </div>
          </AppCard>
          <AppCard class="text-center" hoverable>
            <div class="py-4">
              <div class="text-2xl font-bold text-purple-600">89%</div>
              <div class="text-sm text-muted-foreground">满意度</div>
            </div>
          </AppCard>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AppCard from '@/components/common/AppCard.vue'
import AppButton from '@/components/common/AppButton.vue'

const isLoading = ref(false)

const handleCardClick = () => {
  alert('卡片被点击了！')
}

const toggleLoading = () => {
  isLoading.value = !isLoading.value
  
  // 模拟3秒后自动关闭加载
  if (isLoading.value) {
    setTimeout(() => {
      isLoading.value = false
    }, 3000)
  }
}
</script>