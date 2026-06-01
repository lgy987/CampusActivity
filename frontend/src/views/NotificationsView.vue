<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue'
import { getNotifications, getAnnouncements, markNotificationRead } from '@/api/notifications'
import { showApiError } from '@/api/request'
import type { AnnouncementItem, NotificationItem } from '@/types/api'
import { formatDateTime } from '@/utils'
import SegmentedControl from '@/components/ui/SegmentedControl.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import AppPagination from '@/components/ui/AppPagination.vue'
import { Mail, MailOpen } from 'lucide-vue-next'

const tab = ref<'message' | 'announcement'>('message')
const messages = ref<NotificationItem[]>([])
const announcements = ref<AnnouncementItem[]>([])
const loading = ref(false)

// 消息分页
const messagePage = ref(1)
const messagePageSize = 10
const messageTotal = ref(0)

// 公告分页
const announcementPage = ref(1)
const announcementPageSize = 10
const announcementTotal = ref(0)

const showDetail = ref(false)
const detailTitle = ref('')
const detailTime = ref('')
const detailContent = ref('')

// 消息总页数
const messageTotalPages = computed(() => Math.ceil(messageTotal.value / messagePageSize))

// 公告总页数
const announcementTotalPages = computed(() => Math.ceil(announcementTotal.value / announcementPageSize))

onMounted(loadData)
watch(tab, () => {
  // 切换标签时重置页码
  if (tab.value === 'message') {
    messagePage.value = 1
  } else {
    announcementPage.value = 1
  }
  loadData()
})

async function loadData() {
  loading.value = true
  try {
    if (tab.value === 'announcement') {
      await loadAnnouncements()
    } else {
      await loadMessages()
    }
  } catch (e) {
    showApiError(e)
  } finally {
    loading.value = false
  }
}

async function loadMessages() {
  const data = await getNotifications({ 
    page: messagePage.value, 
    page_size: messagePageSize 
  })
  messages.value = data.list
  messageTotal.value = data.total
}

async function loadAnnouncements() {
  const allAnnouncements = await getAnnouncements()
  // 前端分页
  const start = (announcementPage.value - 1) * announcementPageSize
  const end = start + announcementPageSize
  announcements.value = allAnnouncements.slice(start, end)
  announcementTotal.value = allAnnouncements.length
}

async function openMessage(item: NotificationItem) {
  detailTitle.value = item.title
  detailTime.value = formatDateTime(item.created_at)
  detailContent.value = item.content
  showDetail.value = true
  if (!item.is_read) {
    try {
      await markNotificationRead(item.notification_id)
      item.is_read = true
    } catch {
      /* ignore */
    }
  }
}

function openAnnouncement(item: AnnouncementItem) {
  detailTitle.value = item.title
  detailTime.value = `${formatDateTime(item.start_time)} — ${formatDateTime(item.end_time)}`
  detailContent.value = item.content
  showDetail.value = true
}

// 分页切换
function handleMessagePageChange(page: number) {
  messagePage.value = page
  loadMessages()
}

function handleAnnouncementPageChange(page: number) {
  announcementPage.value = page
  loadAnnouncements()
}
</script>

<template>
  <div class="mx-auto max-w-4xl">
    <div class="proto-card overflow-hidden">
      <div class="border-b px-5 py-3">
        <SegmentedControl
          v-model="tab"
          :options="[
            { value: 'message', label: '活动通知' },
            { value: 'announcement', label: '系统通知' },
          ]"
        />
      </div>

      <div v-if="loading" class="py-16 text-center text-gray-500">加载中...</div>
      <EmptyState
        v-else-if="(tab === 'message' && !messages.length) || (tab === 'announcement' && !announcements.length)"
        message="暂无通知"
      />

      <div v-else>
        <div class="overflow-x-auto">
          <table class="proto-table">
            <thead>
              <tr>
                <th class="w-10"></th>
                <th>标题</th>
                <th>发送时间</th>
                <th v-if="tab === 'message'">状态</th>
              </tr>
            </thead>
            <tbody>
              <template v-if="tab === 'message'">
                <tr
                  v-for="item in messages"
                  :key="item.notification_id"
                  class="cursor-pointer"
                  @click="openMessage(item)"
                >
                  <td>
                    <MailOpen v-if="item.is_read" class="h-4 w-4 text-gray-400" />
                    <Mail v-else class="h-4 w-4 text-[var(--proto-blue)]" />
                  </td>
                  <td :class="!item.is_read && 'font-medium text-gray-900'">{{ item.title }}</td>
                  <td class="text-gray-500">{{ formatDateTime(item.created_at) }}</td>
                  <td class="text-gray-500">{{ item.is_read ? '已读' : '未读' }}</td>
                </tr>
              </template>
              <template v-else>
                <tr
                  v-for="item in announcements"
                  :key="item.announcement_id"
                  class="cursor-pointer"
                  @click="openAnnouncement(item)"
                >
                  <td><Mail class="h-4 w-4 text-gray-400" /></td>
                  <td>{{ item.title }}</td>
                  <td class="text-gray-500">{{ formatDateTime(item.start_time) }}</td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>

        <!-- 消息分页 -->
        <div v-if="tab === 'message' && messageTotalPages > 1" class="flex justify-center py-4">
          <AppPagination 
            v-model:page="messagePage" 
            :total="messageTotal" 
            :page-size="messagePageSize" 
            @update:page="handleMessagePageChange"
          />
        </div>

        <!-- 公告分页 -->
        <div v-if="tab === 'announcement' && announcementTotalPages > 1" class="flex justify-center py-4">
          <AppPagination 
            v-model:page="announcementPage" 
            :total="announcementTotal" 
            :page-size="announcementPageSize" 
            @update:page="handleAnnouncementPageChange"
          />
        </div>
      </div>
    </div>

    <!-- 消息详情（原型：分块白色卡片） -->
    <Teleport to="body">
      <div v-if="showDetail" class="fixed inset-0 z-50 proto-grid-bg">
        <button
          type="button"
          class="absolute left-8 top-20 text-white"
          @click="showDetail = false"
        >
          ← 返回
        </button>
        <div class="flex min-h-screen items-center justify-center p-8">
          <div class="w-full max-w-lg space-y-3">
            <div class="proto-card px-6 py-4 text-sm">
              <span class="text-gray-600">通知标题：</span>{{ detailTitle }}
            </div>
            <div class="proto-card px-6 py-3 text-sm text-gray-600">
              通知时间：{{ detailTime }}
            </div>
            <div class="proto-card px-6 py-5 text-sm">
              <p class="mb-2 text-gray-600">正文：</p>
              <p class="whitespace-pre-wrap leading-relaxed">{{ detailContent }}</p>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>