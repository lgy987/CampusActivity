<template>
  <div class="flex h-screen">
    <AdminSidebar />

    <main class="flex-1 overflow-y-auto bg-blue-600 p-6 custom-scrollbar">
      <div class="max-w-7xl mx-auto">
        <!-- 页面标题 -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-white">用户管理</h1>
          <p class="text-white/70 mt-1">管理平台所有用户账号</p>
        </div>

        <!-- 统计卡片（可点击切换列表） -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
          <div
            @click="activeTab = 'user'"
            class="bg-white rounded-2xl p-6 shadow-sm border text-center cursor-pointer transition-all hover:shadow-md hover:scale-[1.02]"
            :class="activeTab === 'user' ? 'border-blue-500 ring-2 ring-blue-200' : 'border-gray-100'"
          >
            <div class="text-3xl font-bold text-blue-600">{{ stats.userCount }}</div>
            <div class="text-gray-500 mt-2">普通用户数</div>
          </div>
          <div
            @click="activeTab = 'organizer'"
            class="bg-white rounded-2xl p-6 shadow-sm border text-center cursor-pointer transition-all hover:shadow-md hover:scale-[1.02]"
            :class="activeTab === 'organizer' ? 'border-blue-500 ring-2 ring-blue-200' : 'border-gray-100'"
          >
            <div class="text-3xl font-bold text-blue-600">{{ stats.organizerCount }}</div>
            <div class="text-gray-500 mt-2">组织者</div>
          </div>
          <div
            @click="activeTab = 'admin'"
            class="bg-white rounded-2xl p-6 shadow-sm border text-center cursor-pointer transition-all hover:shadow-md hover:scale-[1.02]"
            :class="activeTab === 'admin' ? 'border-blue-500 ring-2 ring-blue-200' : 'border-gray-100'"
          >
            <div class="text-3xl font-bold text-blue-600">{{ stats.adminCount }}</div>
            <div class="text-gray-500 mt-2">管理员</div>
          </div>
          <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 text-center">
            <div class="text-3xl font-bold text-orange-500">{{ stats.pendingOrganizerCount }}</div>
            <div class="text-gray-500 mt-2">待审批组织者</div>
          </div>
        </div>

        <!-- 普通用户列表 -->
        <div v-show="activeTab === 'user'">
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-6 flex flex-wrap gap-4 items-end">
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">学号</label>
              <input
                type="text"
                v-model="userFilters.student_id"
                placeholder="输入学号"
                class="border rounded-lg px-3 py-2 text-sm w-48"
              />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">学院</label>
              <select v-model="userFilters.college" class="border rounded-lg px-3 py-2 text-sm w-48">
                <option value="">全部</option>
                <option v-for="college in collegeOptions" :key="college" :value="college">{{ college }}</option>
              </select>
            </div>
            <div>
              <button @click="fetchUsers" class="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm">筛选</button>
              <button @click="resetUserFilters" class="ml-2 px-4 py-2 border border-gray-300 rounded-lg text-sm">重置</button>
            </div>
          </div>

          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">学号</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">学院</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">专业</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">状态</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                  <tr v-for="u in users" :key="u.user_id">
                    <td class="px-6 py-4">{{ u.student_id }}</td>
                    <td class="px-6 py-4">{{ u.college || '—' }}</td>
                    <td class="px-6 py-4">{{ u.major || '—' }}</td>
                    <td class="px-6 py-4">
                      <span
                        class="px-2 py-1 rounded-full text-xs"
                        :class="u.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
                      >
                        {{ u.status === 'active' ? '正常' : '禁用' }}
                      </span>
                    </td>
                  </tr>
                  <tr v-if="!userLoading && users.length === 0">
                    <td colspan="4" class="text-center py-8 text-gray-500">暂无数据</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="flex justify-center py-4 gap-2" v-if="userTotal > 0">
              <button
                @click="userPage--"
                :disabled="userPage === 1"
                class="px-3 py-1 rounded border text-gray-700 disabled:opacity-50"
              >
                上一页
              </button>
              <span class="px-3 py-1 text-gray-700">第 {{ userPage }} / {{ userTotalPages }} 页</span>
              <button
                @click="userPage++"
                :disabled="userPage === userTotalPages"
                class="px-3 py-1 rounded border text-gray-700 disabled:opacity-50"
              >
                下一页
              </button>
            </div>
          </div>
        </div>

        <!-- 组织者列表 -->
        <div v-show="activeTab === 'organizer'">
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-6 flex flex-wrap gap-4 items-end">
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">组织名称</label>
              <input
                type="text"
                v-model="orgFilters.name"
                placeholder="输入组织名称"
                class="border rounded-lg px-3 py-2 text-sm w-48"
              />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">审核状态</label>
              <select v-model="orgFilters.status" class="border rounded-lg px-3 py-2 text-sm w-36">
                <option value="">全部</option>
                <option value="pending">待审核</option>
                <option value="approved">已通过</option>
                <option value="rejected">已拒绝</option>
              </select>
            </div>
            <div>
              <button @click="fetchOrganizers" class="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm">筛选</button>
              <button @click="resetOrgFilters" class="ml-2 px-4 py-2 border border-gray-300 rounded-lg text-sm">重置</button>
            </div>
          </div>

          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500">组织名</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500">邮箱</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500">审核状态</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500">操作</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                  <tr v-for="org in organizers" :key="org.organizer_id">
                    <td class="px-6 py-4">{{ org.org_name }}</td>
                    <td class="px-6 py-4">{{ org.email }}</td>
                    <td class="px-6 py-4">
                      <span class="px-2 py-1 rounded-full text-xs" :class="getOrgStatusClass(org.status)">
                        {{ getOrgStatusText(org.status) }}
                      </span>
                    </td>
                    <td class="px-6 py-4">
                      <button @click="openOrgDetail(org)" class="px-3 py-1 bg-blue-100 text-blue-700 rounded text-sm">
                        详情
                      </button>
                    </td>
                  </tr>
                  <tr v-if="!orgLoading && organizers.length === 0">
                    <td colspan="4" class="text-center py-8 text-gray-500">暂无数据</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="flex justify-center py-4 gap-2" v-if="orgTotal > 0">
              <button
                @click="orgPage--"
                :disabled="orgPage === 1"
                class="px-3 py-1 rounded border text-gray-700 disabled:opacity-50"
              >
                上一页
              </button>
              <span class="px-3 py-1 text-gray-700">第 {{ orgPage }} / {{ orgTotalPages }} 页</span>
              <button
                @click="orgPage++"
                :disabled="orgPage === orgTotalPages"
                class="px-3 py-1 rounded border text-gray-700 disabled:opacity-50"
              >
                下一页
              </button>
            </div>
          </div>
        </div>

        <!-- 管理员列表 -->
        <div v-show="activeTab === 'admin'">
          <div class="flex justify-end mb-4">
            <button @click="openAddAdminModal" class="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm">+ 新增管理员</button>
          </div>
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">编号</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">用户名</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">邮箱</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">操作</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                  <tr v-for="adm in admins" :key="adm.admin_id">
                    <td class="px-6 py-4">{{ adm.admin_no }}</td>
                    <td class="px-6 py-4">{{ adm.username }}</td>
                    <td class="px-6 py-4">{{ adm.email }}</td>
                    <td class="px-6 py-4">
                      <span v-if="adm.admin_no === '000001'" class="text-gray-400 text-xs">不可操作（超级管理员）</span>
                      <button
                        v-else
                        @click="deleteAdmin(adm.admin_id)"
                        class="px-3 py-1 bg-red-100 text-red-700 rounded text-sm hover:bg-red-200"
                      >
                        删除
                      </button>
                    </td>
                  </tr>
                  <tr v-if="!adminLoading && admins.length === 0">
                    <td colspan="4" class="text-center py-8 text-gray-500">暂无数据</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 组织者审核弹窗 -->
    <AppDialog
      v-model:open="orgModalVisible"
      title="组织者审核"
      cancel-text="关闭"
      :show-confirm="false"
      @cancel="orgModalVisible = false"
    >
      <div class="space-y-4 max-h-[70vh] overflow-y-auto p-1">
        <div>
          <label class="block text-sm font-medium text-gray-700">组织名称</label>
          <input type="text" v-model="currentOrg.org_name" class="w-full border rounded px-3 py-2 bg-gray-50" readonly />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700">邮箱</label>
          <input type="text" v-model="currentOrg.email" class="w-full border rounded px-3 py-2 bg-gray-50" readonly />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700">当前状态</label>
          <span class="inline-block mt-1 px-2 py-1 rounded-full text-xs" :class="getOrgStatusClass(currentOrg.status)">
            {{ getOrgStatusText(currentOrg.status) }}
          </span>
        </div>

        <!-- 组织证明文字 -->
        <div v-if="currentOrg.org_proof_text">
          <label class="block text-sm font-medium text-gray-700">组织证明</label>
          <div class="mt-1 p-3 border rounded bg-gray-50 text-sm text-gray-600 whitespace-pre-wrap">
            {{ currentOrg.org_proof_text }}
          </div>
        </div>

        <!-- 组织证明图片 -->
        <div v-if="currentOrg.org_proof_image">
          <label class="block text-sm font-medium text-gray-700">证明图片</label>
          <div class="mt-1">
            <img 
              :src="currentOrg.org_proof_image" 
              alt="组织证明图片" 
              class="max-w-full max-h-48 rounded border object-contain cursor-pointer"
              @click="previewImage(currentOrg.org_proof_image)"
            />
            <p class="text-xs text-gray-400 mt-1">点击图片可放大查看</p>
          </div>
        </div>

        <!-- 审核操作（仅待审核状态显示） -->
        <div v-if="currentOrg.status === 'pending'" class="pt-2">
          <label class="block text-sm font-medium text-gray-700 mb-2">审核操作</label>
          <div class="flex gap-2">
            <button @click="approveOrganizer" class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
              通过
            </button>
            <button @click="openRejectOrgModal" class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
              拒绝
            </button>
          </div>
        </div>

        <!-- 拒绝理由输入框 -->
        <div v-if="showRejectReason">
          <label class="block text-sm font-medium text-gray-700">拒绝理由</label>
          <textarea v-model="rejectReason" rows="2" class="w-full border rounded px-3 py-2 mt-1" placeholder="请输入拒绝理由"></textarea>
          <button @click="confirmRejectOrganizer" class="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
            确认拒绝
          </button>
        </div>
      </div>
    </AppDialog>

    <!-- 图片预览弹窗 -->
    <AppDialog
      v-model:open="imagePreviewVisible"
      title="图片预览"
      confirm-text="关闭"
      :show-cancel="false"
      @confirm="imagePreviewVisible = false"
    >
      <div class="flex justify-center">
        <img :src="previewImageUrl" alt="预览图片" class="max-w-full max-h-[70vh] object-contain" />
      </div>
    </AppDialog>

    <!-- 新增管理员弹窗 -->
    <AppDialog v-model:open="adminModalVisible" title="新增管理员" confirm-text="添加" cancel-text="取消" @confirm="addAdmin">
      <div class="space-y-3">
        <input type="text" v-model="newAdmin.username" placeholder="用户名" class="w-full border rounded px-3 py-2" />
        <input type="email" v-model="newAdmin.email" placeholder="邮箱" class="w-full border rounded px-3 py-2" />
        <input type="password" v-model="newAdmin.password" placeholder="初始密码" class="w-full border rounded px-3 py-2" />
      </div>
    </AppDialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch } from 'vue'
