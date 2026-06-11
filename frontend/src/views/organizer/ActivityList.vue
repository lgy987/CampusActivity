<template>
  <div class="flex h-screen">
    <OrganizerSidebar />
    <!-- 将背景改为深蓝色 bg-blue-600 -->
    <main class="flex-1 overflow-y-auto bg-blue-600 p-8">
      <div class="max-w-7xl mx-auto">
        <!-- 标题行 -->
        <div class="flex justify-between items-center mb-10">
          <div>
            <div class="flex items-center gap-2 text-white/70 text-sm mb-1">
              <span>活动管理</span>
              <iconify-icon class="text-[10px]" icon="ph:caret-right-bold"></iconify-icon>
              <span class="text-white/90">我的活动</span>
            </div>
            <h1 class="text-3xl font-bold text-white">活动管理</h1>
          </div>
          <AppButton variant="blue" @click="goToCreateActivity" class="px-6 py-2.5 shadow-md">
            <iconify-icon icon="ph:plus-bold"></iconify-icon> 创建活动
          </AppButton>
        </div>

        <!-- 状态筛选按钮组 -->
        <div class="mb-8">
          <div class="flex flex-wrap gap-4 mb-4">
            <span class="text-white/80 text-sm mr-2 self-center">状态：</span>
            <button
              v-for="group in statusGroups"
              :key="group.key"
              @click="setGroup(group.key)"
              class="px-5 py-1.5 rounded-full border transition text-sm font-medium"
              :class="currentGroup === group.key
                ? 'bg-blue-600 text-white border-blue-600 shadow-sm'
                : 'border-white/30 text-white/80 hover:bg-white/10'"
            >
              {{ group.label }}
            </button>
          </div>
          <div class="flex flex-wrap gap-3 pl-2" v-if="subStatuses.length">
            <span class="text-white/60 text-xs mr-2 self-center">细分：</span>
            <button
              v-for="sub in subStatuses"
              :key="sub.key"
              @click="setSubStatus(sub.key)"
              class="px-4 py-1 rounded-full text-sm border transition"
              :class="currentSubStatus === sub.key
                ? 'bg-blue-600 text-white border-blue-600'
                : 'border-white/30 text-white/80 hover:bg-white/10'"
            >
              {{ sub.label }}
            </button>
          </div>
        </div>

        <!-- 筛选栏（白色卡片） -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-8 flex flex-wrap gap-8 items-end">
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">活动分类</label>
            <select v-model="filters.categoryId" class="border rounded-lg px-3 py-2 text-sm w-48 text-gray-900">
              <option value="">全部</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id" class="text-gray-900">{{ cat.name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">开始日期</label>
            <input type="date" v-model="filters.startDate" class="border rounded-lg px-3 py-2 text-sm w-48 text-gray-900">
          </div>
          <div class="flex gap-3">
            <button @click="applyFilters" class="px-5 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium shadow-sm hover:bg-blue-700">筛选</button>
            <button @click="resetFilters" class="px-5 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50">重置</button>
          </div>
        </div>

        <!-- 表格（白色卡片） -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">活动名称</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">分类</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">开始时间</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">校区</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">地点</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="act in activities" :key="act.id" class="hover:bg-gray-50 cursor-pointer" @dblclick="goToDetail(act.id)">
                  <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ act.title }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ act.categoryName }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ formatDateTime(act.startTime) }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ act.campus }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ act.location }}</td>
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
// 脚本部分（保持原样，未作任何改动）
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppPageContainer from '@/components/layout/AppPageContainer.vue'
import AppButton from '@/components/common/AppButton.vue'
import { getMyActivities, getCategories } from '@/api/organizer'
import { useUserStore } from '@/stores/user'
import { showApiError } from '@/api/request'
import OrganizerSidebar from '@/components/layout/OrganizerSidebar.vue'
import { formatDateTime } from '@/utils'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const activities = ref<any[]>([])
const currentPage = ref(1)
const totalPages = ref(1)
const pageSize = 10
const categories = ref<{ id: number; name: string; level: number }[]>([])
const currentGroup = ref('all')
const currentSubStatus = ref('')
const filters = reactive({
  categoryId: '',
  startDate: '',
})

const organizerStatus = computed(() => userStore.userInfo?.status || '')

