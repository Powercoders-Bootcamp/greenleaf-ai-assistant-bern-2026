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
        </div>
      </div>

      {tab === 'chats' ? <AdminChatsTab token={token} /> : <AdminUsersTab token={token} />}
    </section>
  )
}