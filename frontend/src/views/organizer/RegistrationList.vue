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

        <AppCard :loading="loading">
          <div class="flex items-center gap-4 mb-6">
            <h2 class="text-xl font-bold text-gray-800">报名管理 - 活动ID: {{ activityId }}</h2>
          </div>
          <div class="bg-gray-50 rounded-lg p-4 mb-6 grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
            <div>👥 报名人数：{{ totalRegistered }}</div>
          </div>

          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500">学号</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500">学院</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500">专业</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500">年级</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500">报名时间</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500">操作</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="reg in registrations" :key="reg.id">
                  <td class="px-6 py-4 text-sm text-gray-900">{{ reg.studentId }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ reg.college }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ reg.major }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ reg.grade }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ formatDateTime(reg.registeredAt) }}</td>
                  <td class="px-6 py-4">
                    <AppButton size="sm" variant="destructive" @click="openRejectModal(reg.id)">拒绝</AppButton>
                  </td>
                </tr>
                <tr v-if="!loading && registrations.length === 0">
                  <td colspan="6" class="text-center py-12 text-gray-400">暂无报名记录</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-if="totalPages > 1" class="flex justify-center mt-6 gap-2">
            <button v-for="p in totalPages" :key="p" @click="goToPage(p)" class="px-3 py-1 rounded border" :class="p === currentPage ? 'bg-blue-600 text-white' : 'text-gray-700'">{{ p }}</button>
          </div>
        </AppCard>

        <AppDialog v-model:open="rejectModalVisible" title="拒绝报名" confirm-text="确认拒绝" cancel-text="取消" @confirm="confirmReject">
          <textarea v-model="rejectReason" rows="3" placeholder="请输入拒绝理由" class="w-full border rounded-lg px-3 py-2"></textarea>
        </AppDialog>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AppPageContainer from '@/components/layout/AppPageContainer.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppButton from '@/components/common/AppButton.vue'
import AppDialog from '@/components/layout/AppDialog.vue'
import { getActivityRegistrations, rejectRegistration } from '@/api/organizer'
import { showApiError } from '@/api/request'
import OrganizerSidebar from '@/components/layout/OrganizerSidebar.vue'
import { formatDateTime } from '@/utils'

const router = useRouter()
const route = useRoute()
const activityId = Number(route.query.activityId)
const loading = ref(false)
const totalRegistered = ref(0)
const registrations = ref<any[]>([])
const currentPage = ref(1)
const totalPages = ref(1)
const pageSize = 10

const fetchRegistrations = async () => {
  if (!activityId) return
  loading.value = true
  try {
    const data = await getActivityRegistrations(activityId, { page: currentPage.value, page_size: pageSize })
    registrations.value = data.list.map((r: any) => ({
      id: r.registration_id,
      studentId: r.student_id,
      college: r.college,
      major: r.major,
      grade: r.grade,
      registeredAt: r.registration_time
    }))
    totalPages.value = Math.ceil(data.total / pageSize)
    totalRegistered.value = data.total
  } catch (e) {
    showApiError(e, '获取报名列表失败')
  } finally {
    loading.value = false
  }
}

const rejectModalVisible = ref(false)
const rejectReason = ref('')
let currentRejectId: number | null = null

const openRejectModal = (id: number) => {
  currentRejectId = id
  rejectReason.value = ''
  rejectModalVisible.value = true
}
const confirmReject = async () => {
  if (!rejectReason.value.trim()) { alert('请填写拒绝理由'); return }
  try {
    await rejectRegistration(currentRejectId!, rejectReason.value)
    alert('已拒绝该报名')
    await fetchRegistrations()
  } catch (e) {
    showApiError(e, '拒绝失败')
  }
  rejectModalVisible.value = false
}
const goBack = () => router.back()
const goToPage = (page: number) => {
  currentPage.value = page
  fetchRegistrations()
}

onMounted(() => {
  fetchRegistrations()
})
</script>