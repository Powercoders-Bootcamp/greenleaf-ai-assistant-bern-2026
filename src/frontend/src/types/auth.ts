export type UserRole = 'Admin' | 'Employee'

export type AuthUser = {
  id: string | number
  email: string
  role: UserRole
  display_name?: string | null
}

export type AuthResponse = {
  access_token: string
  token_type: 'bearer'
  user: AuthUser
}