<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { User, Lock, Mail, Phone } from 'lucide-vue-next'
import { AppCard, AppForm, AppPageContainer } from '@/components'
import type { FormField } from '@/components/layout/AppForm.vue'
import { register } from '@/api/auth'
import { showApiError } from '@/api/request'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import { toast } from '@/composables/useToast'
import { COLLEGES, GRADES } from '@/utils/constants'
import { isStudentId, isEmail, isUsername, isPassword, isPhone } from '@/utils/validators'

const router = useRouter()
const auth = useAuthStore()
const userStore = useUserStore()
const agreed = ref(false)
const loading = ref(false)

const extra = ref({ gender: '男', college: '', grade: '' })

const fields: FormField[] = [
  { name: 'student_id', label: '学号', required: true, leftIcon: User },
  { name: 'email', label: '邮箱', type: 'email', required: true, leftIcon: Mail },
  { name: 'username', label: '用户名', required: true, leftIcon: User },
  { name: 'phone', label: '联系方式（选填）', leftIcon: Phone },
  { name: 'major', label: '专业', required: true },
  { name: 'password', label: '密码', type: 'password', required: true, leftIcon: Lock },
  {
    name: 'confirm_password',
    label: '确认密码',
    type: 'password',
    required: true,
    leftIcon: Lock,
    rules: [(v, d) => v === d?.password || '两次密码不一致'],
  },
]

async function handleRegister(values: Record<string, string>) {
  if (!agreed.value) {
    toast.error('请同意服务条款')
    return
  }
  const payload: Record<string, string> = { ...values, ...extra.value }
  if (!isStudentId(payload.student_id)) return toast.error('学号须为10位数字')
  if (!isEmail(payload.email)) return toast.error('邮箱格式错误')
  if (!isUsername(payload.username)) return toast.error('用户名格式错误')
  if (!isPassword(payload.password)) return toast.error('密码须6-20位')
  if (!extra.value.college || !extra.value.grade || !payload.major) return toast.error('请完善学院/年级/专业')
  if (!isPhone(payload.phone || '')) return toast.error('手机号格式错误')

  loading.value = true
  try {
    const reg = await register({
      student_id: payload.student_id,
      email: payload.email,
      username: payload.username,
      password: payload.password,
      confirm_password: payload.confirm_password,
      gender: extra.value.gender,
      college: extra.value.college,
      major: payload.major,
      grade: extra.value.grade,
      phone: payload.phone ? payload.phone : null,
    })
    auth.setAuth(reg.token, reg.userId, "user")
    await userStore.fetchProfile()
    toast.success('注册成功，已自动登录')
    router.push('/activities')
  } catch (e) {
    showApiError(e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <AppPageContainer
    variant="gradient"
    :show-grid="true"
    :show-glow="false"
    padding="md"
    max-width="lg"
    class="py-8"
  >
    <AppCard rounded="2xl" class="w-full">
      <h1 class="mb-5 text-center text-lg font-semibold text-blue-600">用户注册</h1>

      <div class="mb-4 grid gap-3 sm:grid-cols-2">
        <div>
          <label class="mb-1 block text-xs text-gray-600">性别</label>
          <select v-model="extra.gender" class="material-input">
            <option value="男">男</option>
            <option value="女">女</option>
          </select>
        </div>
        <div>
          <label class="mb-1 block text-xs text-gray-600">学院</label>
          <select v-model="extra.college" class="material-input">
            <option value="">请选择</option>
            <option v-for="c in COLLEGES" :key="c" :value="c">{{ c }}</option>
          </select>
        </div>
        <div class="sm:col-span-2">
          <label class="mb-1 block text-xs text-gray-600">年级</label>
          <select v-model="extra.grade" class="material-input">
            <option value="">请选择</option>
            <option v-for="g in GRADES" :key="g" :value="g">{{ g }}</option>
          </select>
        </div>
      </div>

      <AppForm
        :fields="fields"
        :columns="2"
        layout="grid"
        gap="sm"
        submit-text="注册"
        submit-variant="blue"
        :submit-full-width="true"
        :loading="loading"
        @submit="handleRegister"
      />

      <label class="mt-3 flex items-center gap-2 text-xs text-muted-foreground">
        <input v-model="agreed" type="checkbox" class="rounded" />
        我已阅读并同意服务条款、隐私条款
      </label>

      <p class="mt-4 text-center">
        <RouterLink to="/login" class="text-sm text-muted-foreground hover:text-blue-600">
          返回上一级页面
        </RouterLink>
      </p>
    </AppCard>
  </AppPageContainer>
</template>