const statusGroups = [
  { key: 'all', label: '全部' },
  { key: 'unpublished', label: '未发布活动' },
  { key: 'published', label: '发布中活动' },
  { key: 'ended', label: '已结束活动' }
]
const unpublishedSubStatuses = [
  { key: '', label: '全部' },
  { key: 'draft', label: '草稿' },
  { key: 'pending', label: '审核中' },
  { key: 'rejected', label: '审核未通过' },
  { key: 'removed', label: '下架' }
]
const publishedSubStatuses = [
  { key: '', label: '全部' },
  { key: 'open', label: '报名中' },
  { key: 'edit_pending', label: '审核修改中' },
  { key: 'ongoing', label: '进行中' }
]
const subStatuses = computed(() => {
  if (currentGroup.value === 'unpublished') return unpublishedSubStatuses
  if (currentGroup.value === 'published') return publishedSubStatuses
  return []
})

const statusTextMap: Record<string, string> = {
  draft: '草稿', pending: '审核中', rejected: '审核未通过', removed: '下架',
  open: '报名中', edit_pending: '审核修改中', ongoing: '进行中', ended: '已结束'
}
const statusColorMap: Record<string, string> = {
  pending: 'bg-yellow-100 text-yellow-700', modifying: 'bg-blue-100 text-blue-700',
  rejected: 'bg-red-100 text-red-700', shelved: 'bg-gray-100 text-gray-700',
  open: 'bg-green-100 text-green-700', ongoing: 'bg-indigo-100 text-indigo-700',
  ended: 'bg-slate-100 text-slate-700'
}
const statusText = (s: string) => statusTextMap[s] || s
const statusColorClass = (s: string) => statusColorMap[s] || 'bg-gray-100 text-gray-700'

const fetchCategories = async () => {
  try {
    const data = await getCategories()
    const flat: { id: number; name: string; level: number }[] = []
    data.forEach((cat: any) => {
      // 添加一级分类
      flat.push({ id: cat.id, name: cat.name, level: 1 })
      // 添加二级分类（带缩进标识）
      if (cat.children && cat.children.length) {
        cat.children.forEach((child: any) => {
          flat.push({ 
            id: child.id, 
            name: `\u00A0\u00A0\u00A0\u00A0${child.name}`, // 添加缩进，区分层级
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
    if (currentGroup.value === 'unpublished') {
      statusParam = currentSubStatus.value || 'draft,pending,rejected,removed'
    } else if (currentGroup.value === 'published') {
      statusParam = currentSubStatus.value || 'open,edit_pending,ongoing'
    } else if (currentGroup.value === 'ended') {
      statusParam = 'ended'
    }
    const params: any = {
      page: currentPage.value,
      page_size: pageSize,
      status: statusParam || undefined,
      category_id: filters.categoryId ? Number(filters.categoryId) : undefined,
      start_date: filters.startDate || undefined
    }
    const data = await getMyActivities(params)
    activities.value = data.list.map((a: any) => ({
      id: a.activity_id,
      title: a.name,
      categoryName: a.category_name,
      startTime: a.start_time,
      campus: a.campus,
      location: a.location,
      status: a.status
    }))
    totalPages.value = Math.ceil(data.total / pageSize)
  } catch (e) {
    showApiError(e, '获取活动列表失败')
  } finally {
    loading.value = false
  }
}

const setGroup = (group: string) => {
  currentGroup.value = group
  currentSubStatus.value = ''
  currentPage.value = 1
  fetchActivities()
}
const setSubStatus = (sub: string) => {
  currentSubStatus.value = sub
  currentPage.value = 1
  fetchActivities()
}
const applyFilters = () => {
  currentPage.value = 1
  fetchActivities()
}
const resetFilters = () => {
  filters.categoryId = ''
  filters.startDate = ''
  currentPage.value = 1
  fetchActivities()
}

const goToPage = (page: number) => {
  currentPage.value = page
  fetchActivities()
}
const goToDetail = (id: number) => router.push(`/organizer/activity?id=${id}`)

const goToCreateActivity = async () => {
  await userStore.fetchProfile()
  const status = userStore.userInfo?.status || ''
  if (status === 'pending') {
    alert('您的账号正在审核中，暂不能创建活动。请等待管理员审核通过后再试。')
    return
  }
  if (status === 'rejected') {
    alert('您的账号审核未通过，无法创建活动。请联系管理员了解具体原因。')
    return
  }
  if (status === 'deleted') {
    alert('您的账号已被注销，无法创建活动。')
    return
  }
  if (status !== 'approved') {
    alert('账号状态异常，无法创建活动')
    return
  }
  // 审核通过，跳转到创建活动页面
  router.push('/organizer/activity')
}

onMounted(async () => {
  // 如果 userStore 中没有用户信息，先获取
  if (!userStore.userInfo) {
    await userStore.fetchProfile()
  }
  fetchCategories()
  fetchActivities()
})

</script>