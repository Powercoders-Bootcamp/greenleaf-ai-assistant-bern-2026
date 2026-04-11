export type AdminChatItem = {
  id: number
  title: string | null
  created_at: string
  updated_at: string
  message_count: number
}

export type AdminChatMessage = {
  id: number
  chat_id: number
  sender_type: 'user' | 'assistant' | 'system'
  content_masked: string
  created_at: string
}

export type AdminChatDetail = AdminChatItem & {
  messages: AdminChatMessage[]
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

export type AdminUserRole = 'Admin' | 'Employee'

export type AdminUserCreatePayload = {
  email: string
  display_name: string
  password: string
  role: AdminUserRole
  is_active: boolean
}

export type AdminUserUpdatePayload = {
  email: string
  display_name: string
  password?: string
  role: AdminUserRole
  is_active: boolean
}

export type AdminUser = {
  id: number
  email: string
  display_name: string
  role: AdminUserRole | string
  is_active: boolean
  created_at?: string
  updated_at?: string
}
