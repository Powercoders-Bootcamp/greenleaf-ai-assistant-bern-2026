export type UserRole = 'admin' | 'user'

export type AuthMode = 'login' | 'register' | 'forgot-password'

export type AuthUser = {
  id: string
  email: string
  role: UserRole
  name?: string
}

export type AuthResponse = {
  token: string
  user: AuthUser
}