<template>
  <div class="flex h-screen">
    <AdminSidebar />
    <main class="flex-1 overflow-y-auto bg-blue-600 p-8">
      <div class="max-w-7xl mx-auto">
        <div class="mb-4">
          <AppButton variant="link" @click="goBack" class="text-white">
            <iconify-icon icon="ph:arrow-left-bold"></iconify-icon> 返回
          </AppButton>
        </div>

        <AppCard :loading="loading">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-800">活动审核详情</h2>
            <span class="px-3 py-1 rounded-full text-sm" :class="statusColorClass(activity.status)">
              {{ statusText(activity.status) }}
            </span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-5 mb-8">
            <div><label class="block text-sm font-medium text-gray-700">活动名称</label><input type="text" v-model="activity.name" class="w-full border rounded-lg px-3 py-2 bg-gray-50" readonly></div>
            <div><label class="block text-sm font-medium text-gray-700">分类</label><input type="text" v-model="activity.category_name" class="w-full border rounded-lg px-3 py-2 bg-gray-50" readonly></div>
            <div><label class="block text-sm font-medium text-gray-700">组织者</label><input type="text" v-model="activity.organizer_name" class="w-full border rounded-lg px-3 py-2 bg-gray-50" readonly></div>
            <div><label class="block text-sm font-medium text-gray-700">开始时间</label><input type="text" :value="formatDateTime(activity.start_time)" class="w-full border rounded-lg px-3 py-2 bg-gray-50" readonly></div>
            <div><label class="block text-sm font-medium text-gray-700">结束时间</label><input type="text" :value="formatDateTime(activity.end_time)" class="w-full border rounded-lg px-3 py-2 bg-gray-50" readonly></div>
            <div><label class="block text-sm font-medium text-gray-700">校区</label><input type="text" v-model="activity.campus" class="w-full border rounded-lg px-3 py-2 bg-gray-50" readonly></div>
            <div><label class="block text-sm font-medium text-gray-700">地点</label><input type="text" v-model="activity.location" class="w-full border rounded-lg px-3 py-2 bg-gray-50" readonly></div>
            <div><label class="block text-sm font-medium text-gray-700">人数上限</label><input type="text" v-model="activity.max_participants" class="w-full border rounded-lg px-3 py-2 bg-gray-50" readonly></div>
            <div><label class="block text-sm font-medium text-gray-700">报名截止时间</label><input type="text" :value="formatDateTime(activity.registration_deadline)" class="w-full border rounded-lg px-3 py-2 bg-gray-50" readonly></div>
            <div><label class="block text-sm font-medium text-gray-700">取消报名截止时间</label><input type="text" :value="formatDateTime(activity.cancel_deadline)" class="w-full border rounded-lg px-3 py-2 bg-gray-50" readonly></div>
            <div><label class="block text-sm font-medium text-gray-700">报名人数</label><input type="text" v-model="activity.current_participants" class="w-full border rounded-lg px-3 py-2 bg-gray-50" readonly></div>
            <div><label class="block text-sm font-medium text-gray-700">签到人数</label><input type="text" v-model="activity.checked_in_count" class="w-full border rounded-lg px-3 py-2 bg-gray-50" readonly></div>
            <div class="md:col-span-2"><label class="block text-sm font-medium text-gray-700">活动简介</label><textarea v-model="activity.description" rows="3" class="w-full border rounded-lg px-3 py-2 bg-gray-50" readonly></textarea></div>
          </div>

          <div class="flex gap-3 pt-4 border-t" v-if="activity.status === 'pending' || activity.status === 'edit_pending'">
            <AppButton variant="blue" @click="approve">通过</AppButton>
            <AppButton variant="destructive" @click="openRejectModal">拒绝</AppButton>
          </div>
          
          <!-- 已审核且未开始的活动：显示下架按钮 -->
          <div class="flex gap-3 pt-4 border-t" v-if="(activity.status === 'open' || activity.status === 'ongoing') && !isActivityStarted">
            <AppButton variant="destructive" @click="openRemoveModal">下架</AppButton>
          </div>
        </AppCard>

        <AppDialog v-model:open="rejectModalVisible" title="拒绝理由" confirm-text="确认拒绝" cancel-text="取消" @confirm="confirmReject">
          <textarea v-model="rejectReason" rows="3" placeholder="请输入拒绝理由" class="w-full border rounded-lg px-3 py-2"></textarea>
        </AppDialog>

        <AppDialog v-model:open="removeModalVisible" title="下架理由" confirm-text="确认下架" cancel-text="取消" @confirm="confirmRemove">
          <textarea v-model="removeReason" rows="3" placeholder="请输入下架理由" class="w-full border rounded-lg px-3 py-2"></textarea>
        </AppDialog>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AdminSidebar from '@/components/layout/AdminSidebar.vue'
