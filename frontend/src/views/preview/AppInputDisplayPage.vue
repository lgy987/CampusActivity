<!-- AppInputDisplay.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-950 p-8">
    <div class="mx-auto max-w-7xl">
      <!-- 页面标题 -->
      <div class="mb-8 text-center">
        <h1 class="text-4xl font-bold mb-2">AppInput 组件演示</h1>
        <p class="text-muted-foreground">功能丰富的输入框封装，支持多种类型、状态、图标和验证</p>
      </div>

      <!-- 1. 基础用法 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">1. 基础用法</p>
        <p class="text-sm text-muted-foreground mb-3">&lt;AppInput v-model="value" placeholder="..." /&gt;</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <p class="text-sm font-medium mb-1">文本输入</p>
            <AppInput 
              v-model="basicInput" 
              placeholder="请输入文本" 
            />
          </div>
          <div>
            <p class="text-sm font-medium mb-1">数字输入</p>
            <AppInput 
              v-model="numberInput" 
              type="number" 
              placeholder="请输入数字" 
            />
          </div>
          <div>
            <p class="text-sm font-medium mb-1">邮箱输入</p>
            <AppInput 
              v-model="emailInput" 
              type="email" 
              placeholder="请输入邮箱" 
            />
          </div>
          <div>
            <p class="text-sm font-medium mb-1">密码输入（带可见性切换）</p>
            <AppInput 
              v-model="passwordInput" 
              type="password" 
              placeholder="请输入密码" 
            />
          </div>
        </div>
      </section>

      <!-- 2. 不同尺寸 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">2. 不同尺寸</p>
        <p class="text-sm text-muted-foreground mb-3">&lt;AppInput size="..." /&gt;</p>
        <div class="space-y-3">
          <div>
            <p class="text-sm font-medium mb-1">sm</p>
            <AppInput size="sm" placeholder="小尺寸输入框" />
          </div>
          <div>
            <p class="text-sm font-medium mb-1">md (默认)</p>
            <AppInput size="md" placeholder="中等尺寸输入框" />
          </div>
          <div>
            <p class="text-sm font-medium mb-1">lg</p>
            <AppInput size="lg" placeholder="大尺寸输入框" />
          </div>
        </div>
      </section>

      <!-- 3. 不同状态 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">3. 不同状态</p>
        <p class="text-sm text-muted-foreground mb-3">错误、成功、禁用、只读状态</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <p class="text-sm font-medium mb-1">错误状态</p>
            <AppInput 
              v-model="errorInput" 
              placeholder="错误示例" 
              error="用户名不能为空" 
            />
          </div>
          <div>
            <p class="text-sm font-medium mb-1">成功状态</p>
            <AppInput 
              v-model="successInput" 
              placeholder="成功示例" 
              success 
            />
          </div>
          <div>
            <p class="text-sm font-medium mb-1">禁用状态</p>
            <AppInput 
              disabled 
              placeholder="禁用输入框" 
              value="禁用的内容" 
            />
          </div>
          <div>
            <p class="text-sm font-medium mb-1">只读状态</p>
            <AppInput 
              readonly 
              placeholder="只读输入框" 
              value="只读的内容" 
            />
          </div>
        </div>
      </section>

      <!-- 4. 带标签 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">4. 带标签</p>
        <p class="text-sm text-muted-foreground mb-3">&lt;AppInput label="..." required /&gt;</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <AppInput 
              v-model="labeledInput1" 
              label="用户名" 
              placeholder="请输入用户名" 
              hint="请输入2-20个字符"
            />
          </div>
          <div>
            <AppInput 
              v-model="labeledInput2" 
              label="邮箱" 
              type="email" 
              placeholder="请输入邮箱" 
              required 
              hint="请输入有效的邮箱地址"
            />
          </div>
        </div>
      </section>

      <!-- 5. 带图标 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">5. 带图标</p>
        <p class="text-sm text-muted-foreground mb-3">&lt;AppInput leftIcon="..." rightIcon="..." /&gt;</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <p class="text-sm font-medium mb-1">左图标</p>
            <AppInput 
              v-model="iconInput1" 
              placeholder="搜索..." 
              :left-icon="Search"
            />
          </div>
          <div>
            <p class="text-sm font-medium mb-1">右图标</p>
            <AppInput 
              v-model="iconInput2" 
              placeholder="日期" 
              :right-icon="Calendar"
            />
          </div>
          <div>
            <p class="text-sm font-medium mb-1">左右图标</p>
            <AppInput 
              v-model="iconInput3" 
              placeholder="用户" 
              :left-icon="User"
              :right-icon="Check"
            />
          </div>
        </div>
      </section>

      <!-- 6. 可清空 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">6. 可清空</p>
        <p class="text-sm text-muted-foreground mb-3">&lt;AppInput clearable /&gt;</p>
        <div>
          <AppInput 
            v-model="clearableInput" 
            placeholder="输入内容后显示清空按钮" 
            clearable 
          />
          <p class="text-xs text-muted-foreground mt-2">当前值: {{ clearableInput || '空' }}</p>
        </div>
      </section>

      <!-- 7. 文本域 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">7. 文本域</p>
        <p class="text-sm text-muted-foreground mb-3">&lt;AppInput as="textarea" rows="..." /&gt;</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <p class="text-sm font-medium mb-1">基础文本域</p>
            <AppInput 
              v-model="textarea1" 
              as="textarea" 
              placeholder="请输入多行文本" 
            />
          </div>
          <div>
            <p class="text-sm font-medium mb-1">带字数限制</p>
            <AppInput 
              v-model="textarea2" 
              as="textarea" 
              placeholder="最多100个字符" 
              :maxlength="100"
              show-count
            />
          </div>
        </div>
      </section>

      <!-- 8. Select 选择器 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">8. Select 选择器</p>
        <p class="text-sm text-muted-foreground mb-3">&lt;AppInput type="select" :options="..." /&gt;</p>
        
        <!-- Select 基础用法 -->
        <div class="mb-6">
          <p class="text-sm font-medium mb-2 text-primary">基础选择器</p>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <AppInput 
                v-model="selectBasic" 
                type="select" 
                label="城市选择"
                :options="cityOptions"
                placeholder="请选择城市"
                hint="选择您所在的城市"
              />
              <p class="text-xs text-muted-foreground mt-2">选中值: {{ selectBasic || '未选择' }}</p>
            </div>
            <div>
              <AppInput 
                v-model="selectRequired" 
                type="select" 
                label="必选字段"
                :options="categoryOptions"
                placeholder="请选择分类"
                required
                :error="selectError"
                @blur="validateSelect"
              />
              <p class="text-xs text-muted-foreground mt-2">选中值: {{ selectRequired || '未选择' }}</p>
            </div>
          </div>
        </div>

        <!-- Select 带图标 -->
        <div class="mb-6">
          <p class="text-sm font-medium mb-2 text-primary">带图标的选择器</p>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <AppInput 
                v-model="selectWithIcon" 
                type="select" 
                label="国家选择"
                :options="countryOptions"
                placeholder="请选择国家"
                :left-icon="Globe"
                hint="选择您的国家"
              />
            </div>
            <div>
              <AppInput 
                v-model="selectDisabled" 
                type="select" 
                label="禁用状态"
                :options="cityOptions"
                placeholder="不可选择"
                disabled
                :left-icon="MapPin"
              />
            </div>
          </div>
        </div>

        <!-- Select 不同尺寸 -->
        <div class="mb-6">
          <p class="text-sm font-medium mb-2 text-primary">不同尺寸的选择器</p>
          <div class="space-y-3">
            <AppInput 
              v-model="selectSm" 
              type="select" 
              label="小尺寸"
              size="sm"
              :options="sizeOptions"
              placeholder="小尺寸选择器"
            />
            <AppInput 
              v-model="selectMd" 
              type="select" 
              label="中等尺寸"
              size="md"
              :options="sizeOptions"
              placeholder="中等尺寸选择器"
            />
            <AppInput 
              v-model="selectLg" 
              type="select" 
              label="大尺寸"
              size="lg"
              :options="sizeOptions"
              placeholder="大尺寸选择器"
            />
          </div>
        </div>

        <!-- Select 错误和成功状态 -->
        <div>
          <p class="text-sm font-medium mb-2 text-primary">状态展示</p>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <AppInput 
                v-model="selectErrorState" 
                type="select" 
                label="错误状态"
                :options="cityOptions"
                placeholder="请选择"
                error="请选择有效的选项"
              />
            </div>
            <div>
              <AppInput 
                v-model="selectSuccessState" 
                type="select" 
                label="成功状态"
                :options="cityOptions"
                placeholder="请选择"
                success
              />
            </div>
          </div>
        </div>
      </section>

      <!-- 9. Toggle 开关 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">9. Toggle 开关</p>
        <p class="text-sm text-muted-foreground mb-3">&lt;AppInput type="toggle" /&gt;</p>
        
        <!-- Toggle 基础用法 -->
        <div class="mb-6">
          <p class="text-sm font-medium mb-2 text-primary">基础开关</p>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <AppInput 
                v-model="toggleBasic" 
                type="toggle" 
                label="通知开关"
                toggle-label="接收推送通知"
                toggle-description="开启后您将收到重要的消息通知"
              />
              <p class="text-xs text-muted-foreground mt-2">状态: {{ toggleBasic ? '已开启' : '已关闭' }}</p>
            </div>
            <div>
              <AppInput 
                v-model="toggleDarkMode" 
                type="toggle" 
                label="深色模式"
                toggle-label="深色主题"
                toggle-description="切换到深色模式以保护眼睛"
                :left-icon="Moon"
              />
              <p class="text-xs text-muted-foreground mt-2">状态: {{ toggleDarkMode ? '深色模式' : '浅色模式' }}</p>
            </div>
          </div>
        </div>

        <!-- Toggle 不同状态 -->
        <div class="mb-6">
          <p class="text-sm font-medium mb-2 text-primary">不同状态</p>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <AppInput 
                v-model="toggleDisabled" 
                type="toggle" 
                label="禁用状态"
                toggle-label="此开关已禁用"
                disabled
              />
            </div>
            <div>
              <AppInput 
                v-model="toggleRequired" 
                type="toggle" 
                label="必选开关"
                toggle-label="同意服务条款"
                required
                :error="toggleError"
                @toggle-change="validateToggle"
              />
            </div>
            <div>
              <AppInput 
                v-model="toggleLoading" 
                type="toggle" 
                label="加载状态"
                toggle-label="正在处理中"
                loading
              />
            </div>
          </div>
        </div>

        <!-- Toggle 分组示例 -->
        <div>
          <p class="text-sm font-medium mb-2 text-primary">通知偏好设置</p>
          <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
            <h4 class="font-semibold mb-4">通知设置</h4>
            <div class="space-y-4">
              <AppInput 
                v-model="notifications.email" 
                type="toggle" 
                label="邮件通知"
                toggle-label="接收邮件通知"
                toggle-description="重要通知将通过邮件发送给您"
              />
              <AppInput 
                v-model="notifications.sms" 
                type="toggle" 
                label="短信通知"
                toggle-label="接收短信通知"
                toggle-description="紧急通知将通过短信发送"
              />
              <AppInput 
                v-model="notifications.push" 
                type="toggle" 
                label="推送通知"
                toggle-label="接收浏览器推送"
                toggle-description="实时消息将通过浏览器推送"
              />
              <AppInput 
                v-model="notifications.marketing" 
                type="toggle" 
                label="营销信息"
                toggle-label="接收营销邮件"
                toggle-description="接收优惠活动和产品更新信息"
              />
            </div>
            <div class="mt-4 p-3 bg-gray-50 dark:bg-gray-700 rounded">
              <p class="text-sm font-medium">通知偏好汇总：</p>
              <p class="text-xs text-muted-foreground mt-1">
                邮件: {{ notifications.email ? '✓' : '✗' }} | 
                短信: {{ notifications.sms ? '✓' : '✗' }} | 
                推送: {{ notifications.push ? '✓' : '✗' }} | 
                营销: {{ notifications.marketing ? '✓' : '✗' }}
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- 10. 综合示例 - 表单 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">10. 综合示例 - 用户设置</p>
        <p class="text-sm text-muted-foreground mb-3">包含 Select 和 Toggle 的完整表单</p>
        <div class="max-w-2xl mx-auto p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
          <h3 class="text-lg font-semibold mb-4">用户偏好设置</h3>
          
          <div class="space-y-4">
            <AppInput 
              v-model="userSettings.username" 
              label="用户名" 
              placeholder="请输入用户名"
              :left-icon="User"
              required
              :error="userSettingsErrors.username"
              @blur="validateUsername2"
            />
            
            <AppInput 
              v-model="userSettings.email" 
              label="邮箱" 
              type="email" 
              placeholder="请输入邮箱"
              :left-icon="Mail"
              required
              :error="userSettingsErrors.email"
              @blur="validateEmail2"
            />
            
            <AppInput 
              v-model="userSettings.language" 
              type="select" 
              label="首选语言"
              :options="languageOptions"
              placeholder="请选择语言"
              :left-icon="Globe"
              required
            />
            
            <AppInput 
              v-model="userSettings.theme" 
              type="select" 
              label="主题风格"
              :options="themeOptions"
              placeholder="请选择主题"
              :left-icon="Palette"
            />
            
            <AppInput 
              v-model="userSettings.notifications" 
              type="toggle" 
              label="通知开关"
              toggle-label="启用所有通知"
              toggle-description="开启后将接收所有类型的通知"
            />
            
            <div class="pl-6 space-y-3" v-show="userSettings.notifications">
              <AppInput 
                v-model="userSettings.emailNotifications" 
                type="toggle" 
                label="邮件通知"
                toggle-label="接收邮件通知"
                size="sm"
              />
              <AppInput 
                v-model="userSettings.pushNotifications" 
                type="toggle" 
                label="推送通知"
                toggle-label="接收浏览器推送"
                size="sm"
              />
            </div>
            
            <AppInput 
              v-model="userSettings.bio" 
              label="个人简介" 
              as="textarea" 
              placeholder="介绍一下自己"
              :maxlength="200"
              show-count
              :rows="3"
            />
            
            <div class="flex gap-3 pt-4">
              <AppButton 
                variant="default" 
                @click="handleSettingsSubmit"
              >
                保存设置
              </AppButton>
              <AppButton 
                variant="outline" 
                @click="resetSettings"
              >
                重置
              </AppButton>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import AppInput from '@/components/common/AppInput.vue'
