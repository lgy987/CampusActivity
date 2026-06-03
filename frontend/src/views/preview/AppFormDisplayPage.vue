<!-- AppFormDisplay.vue -->
<template>
  <div class="min-h-screen p-8">
    <div class="mx-auto max-w-7xl">
      <!-- 页面标题 -->
      <div class="mb-8 text-center">
        <h1 class="text-4xl font-bold mb-2">AppForm 组件演示</h1>
        <p class="text-muted-foreground">强大的表单封装，整合了 AppInput、AppCard、AppButton 和 AppDialog</p>
      </div>

      <!-- 1. 基础表单 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">1. 基础表单</p>
        <p class="text-sm text-muted-foreground mb-3">最简单的表单使用方式</p>
        <AppForm
          :fields="basicFields"
          @submit="handleSubmit"
        />
      </section>

      <!-- 2. 带卡片的表单 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">2. 带卡片包装</p>
        <p class="text-sm text-muted-foreground mb-3">使用卡片包装表单，更美观</p>
        <AppForm
          :fields="cardFields"
          use-card
          card-title="用户信息"
          card-description="请填写以下信息"
          card-variant="color"
          card-color="rgb(99, 102, 241)"
          submit-text="保存信息"
          @submit="handleSubmit"
        />
      </section>

      <!-- 3. 网格布局 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">3. 网格布局</p>
        <p class="text-sm text-muted-foreground mb-3">多列网格布局，适合密集表单</p>
        <AppForm
          :fields="gridFields"
          layout="grid"
          :columns="2"
          use-card
          card-title="注册表单"
          card-description="请填写以下信息完成注册"
          submit-text="注册"
          @submit="handleSubmit"
        />
      </section>

      <!-- 4. 带验证的表单 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">4. 表单验证</p>
        <p class="text-sm text-muted-foreground mb-3">支持自定义验证规则</p>
        <AppForm
          :fields="validationFields"
          use-card
          card-title="表单验证示例"
          card-description="包含各种验证规则"
          @submit="handleSubmit"
        />
      </section>

      <!-- 5. 确认对话框 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">5. 提交确认对话框</p>
        <p class="text-sm text-muted-foreground mb-3">提交前显示确认对话框</p>
        <AppForm
          :fields="confirmFields"
          use-card
          card-title="确认提交示例"
          confirm-before-submit
          confirm-title="确认提交"
          confirm-description="确定要提交这个表单吗？提交后不可修改。"
          @submit="handleSubmit"
        />
      </section>

      <!-- 6. 编辑模式 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">6. 编辑模式</p>
        <p class="text-sm text-muted-foreground mb-3">预填充初始值</p>
        <AppForm
          :fields="editFields"
          :initial-values="editValues"
          mode="edit"
          use-card
          card-title="编辑用户信息"
          submit-text="更新信息"
          @submit="handleSubmit"
        />
      </section>

      <!-- 7. 查看模式 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">7. 查看模式</p>
        <p class="text-sm text-muted-foreground mb-3">只读模式，不可编辑</p>
        <AppForm
          :fields="viewFields"
          :initial-values="viewValues"
          mode="view"
          use-card
          card-title="查看用户详情"
          :show-submit="false"
        />
      </section>

      <!-- 8. 带图标的表单 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">8. 带图标表单</p>
        <p class="text-sm text-muted-foreground mb-3">输入框带左右图标</p>
        <AppForm
          :fields="iconFields"
          use-card
          card-title="登录表单"
          card-variant="color-bg"
          card-color="rgb(59, 130, 246)"
          submit-text="登录"
          @submit="handleSubmit"
        />
      </section>

      <!-- 9. Select 选择器表单 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">9. Select 选择器表单</p>
        <p class="text-sm text-muted-foreground mb-3">下拉选择框的使用</p>
        <AppForm
          :fields="selectFields"
          layout="grid"
          :columns="2"
          use-card
          card-title="选择器示例"
          card-description="各种下拉选择框的使用场景"
          @submit="handleSubmit"
        />
      </section>

      <!-- 10. Toggle 开关表单 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">10. Toggle 开关表单</p>
        <p class="text-sm text-muted-foreground mb-3">开关切换按钮的使用</p>
        <AppForm
          :fields="toggleFields"
          use-card
          card-title="偏好设置"
          card-description="配置您的个性化选项"
          @submit="handleSubmit"
          @toggle-change="handleToggleChange"
        />
      </section>

      <!-- 11. Select + Toggle 组合表单 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">11. 组合表单示例</p>
        <p class="text-sm text-muted-foreground mb-3">Select 和 Toggle 的完整示例</p>
        <AppForm
          :fields="combinedFields"
          layout="grid"
          :columns="2"
          use-card
          card-title="用户设置"
          card-description="完整的用户偏好设置"
          submit-text="保存设置"
          confirm-before-submit
          @submit="handleSubmit"
          @toggle-change="handleToggleChange"
        />
      </section>

      <!-- 12. 复杂表单示例 -->
      <section class="mb-10">
        <p class="text-lg font-semibold mb-2">12. 复杂表单示例</p>
        <p class="text-sm text-muted-foreground mb-3">商品信息表单（包含 Select）</p>
        <AppForm
          :fields="complexFields"
          layout="grid"
          :columns="2"
          use-card
          card-title="商品信息"
          card-description="请填写商品详细信息"
          submit-text="发布商品"
          confirm-before-submit
          @submit="handleSubmit"
        />
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppForm from '@/components/layout/AppForm.vue'
import type { FormField } from '@/components/layout/AppForm.vue'
import { User, Mail, Lock, Phone, MapPin, Package, DollarSign, Tag, FileText, Globe, Bell, Moon, Shield, ShoppingBag, CreditCard } from '@lucide/vue'

