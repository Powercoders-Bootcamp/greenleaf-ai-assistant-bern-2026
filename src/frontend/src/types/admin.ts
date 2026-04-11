export type AdminChatItem = {
  id: number
  title: string
  created_at: string
  updated_at: string
  message_count: number
}

export type AdminChatPageResponse = {
  items: AdminChatItem[]
  page: number
  page_size: number
  total_items: number
  total_pages: number
}

export type ChatRetentionCleanupResponse = {
  deleted_count: number
}

export type AdminUserRole = 'admin' | 'employee' | 'user'

export type AdminUser = {
  id: number
  email: string
  display_name: string
  role: AdminUserRole | string
  is_active: boolean
  created_at?: string
  updated_at?: string
}

export type AdminUserCreatePayload = {
  email: string
  display_name: string
  password: string
  role: string
  is_active: boolean
}

export type AdminUserUpdatePayload = {
  email: string
  display_name: string
  password?: string
  role: string
  is_active: boolean
}