import AppButton from '@/components/common/AppButton.vue'
import { Search, Calendar, User, Check, Mail, Lock, Globe, MapPin, Moon, Palette } from '@lucide/vue'

// 基础输入框
const basicInput = ref('')
const numberInput = ref('')
const emailInput = ref('')
const passwordInput = ref('')

// 状态输入框
const errorInput = ref('错误的内容')
const successInput = ref('成功的内容')
const loadingInput = ref('')

// 标签输入框
const labeledInput1 = ref('')
const labeledInput2 = ref('')

// 图标输入框
const iconInput1 = ref('')
const iconInput2 = ref('')
const iconInput3 = ref('')

// 清空输入框
const clearableInput = ref('')

// 文本域
const textarea1 = ref('')
const textarea2 = ref('')

// Select 数据
const selectBasic = ref('')
const selectRequired = ref('')
const selectWithIcon = ref('')
const selectDisabled = ref('')
const selectSm = ref('')
const selectMd = ref('')
const selectLg = ref('')
const selectErrorState = ref('')
const selectSuccessState = ref('sh')
const selectError = ref('')

// Select 选项
const cityOptions = [
  { value: 'bj', label: '北京' },
  { value: 'sh', label: '上海' },
  { value: 'gz', label: '广州' },
  { value: 'sz', label: '深圳' },
  { value: 'hz', label: '杭州' },
  { value: 'cd', label: '成都' }
]

