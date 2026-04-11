import { useState } from 'react'
import AdminChatsTab from './AdminChatsTab'
import './AdminPanel.css'
import AdminUsersTab from './AdminUsersTab'

type Props = {
  token: string | null
}

export default function AdminPanel({ token }: Props) {
  const [tab, setTab] = useState<'chats' | 'users'>('chats')

  return (
    <section className="admin-panel">
      <div className="admin-panel__header">
        <div>
          <p className="eyebrow">Admin workspace</p>
          <h1>Admin Panel</h1>
          <p className="subtext">
            Review anonymous chat history, retention state and managed users.
          </p>
        </div>

        <div className="admin-tabs">
          <button
            type="button"
            className={`admin-tab-button ${tab === 'chats' ? 'is-active' : ''}`}
            onClick={() => setTab('chats')}
          >
            Chats
          </button>
          <button
            type="button"
            className={`admin-tab-button ${tab === 'users' ? 'is-active' : ''}`}
            onClick={() => setTab('users')}
          >
            Users
          </button>
        </div>
      </div>

      {tab === 'chats' ? <AdminChatsTab token={token} /> : <AdminUsersTab token={token} />}
    </section>
  )
}