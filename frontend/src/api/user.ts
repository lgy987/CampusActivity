import { apiDelete, apiGet, apiPost, apiPut, apiUpload } from './request'
import type { UserProfile } from '@/types/api'

export function getProfile() {
  return apiGet<UserProfile>('/user/profile')
}

export function updateProfile(data: Partial<UserProfile>) {
  return apiPut<null>('/user/profile', data)
}

export function uploadAvatar(file: File) {
  const form = new FormData()
  form.append('avatar', file)
  return apiUpload<{ avatar_url: string }>('/user/avatar', form)

}

/** 文档 3.4：POST /user/reset-password */
export function resetPassword(payload: {
  old_password: string
  new_password: string
  confirm_password: string
}) {
  return apiPost<null>('/user/reset-password', payload)
}

export function deleteAccount() {
  return apiDelete<null>('/user/account', { confirm: true })
}