const categoryOptions = [
  { value: 'tech', label: '科技' },
  { value: 'design', label: '设计' },
  { value: 'business', label: '商业' },
  { value: 'lifestyle', label: '生活方式' }
]

const countryOptions = [
  { value: 'cn', label: '中国' },
  { value: 'us', label: '美国' },
  { value: 'jp', label: '日本' },
  { value: 'kr', label: '韩国' },
  { value: 'uk', label: '英国' }
]

const sizeOptions = [
  { value: 'option1', label: '选项一' },
  { value: 'option2', label: '选项二' },
  { value: 'option3', label: '选项三' }
]

const languageOptions = [
  { value: 'zh', label: '简体中文' },
  { value: 'zh-tw', label: '繁體中文' },
  { value: 'en', label: 'English' },
  { value: 'ja', label: '日本語' }
]

const themeOptions = [
  { value: 'light', label: '浅色主题' },
  { value: 'dark', label: '深色主题' },
  { value: 'auto', label: '跟随系统' }
]

// Toggle 数据
const toggleBasic = ref(false)
const toggleDarkMode = ref(false)
const toggleDisabled = ref(true)
const toggleRequired = ref(false)
const toggleLoading = ref(false)
const toggleError = ref('')

const notifications = reactive({
  email: true,
  sms: false,
  push: true,
  marketing: false
})

