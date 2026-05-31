<template>
  <div class="flex h-screen">
    <OrganizerSidebar />
    <main class="flex-1 overflow-y-auto bg-blue-600 p-8">
      <div class="max-w-7xl mx-auto">
        <div class="mb-6">
          <h1 class="text-3xl font-bold text-white">个人中心</h1>
          <p class="text-white/70 mt-1">账号信息与管理</p>
        </div>

        <AppCard>
          <div class="flex flex-col items-center py-6 border-b border-gray-100">
            <div class="relative">
              <img
                :src="avatarUrl || `https://api.dicebear.com/7.x/avataaars/svg?seed=${formData.org_name || 'default'}`"
                class="w-28 h-28 rounded-full border-4 border-blue-100 object-cover"
              />
              <label class="absolute bottom-0 right-0 bg-white rounded-full p-1 shadow-md cursor-pointer">
                <Pencil class="h-4 w-4 text-gray-500" />
                <input
                  type="file"
                  accept="image/jpeg,image/png"
                  class="hidden"
                  @change="handleAvatarChange"
                  :disabled="uploadingAvatar"
                />
              </label>
            </div>
            <h2 class="text-2xl font-bold mt-3 text-gray-800">{{ formData.org_name }}</h2>
            <p class="text-gray-500">组织者</p>
            <div class="mt-2 inline-block px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs">
              {{ statusText(profileStatus) }}
            </div>
          </div>

          <div class="space-y-5 mt-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">组织名称</label>
              <input type="text" v-model="formData.org_name" class="w-full border rounded-lg px-3 py-2 bg-gray-50" disabled />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
              <input type="email" v-model="formData.email" class="w-full border rounded-lg px-3 py-2 bg-gray-50" disabled />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">组织简介</label>
              <textarea v-model="formData.description" rows="3" class="w-full border rounded-lg px-3 py-2 bg-gray-50" disabled></textarea>
            </div>
          </div>

          <div class="flex flex-wrap gap-3 mt-8 pt-4 border-t border-gray-100">
            <AppButton variant="outline" @click="openChangePasswordModal">修改密码</AppButton>
            <AppButton variant="outline" @click="handleLogout">登出账号</AppButton>
            <AppButton variant="destructive" @click="handleDeleteAccount">注销账号</AppButton>
          </div>
        </AppCard>

        <AppDialog v-model:open="pwdModalVisible" title="修改密码" confirm-text="保存" cancel-text="取消" @confirm="changePassword">
          <div class="space-y-3">
            <input type="password" v-model="oldPassword" placeholder="当前密码" class="w-full border rounded px-3 py-2">
            <input type="password" v-model="newPassword" placeholder="新密码" class="w-full border rounded px-3 py-2">
            <input type="password" v-model="confirmPassword" placeholder="确认新密码" class="w-full border rounded px-3 py-2">
          </div>
        </AppDialog>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Pencil } from 'lucide-vue-next'
import AppCard from '@/components/common/AppCard.vue'
import AppButton from '@/components/common/AppButton.vue'
import AppDialog from '@/components/layout/AppDialog.vue'
import OrganizerSidebar from '@/components/layout/OrganizerSidebar.vue'
import { getProfile, uploadAvatar, resetPassword, deleteAccount } from '@/api/user'
import { login, logout } from '@/api/auth'
import { showApiError } from '@/api/request'

const router = useRouter()

// 个人信息
const formData = reactive({
  org_name: '',
  email: '',
  description: ''
})

const profileStatus = ref('approved')
const avatarUrl = ref('')
const uploadingAvatar = ref(false)

// 获取个人资料
const fetchProfile = async () => {
  try {
    const data = await getProfile() as any
    formData.org_name = data.org_name || ''
    formData.email = data.email || ''
    formData.description = data.org_proof_text || ''
    profileStatus.value = data.status || 'approved'
    avatarUrl.value = data.avatar || ''
  } catch (e) {
    showApiError(e, '获取个人信息失败')
  }
}

// 头像上传（与普通用户完全一致，不再重新拉取个人信息）
const handleAvatarChange = async (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  if (!['image/jpeg', 'image/png'].includes(file.type)) {
    alert('仅支持 JPG 或 PNG 格式')
    return
  }
  if (file.size > 2 * 1024 * 1024) {
    alert('图片大小不能超过 2MB')
    return
  }

  uploadingAvatar.value = true
  try {
    const res = await uploadAvatar(file)
    avatarUrl.value = res.avatar_url  // 直接使用返回的新URL
    alert('头像更新成功')
  } catch (e: any) {
    const msg = e.response?.data?.message || e.message || '上传失败'
    alert(msg)
  } finally {
    uploadingAvatar.value = false
    if (input) input.value = ''  // 清空 input，允许重复上传同一文件
  }
}

// 修改密码
const pwdModalVisible = ref(false)
const oldPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const changingPassword = ref(false)

const openChangePasswordModal = () => {
  oldPassword.value = ''
  newPassword.value = ''
  confirmPassword.value = ''
  pwdModalVisible.value = true
}

const changePassword = async () => {
  if (!oldPassword.value || !newPassword.value || !confirmPassword.value) {
    alert('请填写完整')
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    alert('新密码与确认密码不一致')
    return
  }
  if (newPassword.value.length < 6 || newPassword.value.length > 20) {
    alert('新密码长度需为 6-20 位')
    return
  }

  changingPassword.value = true
  try {
    await resetPassword({
      old_password: oldPassword.value,
      new_password: newPassword.value,
      confirm_password: confirmPassword.value
    })
    alert('密码修改成功')
    pwdModalVisible.value = false
    oldPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
  } catch (e: any) {
    const msg = e.response?.data?.message || e.message || '修改失败，请检查旧密码是否正确'
    alert(msg)
  } finally {
    changingPassword.value = false
  }
}

// 退出登录
const handleLogout = async () => {
  if (confirm('确定退出登录吗？')) {
    try {
      await logout()
    } catch {}
    router.push('/login')
  }
}

// 注销账号
const handleDeleteAccount = async () => {
  if (confirm('注销账号后将无法恢复，所有数据将被清除。确定注销吗？')) {
    try {
      await deleteAccount()
      alert('账号已注销')
      router.push('/login')
    } catch (e) {
      showApiError(e, '注销失败')
    }
  }
}

const statusText = (status: string) => {
  const map: Record<string, string> = { 
    pending: '审核中', 
    approved: '已认证', 
    rejected: '审核未通过' 
  }
  return map[status] || status
}

onMounted(() => {
  fetchProfile()
})
</script>