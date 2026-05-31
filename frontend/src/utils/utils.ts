import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDateTime(value?: string | null): string {
  if (!value) return '-'
  
  // ISO 格式 "2026-06-03T19:08:00Z" 可以直接解析
  const d = new Date(value)
  
  if (Number.isNaN(d.getTime())) return value
  
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}