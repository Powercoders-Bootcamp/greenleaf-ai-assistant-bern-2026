export type Message = {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

export type AdminChat = {
  id: number
  title: string
  created_at: string
  updated_at: string
  message_count: number
}

export type AdminChatListResponse = {
  chats: AdminChat[]
  total: number
  page: number
  per_page: number
}