// 用户设置表单
const userSettings = reactive({
  username: '',
  email: '',
  language: '',
  theme: '',
  notifications: true,
  emailNotifications: true,
  pushNotifications: false,
  bio: ''
})

const userSettingsErrors = reactive({
  username: '',
  email: ''
})

// 验证函数
const validateSelect = () => {
  if (!selectRequired.value) {
    selectError.value = '请选择一个选项'
  } else {
    selectError.value = ''
  }
}

const validateToggle = () => {
  if (!toggleRequired.value) {
    toggleError.value = '请同意服务条款'
  } else {
    toggleError.value = ''
  }
}

const validateUsername2 = () => {
  if (!userSettings.username) {
    userSettingsErrors.username = '请输入用户名'
  } else if (userSettings.username.length < 2) {
    userSettingsErrors.username = '用户名至少2个字符'
  } else {
    userSettingsErrors.username = ''
  }
}

const validateEmail2 = () => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!userSettings.email) {
    userSettingsErrors.email = '请输入邮箱'
  } else if (!emailRegex.test(userSettings.email)) {
    userSettingsErrors.email = '请输入有效的邮箱地址'
  } else {
    userSettingsErrors.email = ''
  }
}

const handleSettingsSubmit = () => {
  validateUsername2()
  validateEmail2()
  
  if (!userSettingsErrors.username && !userSettingsErrors.email && userSettings.language) {
    alert(`设置已保存！\n用户名：${userSettings.username}\n邮箱：${userSettings.email}\n语言：${userSettings.language}\n主题：${userSettings.theme || '默认'}`)
  } else if (!userSettings.language) {
    alert('请选择首选语言')
  }
}

