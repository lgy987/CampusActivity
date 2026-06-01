<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getActivityDetail } from '@/api/activities'
import { registerActivity, cancelRegistration } from '@/api/registrations'
import { checkin } from '@/api/checkin'
import { showApiError } from '@/api/request'
import type { ActivityDetail } from '@/types/api'
import { formatDateTime } from '@/utils'
import { toast } from '@/composables/useToast'
import ConfirmDialog from '@/components/ui/ConfirmDialog.vue'
import CheckinDialog from '@/components/ui/CheckinDialog.vue'
import { ArrowLeft } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const activityId = Number(route.params.id)

const activity = ref<ActivityDetail | null>(null)
const loading = ref(true)
const actionLoading = ref(false)
const checkinLoading = ref(false)
const showCancelConfirm = ref(false)
const showCheckinDialog = ref(false)

const canRegister = computed(() => {
  const a = activity.value
  if (!a || (a.status !== 'open' && a.status !== 'edit_pending')) return false
  if (a.is_registered) return false
  // 只有永久封禁的用户不能报名
  // 被拒绝（rejected）的用户可以报名，会显示"重新报名"按钮
  return a.registration_status !== 'blocked'
})

const canCancel = computed(() => {
  const a = activity.value
  if (!a) return false
  // 活动必须是报名中状态或修改待审核状态（仍然允许取消报名）
  const isOpen = a.status === 'open' || a.status === 'edit_pending'
  // 用户已报名，且报名状态是有效的（registered 或 re_registered）
  const isActive = a.is_registered === true && 
    (a.registration_status === 'registered' || a.registration_status === 're_registered')
  return isOpen && isActive
})


function isCheckedIn(a: ActivityDetail) {
  return a.check_status === true || a.check_status === 'true'
}

const durationText = computed(() => {
  if (!activity.value) return '-'
  const start = new Date(activity.value.start_time.replace(/-/g, '/'))
  const end = new Date(activity.value.end_time.replace(/-/g, '/'))
  const hours = Math.round((end.getTime() - start.getTime()) / 3600000)
  return hours >= 1 ? `${hours}小时` : '不足1小时'
})

onMounted(loadDetail)

async function loadDetail() {
  loading.value = true
  try {
    activity.value = await getActivityDetail(activityId)
  } catch (e) {
    showApiError(e)
    router.push('/activities')
  } finally {
    loading.value = false
  }
}

async function handleRegister() {
  if (!activity.value) return
  actionLoading.value = true
  try {
    const res = await registerActivity(activity.value.activity_id)
    toast.success('报名成功')
    activity.value.is_registered = true
    activity.value.registration_status = res.status
    activity.value.current_participants = activity.value.max_participants - res.remaining_slots
  } catch (e) {
    showApiError(e)
  } finally {
    actionLoading.value = false
  }
}

async function handleCancel() {
  if (!activity.value) return
  actionLoading.value = true
  try {
    await cancelRegistration(activity.value.activity_id)
    toast.success('取消成功，名额将在2分钟后释放')
    activity.value.is_registered = false
    activity.value.registration_status = 'cancelled'
    showCancelConfirm.value = false
    setTimeout(() => {
      loadDetail()
    }, 120000)
  } catch (e) {
    showApiError(e)
  } finally {
    actionLoading.value = false
  }
}

async function handleCheckin(code: string) {
  if (!code.trim()) {
    toast.error('请输入签到码')
    return
  }
  checkinLoading.value = true
  try {
    const res = await checkin(activityId, code.trim())
    toast.success(`签到成功！${formatDateTime(res.checkin_time)}`)
    if (activity.value) activity.value.check_status = true
    showCheckinDialog.value = false
  } catch (e) {
    showApiError(e)
  } finally {
    checkinLoading.value = false
  }
}
</script>

