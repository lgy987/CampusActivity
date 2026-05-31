// src/api/organizer.ts
import { apiGet, apiPost, apiPut, apiDelete } from './request'
import type { ActivityDetail, ActivityListItem, CategoryNode, PaginatedList } from '@/types/api'

export interface ActivityQuery {
  page?: number
  page_size?: number
  /** 支持多状态逗号分隔，如 open,ongoing */
  status?: string
  category_id?: number
  campus?: string
  keyword?: string
  start_date?: string
}

export function getActivities(params: ActivityQuery) {
  return apiGet<PaginatedList<ActivityListItem>>('/activities', params as Record<string, unknown>)
}


export function getActivityDetail(id: number) {
  return apiGet<ActivityDetail>(`/activities/${id}`)
}

export function getCategories() {
  return apiGet<CategoryNode[]>('/categories')
}

