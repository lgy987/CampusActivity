<template>
  <div class="flex h-screen">
    <OrganizerSidebar />
    <main class="flex-1 overflow-y-auto bg-blue-600 p-8">
      <div class="max-w-7xl mx-auto">
        <div class="mb-4">
          <AppButton variant="link" @click="goBack" class="text-white">
            <iconify-icon icon="ph:arrow-left-bold"></iconify-icon> 返回
          </AppButton>
        </div>

        <AppCard>
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-800">{{ isEdit ? '编辑活动' : '创建活动' }}</h2>
            <span class="px-3 py-1 rounded-full text-sm" :class="statusColorClass(activityData.status)">
              {{ statusText(activityData.status) }}
            </span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">活动名称</label>
              <input type="text" v-model="formData.name" class="w-full border rounded-lg px-3 py-2">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">分类</label>
              <select v-model="formData.category_id" class="w-full border rounded-lg px-3 py-2">
                <option v-for="cat in categoryOptions" :key="cat.value" :value="cat.value">{{ cat.label }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">开始时间</label>
              <input type="datetime-local" v-model="formData.start_time" class="w-full border rounded-lg px-3 py-2">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">结束时间</label>
              <input type="datetime-local" v-model="formData.end_time" class="w-full border rounded-lg px-3 py-2">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">校区</label>
              <select v-model="formData.campus" class="w-full border rounded-lg px-3 py-2">
                <option value="">请选择校区</option>
                <option value="良乡">良乡</option>
                <option value="中关村">中关村</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">地点</label>
              <input type="text" v-model="formData.location" class="w-full border rounded-lg px-3 py-2">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">人数上限</label>
              <input type="number" v-model="formData.max_participants" min="1" class="w-full border rounded-lg px-3 py-2">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">报名截止时间</label>
              <input type="datetime-local" v-model="formData.registration_deadline" class="w-full border rounded-lg px-3 py-2">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">取消报名截止时间</label>
              <input type="datetime-local" v-model="formData.cancel_deadline" class="w-full border rounded-lg px-3 py-2">
            </div>
            <div class="col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">活动简介</label>
              <textarea v-model="formData.description" rows="3" class="w-full border rounded-lg px-3 py-2"></textarea>
            </div>
          </div>

          <div class="flex flex-wrap gap-3 pt-4 mt-4 border-t">
            <AppButton variant="blue" @click="handleSave" :disabled="saving">保存修改</AppButton>
            <AppButton variant="blue" @click="handleApplyReview" :disabled="!canApplyReview || submitting">申请审核</AppButton>
            <template v-if="isEdit && activityId">
              <AppButton variant="blue" @click="goToRegistrations">报名管理</AppButton>
              <AppButton variant="blue" @click="generateQRCode">生成签到码</AppButton>
              <AppButton variant="blue" @click="goToSignRecords">签到管理</AppButton>
              <AppButton variant="blue" @click="goToStats">数据统计</AppButton>
              <AppButton variant="destructive" @click="handleDelete" :disabled="!canDelete">删除活动</AppButton>
            </template>
          </div>
        </AppCard>

        <AppDialog v-model:open="qrDialogVisible" title="签到码" confirm-text="关闭" @confirm="qrDialogVisible = false">
          <div class="text-center py-4">
            <p class="text-2xl font-mono tracking-wider">{{ qrCode }}</p>
            <p class="text-sm text-gray-500 mt-2">有效期至活动结束</p>
          </div>
        </AppDialog>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AppCard from '@/components/common/AppCard.vue'
import AppButton from '@/components/common/AppButton.vue'
import AppDialog from '@/components/layout/AppDialog.vue'
import { createActivity, updateActivity, deleteActivity, submitActivity, getActivityDetail, getCategories, getCheckinCode } from '@/api/organizer'
import { showApiError } from '@/api/request'
import OrganizerSidebar from '@/components/layout/OrganizerSidebar.vue'

// 辅助函数：将后端 UTC 时间格式转换为 datetime-local 格式（本地时间）
const toDatetimeLocal = (dateStr: string): string => {
  if (!dateStr) return ''
  // 将 UTC 时间字符串转换为 Date 对象
  const date = new Date(dateStr)
  if (isNaN(date.getTime())) return ''
  
  // 获取本地时间的年月日时分
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  
  return `${year}-${month}-${day}T${hours}:${minutes}`
}

// 辅助函数：将 datetime-local 格式转换为 UTC 后端格式
const toBackendDateTime = (localStr: string): string => {
  if (!localStr) return ''
  // 将本地时间转换为 UTC 时间
  const date = new Date(localStr)
  const year = date.getUTCFullYear()
  const month = String(date.getUTCMonth() + 1).padStart(2, '0')
  const day = String(date.getUTCDate()).padStart(2, '0')
  const hours = String(date.getUTCHours()).padStart(2, '0')
  const minutes = String(date.getUTCMinutes()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}:00`
}

const router = useRouter()
const route = useRoute()
const activityId = computed(() => route.query.id ? Number(route.query.id) : null)
const isEdit = computed(() => !!activityId.value)

const formData = reactive({
  name: '',
  category_id: undefined as number | undefined,
  start_time: '',
  end_time: '',
  campus: '',
  location: '',
  max_participants: 0,
  registration_deadline: '',
  cancel_deadline: '',
  description: ''
})

const activityData = reactive({
  id: 0,
  status: '',
  current_participants: 0
})
const categoryOptions = ref<{ value: number; label: string }[]>([])

const isLoadingData = ref(false)
const isRegistrationManuallyChanged = ref(false)
const isCancelManuallyChanged = ref(false)
const isAutoUpdating = ref(false)
const saving = ref(false)
const submitting = ref(false)

// 重置表单
const resetForm = () => {
  formData.name = ''
  formData.category_id = undefined
  formData.start_time = ''
  formData.end_time = ''
  formData.campus = ''
  formData.location = ''
  formData.max_participants = 0
  formData.registration_deadline = ''
  formData.cancel_deadline = ''
  formData.description = ''
  activityData.id = 0
  activityData.status = ''
  activityData.current_participants = 0
  isRegistrationManuallyChanged.value = false
  isCancelManuallyChanged.value = false
  isAutoUpdating.value = false
}

// 监听报名截止时间手动修改
watch(() => formData.registration_deadline, (newVal, oldVal) => {
  if (isAutoUpdating.value) return
  if (!isLoadingData.value && oldVal !== undefined && newVal !== oldVal) {
    isRegistrationManuallyChanged.value = true
  }
})

// 监听取消报名截止时间手动修改
watch(() => formData.cancel_deadline, (newVal, oldVal) => {
  if (isAutoUpdating.value) return
  if (!isLoadingData.value && oldVal !== undefined && newVal !== oldVal) {
    isCancelManuallyChanged.value = true
  }
})

// 监听开始时间变化
watch(() => formData.start_time, (newStartTime) => {
  if (isLoadingData.value) return
  if (!newStartTime) return
  
  const startDate = new Date(newStartTime)
  const deadlineDate = new Date(startDate.getTime() - 60 * 60 * 1000)
  
  const year = deadlineDate.getFullYear()
  const month = String(deadlineDate.getMonth() + 1).padStart(2, '0')
  const day = String(deadlineDate.getDate()).padStart(2, '0')
  const hours = String(deadlineDate.getHours()).padStart(2, '0')
  const minutes = String(deadlineDate.getMinutes()).padStart(2, '0')
  
  const deadlineStr = `${year}-${month}-${day}T${hours}:${minutes}`
  
  isAutoUpdating.value = true
  
  if (!isRegistrationManuallyChanged.value) {
    formData.registration_deadline = deadlineStr
  }
  if (!isCancelManuallyChanged.value) {
    formData.cancel_deadline = deadlineStr
  }
  
  setTimeout(() => {
    isAutoUpdating.value = false
  }, 100)
})

const canSave = computed(() => true)
// 允许提交审核的状态：草稿、被拒绝
const canApplyReview = computed(() => 
  activityData.status === 'draft'
)
const canDelete = computed(() => !['ended', 'removed'].includes(activityData.status))

const statusText = (s: string) => {
  const map: Record<string, string> = {
    draft: '草稿', pending: '待审核', rejected: '审核未通过',
    open: '报名中', edit_pending: '修改审核中', ongoing: '进行中',
    ended: '已结束', removed: '已下架'
  }
  return map[s] || s
}

const statusColorClass = (s: string) => {
  const map: Record<string, string> = {
    draft: 'bg-gray-100 text-gray-700', pending: 'bg-yellow-100 text-yellow-700',
    rejected: 'bg-red-100 text-red-700', open: 'bg-green-100 text-green-700',
    edit_pending: 'bg-blue-100 text-blue-700', ongoing: 'bg-indigo-100 text-indigo-700',
    ended: 'bg-slate-100 text-slate-700', removed: 'bg-gray-100 text-gray-700'
  }
  return map[s] || 'bg-gray-100'
}

const fetchCategories = async () => {
  try {
    const data = await getCategories()
    const flat: { value: number; label: string }[] = []
    
    data.forEach((cat: any) => {
      flat.push({ value: cat.id, label: cat.name })
      if (cat.children && cat.children.length) {
        cat.children.forEach((child: any) => {
          flat.push({ 
            value: child.id, 
            label: `\u00A0\u00A0\u00A0\u00A0${child.name}`
          })
        })
      }
    })
    categoryOptions.value = flat
  } catch (e) {
    showApiError(e, '获取分类失败')
  }
}

const fetchActivityDetail = async () => {
  if (!isEdit.value) return
  isLoadingData.value = true  
  try {
    const id = activityId.value
    if (!id) return
    const data = await getActivityDetail(id)
    activityData.id = data.activity_id
    activityData.status = data.status
    activityData.current_participants = data.current_participants
    formData.name = data.name
    formData.category_id = data.category_id
    formData.start_time = toDatetimeLocal(data.start_time)
    formData.end_time = toDatetimeLocal(data.end_time)
    formData.campus = data.campus
    formData.location = data.location
    formData.max_participants = data.max_participants
    formData.registration_deadline = toDatetimeLocal(data.registration_deadline)
    formData.cancel_deadline = toDatetimeLocal(data.cancel_deadline)
    formData.description = data.description
    // 重置手动修改标志
    isRegistrationManuallyChanged.value = false
    isCancelManuallyChanged.value = false
    isAutoUpdating.value = false
  } catch (e) {
    console.error('获取活动详情失败:', e)
    showApiError(e, '获取活动详情失败')
  } finally {
    isLoadingData.value = false
  }
}

// 监听路由变化，只重置表单
watch(activityId, (newId) => {
  if (!newId) {
    resetForm()
  }
})

// 监听编辑状态和活动ID，加载数据
watch([isEdit, activityId], async ([edit, id]) => {
  if (edit && id) {
    await fetchActivityDetail()
  }
}, { immediate: true })

const handleSave = async () => {
  if (saving.value) return
  if (!formData.name) { alert('请填写活动名称'); return }
  if (!formData.category_id) { alert('请选择分类'); return }
  if (!formData.start_time) { alert('请选择开始时间'); return }
  if (!formData.end_time) { alert('请选择结束时间'); return }
  if (!formData.campus) { alert('请选择校区'); return }

  saving.value = true
  try {
    const payload = {
      name: formData.name,
      category_id: formData.category_id,
      start_time: toBackendDateTime(formData.start_time),
      end_time: toBackendDateTime(formData.end_time),
      campus: formData.campus,
      location: formData.location,
      max_participants: formData.max_participants,
      registration_deadline: toBackendDateTime(formData.registration_deadline),
      cancel_deadline: toBackendDateTime(formData.cancel_deadline),
      description: formData.description,
      save_as_draft: true
    }

    if (isEdit.value) {
      await updateActivity(activityId.value!, payload)
      alert('保存成功')
      await fetchActivityDetail()
    } else {
      const data = await createActivity(payload)
      console.log('创建活动成功:', data)
      alert('创建成功')
      router.replace(`/organizer/activity?id=${data.activity_id}`)
      setTimeout(() => {
        fetchActivityDetail()
      }, 100)
    }
  } catch (e: any) {
    console.error('保存失败:', e)
    if (e.response?.status === 405) {
      alert('活动状态不允许修改（可能已开始或已结束）')
    } else {
      showApiError(e, isEdit.value ? '保存失败' : '创建失败')
    }
  } finally {
    saving.value = false
  }
}

const handleApplyReview = async () => {
  if (!isEdit.value) {
    alert('请先保存活动后再提交审核')
    return
  }
  if (submitting.value) return
  
  submitting.value = true
  try {
    await submitActivity(activityId.value!)
    alert('已提交审核')
    await fetchActivityDetail()
  } catch (e) {
    console.error('提交审核失败:', e)
    showApiError(e, '提交审核失败')
  } finally {
    submitting.value = false
  }
}

const handleDelete = async () => {
  if (!confirm('确定删除该活动吗？')) return
  try {
    await deleteActivity(activityId.value!)
    alert('删除成功')
    router.push('/organizer/activities')
  } catch (e) {
    showApiError(e, '删除失败')
  }
}

const goToRegistrations = () => router.push(`/organizer/registrations?activityId=${activityId.value}`)
const goToSignRecords = () => router.push(`/organizer/signs?activityId=${activityId.value}`)
const goToStats = () => router.push(`/organizer/stats?activityId=${activityId.value}`)

const qrDialogVisible = ref(false)
const qrCode = ref('')
const generateQRCode = async () => {
  if (!activityId.value) return
  try {
    const data = await getCheckinCode(activityId.value)
    qrCode.value = data.checkin_code
    qrDialogVisible.value = true
  } catch (e) {
    showApiError(e, '获取签到码失败')
  }
}

// 修改返回函数：直接跳转到列表页
const goBack = () => {
  router.push('/organizer/activities')
}

onMounted(() => {
  fetchCategories()
})
</script>