const resetSettings = () => {
  userSettings.username = ''
  userSettings.email = ''
  userSettings.language = ''
  userSettings.theme = ''
  userSettings.notifications = true
  userSettings.emailNotifications = true
  userSettings.pushNotifications = false
  userSettings.bio = ''
  userSettingsErrors.username = ''
  userSettingsErrors.email = ''
}

// 表单验证（原有）
const form = reactive({
  username: '',
  email: '',
  password: '',
  bio: ''
})

const formErrors = reactive({
  username: '',
  email: '',
  password: ''
})

const validateUsername = () => {
  if (!form.username) {
    formErrors.username = '请输入用户名'
  } else if (form.username.length < 2) {
    formErrors.username = '用户名至少2个字符'
  } else {
    formErrors.username = ''
  }
}

const validateEmail = () => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!form.email) {
    formErrors.email = '请输入邮箱'
  } else if (!emailRegex.test(form.email)) {
    formErrors.email = '请输入有效的邮箱地址'
  } else {
    formErrors.email = ''
  }
}

const validatePassword = () => {
  if (!form.password) {
    formErrors.password = '请输入密码'
  } else if (form.password.length < 6) {
    formErrors.password = '密码至少6个字符'
  } else {
    formErrors.password = ''
  }
}

const handleSubmit = () => {
  validateUsername()
  validateEmail()
  validatePassword()
  
  if (!formErrors.username && !formErrors.email && !formErrors.password) {
    alert(`注册成功！\n用户名：${form.username}\n邮箱：${form.email}`)
  }
}
</script>