<template>
  <div class="mx-auto max-w-6xl">
    <button
      type="button"
      class="mb-4 flex items-center text-white hover:opacity-80"
      @click="router.push('/activities')"
    >
      <ArrowLeft class="mr-1 h-5 w-5" /> 返回
    </button>

    <div v-if="loading" class="py-16 text-center text-white">加载中...</div>

    <template v-else-if="activity">
      <div class="mb-4 rounded bg-white/90 px-6 py-2 text-center text-gray-800">活动详情</div>

      <div class="flex flex-col gap-4 lg:flex-row">
        <!-- 左侧基本信息 -->
        <div class="proto-card w-full shrink-0 p-5 lg:w-80">
          <h3 class="mb-4 flex items-center gap-2 border-l-4 border-[var(--proto-blue)] pl-2 font-semibold">
            活动基本信息
          </h3>
          <dl class="space-y-2.5 text-sm">
            <div class="flex justify-between gap-2">
              <dt class="text-gray-500">活动名称</dt>
              <dd class="text-right font-medium">{{ activity.name }}</dd>
            </div>
            <div class="flex justify-between"><dt class="text-gray-500">活动ID</dt><dd>{{ String(activity.activity_id).padStart(3, '0') }}</dd></div>
            <div class="flex justify-between"><dt class="text-gray-500">活动分类</dt><dd>{{ activity.category_name }}</dd></div>
            <div class="flex justify-between"><dt class="text-gray-500">举办单位</dt><dd>{{ activity.organizer_name }}</dd></div>
            <div class="flex justify-between"><dt class="text-gray-500">开始时间</dt><dd>{{ formatDateTime(activity.start_time) }}</dd></div>
            <div class="flex justify-between"><dt class="text-gray-500">结束时间</dt><dd>{{ formatDateTime(activity.end_time) }}</dd></div>
            <div class="flex justify-between"><dt class="text-gray-500">校区</dt><dd>{{ activity.campus }}校区</dd></div>
            <div class="flex justify-between"><dt class="text-gray-500">地点</dt><dd>{{ activity.location }}</dd></div>
            <div class="flex justify-between">
              <dt class="text-gray-500">当前/最大人数</dt>
              <dd>{{ activity.current_participants }}/{{ activity.max_participants }}</dd>
            </div>
            <div class="flex justify-between"><dt class="text-gray-500">报名截止</dt><dd class="text-xs">{{ formatDateTime(activity.registration_deadline) }}</dd></div>
            <div class="flex justify-between"><dt class="text-gray-500">取消截止</dt><dd class="text-xs">{{ formatDateTime(activity.cancel_deadline) }}</dd></div>
          </dl>
          
          <!-- 按钮区域 -->
          <div class="mt-6 flex gap-3">
            <!-- 可以报名（未报名且未被封禁） -->
            <button
              v-if="canRegister"
              type="button"
              class="proto-btn-outline flex-1"
              :disabled="actionLoading"
              @click="handleRegister"
            >
              报名
            </button>
            <!-- 可以取消报名 -->
            <button
              v-else-if="canCancel"
              type="button"
              class="proto-btn-outline flex-1"
              :disabled="actionLoading"
              @click="showCancelConfirm = true"
            >
              取消报名
            </button>
            <!-- 被拒绝（rejected）可以重新报名 -->
            <button
              v-else-if="activity.registration_status === 'rejected'"
              type="button"
              class="proto-btn-outline flex-1"
              :disabled="actionLoading"
              @click="handleRegister"
            >
              重新报名
            </button>
            <!-- 永久封禁 -->
            <button
              v-else-if="activity.registration_status === 'blocked'"
              type="button"
              class="proto-btn-outline flex-1 opacity-50"
              disabled
            >
              已被禁止报名
            </button>
            <!-- 活动已截止或其他情况 -->
            <button
              v-else
              type="button"
              class="proto-btn-outline flex-1 opacity-50"
              disabled
            >
              已截止
            </button>
            
            <!-- 签到按钮 -->
            <button
              type="button"
              class="proto-btn-outline flex-1"
              :disabled="activity && isCheckedIn(activity)"
              @click="showCheckinDialog = true"
            >
              {{ activity && isCheckedIn(activity) ? '已签到' : '签到' }}
            </button>
          </div>
        </div>

        <!-- 右侧简介 -->
        <div class="proto-card flex-1 p-6">
          <p class="mb-2 text-sm font-medium text-gray-600">正文：</p>
          <p class="whitespace-pre-wrap text-sm leading-relaxed text-gray-700">{{ activity.description }}</p>
        </div>
      </div>
    </template>

    <ConfirmDialog
      :open="showCancelConfirm"
      title="取消报名"
      message="确认取消报名吗？"
      destructive
      :loading="actionLoading"
      @close="showCancelConfirm = false"
      @confirm="handleCancel"
    />
    <CheckinDialog
      :open="showCheckinDialog"
      :loading="checkinLoading"
      @close="showCheckinDialog = false"
      @confirm="handleCheckin"
    />
  </div>
</template>