// 基础字段
const basicFields: FormField[] = [
  { name: 'name', label: '姓名', placeholder: '请输入姓名', required: true },
  { name: 'email', label: '邮箱', type: 'email', placeholder: '请输入邮箱', required: true }
]

// 卡片字段
const cardFields: FormField[] = [
  { name: 'username', label: '用户名', placeholder: '请输入用户名', required: true },
  { name: 'bio', label: '个人简介', type: 'textarea', placeholder: '介绍一下自己', rows: 3 }
]

// 网格字段
const gridFields: FormField[] = [
  { name: 'firstName', label: '名', placeholder: '请输入名', required: true },
  { name: 'lastName', label: '姓', placeholder: '请输入姓', required: true },
  { name: 'email', label: '邮箱', type: 'email', placeholder: '请输入邮箱', required: true },
  { name: 'phone', label: '手机号', type: 'tel', placeholder: '请输入手机号' }
]

// 验证字段
const validationFields: FormField[] = [
  { 
    name: 'username', 
    label: '用户名', 
    placeholder: '请输入用户名', 
    required: true,
    hint: '2-20个字符',
    rules: [
      (val: string) => (val && val.length >= 2) || '用户名至少2个字符',
      (val: string) => (val && val.length <= 20) || '用户名最多20个字符'
    ]
  },
  { 
    name: 'email', 
    label: '邮箱', 
    type: 'email', 
    placeholder: '请输入邮箱', 
    required: true 
  },
  { 
    name: 'password', 
    label: '密码', 
    type: 'password', 
    placeholder: '请输入密码', 
    required: true,
    rules: [
      (val: string) => (val && val.length >= 6) || '密码至少6个字符'
    ]
  },
  { 
    name: 'confirmPassword', 
    label: '确认密码', 
    type: 'password', 
    placeholder: '请再次输入密码', 
    required: true,
    rules: [
      (val: string, formData: any) => val === formData?.password || '两次输入的密码不一致'
    ]
  }
]

// 确认字段
const confirmFields: FormField[] = [
  { name: 'title', label: '标题', placeholder: '请输入标题', required: true },
  { name: 'content', label: '内容', type: 'textarea', placeholder: '请输入内容', required: true, rows: 4 }
]

