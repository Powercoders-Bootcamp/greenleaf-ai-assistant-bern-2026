import { useState } from 'react'
import AdminChatsTab from './AdminChatsTab'
import './AdminPanel.css'
import AdminRetentionTab from './AdminRetentionTab'
import AdminUsersTab from './AdminUsersTab'

type Props = {
  token: string | null
}

export default function AdminPanel({ token }: Props) {
  const [tab, setTab] = useState<'chats' | 'users' | 'retention'>('chats')

  return (
    <section className="admin-panel">
      <div className="admin-panel__header admin-panel__header--compact">
        <div className="admin-tabs" role="tablist" aria-label="Admin sections">
          <button
            type="button"
            role="tab"
            aria-selected={tab === 'chats'}
            className={`admin-tab-button ${tab === 'chats' ? 'is-active' : ''}`}
            onClick={() => setTab('chats')}
          >
            Chats
          </button>

          <button
            type="button"
            role="tab"
            aria-selected={tab === 'users'}
            className={`admin-tab-button ${tab === 'users' ? 'is-active' : ''}`}
            onClick={() => setTab('users')}
          >
            Users
          </button>

          <button
            type="button"
            role="tab"
            aria-selected={tab === 'retention'}
            className={`admin-tab-button ${tab === 'retention' ? 'is-active' : ''}`}
            onClick={() => setTab('retention')}
          >
            Retention
          </button>
        </div>
      </div>

      {tab === 'chats' && <AdminChatsTab token={token} />}
      {tab === 'users' && <AdminUsersTab token={token} />}
      {tab === 'retention' && <AdminRetentionTab token={token} />}
    </section>
  )
}