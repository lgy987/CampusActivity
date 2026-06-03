<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getProfile, updateProfile, uploadAvatar, deleteAccount, resetPassword } from '@/api/user'
import { login, logout } from '@/api/auth'
import { showApiError } from '@/api/request'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import { toast } from '@/composables/useToast'
import { COLLEGES, GRADES, ACHIEVEMENT_TIERS } from '@/utils/constants'
import { isPassword, isPhone } from '@/utils/validators'
import Dialog from '@/components/ui/Dialog.vue'
import ConfirmDialog from '@/components/ui/ConfirmDialog.vue'
import { Pencil, HelpCircle } from 'lucide-vue-next'
import type { UserProfile } from '@/types/api'

const router = useRouter()
const auth = useAuthStore()
const userStore = useUserStore()

const profile = ref<UserProfile | null>(null)
const loading = ref(false)
const saving = ref(false)
const showPasswordDialog = ref(false)
const showDeleteConfirm = ref(false)
const showAchievementTip = ref(false)
const passwordForm = ref({ old_password: '', new_password: '', confirm_password: '' })
const passwordLoading = ref(false)
const deleteLoading = ref(false)

onMounted(loadProfile)

async function loadProfile() {
  loading.value = true
  try {
    const data = await getProfile()
   profile.value = {
      ...data,
      phone: data.phone || '',  // null 或 undefined 都转为空字符串
    }
  } catch (e) {
    showApiError(e)
  } finally {
    loading.value = false
  }
}

async function handleAvatarChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file || !profile.value) return
  try {
    const res = await uploadAvatar(file)
    profile.value.avatar = res.avatar_url
    toast.success('头像上传成功')
  } catch (err) {
    showApiError(err)
  }
}

async function handleSave() {
  if (!profile.value) return
  const phone = profile.value.phone?.trim()
  if (phone && !isPhone(phone)) {
    toast.error('手机号须为11位')
    return
  }
  saving.value = true
  try {
    await updateProfile({
      username: profile.value.username,
      gender: profile.value.gender,
      college: profile.value.college,
      major: profile.value.major,
      grade: profile.value.grade,
      ...(phone ? { phone } : {}),
    })
    toast.success('保存成功')
  } catch (e) {
    showApiError(e)
  } finally {
    saving.value = false
  }
}

async function handleChangePassword() {
  if (!profile.value) return
  if (!passwordForm.value.old_password) {
    toast.error('请输入现有密码')
    return
  }
  if (!isPassword(passwordForm.value.new_password)) {
    toast.error('新密码须为6-20位')
    return
  }
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    toast.error('两次新密码不一致')
    return
  }
  passwordLoading.value = true
  try {
    
    await resetPassword({
      old_password: passwordForm.value.old_password,
      new_password: passwordForm.value.new_password,
      confirm_password: passwordForm.value.confirm_password,
    })
    toast.success('密码修改成功')
    passwordForm.value = { old_password: '', new_password: '', confirm_password: '' }
    showPasswordDialog.value = false
  } catch (error: any) {
    const message = error?.response?.data?.message || error?.message || ''
    if (message.includes('旧密码') || message.includes('密码错误')) {
      toast.error('旧密码错误，请重新输入')
    } else {
      toast.error(message || '密码修改失败')
    }
    // 只清空旧密码输入框
    passwordForm.value.old_password = ''
  } finally {
    passwordLoading.value = false
  }
}

async function handleLogout() {
  try {
    await logout()
  } catch {
    /* ignore */
  }
  auth.clearAuth()
  userStore.clearProfile()
  router.push('/login')
}

async function handleDeleteAccount() {
  deleteLoading.value = true
  try {
    await deleteAccount()
    auth.clearAuth()
    router.push('/register')
  } catch (e) {
    showApiError(e)
  } finally {
    deleteLoading.value = false
    showDeleteConfirm.value = false
  }
}
</script>