// 编辑字段和值
const editFields: FormField[] = [
  { name: 'name', label: '姓名', placeholder: '请输入姓名', required: true },
  { name: 'email', label: '邮箱', type: 'email', placeholder: '请输入邮箱', required: true },
  { name: 'role', label: '角色', type: 'select', placeholder: '请选择角色', options: [
    { value: 'admin', label: '管理员' },
    { value: 'user', label: '普通用户' },
    { value: 'guest', label: '访客' }
  ]}
]

const editValues = {
  name: '张三',
  email: 'zhangsan@example.com',
  role: 'admin'
}

// 查看字段和值
const viewFields: FormField[] = [
  { name: 'productName', label: '产品名称' },
  { name: 'price', label: '价格' },
  { name: 'category', label: '分类' },
  { name: 'status', label: '状态' }
]

const viewValues = {
  productName: '智能手机',
  price: '¥3,999',
  category: '电子产品',
  status: '在售'
}

// 图标字段
const iconFields: FormField[] = [
  { name: 'email', label: '邮箱', type: 'email', placeholder: '请输入邮箱', leftIcon: Mail, required: true },
  { name: 'password', label: '密码', type: 'password', placeholder: '请输入密码', leftIcon: Lock, required: true }
]

// Select 字段
const selectFields: FormField[] = [
  { 
    name: 'country', 
    label: '国家', 
    type: 'select', 
    placeholder: '请选择国家', 
    required: true,
    leftIcon: Globe,
    options: [
      { value: 'cn', label: '中国' },
      { value: 'us', label: '美国' },
      { value: 'jp', label: '日本' },
      { value: 'kr', label: '韩国' },
      { value: 'uk', label: '英国' }
    ]
  },
  { 
    name: 'city', 
    label: '城市', 
    type: 'select', 
    placeholder: '请选择城市', 
    required: true,
    leftIcon: MapPin,
    options: [
      { value: 'bj', label: '北京' },
      { value: 'sh', label: '上海' },
      { value: 'gz', label: '广州' },
      { value: 'sz', label: '深圳' },
      { value: 'hz', label: '杭州' }
    ]
  },
  { 
    name: 'language', 
    label: '语言', 
    type: 'select', 
    placeholder: '请选择语言',
    options: [
      { value: 'zh', label: '简体中文' },
      { value: 'zh-tw', label: '繁體中文' },
      { value: 'en', label: 'English' },
      { value: 'ja', label: '日本語' }
    ]
  },
  { 
    name: 'theme', 
    label: '主题', 
    type: 'select', 
    placeholder: '请选择主题',
    options: [
      { value: 'light', label: '浅色主题' },
      { value: 'dark', label: '深色主题' },
      { value: 'auto', label: '跟随系统' }
    ]
  }
]

// Toggle 字段
const toggleFields: FormField[] = [
  { 
    name: 'emailNotifications', 
    label: '邮件通知', 
    type: 'toggle',
    toggleLabel: '接收邮件通知',
    toggleDescription: '开启后将接收系统邮件和通知'
  },
  { 
    name: 'pushNotifications', 
    label: '推送通知', 
    type: 'toggle',
    toggleLabel: '接收推送通知',
    toggleDescription: '开启后将接收浏览器推送消息'
  },
  { 
    name: 'darkMode', 
    label: '深色模式', 
    type: 'toggle',
    toggleLabel: '启用深色模式',
    toggleDescription: '切换到深色主题以保护眼睛',
    leftIcon: Moon
  },
  { 
    name: 'marketing', 
    label: '营销信息', 
    type: 'toggle',
    toggleLabel: '接收营销邮件',
    toggleDescription: '开启后可能收到优惠活动信息',
    required: true
  }
]

