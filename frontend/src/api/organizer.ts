import { apiGet, apiPost, apiPut, apiDelete } from './request'
import type {
  ActivityListItem,
  ActivityDetail,
  CategoryNode,
  RegistrationItem,
} from '@/types/api'

// ==================== 4. 活动管理接口 ====================

// 4.1 创建活动（草稿）
export function createActivity(data: {
  name: string
  category_id: number
  start_time: string
  end_time: string
  campus: string
  location: string
  max_participants: number
  registration_deadline: string
  cancel_deadline: string
  description: string
}) {
  return apiPost<{ activity_id: number; status: 'draft' | 'pending' }>('/organizer/activities', data)
}

// 4.2 提交审核
export function submitActivity(activityId: number) {
  return apiPost<{ activity_id: number; status: 'pending' | 'edit_pending' }>(
    `/organizer/activities/${activityId}/submit`
  )
}

// 4.5 更新活动
export function updateActivity(
  activityId: number,
  data: {
    name?: string
    category_id?: number
    start_time?: string
    end_time?: string
    campus?: string
    location?: string
    max_participants?: number
    registration_deadline?: string
    cancel_deadline?: string
    description?: string
  }
) {
  return apiPut<{ activity_id: number; status: string }>(`/organizer/activities/${activityId}`, data)
}

// 4.6 删除活动
export function deleteActivity(activityId: number) {
  return apiDelete<null>(`/organizer/activities/${activityId}`)
}

// 4.7 获取我发布的活动
export function getMyActivities(params?: {
  page?: number
  page_size?: number
  status?: 'draft' | 'pending' | 'approved' | 'rejected' | 'open' | 'closed' | 'cancelled'
}) {
  return apiGet<{ total: number; page: number; page_size: number; list: ActivityListItem[] }>(
    '/organizer/activities',
    params
  )
}

// 获取单个活动详情（组织者视角，用于编辑）
export function getActivityDetail(activityId: number) {
  return apiGet<ActivityDetail>(`/activities/${activityId}`)
}

// ==================== 5. 报名管理（组织者） ====================

// 5.4 获取活动报名人员列表
export function getActivityRegistrations(
  activityId: number,
  params?: {
    page?: number
    page_size?: number
    status?: 'registered' | 'cancelled' | 'rejected'
    checkin_status?: 'checked' | 'not_checked'
  }
) {
  return apiGet<{
    total: number
    list: {
      registration_id: number
      user_id: number
      student_id: string
      gender: string
      college: string
      major: string
      grade: string
      registration_time: string
      status: string
      reject_reason: string | null
      checkin_status: string
    }[]
  }>(`/organizer/activities/${activityId}/registrations`, params)
}

// 5.5 拒绝报名
export function rejectRegistration(registrationId: number, reason: string) {
  return apiPost<{ new_status: string; reject_count: number }>(`/organizer/registrations/${registrationId}/reject`, {
    reason,
  })
}

// 5.6 获取活动数据统计
export function getRegistrationStats(activityId: number) {
  return apiGet<{
    total_registered: number
    remaining_slots: number
    total_checked: number
    by_gender: Record<string, number>
    by_college: Record<string, number>
    by_grade: Record<string, number>
    by_major: Record<string, number>
  }>(`/activities/${activityId}/registration-stats`)
}

// ==================== 6. 签到接口 ====================

// 6.1 获取签到码
export function getCheckinCode(activityId: number) {
  return apiGet<{ checkin_code: string }>(`/organizer/activities/${activityId}/checkin-code`)
}

// 6.3 手动签到
export function manualCheckin(activityId: number, student_id: string) {
  return apiPost<{ user_id: number; checkin_time: string }>(
    `/organizer/activities/${activityId}/manual-checkin`,
    { student_id }
  )
}

// 6.5 获取活动签到情况
export function getActivityCheckins(activityId: number) {
  return apiGet<{
    total_registered: number
    checked_in: number
    not_checked_in: number
    checkin_rate: string
    checkin_list: {
      user_id: number
      student_id: string
      checkin_time: string
      checkin_method: string
    }[]
    notCheckedIn: {
      user_id: number
      student_id: string
    }[]
  }>(`/organizer/activities/${activityId}/checkins`)
}

// ==================== 其他 ====================

// 4.8 获取分类列表
export function getCategories() {
  return apiGet<CategoryNode[]>('/categories')
}