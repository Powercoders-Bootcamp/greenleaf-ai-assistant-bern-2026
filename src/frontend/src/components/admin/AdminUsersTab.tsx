import { useCallback, useEffect, useMemo, useState } from 'react'
import { apiRequest } from '../../lib/api'
import type { AdminUser } from '../../types/admin'
import UsersModal from './UsersModal'

type Props = {
  token: string | null
}

type UserSubmitPayload = {
  email: string
  display_name: string
  password?: string
  role: 'Admin' | 'Employee'
  is_active: boolean
}

export default function AdminUsersTab({ token }: Props) {
  const [users, setUsers] = useState<AdminUser[]>([])
  const [loading, setLoading] = useState(false)
  const [refreshing, setRefreshing] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [modalOpen, setModalOpen] = useState(false)
  const [editingUser, setEditingUser] = useState<AdminUser | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState<string | null>(null)

  const sortedUsers = useMemo(() => {
    return [...users].sort((a, b) => {
      const roleCompare = String(a.role).localeCompare(String(b.role))
      if (roleCompare !== 0) return roleCompare

      const nameA = a.display_name?.trim() || a.email
      const nameB = b.display_name?.trim() || b.email
      return nameA.localeCompare(nameB)
    })
  }, [users])

  const loadUsers = useCallback(
    async (mode: 'initial' | 'refresh' = 'initial') => {
      if (!token) return

      if (mode === 'refresh') {
        setRefreshing(true)
      } else {
        setLoading(true)
      }

      setError(null)

      try {
        const data = await apiRequest<AdminUser[]>('/users', { token })
        setUsers(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load users.')
      } finally {
        setLoading(false)
        setRefreshing(false)
      }
    },
    [token]
  )

  useEffect(() => {
    void loadUsers()
  }, [loadUsers])

  const handleCreate = () => {
    setEditingUser(null)
    setSubmitError(null)
    setModalOpen(true)
  }

  const handleEdit = (user: AdminUser) => {
    setEditingUser(user)
    setSubmitError(null)
    setModalOpen(true)
  }

  const handleCloseModal = () => {
    if (submitting) return
    setModalOpen(false)
    setEditingUser(null)
    setSubmitError(null)
  }

  const handleDelete = async (user: AdminUser) => {
    if (!token) return

    const confirmed = window.confirm(`Delete user "${user.email}"?`)
    if (!confirmed) return

    try {
      setError(null)

      await apiRequest<void>(`/users/${user.id}`, {
        method: 'DELETE',
        token,
      })

      await loadUsers('refresh')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete user.')
    }
  }

  const handleSubmit = async (payload: UserSubmitPayload) => {
    if (!token) return

    setSubmitting(true)
    setSubmitError(null)

    try {
      if (editingUser) {
        await apiRequest(`/users/${editingUser.id}`, {
          method: 'PUT',
          body: payload,
          token,
        })
      } else {
        await apiRequest('/users', {
          method: 'POST',
          body: payload,
          token,
        })
      }

      setModalOpen(false)
      setEditingUser(null)
      await loadUsers('refresh')
    } catch (err) {
      setSubmitError(err instanceof Error ? err.message : 'Failed to save user.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <section className="admin-tab">
      <div className="admin-tab__header">
        <div>
          <h2>User management</h2>
          <p>Manage admin and employee accounts.</p>
        </div>

        <div className="admin-tab__actions">
          <button
            type="button"
            className="admin-button admin-button--ghost"
            onClick={() => void loadUsers('refresh')}
            disabled={loading || refreshing}
          >
            {refreshing ? 'Refreshing...' : 'Refresh'}
          </button>

          <button
            type="button"
            className="admin-button"
            onClick={handleCreate}
            disabled={loading}
          >
            Create user
          </button>
        </div>
      </div>

      {loading && <p className="admin-feedback">Loading users...</p>}
      {error && <p className="admin-feedback admin-feedback--error">{error}</p>}

      <div className="admin-table-wrap">
        <table className="admin-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Email</th>
              <th>Name</th>
              <th>Role</th>
              <th>Status</th>
              <th aria-label="Actions" />
            </tr>
          </thead>

          <tbody>
            {sortedUsers.map((user) => (
              <tr key={user.id}>
                <td>{user.id}</td>
                <td>{user.email}</td>
                <td>{user.display_name}</td>
                <td>
                  <span className={`admin-pill admin-pill--${String(user.role).toLowerCase()}`}>
                    {user.role}
                  </span>
                </td>
                <td>
                  <span
                    className={`admin-pill ${
                      user.is_active ? 'admin-pill--success' : 'admin-pill--muted'
                    }`}
                  >
                    {user.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td>
                  <div className="admin-row-actions">
                    <button
                      type="button"
                      className="admin-button admin-button--ghost"
                      onClick={() => handleEdit(user)}
                    >
                      Edit
                    </button>

                    <button
                      type="button"
                      className="admin-button admin-button--danger"
                      onClick={() => void handleDelete(user)}
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}

            {!loading && sortedUsers.length === 0 && (
              <tr>
                <td colSpan={6}>
                  <div className="admin-empty">No users found.</div>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <UsersModal
        open={modalOpen}
        mode={editingUser ? 'edit' : 'create'}
        user={editingUser}
        loading={submitting}
        error={submitError}
        onClose={handleCloseModal}
        onSubmit={handleSubmit}
      />
    </section>
  )
}