// 组合字段
const combinedFields: FormField[] = [
  { name: 'username', label: '用户名', placeholder: '请输入用户名', required: true, leftIcon: User },
  { name: 'email', label: '邮箱', type: 'email', placeholder: '请输入邮箱', required: true, leftIcon: Mail },
  { 
    name: 'timezone', 
    label: '时区', 
    type: 'select', 
    placeholder: '请选择时区', 
    required: true,
    leftIcon: Globe,
    options: [
      { value: 'asia/shanghai', label: 'Asia/Shanghai (UTC+8)' },
      { value: 'asia/tokyo', label: 'Asia/Tokyo (UTC+9)' },
      { value: 'america/new_york', label: 'America/New York (UTC-5)' },
      { value: 'europe/london', label: 'Europe/London (UTC+0)' }
    ]
  },
  { 
    name: 'language', 
    label: '语言', 
    type: 'select', 
    placeholder: '请选择语言',
    leftIcon: Globe,
    options: [
      { value: 'zh', label: '简体中文' },
      { value: 'en', label: 'English' },
      { value: 'ja', label: '日本語' }
    ]
  },
  { 
    name: 'emailNotifications', 
    label: '邮件通知', 
    type: 'toggle',
    toggleLabel: '接收邮件通知',
    toggleDescription: '重要通知将通过邮件发送'
  },
  { 
    name: 'smsNotifications', 
    label: '短信通知', 
    type: 'toggle',
    toggleLabel: '接收短信通知',
    toggleDescription: '紧急通知将通过短信发送'
  },
  { 
    name: 'newsletter', 
    label: '订阅资讯', 
    type: 'toggle',
    toggleLabel: '订阅每周资讯',
    toggleDescription: '每周接收精选内容推送',
    required: true
  },
  { 
    name: 'bio', 
    label: '个人简介', 
    type: 'textarea', 
    placeholder: '介绍一下自己',
    rows: 3,
    maxlength: 200,
    showCount: true
  }
]

// 复杂字段（更新为包含 Select）
const complexFields: FormField[] = [
  { name: 'productName', label: '商品名称', placeholder: '请输入商品名称', required: true, leftIcon: Package },
  { name: 'price', label: '价格', type: 'number', placeholder: '请输入价格', required: true, leftIcon: DollarSign },
  { 
    name: 'category', 
    label: '分类', 
    type: 'select', 
    placeholder: '请选择分类', 
    required: true, 
    leftIcon: Tag,
    options: [
      { value: 'electronics', label: '电子产品' },
      { value: 'clothing', label: '服装服饰' },
      { value: 'books', label: '图书文具' },
      { value: 'food', label: '食品饮料' },
      { value: 'beauty', label: '美妆个护' }
    ]
  },
  { 
    name: 'brand', 
    label: '品牌', 
    type: 'select', 
    placeholder: '请选择品牌',
    leftIcon: ShoppingBag,
    options: [
      { value: 'apple', label: 'Apple' },
      { value: 'samsung', label: 'Samsung' },
      { value: 'huawei', label: 'Huawei' },
      { value: 'xiaomi', label: 'Xiaomi' },
      { value: 'other', label: '其他' }
    ]
  },
  { name: 'stock', label: '库存', type: 'number', placeholder: '请输入库存', required: true },
  { 
    name: 'shipping', 
    label: '配送方式', 
    type: 'select', 
    placeholder: '请选择配送方式',
    leftIcon: CreditCard,
    options: [
      { value: 'express', label: '快递配送' },
      { value: 'pickup', label: '到店自提' },
      { value: 'overnight', label: '次日达' }
    ]
  },
  { name: 'description', label: '商品描述', type: 'textarea', placeholder: '请输入商品描述', rows: 4, leftIcon: FileText },
  { name: 'address', label: '发货地址', placeholder: '请输入发货地址', leftIcon: MapPin },
  { 
    name: 'onSale', 
    label: '上架销售', 
    type: 'toggle',
    toggleLabel: '立即上架',
    toggleDescription: '开启后商品将立即上架销售',
    required: true
  }
]

// 处理提交
const handleSubmit = (values: any) => {
  console.log('表单提交:', values)
  alert(`提交成功！\n${JSON.stringify(values, null, 2)}`)
}

// 处理 Toggle 变化
const handleToggleChange = (name: string, value: boolean) => {
  console.log(`Toggle ${name} 变化为:`, value)
}
</script>