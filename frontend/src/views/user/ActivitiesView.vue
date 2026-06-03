<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { getActivities, getCategories } from '@/api/activities'
import { showApiError } from '@/api/request'
import type { ActivityListItem, CategoryNode } from '@/types/api'
import { CAMPUSES } from '@/utils/constants'
import { formatDateTime } from '@/utils'
import SegmentedControl from '@/components/ui/SegmentedControl.vue'
import AppPagination from '@/components/ui/AppPagination.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import { Search } from 'lucide-vue-next'

const router = useRouter()

const statusTab = ref('open,edit_pending')
const activities = ref<ActivityListItem[]>([])
const categories = ref<CategoryNode[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 10
const loading = ref(false)

const filters = ref({
  keyword: '',
  activity_id: '',
  category_id: '',
  start_year: '',
  start_month: '',
  start_day: '',
  campus: '',
})

const categoryOptions = computed(() => {
  const opts = [{ value: '', label: '不限' }]
  for (const c of categories.value) {
    opts.push({ value: String(c.id), label: c.name })
    c.children?.forEach((ch) => opts.push({ value: String(ch.id), label: ch.name }))
  }
  return opts
})

const startDate = computed(() => {
  const { start_year: y, start_month: m, start_day: d } = filters.value
  if (!y || !m || !d) return ''
  return `${y}-${m.padStart(2, '0')}-${d.padStart(2, '0')}`
})

onMounted(async () => {
  try {
    categories.value = await getCategories()
  } catch {
    /* optional */
  }
  await fetchList()
})

async function fetchList() {
  loading.value = true
  try {
    const params: Record<string, unknown> = {
      page: page.value,
      page_size: pageSize,
      status: statusTab.value,
    }
    if (filters.value.keyword) params.keyword = filters.value.keyword
    if (filters.value.category_id) params.category_id = Number(filters.value.category_id)
    if (startDate.value) params.start_date = startDate.value
    if (filters.value.campus) params.campus = filters.value.campus.replace('校区', '')

    const data = await getActivities(params)
    let list = data.list
    if (filters.value.activity_id) {
      const id = Number(filters.value.activity_id)
      if (!Number.isNaN(id)) list = list.filter((a) => a.activity_id === id)
    }
    activities.value = list
    total.value = filters.value.activity_id ? list.length : data.total
  } catch (e) {
    showApiError(e)
  } finally {
    loading.value = false
  }
}

watch(statusTab, () => {
  page.value = 1
  fetchList()
})

function goDetail(id: number) {
  router.push(`/activities/${id}`)
}

const years = ['2025', '2026', '2027', '2028']
const months = Array.from({ length: 12 }, (_, i) => String(i + 1))
const days = Array.from({ length: 31 }, (_, i) => String(i + 1))
</script>

<template>
  <div class="mx-auto max-w-5xl">
    <div class="proto-card overflow-hidden">
      <!-- 顶部 Tab -->
      <div class="flex items-center justify-between border-b px-5 py-3">
        <SegmentedControl
          v-model="statusTab"
          :options="[
            { value: 'open,edit_pending', label: '将要进行的活动' },
            { value: 'ongoing', label: '正在进行的活动' },
          ]"
        />
        <Search class="h-5 w-5 text-gray-400" />
      </div>

      <!-- 筛选区 -->
      <div class="space-y-4 border-b bg-white px-5 py-4 text-sm">
        <div class="flex flex-wrap items-center gap-3">
          <span class="text-gray-600">活动类别</span>
          <select v-model="filters.category_id" class="rounded border border-gray-300 px-3 py-1.5">
            <option v-for="o in categoryOptions" :key="o.value" :value="o.value">{{ o.label }}</option>
          </select>
        </div>
        <div class="grid gap-4 sm:grid-cols-2">
          <div class="flex items-center gap-2">
            <span class="shrink-0 text-gray-600">活动名称</span>
            <div class="relative flex-1">
              <input v-model="filters.keyword" class="w-full rounded border border-gray-300 py-1.5 pl-3 pr-8" />
              <Search class="absolute right-2 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
            </div>
          </div>
          <div class="flex items-center gap-2">
            <span class="shrink-0 text-gray-600">活动ID</span>
            <div class="relative flex-1">
              <input v-model="filters.activity_id" class="w-full rounded border border-gray-300 py-1.5 pl-3 pr-8" />
              <Search class="absolute right-2 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
            </div>
          </div>
        </div>
        <div class="flex flex-wrap items-center gap-3">
          <span class="text-gray-600">开始时间</span>
          <select v-model="filters.start_year" class="rounded border border-gray-300 px-2 py-1.5">
            <option value="">年</option>
            <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
          </select>
          <select v-model="filters.start_month" class="rounded border border-gray-300 px-2 py-1.5">
            <option value="">月</option>
            <option v-for="m in months" :key="m" :value="m">{{ m }}</option>
          </select>
          <select v-model="filters.start_day" class="rounded border border-gray-300 px-2 py-1.5">
            <option value="">日</option>
            <option v-for="d in days" :key="d" :value="d">{{ d }}</option>
          </select>
          <span class="ml-4 text-gray-600">校区</span>
          <select v-model="filters.campus" class="rounded border border-gray-300 px-3 py-1.5">
            <option value="">不限</option>
            <option v-for="c in CAMPUSES" :key="c" :value="c">{{ c }}校区</option>
          </select>
          <button type="button" class="proto-btn-primary ml-auto" @click="page = 1; fetchList()">搜索</button>
        </div>
      </div>

      <!-- 表格 -->
      <div v-if="loading" class="py-16 text-center text-gray-500">加载中...</div>
      <EmptyState v-else-if="!activities.length" message="暂无活动，请稍后再来" />
      <div v-else class="overflow-x-auto">
        <table class="proto-table">
          <thead>
            <tr>
              <th>活动ID</th>
              <th>活动名称</th>
              <th>活动地点</th>
              <th>开始时间</th>
              <th>结束时间</th>
              <th>活动分类</th>
              <th>报名人数</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in activities" :key="item.activity_id" @click="goDetail(item.activity_id)">
              <td>{{ String(item.activity_id).padStart(3, '0') }}</td>
              <td>{{ item.name }}</td>
              <td>{{ item.campus }}{{ item.location }}</td>
              <td>{{ formatDateTime(item.start_time) }}</td>
              <td>{{ item.end_time ? formatDateTime(item.end_time) : '—' }}</td>
              <td>{{ item.category_name }}</td>
              <td>{{ item.current_participants }}/{{ item.max_participants }}</td>
            </tr>
            <tr v-for="n in Math.max(0, 5 - activities.length)" :key="'empty-' + n">
              <td colspan="7" class="h-10">&nbsp;</td>
            </tr>
          </tbody>
        </table>
      </div>

      <AppPagination v-model:page="page" :total="total" :page-size="pageSize" @update:page="fetchList" />
    </div>
  </div>
</template>