import AppPageContainer from '@/components/layout/AppPageContainer.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppButton from '@/components/common/AppButton.vue'
import AppDialog from '@/components/layout/AppDialog.vue'
import { getActivityDetail, reviewActivity, removeActivity } from '@/api/admin'
import { showApiError } from '@/api/request'
import { formatDateTime } from '@/utils'

const router = useRouter()
const route = useRoute()
const activityId = Number(route.params.id)
const loading = ref(false)

const activity = reactive({
  activity_id: 0,
  name: '',
  category_name: '',
  organizer_name: '',
  start_time: '',
  end_time: '',
  campus: '',
  location: '',
  max_participants: 0,
  current_participants: 0,
  registration_deadline: '',
  cancel_deadline: '',
  description: '',
  status: '',
  checked_in_count: 0
})

// 判断活动是否已开始
const isActivityStarted = computed(() => {
  if (!activity.start_time) return false
  const startDate = new Date(activity.start_time)
  return startDate <= new Date()
})

const statusText = (status: string) => {
  const map: Record<string, string> = { 
    pending: '审核中', 
    edit_pending: '修改待审核',  
    open: '已通过',
    ongoing: '进行中',
    ended: '已结束',
    rejected: '已拒绝', 
    removed: '已下架' 
  }
  return map[status] || status
}

const statusColorClass = (status: string) => {
  const map: Record<string, string> = { 
    pending: 'bg-yellow-100 text-yellow-700',
    edit_pending: 'bg-orange-100 text-orange-700',
    open: 'bg-green-100 text-green-700',
    ongoing: 'bg-blue-100 text-blue-700',
    ended: 'bg-gray-100 text-gray-700',
    rejected: 'bg-red-100 text-red-700', 
    removed: 'bg-gray-100 text-gray-700' 
  }
  return map[status] || 'bg-gray-100'
}

const fetchActivityDetail = async () => {
  loading.value = true
  try {
    const data = await getActivityDetail(activityId) as any
    activity.activity_id = data.activity_id
    activity.name = data.name
    activity.category_name = data.category_name
    activity.organizer_name = data.organizer_name
    activity.start_time = data.start_time
    activity.end_time = data.end_time
    activity.campus = data.campus
    activity.location = data.location
    activity.max_participants = data.max_participants
    activity.current_participants = data.current_participants
    activity.registration_deadline = data.registration_deadline
    activity.cancel_deadline = data.cancel_deadline
    activity.description = data.description
    activity.status = data.status
    activity.checked_in_count = data.checked_in_count || 0
  } catch (e) {
    showApiError(e, '获取活动详情失败')
  } finally {
    loading.value = false
  }
}

const approve = async () => {
  if (!confirm('确定通过该活动吗？')) return
  try {
    await reviewActivity(activityId, 'approve')
    alert('审核通过')
    router.push('/admin/audit')
  } catch (e) { 
    showApiError(e, '审核失败') 
  }
}

const rejectModalVisible = ref(false)
const rejectReason = ref('')
const openRejectModal = () => { 
  rejectReason.value = '' 
  rejectModalVisible.value = true 
}
const confirmReject = async () => {
  if (!rejectReason.value.trim()) { 
    alert('请填写拒绝理由')
    return 
  }
  try {
    await reviewActivity(activityId, 'reject', rejectReason.value)
    alert('已拒绝')
    router.push('/admin/audit')
  } catch (e) { 
    showApiError(e, '拒绝失败') 
  }
}

const removeModalVisible = ref(false)
const removeReason = ref('')
const openRemoveModal = () => { 
  removeReason.value = '' 
  removeModalVisible.value = true 
}
const confirmRemove = async () => {
  if (!removeReason.value.trim()) { 
    alert('请填写下架理由')
    return 
  }
  try {
    await removeActivity(activityId, removeReason.value)
    alert('活动已下架')
    router.push('/admin/audit')
  } catch (e) { 
    showApiError(e, '下架失败') 
  }
}

const goBack = () => router.back()

onMounted(() => {
  fetchActivityDetail()
})
</script>