import AdminSidebar from '@/components/layout/AdminSidebar.vue'
import AppDialog from '@/components/layout/AppDialog.vue'
import request from '@/api/request'
import { showApiError } from '@/api/request'

// 标签页
const activeTab = ref<'user' | 'organizer' | 'admin'>('user')

// 统计数据
const stats = reactive({
  userCount: 0,
  organizerCount: 0,
  adminCount: 0,
  pendingOrganizerCount: 0
})

// 学院下拉选项
const collegeOptions = [
  '化学与化工学院',
  '生命学院',
  '空天科学与技术学院',
  '医学技术学院',
  '机电学院',
  '机械与车辆学院',
  '数学与统计学院',
  '光电学院',
  '物理学院',
  '信息与电子学院',
  '管理学院',
  '集成电路与电子学院',
  '经济学院',
  '自动化学院',
  '教育学院',
  '计算机学院',
  '网络空间安全学院',
  '法学院',
  '外国语学院',
  '设计与艺术学院',
  '材料学院'
]

// 图片预览
const imagePreviewVisible = ref(false)
const previewImageUrl = ref('')

// 普通用户
const userLoading = ref(false)
const users = ref<any[]>([])
const userFilters = reactive({ student_id: '', college: '' })
const userPage = ref(1)
const userPageSize = 10
const userTotal = ref(0)
const userTotalPages = computed(() => Math.ceil(userTotal.value / userPageSize))

