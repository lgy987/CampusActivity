<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getLeaderboard } from '@/api/statistics'
import { showApiError } from '@/api/request'
import { useAuthStore } from '@/stores/auth'
import type { RankingItem } from '@/types/api'
import { COLLEGES, GRADES } from '@/utils/constants'
import AppPagination from '@/components/ui/AppPagination.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import { Trophy } from 'lucide-vue-next'

const auth = useAuthStore()
const list = ref<RankingItem[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 10
const loading = ref(false)

const filters = ref({ period: 'all', college: '', grade: '' })

onMounted(() => fetchRanking())

async function fetchRanking() {
  loading.value = true
  try {
    const params: Record<string, unknown> = {
      page: page.value,
      page_size: pageSize,
      period: filters.value.period,
    }
    if (filters.value.college) params.college = filters.value.college
    if (filters.value.grade) params.grade = filters.value.grade
    const data = await getLeaderboard(params)
    list.value = data.list
    total.value = data.total
  } catch (e) {
    showApiError(e)
  } finally {
    loading.value = false
  }
}

function handleFilter() {
  page.value = 1  // 重置页码
  fetchRanking()
}

function resetFilters() {
  filters.value = { period: 'all', college: '', grade: '' }
  page.value = 1
  fetchRanking()
}


function isCurrentUser(item: RankingItem) {
  return auth.userId === item.user_id
}
</script>

<template>
  <div class="mx-auto max-w-3xl">
    <div class="proto-card overflow-hidden">
      <div class="flex flex-wrap gap-4 border-b px-5 py-4 text-sm">
        <div class="flex items-center gap-2">
          <span class="text-gray-600">时间筛选</span>
          <select v-model="filters.period" class="rounded border border-gray-300 px-3 py-1.5">
            <option value="all">全部</option>
            <option value="week">本周</option>
            <option value="month">本月</option>
          </select>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-gray-600">学院</span>
          <select v-model="filters.college" class="rounded border border-gray-300 px-3 py-1.5">
            <option value="">全部</option>
            <option v-for="c in COLLEGES" :key="c" :value="c">{{ c }}</option>
          </select>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-gray-600">年级</span>
          <select v-model="filters.grade" class="rounded border border-gray-300 px-3 py-1.5">
            <option value="">全部</option>
            <option v-for="g in GRADES" :key="g" :value="g">{{ g }}</option>
          </select>
        </div>
        <button type="button" class="proto-btn-primary" @click="handleFilter">筛选</button>
        <button type="button" class="proto-btn-outline" @click="resetFilters">重置</button>
      </div>

      <div v-if="loading" class="py-16 text-center text-gray-500">加载中...</div>
      <EmptyState v-else-if="!list.length" message="暂无排行数据" />

      <div v-else class="overflow-x-auto">
        <table class="proto-table">
          <thead>
            <tr>
              <th class="w-16">排名</th>
              <th>学号</th>
              <th class="text-right">有效参与次数</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in list"
              :key="item.user_id"
              :class="isCurrentUser(item) ? 'bg-blue-100 font-semibold' : ''"
            >
              <td class="relative">
                <Trophy v-if="item.rank === 1" class="absolute -left-2 h-5 w-5 text-amber-500" />
                {{ item.rank }}
              </td>
              <td>{{ item.student_id }}</td>
              <td class="text-right">{{ item.effective_participation_count }}</td>
            </tr>
            <tr v-for="n in Math.max(0, 6 - list.length)" :key="'e' + n">
              <td colspan="3" class="h-10">&nbsp;</td>
            </tr>
          </tbody>
        </table>
      </div>

      <AppPagination v-model:page="page" :total="total" :page-size="pageSize" @update:page="fetchRanking" />
    </div>
  </div>
</template>
