export type UserRole = 'Admin' | 'Employee'

export type AuthMode = 'login' | 'register' | 'forgot-password'

export type AuthUser = {
  id: string | number
  email: string
  role: UserRole
  display_name?: string | null
}

export type AuthResponse = {
  token: string
  user: AuthUser
}