<template>
  <div class="mx-auto max-w-4xl">
    <div v-if="loading" class="proto-card py-16 text-center text-gray-500">加载中...</div>

    <div v-else-if="profile" class="proto-card p-6">
      <h2 class="mb-6 text-lg font-semibold text-gray-800">个人主页</h2>

      <div class="mb-6 flex flex-wrap items-start gap-6">
        <div class="relative">
          <img
            :src="profile.avatar || `https://api.dicebear.com/7.x/avataaars/svg?seed=${profile.student_id}`"
            class="h-24 w-24 rounded border object-cover"
            alt="头像"
          />
          <label class="absolute -bottom-1 -right-1 cursor-pointer rounded-full bg-white p-1 shadow border">
            <Pencil class="h-3.5 w-3.5 text-gray-500" />
            <input type="file" accept="image/*" class="hidden" @change="handleAvatarChange" />
          </label>
        </div>
        <div class="relative">
          <div class="flex items-center gap-2 text-sm">
            <span class="text-gray-600">成就称号</span>
            <span class="font-semibold text-amber-600">
              {{ profile.achievement?.title || '暂无成就' }}
            </span>
            <button
              type="button"
              class="text-gray-400"
              @mouseenter="showAchievementTip = true"
              @mouseleave="showAchievementTip = false"
            >
              <HelpCircle class="h-4 w-4" />
            </button>
          </div>
          <div
            v-if="showAchievementTip"
            class="absolute z-10 mt-2 w-52 rounded border bg-white p-3 text-xs shadow-lg"
          >
            <p v-for="t in ACHIEVEMENT_TIERS" :key="t.title">
              累计签到{{ t.required }}次 → {{ t.title }}
            </p>
          </div>
        </div>
      </div>

      <div class="grid gap-6 lg:grid-cols-2">
        <div class="space-y-4">
          <div v-for="field in [
            { key: 'username', label: '用户名', editable: true },
            { key: 'phone', label: '联系方式', placeholder: '联系人手机号码', editable: true },
          ]" :key="field.key">
          <label class="mb-1 block text-sm text-gray-600">{{ field.label }}</label>
          <div class="relative">
          <input
            v-model="(profile as any)[field.key]"
            :placeholder= "(field as any).placeholder || field.label"
            class="w-full rounded border border-gray-300 px-3 py-2 pr-8 text-sm"
          />
          <Pencil class="absolute right-2 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-gray-400" />
          </div>
        </div>
          <div>
            <label class="mb-1 block text-sm text-gray-600">邮箱</label>
            <input :value="profile.email" disabled class="w-full rounded border bg-gray-50 px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="mb-1 block text-sm text-gray-600">学号</label>
            <input :value="profile.student_id" disabled class="w-full rounded border bg-gray-50 px-3 py-2 text-sm" />
          </div>
        </div>

        <div class="space-y-4">
          <div v-for="sel in [
            { key: 'grade', label: '年级', options: GRADES },
            { key: 'gender', label: '性别', options: ['男', '女'] },
            { key: 'college', label: '学院', options: COLLEGES },
          ]" :key="sel.key">
            <label class="mb-1 block text-sm text-gray-600">{{ sel.label }}</label>
            <select v-model="(profile as any)[sel.key]" class="w-full rounded border border-gray-300 px-3 py-2 text-sm">
              <option v-for="o in sel.options" :key="o" :value="o">{{ o }}</option>
            </select>
          </div>
          <div>
            <label class="mb-1 block text-sm text-gray-600">专业</label>
            <input v-model="profile.major" class="w-full rounded border border-gray-300 px-3 py-2 text-sm" />
          </div>
        </div>
      </div>

      <div class="mt-8 flex flex-wrap justify-center gap-4">
        <button type="button" class="proto-btn-primary min-w-[100px]" :disabled="saving" @click="handleSave">
          {{ saving ? '保存中...' : '保存' }}
        </button>
        <button type="button" class="proto-btn-primary min-w-[100px]" @click="showPasswordDialog = true">修改密码</button>
        <button type="button" class="proto-btn-primary min-w-[100px]" @click="handleLogout">登出账号</button>
        <button type="button" class="proto-btn-primary min-w-[100px]" @click="showDeleteConfirm = true">注销账号</button>
      </div>
    </div>

    <Dialog :open="showPasswordDialog" title="修改密码" @close="showPasswordDialog = false">
      <div class="space-y-3">
        <input v-model="passwordForm.old_password" type="password" placeholder="现有密码" class="w-full rounded border px-3 py-2 text-sm" />
        <input v-model="passwordForm.new_password" type="password" placeholder="新密码" class="w-full rounded border px-3 py-2 text-sm" />
        <input v-model="passwordForm.confirm_password" type="password" placeholder="确认新密码" class="w-full rounded border px-3 py-2 text-sm" />
      </div>
      <template #footer>
        <button type="button" class="proto-btn-outline" @click="showPasswordDialog = false">取消</button>
        <button type="button" class="proto-btn-primary" :disabled="passwordLoading" @click="handleChangePassword">确认修改</button>
      </template>
    </Dialog>

    <ConfirmDialog
      :open="showDeleteConfirm"
      title="注销账号"
      message="账号注销后所有数据不可恢复，确定要注销吗？"
      destructive
      :loading="deleteLoading"
      @close="showDeleteConfirm = false"
      @confirm="handleDeleteAccount"
    />
  </div>
</template>
