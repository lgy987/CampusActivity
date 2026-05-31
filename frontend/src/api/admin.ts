import { apiGet, apiPost, apiPut, apiDelete } from './request'
import type { ActivityListItem, CategoryNode, UserProfile } from '@/types/api'
import type { ActivityDetail } from '@/types/api'
// ==================== 活动管理 ====================

export function getAdminActivities(params?: {
  page?: number
  page_size?: number
  status?: string
  category_id?: number
  keyword?: string
}) {
  return apiGet<{ list: ActivityListItem[]; total: number }>('/admin/activities', params)
}

export function getActivityDetail(activityId: number) {
  return apiGet<ActivityDetail>(`/admin/activities/${activityId}`)
}

export function auditActivity(activityId: number, status: 'approved' | 'rejected', remark?: string) {
  return apiPost<null>(`/admin/activities/${activityId}/review`, { status, remark })
}

export function deleteActivity(activityId: number) {
  return apiDelete<null>(`/admin/activities/${activityId}`)
}

export function getActivityRegistrations(activityId: number, params?: { page?: number; page_size?: number; status?: string }) {
  return apiGet<{ items: any[]; total: number }>(`/admin/activities/${activityId}/registrations`, params)
}

export function reviewActivity(activityId: number, action: 'approve' | 'reject', rejectReason?: string) {
  return apiPut<{ activity_id: number; new_status: string }>(`/admin/activities/${activityId}/review`, {
    action,
    reject_reason: rejectReason,
  })
}

export function removeActivity(activityId: number, reason: string) {
  return apiPut<null>(`/admin/activities/${activityId}/remove`, { reason })
}

// ==================== 用户管理 ====================

export function getUsers(params?: {
  page?: number
  page_size?: number
  role?: 'user' | 'organizer' | 'admin'
  status?: 'active' | 'banned' | 'pending'
  keyword?: string
}) {
  return apiGet<{ items: UserProfile[]; total: number }>('/admin/users', params)
}

export function getUserDetail(userId: number) {
  return apiGet<UserProfile>(`/admin/users/${userId}`)
}

export function updateUserStatus(userId: number, status: 'active' | 'banned') {
  return apiPut<null>(`/admin/users/${userId}/status`, { status })
}

export function resetUserPassword(userId: number, newPassword: string) {
  return apiPost<null>(`/admin/users/${userId}/reset-password`, { password: newPassword })
}

// 获取组织者列表
export function getOrganizers(params?: { page?: number; page_size?: number; org_name?: string; status?: string }) {
  return apiGet<{ items: any[]; total: number }>('/admin/organizers', params)
}

// 审核组织者
export function reviewOrganizer(organizerId: number, action: 'approve' | 'reject', rejectReason?: string) {
  return apiPut<{ organizer_id: number; status: string }>(`/admin/organizers/${organizerId}/review`, {
    action,
    reject_reason: rejectReason,
  })
}

// 获取管理员列表
export function getAdmins() {
  return apiGet<any[]>('/admin/admins')
}

// 创建管理员
export function createAdmin(data: { email: string; password: string; username: string; role?: string }) {
  return apiPost<{ admin_id: number; admin_no: string }>('/admin/admins', data)
}

// 删除管理员
export function deleteAdmin(adminId: number) {
  return apiDelete<null>(`/admin/admins/${adminId}`)
}

// ==================== 分类管理 ====================

export function getCategories() {
  return apiGet<CategoryNode[]>('/categories')
}

export function createCategory(data: { name: string; parent_id?: number; sort_order?: number }) {
  return apiPost<CategoryNode>('/admin/categories', data)
}

export function updateCategory(categoryId: number, data: { name?: string; sort_order?: number }) {
  return apiPut<CategoryNode>(`/admin/categories/${categoryId}`, data)
}

export function deleteCategory(categoryId: number) {
  return apiDelete<null>(`/admin/categories/${categoryId}`)
}

// ==================== 统计 ====================

export function getPlatformStatistics() {
  return apiGet<{
    activities: {
      total: number
      by_status: Record<string, number>
      by_categories: Record<string, number>
    }
    user: {
      total: number
      student: number
      organize: number
      admin: number
    }
    total_participation_count: number
    average_checkin_rate: string
  }>('/admin/statistics')
}

// 保留原有的 getStatistics 以防其他页面使用
export function getStatistics(params?: { start_date?: string; end_date?: string; campus?: string }) {
  return apiGet<{
    total_users: number
    total_activities: number
    total_registrations: number
    activity_trend: Array<{ date: string; count: number }>
    category_distribution: Array<{ category: string; count: number }>
    campus_distribution: Array<{ campus: string; count: number }>
  }>('/admin/statistics', params)
}

// ==================== 公告管理 ====================

export function getAnnouncements() {
  return apiGet<any[]>('/announcements')
}

export function publishAnnouncement(data: { title: string; content: string; start_time?: string; end_time?: string }) {
  return apiPost<{ announcement_id: number }>('/admin/announcements', data)
}

export function removeAnnouncement(id: number) {
  return apiDelete<null>(`/admin/announcements/${id}`)
}