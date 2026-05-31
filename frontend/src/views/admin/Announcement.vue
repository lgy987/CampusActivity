<template>
  <div class="flex h-screen">
    <AdminSidebar />
    <main class="flex-1 overflow-y-auto bg-blue-600 p-8">
      <div class="max-w-7xl mx-auto">
        <div class="mb-6">
          <h1 class="text-3xl font-bold text-white">系统公告管理</h1>
          <p class="text-white/70 mt-1">发布与管理系统公告</p>
        </div>

        <div class="flex justify-end mb-4">
          <AppButton variant="blue" @click="openCreateModal">发布公告</AppButton>
        </div>

        <AppCard :loading="loading">
          <div class="space-y-4">
            <div v-for="ann in announcements" :key="ann.announcement_id" class="border-b pb-3">
              <div class="flex justify-between items-start">
                <div>
                  <h3 class="font-semibold text-gray-900">{{ ann.title }}</h3>
                  <p class="text-xs text-gray-400 mt-1">{{ ann.start_time ? formatDateTime(ann.start_time) : '-' }}</p>
                  <p class="text-sm text-gray-600 mt-1">{{ ann.content }}</p>
                </div>
                <div class="flex gap-2">
                  <AppButton size="sm" variant="outline" @click="openEditModal(ann)">编辑</AppButton>
                  <AppButton size="sm" variant="destructive" @click="removeAnnouncement(ann.announcement_id)">删除</AppButton>
                </div>
              </div>
            </div>
            <div v-if="announcements.length === 0" class="text-center text-gray-400 py-8">暂无公告</div>
          </div>
          <div v-if="totalPages > 1" class="flex justify-center mt-6 gap-2">
            <button v-for="p in totalPages" :key="p" @click="goToPage(p)" class="px-3 py-1 rounded border" :class="p === currentPage ? 'bg-blue-600 text-white' : 'text-gray-700'">{{ p }}</button>
          </div>
        </AppCard>

        <AppDialog v-model:open="modalVisible" :title="modalTitle" confirm-text="发布" cancel-text="取消" @confirm="submitAnnouncement">
          <div class="space-y-3">
            <input type="text" v-model="form.title" placeholder="标题" class="w-full border rounded px-3 py-2">
            <textarea v-model="form.content" rows="4" placeholder="内容" class="w-full border rounded px-3 py-2"></textarea>
            <input type="datetime-local" v-model="form.start_time_local" placeholder="开始时间（可选）" class="w-full border rounded px-3 py-2">
            <input type="datetime-local" v-model="form.end_time_local" placeholder="结束时间（可选）" class="w-full border rounded px-3 py-2">
          </div>
        </AppDialog>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import AdminSidebar from '@/components/layout/AdminSidebar.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppButton from '@/components/common/AppButton.vue'
import AppDialog from '@/components/layout/AppDialog.vue'
import { getAnnouncements, publishAnnouncement, removeAnnouncement as apiRemoveAnnouncement } from '@/api/admin'
import { showApiError } from '@/api/request'

const loading = ref(false)
const announcements = ref<any[]>([])
const currentPage = ref(1)
const totalPages = ref(1)
const pageSize = 10

const fetchAnnouncements = async () => {
  loading.value = true
  try {
    const data = await getAnnouncements()
    // 后端直接返回数组，不需要兼容处理
    announcements.value = Array.isArray(data) ? data : []
    totalPages.value = Math.ceil(announcements.value.length / pageSize)
  } catch (e) {
    showApiError(e, '获取公告列表失败')
  } finally {
    loading.value = false
  }
}

const modalVisible = ref(false)
const modalTitle = ref('发布公告')
const editingId = ref<number | null>(null)
const form = reactive({
  title: '',
  content: '',
  start_time_local: '',
  end_time_local: ''
})

// 转换 datetime-local 值为 YYYY-MM-DD HH:MM:SS
const convertToDateTime = (localValue: string): string => {
  if (!localValue) return ''
  
  console.log('convertToDateTime 输入:', localValue)
  const date = new Date(localValue)
  console.log('解析后的 Date:', date)
  
  const year = date.getUTCFullYear()
  const month = String(date.getUTCMonth() + 1).padStart(2, '0')
  const day = String(date.getUTCDate()).padStart(2, '0')
  const hours = String(date.getUTCHours()).padStart(2, '0')
  const minutes = String(date.getUTCMinutes()).padStart(2, '0')
  const seconds = String(date.getUTCSeconds()).padStart(2, '0')
  
  const result = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
  
  return result
}

const formatDateTime = (dateStr: string) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  if (isNaN(date.getTime())) return dateStr
  
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  
  const result = `${year}-${month}-${day} ${hours}:${minutes}`
  return result
}

const openCreateModal = () => {
  modalTitle.value = '发布公告'
  editingId.value = null
  form.title = ''
  form.content = ''
  form.start_time_local = ''
  form.end_time_local = ''
  modalVisible.value = true
}

const openEditModal = (ann: any) => {
  modalTitle.value = '编辑公告'
  editingId.value = ann.announcement_id
  form.title = ann.title
  form.content = ann.content
  if (ann.start_time) form.start_time_local = formatDateTime(ann.start_time)
  else form.start_time_local = ''
  if (ann.end_time) form.end_time_local = formatDateTime(ann.end_time)
  else form.end_time_local = ''
  modalVisible.value = true
}

const submitAnnouncement = async () => {
  if (!form.title.trim() || !form.content.trim()) {
    alert('请填写标题和内容')
    return
  }

  const payload: any = {
    title: form.title,
    content: form.content,
  }
  if (form.start_time_local) {
    payload.start_time = convertToDateTime(form.start_time_local)
  }
  if (form.end_time_local) {
    payload.end_time = convertToDateTime(form.end_time_local)
  }

  try {
    if (editingId.value) {
      const idx = announcements.value.findIndex(a => a.announcement_id === editingId.value)
      if (idx !== -1) {
        announcements.value[idx] = { ...announcements.value[idx], ...payload }
        alert('公告已更新（模拟）')
      }
    } else {
      await publishAnnouncement(payload)
      alert('公告发布成功')
    }
    modalVisible.value = false
    await fetchAnnouncements()
    if (announcements.value.length === 0) {
      alert('发布成功但列表为空，这可能是因为公告设置了未来的开始时间或已过期。建议不填写时间字段，让公告永久有效。')
    }
  } catch (e: any) {
    const msg = e.response?.data?.message || e.message || '操作失败'
    alert(msg)
  }
}

const removeAnnouncement = async (id: number) => {
  if (!confirm('确定删除该公告吗？')) return
  try {
    await apiRemoveAnnouncement(id)
    alert('已删除')
    await fetchAnnouncements()
  } catch (e) {
    showApiError(e, '删除失败')
  }
}

const goToPage = (p: number) => {
  currentPage.value = p
  fetchAnnouncements()
}

onMounted(() => {
  fetchAnnouncements()
})
</script>