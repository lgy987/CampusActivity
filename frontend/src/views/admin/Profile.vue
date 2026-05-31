<template>
  <div class="flex h-screen">
    <AdminSidebar />
    <main class="flex-1 overflow-y-auto bg-blue-600 p-8">
      <div class="max-w-7xl mx-auto">
        <div class="mb-6">
          <h1 class="text-3xl font-bold text-white">个人中心</h1>
          <p class="text-white/70 mt-1">账号信息与管理</p>
        </div>

        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden max-w-3xl mx-auto">
          <div class="flex flex-col items-center py-8 px-6 border-b border-gray-100 bg-gray-50">
            <div class="relative">
              <img
                :src="avatar || defaultAvatar"
                class="w-28 h-28 rounded-full border-4 border-blue-100 object-cover"
                @error="handleImageError"
              />
              <label class="absolute bottom-0 right-0 bg-white rounded-full p-1 shadow-md cursor-pointer hover:bg-gray-100">
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
            <h2 class="text-2xl font-bold mt-3 text-gray-800">{{ username }}</h2>
            <p class="text-gray-500">{{ role === 'super_admin' ? '超级管理员' : '管理员' }}</p>
            <div class="mt-2 inline-block px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs">认证管理员</div>
          </div>

          <div class="p-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-5">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">用户名</label>
                <input type="text" v-model="username" class="w-full border rounded-lg px-3 py-2 bg-gray-50" disabled />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
                <input type="email" v-model="email" class="w-full border rounded-lg px-3 py-2 bg-gray-50" disabled />
              </div>
            </div>
            <div class="flex flex-wrap gap-3 mt-8 pt-4 border-t border-gray-100">
              <AppButton variant="outline" @click="openPwdModal">修改密码</AppButton>
              <AppButton variant="outline" @click="handleLogout">登出账号</AppButton>
              <AppButton variant="destructive" @click="handleDeleteAccount">注销账号</AppButton>
            </div>
          </div>
        </div>

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
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Pencil } from 'lucide-vue-next'
import AdminSidebar from '@/components/layout/AdminSidebar.vue'
import AppButton from '@/components/common/AppButton.vue'
import AppDialog from '@/components/layout/AppDialog.vue'
import { getProfile, uploadAvatar, resetPassword, deleteAccount } from '@/api/user'
import { login, logout } from '@/api/auth'
import { showApiError } from '@/api/request'

const router = useRouter()
const username = ref('')
const email = ref('')
const avatar = ref('')
const role = ref('')
const uploadingAvatar = ref(false)

// 默认头像：基于用户名生成，保证唯一性
const defaultAvatar = computed(() => {
  const seed = username.value || 'admin'
  return `https://api.dicebear.com/7.x/avataaars/svg?seed=${seed}`
})

const pwdModalVisible = ref(false)
const oldPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const changingPassword = ref(false)

const fetchProfile = async () => {
  try {
    const data = await getProfile()
    username.value = data.username
    email.value = data.email
    avatar.value = data.avatar || ''
    role.value = (data as any).role || ''
  } catch (e) {
    showApiError(e, '获取个人信息失败')
  }
}

// 头像上传（关键修改：去掉 fetchProfile，直接使用返回的 URL）
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
    // 直接使用接口返回的新头像 URL，不重新拉取个人信息（避免被旧数据覆盖）
    avatar.value = res.avatar_url
    alert('头像更新成功')
  } catch (e: any) {
    const msg = e.response?.data?.message || e.message || '上传失败'
    alert(msg)
  } finally {
    uploadingAvatar.value = false
    if (input) input.value = ''
  }
}

// 图片加载失败时回退到默认头像
const handleImageError = (e: Event) => {
  const img = e.target as HTMLImageElement
  img.src = defaultAvatar.value
}

// 修改密码（保持不变）
const openPwdModal = () => {
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

const handleLogout = async () => {
  if (confirm('确定要退出登录吗？')) {
    try {
      await logout()
    } catch {}
    router.push('/login')
  }
}

const handleDeleteAccount = async () => {
  if (confirm('注销账号后将无法恢复，所有数据将被清除。确定注销吗？')) {
    try {
      await deleteAccount()
      router.push('/login')
    } catch (e) {
      showApiError(e, '注销失败')
    }
  }
}

onMounted(() => {
  fetchProfile()
})
</script>