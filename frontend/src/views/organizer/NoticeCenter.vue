<template>
  <div class="flex h-screen">
    <OrganizerSidebar />
    <main class="flex-1 overflow-y-auto bg-blue-600 p-8">
      <div class="max-w-7xl mx-auto">
        <div class="mb-6">
          <h1 class="text-3xl font-bold text-white">公告与消息中心</h1>
          <p class="text-white/70 mt-1">系统公告和个人通知</p>
        </div>

        <div class="flex gap-4 mb-6 border-b border-white/20">
          <button @click="activeTab = 'announcement'" class="pb-2 px-1 font-medium transition" :class="activeTab === 'announcement' ? 'text-blue-400 border-b-2 border-blue-400' : 'text-white/70 hover:text-white'">系统公告</button>
          <button @click="activeTab = 'message'" class="pb-2 px-1 font-medium transition" :class="activeTab === 'message' ? 'text-blue-400 border-b-2 border-blue-400' : 'text-white/70 hover:text-white'">我的消息 <span v-if="unreadCount > 0" class="ml-1 px-1.5 py-0.5 text-xs bg-red-500 text-white rounded-full">{{ unreadCount }}</span></button>
        </div>

        <div v-if="activeTab === 'announcement'">
          <AppCard :loading="loadingAnnouncement">
            <div class="space-y-4">
              <div v-for="ann in announcements" :key="ann.announcement_id" class="border-b pb-3">
                <h3 class="font-semibold text-gray-900">{{ ann.title }}</h3>
                <p class="text-xs text-gray-400 mt-1">{{ formatDateTime(ann.start_time) }}</p>
                <p class="text-sm text-gray-600 mt-1">{{ ann.content }}</p>
              </div>
              <div v-if="announcements.length === 0 && !loadingAnnouncement" class="text-center text-gray-400 py-8">暂无公告</div>
            </div>
            <div v-if="announcementTotalPages > 1" class="flex justify-center mt-6 gap-2">
              <button v-for="p in announcementTotalPages" :key="p" @click="goToAnnouncementPage(p)" class="px-3 py-1 rounded border" :class="p === announcementPage ? 'bg-blue-600 text-white' : 'text-gray-700'">{{ p }}</button>
            </div>
          </AppCard>
        </div>

        <div v-else>
          <AppCard :loading="loadingMessage">
            <div class="space-y-3">
              <div v-for="msg in messages" :key="msg.notification_id" class="p-3 rounded-lg border-l-4" :class="getMessageClass(msg)">
                <div class="flex justify-between items-start">
                  <div>
                    <div class="font-semibold text-gray-900">{{ msg.title }}</div>
                    <div class="text-xs text-gray-400 mt-1">{{ formatDateTime(msg.created_at) }}</div>
                    <div class="text-sm text-gray-700 mt-1">{{ msg.content }}</div>
                  </div>
                  <button v-if="!msg.is_read" @click="markAsRead(msg.notification_id)" class="text-blue-500 text-xs hover:underline">标记已读</button>
                </div>
              </div>
              <div v-if="messages.length === 0 && !loadingMessage" class="text-center text-gray-400 py-8">暂无消息</div>
            </div>
            <div class="flex justify-between items-center mt-4">
              <button v-if="unreadCount > 0" @click="markAllAsRead" class="text-sm text-blue-500 hover:underline">全部已读</button>
              <div v-if="messageTotalPages > 1" class="flex justify-center gap-2">
                <button v-for="p in messageTotalPages" :key="p" @click="goToMessagePage(p)" class="px-3 py-1 rounded border" :class="p === messagePage ? 'bg-blue-600 text-white' : 'text-gray-700'">{{ p }}</button>
              </div>
            </div>
          </AppCard>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppPageContainer from '@/components/layout/AppPageContainer.vue'
import AppCard from '@/components/common/AppCard.vue'
import { getNotifications, markNotificationRead, getAnnouncements } from '@/api/notifications'
import { showApiError } from '@/api/request'
import OrganizerSidebar from '@/components/layout/OrganizerSidebar.vue'
import { formatDateTime } from '@/utils'
const router = useRouter()
const activeTab = ref<'announcement' | 'message'>('announcement')
const loadingAnnouncement = ref(false)
const loadingMessage = ref(false)

const announcements = ref<any[]>([])
const announcementPage = ref(1)
const announcementTotalPages = ref(1)
const announcementPageSize = 10

const messages = ref<any[]>([])
const unreadCount = ref(0)
const messagePage = ref(1)
const messageTotalPages = ref(1)
const messagePageSize = 10

const fetchAnnouncements = async () => {
  loadingAnnouncement.value = true
  try {
    const data = await getAnnouncements()
    announcements.value = data
    announcementTotalPages.value = Math.ceil(data.length / announcementPageSize)
  } catch (e) {
    showApiError(e, '获取公告失败')
  } finally {
    loadingAnnouncement.value = false
  }
}
const fetchMessages = async () => {
  loadingMessage.value = true
  try {
    const data = await getNotifications({ page: messagePage.value, page_size: messagePageSize })
    messages.value = data.list
    unreadCount.value = data.unread_count
    messageTotalPages.value = Math.ceil(data.total / messagePageSize)
  } catch (e) {
    showApiError(e, '获取消息失败')
  } finally {
    loadingMessage.value = false
  }
}
const markAsRead = async (id: number) => {
  try {
    await markNotificationRead(id)
    const idx = messages.value.findIndex(m => m.notification_id === id)
    if (idx !== -1) {
      messages.value[idx].is_read = true
      unreadCount.value = messages.value.filter(m => !m.is_read).length
    }
    alert('已标记为已读')
  } catch (e) {
    showApiError(e, '操作失败')
  }
}
const markAllAsRead = () => {
  alert('请逐个标记已读')
}
const getMessageClass = (msg: any) => {
  if (msg.is_read) return 'bg-gray-50 border-l-gray-400'
  switch (msg.type) {
    case 'success': return 'bg-green-50 border-l-green-500'
    case 'error': return 'bg-red-50 border-l-red-500'
    default: return 'bg-blue-50 border-l-blue-500'
  }
}
const goToAnnouncementPage = (page: number) => { announcementPage.value = page; fetchAnnouncements() }
const goToMessagePage = (page: number) => { messagePage.value = page; fetchMessages() }

onMounted(() => {
  fetchAnnouncements()
  fetchMessages()
})
</script>