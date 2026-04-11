import { useEffect, useMemo, useState } from 'react'
import type {
  AdminUser,
  AdminUserCreatePayload,
  AdminUserUpdatePayload,
} from '../../types/admin'

type Props = {
  open: boolean
  mode: 'create' | 'edit'
  user?: AdminUser | null
  loading?: boolean
  error?: string | null
  onClose: () => void
  onSubmit: (
    payload: AdminUserCreatePayload | AdminUserUpdatePayload
  ) => Promise<void> | void
}

type FormState = {
  email: string
  display_name: string
  password: string
  role: string
  is_active: boolean
}

const INITIAL_FORM: FormState = {
  email: '',
  display_name: '',
  password: '',
  role: 'employee',
  is_active: true,
}

export default function UsersModal({
  open,
  mode,
  user,
  loading = false,
  error = null,
  onClose,
  onSubmit,
}: Props) {
  const [form, setForm] = useState<FormState>(INITIAL_FORM)

  useEffect(() => {
    if (!open) return

    if (mode === 'edit' && user) {
      setForm({
        email: user.email ?? '',
        display_name: user.display_name ?? '',
        password: '',
        role: user.role ?? 'employee',
        is_active: user.is_active ?? true,
      })
      return
    }

    setForm(INITIAL_FORM)
  }, [open, mode, user])

  const title = useMemo(
    () => (mode === 'create' ? 'Create user' : 'Edit user'),
    [mode]
  )

  if (!open) return null

  const updateField = <K extends keyof FormState>(key: K, value: FormState[K]) => {
    setForm((prev) => ({ ...prev, [key]: value }))
  }

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    const email = form.email.trim()
    const displayName = form.display_name.trim()
    const password = form.password.trim()
    const role = form.role.trim()

    if (mode === 'create') {
      await onSubmit({
        email,
        display_name: displayName,
        password,
        role,
        is_active: form.is_active,
      })
      return
    }

    await onSubmit({
      email,
      display_name: displayName,
      password: password ? password : undefined,
      role,
      is_active: form.is_active,
    })
  }

  return (
    <div
      className="admin-modal__backdrop"
      role="presentation"
      onClick={() => {
        if (loading) return
        onClose()
      }}
    >
      <div
        className="admin-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="admin-user-modal-title"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="admin-modal__header">
          <h3 id="admin-user-modal-title">{title}</h3>

          <button
            type="button"
            className="admin-icon-button"
            onClick={onClose}
            disabled={loading}
            aria-label="Close modal"
          >
            ×
          </button>
        </div>

        <form className="admin-modal__form" onSubmit={handleSubmit}>
          <label className="admin-field">
            <span>Email</span>
            <input
              type="email"
              value={form.email}
              onChange={(event) => updateField('email', event.target.value)}
              required
              disabled={loading}
              autoComplete="email"
            />
          </label>

          <label className="admin-field">
            <span>Display name</span>
            <input
              type="text"
              value={form.display_name}
              onChange={(event) => updateField('display_name', event.target.value)}
              required
              disabled={loading}
              autoComplete="name"
            />
          </label>

          <label className="admin-field">
            <span>{mode === 'create' ? 'Password' : 'New password (optional)'}</span>
            <input
              type="password"
              value={form.password}
              onChange={(event) => updateField('password', event.target.value)}
              required={mode === 'create'}
              disabled={loading}
              autoComplete={mode === 'create' ? 'new-password' : 'off'}
            />
          </label>

          <label className="admin-field">
            <span>Role</span>
            <select
              value={form.role}
              onChange={(event) => updateField('role', event.target.value)}
              disabled={loading}
            >
              <option value="employee">employee</option>
              <option value="admin">admin</option>
              <option value="user">user</option>
            </select>
          </label>

          <label className="admin-checkbox">
            <input
              type="checkbox"
              checked={form.is_active}
              onChange={(event) => updateField('is_active', event.target.checked)}
              disabled={loading}
            />
            <span>Active account</span>
          </label>

          {error && <p className="admin-feedback admin-feedback--error">{error}</p>}

          <div className="admin-modal__actions">
            <button
              type="button"
              className="admin-button admin-button--ghost"
              onClick={onClose}
              disabled={loading}
            >
              Cancel
            </button>

            <button type="submit" className="admin-button" disabled={loading}>
              {loading ? 'Saving...' : mode === 'create' ? 'Create user' : 'Save changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}