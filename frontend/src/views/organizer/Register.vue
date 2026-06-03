<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-xl w-full max-w-md p-6">
      <div class="text-center mb-6">
        <h1 class="text-2xl font-bold text-blue-600">CampusActivity</h1>
        <p class="text-gray-500 text-sm">组织者注册</p>
        <p class="text-xs text-gray-400 mt-1">申请发布活动权限，需管理员审核</p>
      </div>

      <form @submit.prevent="handleRegister">
        <!-- 邮箱 -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">邮箱 *</label>
          <input 
            type="email" 
            v-model="form.email" 
            required 
            class="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
            placeholder="org@example.com"
          >
          <p class="text-xs text-gray-400 mt-1">请使用合法邮箱，系统将校验唯一性</p>
        </div>

        <!-- 组织名称 -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">组织名称 *</label>
          <input 
            type="text" 
            v-model="form.org_name" 
            required 
            minlength="2" 
            maxlength="20" 
            class="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500" 
            placeholder="2-20位字符（字母/数字/中文）"
          >
          <p class="text-xs text-gray-400 mt-1">长度2-20，支持字母、数字、中文</p>
        </div>

        <!-- 密码 -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">密码 *</label>
          <input 
            type="password" 
            v-model="form.password" 
            required 
            minlength="6" 
            maxlength="20" 
            class="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500" 
            placeholder="6-20位字符"
          >
          <p class="text-xs text-gray-400 mt-1">6-20位，建议字母+数字组合（后端将加密存储）</p>
        </div>

        <!-- 确认密码 -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">确认密码 *</label>
          <input 
            type="password" 
            v-model="form.confirm_password" 
            required 
            class="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500" 
            placeholder="再次输入密码"
          >
        </div>

        <!-- 组织证明文字 -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">组织证明</label>
          <textarea 
            v-model="form.org_proof_text" 
            rows="3" 
            class="w-full border rounded-lg px-3 py-2" 
            placeholder="请描述组织身份、活动范围（可选）"
          ></textarea>
        </div>

        <!-- 组织证明图片（可选） -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">上传证明图片（可选）</label>
          <input 
            type="file" 
            ref="fileInput" 
            accept="image/jpeg,image/png" 
            @change="handleFileChange" 
            class="hidden"
          >
          <button 
            type="button" 
            @click="triggerFileInput" 
            class="w-full border border-dashed rounded-lg py-2 text-gray-500 hover:bg-gray-50"
            :disabled="uploading"
          >
            {{ uploading ? '上传中...' : '上传证明图片' }}
          </button>
          <p v-if="uploadedImageUrl" class="text-xs text-green-600 mt-1">✓ 已上传图片</p>
          <p v-else-if="form.org_proof_image" class="text-xs text-gray-500 mt-1">已选择：{{ form.org_proof_image }}</p>
          <p class="text-xs text-gray-400 mt-1">支持图片格式（jpg/png），大小不超过2MB</p>
        </div>

        <div class="text-xs text-gray-500 text-center mb-4">
          注册后需要管理员审核发布资质，审核通过后方可创建活动。
        </div>

        <AppButton type="submit" variant="blue" class="w-full" :loading="loading">
          提交注册申请
        </AppButton>

        <div class="text-center mt-4 text-sm">
          已有账号？
          <router-link to="/login" class="text-blue-600 hover:underline">立即登录</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppButton from '@/components/common/AppButton.vue'
import { registerOrganizer, uploadOrganizerProof } from '@/api/auth'

const router = useRouter()
const auth = useAuthStore()  // 使用 authStore
const loading = ref(false)
const uploading = ref(false)
const fileInput = ref<HTMLInputElement>()
const uploadedImageUrl = ref('')

const form = ref({
  email: '',
  org_name: '',
  password: '',
  confirm_password: '',
  org_proof_text: '',
  org_proof_image: ''
})

const handleFileChange = async (e: Event) => {
  const input = e.target as HTMLInputElement
  if (!input.files || !input.files[0]) return
  
  const file = input.files[0]
  
  if (file.size > 2 * 1024 * 1024) {
    alert('图片大小不能超过2MB')
    input.value = ''
    return
  }
  
  if (!['image/jpeg', 'image/png'].includes(file.type)) {
    alert('只支持 jpg/png 格式')
    input.value = ''
    return
  }
  
  uploading.value = true
  
  try {
    const formData = new FormData()
    formData.append('proof_image', file)
    
    const res = await uploadOrganizerProof(formData)
    uploadedImageUrl.value = res.image_url
    form.value.org_proof_image = res.image_url
    alert('图片上传成功')
  } catch (err: any) {
    console.error('上传失败:', err)
    const message = err.response?.data?.message || err.message || '图片上传失败，请重试'
    alert(message)
    input.value = ''
  } finally {
    uploading.value = false
  }
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleRegister = async () => {
  if (!form.value.email) {
    alert('请输入邮箱')
    return
  }
  if (!form.value.org_name) {
    alert('请输入组织名称')
    return
  }
  if (!form.value.password) {
    alert('请输入密码')
    return
  }
  if (form.value.password !== form.value.confirm_password) {
    alert('两次输入的密码不一致')
    return
  }
  if (form.value.password.length < 6) {
    alert('密码长度不能小于6位')
    return
  }

  loading.value = true
  try {
    const data = await registerOrganizer({
      email: form.value.email,
      org_name: form.value.org_name,
      password: form.value.password,
      confirm_password: form.value.confirm_password,
      org_proof_text: form.value.org_proof_text,
      org_proof_image: form.value.org_proof_image || undefined
    })
    
    console.log('注册响应:', data)
    auth.setAuth(data.token, data.userId, 'organizer')
    
    alert('注册成功，请等待管理员审核')
    router.push('/organizer/activities')
  } catch (err: any) {
    console.error('注册失败:', err)
    const message = err.response?.data?.message || err.message || '网络错误，请稍后重试'
    alert(message)
  } finally {
    loading.value = false
  }
}
</script>