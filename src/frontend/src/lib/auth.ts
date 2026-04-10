import type { AuthResponse, AuthUser } from '../types/auth'

const TOKEN_KEY = 'greenleaf_auth_token'
const USER_KEY = 'greenleaf_auth_user'

export function getStoredToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function setStoredToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token)
}

export function clearStoredToken(): void {
  localStorage.removeItem(TOKEN_KEY)
}

export function getStoredUser(): AuthUser | null {
  const raw = localStorage.getItem(USER_KEY)

  if (!raw) return null

  try {
    return JSON.parse(raw) as AuthUser
  } catch {
    localStorage.removeItem(USER_KEY)
    return null
  }
}

export function setStoredUser(user: AuthUser): void {
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

export function clearStoredUser(): void {
  localStorage.removeItem(USER_KEY)
}

export function clearAuthSession(): void {
  clearStoredToken()
  clearStoredUser()
}

export function persistAuthSession(payload: AuthResponse): void {
  setStoredToken(payload.token)
  setStoredUser(payload.user)
}