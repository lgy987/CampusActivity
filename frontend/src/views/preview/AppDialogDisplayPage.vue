<!-- AppDialogDisplay.vue -->
<template>
  <div class="min-h-screen p-8">
    <div class="mx-auto max-w-7xl">
      <!-- 页面标题 -->
      <div class="mb-8 text-center">
        <h1 class="text-4xl font-bold mb-2">AppDialog 组件演示</h1>
        <p class="text-muted-foreground">功能丰富的对话框封装，支持多种尺寸、按钮变体和交互方式</p>
      </div>

      <!-- 1. 基础用法 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">1. 基础用法</p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <p class="text-sm font-medium mb-1">基础对话框</p>
            <p class="text-sm text-muted-foreground mb-3">&lt;AppDialog title="..." description="..."&gt;</p>
            <AppDialog 
              title="基础对话框" 
              description="这是一个简单的对话框示例"
            >
              <template #trigger>
                <AppButton variant="outline" size="sm" class="w-full">打开基础对话框</AppButton>
              </template>
              <p class="text-sm text-muted-foreground">这里是对话框的内容区域，可以放置任何内容。</p>
            </AppDialog>
          </div>

          <div>
            <p class="text-sm font-medium mb-1">自定义头部</p>
            <p class="text-sm text-muted-foreground mb-3">&lt;template #header /&gt;</p>
            <AppDialog>
              <template #trigger>
                <AppButton variant="outline" size="sm" class="w-full">自定义头部</AppButton>
              </template>
              <template #header>
                <div class="flex items-center gap-2">
                  <div class="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-lg">
                    🎉
                  </div>
                  <div>
                    <h2 class="text-lg font-semibold">自定义头部</h2>
                    <p class="text-xs text-muted-foreground">这是自定义的头部内容</p>
                  </div>
                </div>
              </template>
              <p class="text-sm">完全自定义头部内容的对话框。</p>
            </AppDialog>
          </div>

          <div>
            <p class="text-sm font-medium mb-1">自定义底部</p>
            <p class="text-sm text-muted-foreground mb-3">&lt;template #header /&gt;</p>
            <AppDialog title="自定义底部按钮">
              <template #trigger>
                <AppButton variant="outline" size="sm" class="w-full">自定义底部</AppButton>
              </template>
              <template #footer>
                <div class="flex justify-between w-full">
                  <AppButton variant="ghost" size="sm">帮助</AppButton>
                  <div class="flex gap-2">
                    <AppButton variant="outline" size="sm">取消</AppButton>
                    <AppButton variant="default" size="sm">确认</AppButton>
                  </div>
                </div>
              </template>
              <p class="text-sm">完全自定义底部按钮区域的对话框。</p>
            </AppDialog>
          </div>
        </div>
      </section>

      <!-- 2. 不同尺寸 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">2. 不同尺寸</p>
        <p class="text-sm text-muted-foreground mb-3">&lt;AppDialog size="..."&gt;</p>
        <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
          <div>
            <p class="text-sm font-medium mb-1">sm</p>
            <AppDialog title="小尺寸对话框" size="sm">
              <template #trigger>
                <AppButton variant="outline" size="sm" class="w-full">sm</AppButton>
              </template>
              <p class="text-sm">小尺寸对话框，适合简单内容。</p>
            </AppDialog>
          </div>

          <div>
            <p class="text-sm font-medium mb-1">md</p>
            <AppDialog title="中等尺寸对话框" size="md">
              <template #trigger>
                <AppButton variant="outline" size="sm" class="w-full">md</AppButton>
              </template>
              <p class="text-sm">中等尺寸对话框（默认），适合常规内容。</p>
            </AppDialog>
          </div>

          <div>
            <p class="text-sm font-medium mb-1">lg</p>
            <AppDialog title="大尺寸对话框" size="lg">
              <template #trigger>
                <AppButton variant="outline" size="sm" class="w-full">lg</AppButton>
              </template>
              <p class="text-sm">大尺寸对话框，适合较多内容。</p>
            </AppDialog>
          </div>

          <div>
            <p class="text-sm font-medium mb-1">xl</p>
            <AppDialog title="超大尺寸对话框" size="xl">
              <template #trigger>
                <AppButton variant="outline" size="sm" class="w-full">xl</AppButton>
              </template>
              <p class="text-sm">超大尺寸对话框，适合复杂表单。</p>
            </AppDialog>
          </div>

          <div>
            <p class="text-sm font-medium mb-1">full</p>
            <AppDialog title="全屏尺寸" size="full">
              <template #trigger>
                <AppButton variant="outline" size="sm" class="w-full">full</AppButton>
              </template>
              <div class="space-y-3">
                <p class="text-sm">全屏尺寸对话框，适合大型内容展示。</p>
                <div class="grid grid-cols-2 gap-3">
                  <div class="h-24 bg-secondary rounded-lg flex items-center justify-center text-sm">区块 1</div>
                  <div class="h-24 bg-secondary rounded-lg flex items-center justify-center text-sm">区块 2</div>
                </div>
              </div>
            </AppDialog>
          </div>
        </div>
      </section>

      <!-- 3. 按钮变体 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">3. 按钮变体</p>
        <p class="text-sm text-muted-foreground mb-3">&lt;AppDialog confirmText="..." confirmVariant="..." cancelText="..." cancelVariant="..."&gt;</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p class="text-sm font-medium mb-1">危险操作</p>
            <p class="text-sm text-muted-foreground mb-3">&lt;AppDialog confirmVariant = "destructive"&gt;</p>
            <AppDialog 
              title="危险操作" 
              description="此操作不可撤销，请谨慎操作。"
              confirmText="删除"
              confirmVariant="destructive"
            >
              <template #trigger>
                <AppButton variant="destructive" size="sm" class="w-full">危险对话框</AppButton>
              </template>
              <p class="text-sm">确认删除这个项目吗？</p>
            </AppDialog>
          </div>

          <div>
            <p class="text-sm font-medium mb-1">蓝色主题</p>
            <p class="text-sm text-muted-foreground mb-3">&lt;AppDialog confirmVariant = "blue"&gt;</p>
            <AppDialog 
              title="蓝色主题对话框" 
              confirmVariant="blue"
              confirmText="确认"
            >
              <template #trigger>
                <AppButton variant="blue" size="sm" class="w-full">蓝色主题</AppButton>
              </template>
              <p class="text-sm">使用蓝色按钮的对话框。</p>
            </AppDialog>
          </div>
        </div>
      </section>

      <!-- 4. 交互控制 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">4. 交互控制</p>
        <p class="text-sm text-muted-foreground mb-3">控制关闭行为和加载状态</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p class="text-sm font-medium mb-1">禁止点击外部关闭</p>
            <p class="text-sm text-muted-foreground mb-3">&lt;AppDialog :close-on-click-outside="false"&gt;</p>
            <AppDialog 
              title="点击外部不关闭" 
              :close-on-click-outside="false"
              confirmText="确定"
            >
              <template #trigger>
                <AppButton variant="outline" size="sm" class="w-full">禁止外部关闭</AppButton>
              </template>
              <p class="text-sm">点击对话框外部不会关闭，必须点击按钮才能关闭。</p>
            </AppDialog>
          </div>

          <div>
            <p class="text-sm font-medium mb-1">异步加载</p>
            <p class="text-sm text-muted-foreground mb-3">&lt;AppDialog :confirm-loading="loadingStates.dialog1"&gt;</p>
            <AppDialog 
              title="异步操作" 
              description="点击确认后模拟3秒异步操作"
              confirmText="提交"
              :confirm-loading="loadingStates.dialog1"
              @confirm="() => handleAsyncConfirm('dialog1')"
            >
              <template #trigger>
                <AppButton variant="outline" size="sm" class="w-full">异步加载</AppButton>
              </template>
              <p class="text-sm">点击确认按钮后会出现加载状态，3秒后自动关闭。</p>
            </AppDialog>
          </div>
        </div>
      </section>

      <!-- 5. 表单对话框 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">5. 表单示例</p>
        <p class="text-sm text-muted-foreground mb-3">配合表单使用</p>
        <div>
          <AppDialog 
            title="编辑用户信息" 
            description="修改用户的个人信息"
            confirmText="保存"
            @confirm="handleFormSubmit"
          >
            <template #trigger>
              <AppButton variant="default" size="sm" class="w-full md:w-auto">打开表单对话框</AppButton>
            </template>
            <div class="space-y-4">
              <div>
                <label class="text-sm font-medium mb-1 block">用户名</label>
                <input 
                  v-model="formData.username"
                  type="text" 
                  class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                  placeholder="请输入用户名"
                >
              </div>
              <div>
                <label class="text-sm font-medium mb-1 block">邮箱</label>
                <input 
                  v-model="formData.email"
                  type="email" 
                  class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                  placeholder="请输入邮箱"
                >
              </div>
              <div>
                <label class="text-sm font-medium mb-1 block">角色</label>
                <select 
                  v-model="formData.role"
                  class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="admin">管理员</option>
                  <option value="user">普通用户</option>
                  <option value="guest">访客</option>
                </select>
              </div>
            </div>
          </AppDialog>
        </div>
      </section>

      <!-- 6. 复杂内容 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">6. 复杂内容示例</p>
        <p class="text-sm text-muted-foreground mb-3">展示统计图表等复杂内容</p>
        <div>
          <AppDialog title="详细统计信息" size="lg">
            <template #trigger>
              <AppButton variant="outline" size="sm">查看统计详情</AppButton>
            </template>
            <div class="space-y-4">
              <div class="grid grid-cols-3 gap-3">
                <div class="text-center p-3 bg-secondary rounded-lg">
                  <div class="text-xl font-bold text-primary">1,234</div>
                  <div class="text-xs text-muted-foreground">总访问量</div>
                </div>
                <div class="text-center p-3 bg-secondary rounded-lg">
                  <div class="text-xl font-bold text-green-600">+23%</div>
                  <div class="text-xs text-muted-foreground">增长率</div>
                </div>
                <div class="text-center p-3 bg-secondary rounded-lg">
                  <div class="text-xl font-bold text-blue-600">89%</div>
                  <div class="text-xs text-muted-foreground">满意度</div>
                </div>
              </div>
              <div class="border-t pt-3">
                <h4 class="font-semibold text-sm mb-2">详细数据</h4>
                <div class="space-y-2">
                  <div class="flex justify-between text-sm">
                    <span class="text-muted-foreground">昨日访问</span>
                    <span class="font-medium">456</span>
                  </div>
                  <div class="flex justify-between text-sm">
                    <span class="text-muted-foreground">今日访问</span>
                    <span class="font-medium">789</span>
                  </div>
                  <div class="flex justify-between text-sm">
                    <span class="text-muted-foreground">平均停留时间</span>
                    <span class="font-medium">3分42秒</span>
                  </div>
                </div>
              </div>
            </div>
          </AppDialog>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import AppDialog from '@/components/layout/AppDialog.vue'
import AppButton from '@/components/common/AppButton.vue'

// 表单数据
const formData = reactive({
  username: '张三',
  email: 'zhangsan@example.com',
  role: 'admin'
})

// 加载状态
const loadingStates = reactive({
  dialog1: false
})

// 异步确认
const handleAsyncConfirm = (key: string) => {
  loadingStates[key as keyof typeof loadingStates] = true
  setTimeout(() => {
    loadingStates[key as keyof typeof loadingStates] = false
    alert('操作完成！')
  }, 3000)
}

// 表单提交
const handleFormSubmit = () => {
  alert(`保存成功！\n用户名：${formData.username}\n邮箱：${formData.email}\n角色：${formData.role}`)
}
</script>