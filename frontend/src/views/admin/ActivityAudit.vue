<template>
  <div class="flex h-screen">
    <AdminSidebar />
    <main class="flex-1 overflow-y-auto bg-blue-600 p-8">
      <div class="max-w-7xl mx-auto">
        <div class="mb-6">
          <h1 class="text-3xl font-bold text-white">活动审核</h1>
          <p class="text-white/70 mt-1">审核活动申请</p>
        </div>

        <!-- 筛选栏 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-8 flex flex-wrap gap-8 items-end">
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">审核状态</label>
            <select v-model="filters.status" class="border rounded-lg px-3 py-2 text-sm w-36 text-gray-900">
              <option value="pending">未审核</option>
              <option value="end">已审核</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">活动分类</label>
            <select v-model="filters.categoryId" class="border rounded-lg px-3 py-2 text-sm w-36 text-gray-900">
              <option value="">全部</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id" class="text-gray-900">{{ cat.name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">开始时间(起)</label>
            <input type="date" v-model="filters.startDateFrom" class="border rounded-lg px-3 py-2 text-sm w-36 text-gray-900">
          </div>
          <div class="flex gap-3">
            <button @click="applyFilters" class="px-5 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium shadow-sm hover:bg-blue-700">筛选</button>
            <button @click="resetFilters" class="px-5 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50">重置</button>
          </div>
        </div>

        <!-- 表格 -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">活动名称</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">组织者</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">分类</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">开始时间</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">校区</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="act in activities" :key="act.activity_id" class="hover:bg-gray-50 cursor-pointer" @dblclick="goToDetail(act.activity_id)">
                  <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ act.name }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ act.organizer_name }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ act.category_name }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ formatDateTime(act.start_time) }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ act.campus }}</td>
                  <td class="px-6 py-4"><span class="px-2 py-1 rounded-full text-xs font-medium" :class="statusColorClass(act.status)">{{ statusText(act.status) }}</span></td>
                </tr>
                <tr v-if="!loading && activities.length === 0">
                  <td colspan="6" class="text-center py-16 text-gray-400">暂无活动</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="totalPages > 1" class="flex justify-center py-4 gap-2">
            <button v-for="p in totalPages" :key="p" @click="goToPage(p)" class="px-3 py-1 rounded border" :class="p === currentPage ? 'bg-blue-600 text-white' : 'text-gray-700'">{{ p }}</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AdminSidebar from '@/components/layout/AdminSidebar.vue'
import { getAdminActivities, getCategories } from '@/api/admin'
import { showApiError } from '@/api/request'
import { formatDateTime } from '@/utils'

const router = useRouter()
const loading = ref(false)
const activities = ref<any[]>([])
const currentPage = ref(1)
const totalPages = ref(1)
const pageSize = 10
const categories = ref<{ id: number; name: string }[]>([])
const filters = reactive({
  status: 'pending',
  categoryId: '',
  startDateFrom: '',
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

const fetchCategories = async () => {
  try {
    const data = await getCategories()
    const flat: { id: number; name: string; level: number }[] = []
    data.forEach((cat: any) => {
      flat.push({ id: cat.id, name: cat.name, level: 1 })
      if (cat.children && cat.children.length) {
        cat.children.forEach((child: any) => {
          flat.push({ 
            id: child.id, 
            name: `\u00A0\u00A0\u00A0\u00A0${child.name}`,
            level: 2 
          })
        })  
      }
    }) 
    categories.value = flat
  } catch (e) {
    showApiError(e, '获取分类失败')
  }
}

const fetchActivities = async () => {
  loading.value = true
  try {
    let statusParam = ''
    if (filters.status === 'pending') statusParam = 'pending,edit_pending'
    else if (filters.status === 'end') statusParam = 'open,ongoing,ended,rejected,removed'
    const params: any = {
      page: currentPage.value,
      page_size: pageSize,
      status: statusParam || undefined,
      category_id: filters.categoryId ? Number(filters.categoryId) : undefined,
      start_date: filters.startDateFrom || undefined,
    }
    const data = await getAdminActivities(params)
    activities.value = data.list || []
    const total = data.total || activities.value.length
    totalPages.value = Math.ceil(total / pageSize)
  } catch (e) { 
    showApiError(e, '获取审核列表失败') 
  } finally { 
    loading.value = false 
  }
}

const applyFilters = () => { 
  currentPage.value = 1
  fetchActivities() 
}

const resetFilters = () => {
  filters.status = 'pending'
  filters.categoryId = ''
  filters.startDateFrom = ''
  applyFilters()
}

const goToPage = (page: number) => { 
  currentPage.value = page
  fetchActivities() 
}

const goToDetail = (id: number) => router.push(`/admin/audit/${id}`)

onMounted(() => {
  fetchCategories()
  fetchActivities()
})
</script>