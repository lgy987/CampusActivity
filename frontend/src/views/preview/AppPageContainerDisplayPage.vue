<!-- AppPageContainerDisplay.vue -->
<template>
  <div class="min-h-screen p-8">
    <div class="mx-auto max-w-7xl">
      <!-- 页面标题 -->
      <div class="mb-8 text-center">
        <h1 class="text-4xl font-bold mb-2">AppPageContainer 组件演示</h1>
        <p class="text-muted-foreground">功能丰富的页面容器，支持多种背景样式、网格背景和光晕效果</p>
      </div>

      <!-- 1. 基础变体 -->
      <section class="mb-12">
        <p class="text-lg font-semibold mb-3">1. 基础变体</p>
        <p class="text-sm text-muted-foreground mb-4">&lt;AppPageContainer variant="..."&gt;</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Light 变体 -->
          <div>
            <p class="text-sm font-medium mb-2">light</p>
            <AppPageContainer variant="light" class="h-64 rounded-xl overflow-hidden">
              <div class="flex items-center justify-center h-full">
                <p class="text-gray-900">浅色渐变背景</p>
              </div>
            </AppPageContainer>
          </div>

          <!-- Dark 变体 -->
          <div>
            <p class="text-sm font-medium mb-2">dark</p>
            <AppPageContainer variant="dark" class="h-64 rounded-xl overflow-hidden">
              <div class="flex items-center justify-center h-full">
                <p class="text-white">深色渐变背景</p>
              </div>
            </AppPageContainer>
          </div>

          <!-- Gradient 变体 -->
          <div>
            <p class="text-sm font-medium mb-2">gradient</p>
            <AppPageContainer variant="gradient" class="h-64 rounded-xl overflow-hidden">
              <div class="flex items-center justify-center h-full">
                <p class="text-white">蓝紫渐变背景</p>
              </div>
            </AppPageContainer>
          </div>

          <!-- Particle 变体 -->
          <div>
            <p class="text-sm font-medium mb-2">particle</p>
            <AppPageContainer variant="particle" class="h-64 rounded-xl overflow-hidden">
              <div class="flex items-center justify-center h-full">
                <p class="text-white">粒子动画背景</p>
              </div>
            </AppPageContainer>
          </div>

          <!-- Wave 变体 -->
          <div class="md:col-span-2">
            <p class="text-sm font-medium mb-2">wave</p>
            <AppPageContainer variant="wave" class="h-64 rounded-xl overflow-hidden">
              <div class="flex items-center justify-center h-full">
                <p class="text-white">波浪动画背景</p>
              </div>
            </AppPageContainer>
          </div>
        </div>
      </section>

      <!-- 2. 网格背景 -->
      <section class="mb-12">
        <p class="text-lg font-semibold mb-3">2. 网格背景</p>
        <p class="text-sm text-muted-foreground mb-4">&lt;AppPageContainer showGrid&gt;</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <p class="text-sm font-medium mb-2">showGrid="true" (默认)</p>
            <AppPageContainer variant="gradient" showGrid class="h-64 rounded-xl overflow-hidden">
              <div class="flex items-center justify-center h-full">
                <p class="text-white text-center">显示网格背景<br>网格线点缀</p>
              </div>
            </AppPageContainer>
          </div>

          <div>
            <p class="text-sm font-medium mb-2">showGrid="false"</p>
            <AppPageContainer variant="gradient" :showGrid="false" class="h-64 rounded-xl overflow-hidden">
              <div class="flex items-center justify-center h-full">
                <p class="text-white text-center">无网格背景<br>纯净渐变</p>
              </div>
            </AppPageContainer>
          </div>
        </div>
      </section>

      <!-- 3. 光晕效果 -->
      <section class="mb-12">
        <p class="text-lg font-semibold mb-3">3. 光晕效果</p>
        <p class="text-sm text-muted-foreground mb-4">&lt;AppPageContainer showGlow&gt;</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <p class="text-sm font-medium mb-2">showGlow="true" (默认)</p>
            <AppPageContainer variant="light" showGlow class="h-64 rounded-xl overflow-hidden">
              <div class="flex items-center justify-center h-full">
                <p class="text text-center">显示光晕效果<br>彩色发光圆球</p>
              </div>
            </AppPageContainer>
          </div>

          <div>
            <p class="text-sm font-medium mb-2">showGlow="false"</p>
            <AppPageContainer variant="light" :showGlow="false" class="h-64 rounded-xl overflow-hidden">
              <div class="flex items-center justify-center h-full">
                <p class="text text-center">无光晕效果<br>简洁背景</p>
              </div>
            </AppPageContainer>
          </div>
        </div>
      </section>

      <!-- 4. 滚动指示器 -->
      <section class="mb-12">
        <p class="text-lg font-semibold mb-3">4. 滚动指示器</p>
        <p class="text-sm text-muted-foreground mb-4">&lt;AppPageContainer showScrollIndicator&gt;</p>
        <AppPageContainer variant="dark" showGrid showScrollIndicator class="h-96 rounded-xl overflow-y-auto">
          <div class="py-12 px-6 text-center text-white">
            <h2 class="text-2xl font-bold mb-4">滚动指示器演示</h2>
            <div class="space-y-4">
              <p>向下滚动查看指示器效果</p>
              <div class="h-32 bg-white/10 rounded-lg flex items-center justify-center">
                内容区域 1
              </div>
              <div class="h-32 bg-white/10 rounded-lg flex items-center justify-center">
                内容区域 2
              </div>
              <div class="h-32 bg-white/10 rounded-lg flex items-center justify-center">
                内容区域 3
              </div>
              <div class="h-32 bg-white/10 rounded-lg flex items-center justify-center">
                内容区域 4
              </div>
            </div>
          </div>
        </AppPageContainer>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppPageContainer from '@/components/layout/AppPageContainer.vue'
</script>