// 组织者
const orgLoading = ref(false)
const organizers = ref<any[]>([])
const orgFilters = reactive({ name: '', status: '' })
const orgPage = ref(1)
const orgPageSize = 10
const orgTotal = ref(0)
const orgTotalPages = computed(() => Math.ceil(orgTotal.value / orgPageSize))
const orgModalVisible = ref(false)
const currentOrg = ref<any>({})
const showRejectReason = ref(false)
const rejectReason = ref('')

// 管理员
const adminLoading = ref(false)
const admins = ref<any[]>([])
const adminModalVisible = ref(false)
const newAdmin = reactive({ username: '', email: '', password: '' })

// 辅助函数
const getOrgStatusText = (status: string) =>
  ({ pending: '待审核', approved: '已通过', rejected: '已拒绝' }[status] || status)
const getOrgStatusClass = (status: string) =>
  ({
    pending: 'bg-yellow-100 text-yellow-700',
    approved: 'bg-green-100 text-green-700',
    rejected: 'bg-red-100 text-red-700'
  }[status] || 'bg-gray-100')

// 图片预览
const previewImage = (url: string) => {
  previewImageUrl.value = url
  imagePreviewVisible.value = true
}

// 获取普通用户列表
const fetchUsers = async () => {
  userLoading.value = true
  try {
    const params: any = { page: userPage.value, page_size: userPageSize }
    if (userFilters.student_id) params.student_id = userFilters.student_id
    if (userFilters.college) params.college = userFilters.college
    const res = await request.get('/admin/users', { params })
    const data = res.data.data || {}
    const list = data.list || data.items || []
    users.value = list
    userTotal.value = data.total || list.length
    stats.userCount = userTotal.value
  } catch (e) {
    showApiError(e, '获取用户列表失败')
  } finally {
    userLoading.value = false
  }
}

