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
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold text-gray-800">签到管理 - 活动ID: {{ activityId }}</h2>
            <AppButton variant="blue" @click="openManualSignModal">手动签到</AppButton>
          </div>
          <div class="bg-gray-50 rounded-lg p-4 mb-6 grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
            <div>👥 已签到：{{ checkedInCount }} / {{ totalRegistered }}</div>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500">学号</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500">学院</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500">专业</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500">年级</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500">签到时间</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="sign in signRecords" :key="sign.userId">
                  <td class="px-6 py-4 text-sm text-gray-900">{{ sign.studentId }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ sign.college }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ sign.major }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ sign.grade }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500">
                    <span v-if="sign.checkinTime" class="text-green-600">{{ formatDateTime(sign.checkinTime) }}</span>
                  </td>
                </tr>
                <tr v-if="!loading && signRecords.length === 0">
                  <td colspan="5" class="text-center py-12 text-gray-400">暂无签到记录</td>
                </tr>
              </tbody>
            </table>
          </div>
        </AppCard>

        <AppDialog v-model:open="manualSignModalVisible" title="手动签到" confirm-text="确认签到" cancel-text="取消" @confirm="confirmManualSign">
          <input v-model="manualStudentId" placeholder="请输入学号" class="w-full border rounded px-3 py-2">
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
import { getActivityCheckins, manualCheckin } from '@/api/organizer'
import { showApiError } from '@/api/request'
import OrganizerSidebar from '@/components/layout/OrganizerSidebar.vue'
import {formatDateTime } from '@/utils'
const router = useRouter()
const route = useRoute()
const activityId = Number(route.query.activityId)
const loading = ref(false)
const totalRegistered = ref(0)
const checkedInCount = ref(0)
const signRecords = ref<any[]>([])

const fetchSignRecords = async () => {
  if (!activityId) return
  loading.value = true
  try {
    const data = await getActivityCheckins(activityId)
    totalRegistered.value = data.total_registered
    checkedInCount.value = data.checked_in
    signRecords.value = data.checkin_list.map((c: any) => ({
      userId: c.user_id,
      studentId: c.student_id,
      college: c.college,
      major: c.major,
      grade: c.grade,
      checkinTime: c.checkin_time
    }))
  } catch (e) {
    showApiError(e, '获取签到记录失败')
  } finally {
    loading.value = false
  }
}

const manualSignModalVisible = ref(false)
const manualStudentId = ref('')
const openManualSignModal = () => {
  manualStudentId.value = ''
  manualSignModalVisible.value = true
}
const confirmManualSign = async () => {
  if (!manualStudentId.value.trim()) {
    alert('请输入学号')
    return
  }
  try {
    await manualCheckin(activityId, manualStudentId.value)
    alert('签到成功')
    await fetchSignRecords()
    manualSignModalVisible.value = false
  } catch (e) {
    showApiError(e, '签到失败')
  }
}
const goBack = () => router.back()

onMounted(() => {
  fetchSignRecords()
})
</script>