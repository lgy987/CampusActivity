import { apiPost, apiUpload } from './request'
import type { LoginData, RegisterData } from '@/types/api'

export interface RegisterPayload {
  student_id: string
  email: string
  username: string
  password: string
  confirm_password: string
  gender: string
  college: string
  major: string
  grade: string
  phone?: string | null
}

export interface OrganizerRegisterPayload {
  email: string
  org_name: string
  password: string
  confirm_password: string
  org_proof_text?: string
  org_proof_image?: string
}

// 登录：接收对象参数 { role, account, password }
export function login(data: { role: string; account: string; password: string }) {
  return apiPost<LoginData>('/auth/login', data)
}

// 普通用户注册
export function register(payload: RegisterPayload) {
  return apiPost<RegisterData>('/auth/register/user', payload)
}

// 组织者注册
export function registerOrganizer(payload: OrganizerRegisterPayload) {
  return apiPost<RegisterData>('/auth/register/organizer', payload)
}


export function uploadOrganizerProof(formData: FormData) {
  return apiUpload<{ image_url: string }>('/auth/upload-organizer-proof', formData)
}
// 退出登录
export function logout() {
  return apiPost<null>('/auth/logout')}