const resetUserFilters = () => {
  userFilters.student_id = ''
  userFilters.college = ''
  userPage.value = 1
  fetchUsers()
}

// 获取组织者列表
const fetchOrganizers = async () => {
  orgLoading.value = true
  try {
    const params: any = { page: orgPage.value, page_size: orgPageSize }
    if (orgFilters.name) params.org_name = orgFilters.name
    if (orgFilters.status) params.status = orgFilters.status
    const res = await request.get('/admin/organizers', { params })
    const data = res.data.data || {}
    const list = data.list || data.items || []
    organizers.value = list
    orgTotal.value = data.total || list.length
    stats.organizerCount = orgTotal.value
    stats.pendingOrganizerCount = list.filter((o: any) => o.status === 'pending').length
  } catch (e) {
    showApiError(e, '获取组织者列表失败')
  } finally {
    orgLoading.value = false
  }
}

const resetOrgFilters = () => {
  orgFilters.name = ''
  orgFilters.status = ''
  orgPage.value = 1
  fetchOrganizers()
}

const openOrgDetail = async (org: any) => {
  try {
    const res = await request.get(`/admin/organizers/${org.organizer_id}`)
    const detail = res.data.data || res.data
    currentOrg.value = {
      ...detail,
      org_proof_image: detail.org_proof_image || '',
      org_proof_text: detail.org_proof_text || ''
    }
    showRejectReason.value = false
    rejectReason.value = ''
    orgModalVisible.value = true
  } catch (e) {
    showApiError(e, '获取组织者详情失败')
  }
}

const approveOrganizer = async () => {
  try {
    await request.put(`/admin/organizers/${currentOrg.value.organizer_id}/review`, { action: 'approve' })
    alert('已通过')
    orgModalVisible.value = false
    fetchOrganizers()
  } catch (e) {
    showApiError(e, '操作失败')
  }
}

const openRejectOrgModal = () => {
  showRejectReason.value = true
}

const confirmRejectOrganizer = async () => {
  if (!rejectReason.value.trim()) {
    alert('请填写拒绝理由')
    return
  }
  try {
    await request.put(`/admin/organizers/${currentOrg.value.organizer_id}/review`, {
      action: 'reject',
      reject_reason: rejectReason.value
    })
    alert('已拒绝')
    orgModalVisible.value = false
    fetchOrganizers()
  } catch (e) {
    showApiError(e, '操作失败')
  }
}

// 获取管理员列表
const fetchAdmins = async () => {
  adminLoading.value = true
  try {
    const res = await request.get('/admin/admins')
    let adminList = res.data.data
    if (Array.isArray(adminList)) {
      admins.value = adminList
    } else if (adminList && Array.isArray(adminList.list)) {
      admins.value = adminList.list
    } else if (adminList && Array.isArray(adminList.items)) {
      admins.value = adminList.items
    } else {
      admins.value = []
    }
    stats.adminCount = admins.value.length
  } catch (e) {
    showApiError(e, '获取管理员列表失败')
  } finally {
    adminLoading.value = false
  }
}

const openAddAdminModal = () => {
  newAdmin.username = ''
  newAdmin.email = ''
  newAdmin.password = ''
  adminModalVisible.value = true
}

const addAdmin = async () => {
  if (!newAdmin.username || !newAdmin.email || !newAdmin.password) {
    alert('请填写完整')
    return
  }
  try {
    await request.post('/admin/admins', {
      username: newAdmin.username,
      email: newAdmin.email,
      password: newAdmin.password,
      role: 'admin'
    })
    alert('管理员添加成功')
    adminModalVisible.value = false
    fetchAdmins()
  } catch (e) {
    showApiError(e, '操作失败')
  }
}

const deleteAdmin = async (id: number) => {
  if (!confirm('确定删除该管理员吗？')) return
  try {
    await request.delete(`/admin/admins/${id}`)
    alert('已删除')
    fetchAdmins()
  } catch (e) {
    showApiError(e, '操作失败')
  }
}

// 监听分页和筛选变化
watch(userPage, () => {
  if (activeTab.value === 'user') fetchUsers()
})
watch(orgPage, () => {
  if (activeTab.value === 'organizer') fetchOrganizers()
})
watch([() => userFilters.student_id, () => userFilters.college], () => {
  if (activeTab.value === 'user') {
    userPage.value = 1
    fetchUsers()
  }
})
watch([() => orgFilters.name, () => orgFilters.status], () => {
  if (activeTab.value === 'organizer') {
    orgPage.value = 1
    fetchOrganizers()
  }
})

onMounted(() => {
  fetchUsers()
  fetchOrganizers()
  fetchAdmins()
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
</style>