import { useCallback, useEffect, useMemo, useState } from 'react'
import { apiRequest } from '../../lib/api'
import type { AdminChatItem, AdminChatPageResponse } from '../../types/admin'
import ChatRetentionBar from './ChatRetentionBar'

type Props = {
  token: string | null
}

function formatDate(value: string) {
  const date = new Date(value)

  if (Number.isNaN(date.getTime())) {
    return value
  }

  return date.toLocaleString([], {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export default function AdminChatsTab({ token }: Props) {
  const [items, setItems] = useState<AdminChatItem[]>([])
  const [page, setPage] = useState(1)
  const [pageSize] = useState(20)
  const [totalPages, setTotalPages] = useState(1)
  const [totalItems, setTotalItems] = useState(0)
  const [selectedChatId, setSelectedChatId] = useState<number | null>(null)

  const [loading, setLoading] = useState(false)
  const [refreshing, setRefreshing] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const selectedChat = useMemo(
    () => items.find((item) => item.id === selectedChatId) ?? null,
    [items, selectedChatId]
  )

  const syncSelection = useCallback(
    (nextItems: AdminChatItem[]) => {
      if (nextItems.length === 0) {
        setSelectedChatId(null)
        return
      }

      if (!selectedChatId) {
        setSelectedChatId(nextItems[0].id)
        return
      }

      const exists = nextItems.some((item) => item.id === selectedChatId)

      if (!exists) {
        setSelectedChatId(nextItems[0].id)
      }
    },
    [selectedChatId]
  )

  const fetchChats = useCallback(
    async (mode: 'initial' | 'refresh' = 'initial') => {
      if (!token) return

      if (mode === 'refresh') {
        setRefreshing(true)
      } else {
        setLoading(true)
      }

      setError(null)

      try {
        const data = await apiRequest<AdminChatPageResponse>(
          `/admin/chats?page=${page}&page_size=${pageSize}`,
          { token }
        )

        setItems(data.items)
        setTotalPages(Math.max(data.total_pages, 1))
        setTotalItems(data.total_items)
        syncSelection(data.items)

        if (data.items.length === 0 && page > 1) {
          setPage((prev) => Math.max(1, prev - 1))
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load admin chats.')
      } finally {
        setLoading(false)
        setRefreshing(false)
      }
    },
    [page, pageSize, syncSelection, token]
  )

  useEffect(() => {
    void fetchChats()
  }, [fetchChats])

  const handleRefresh = async () => {
    await fetchChats('refresh')
  }

  const handleDeleteChat = async (chatId: number) => {
    if (!token) return

    const confirmed = window.confirm(`Delete anonymous chat #${chatId}?`)
    if (!confirmed) return

    try {
      setError(null)

      await apiRequest<void>(`/admin/chats/${chatId}`, {
        method: 'DELETE',
        token,
      })

      const remainingItems = items.filter((item) => item.id !== chatId)

      if (remainingItems.length === 0 && page > 1) {
        setPage((prev) => Math.max(1, prev - 1))
        return
      }

      await fetchChats('refresh')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not delete chat.')
    }
  }

  const canGoPrev = page > 1
  const canGoNext = page < totalPages

  return (
    <section className="admin-tab admin-chats-tab">
      <div className="admin-tab__header">
        <div>
          <h2>Anonymous chats</h2>
          <p>
            Review conversation metadata, timestamps and retention state.
          </p>
        </div>

        <div className="admin-tab__actions">
          <button
            type="button"
            className="admin-button admin-button--ghost"
            onClick={handleRefresh}
            disabled={loading || refreshing}
          >
            {refreshing ? 'Refreshing...' : 'Refresh'}
          </button>
        </div>
      </div>

      <ChatRetentionBar
        token={token}
        onCleanupSuccess={() => {
          void fetchChats('refresh')
        }}
      />

      {loading && <p className="admin-feedback">Loading conversations...</p>}
      {error && <p className="admin-feedback admin-feedback--error">{error}</p>}

      <div className="admin-master-detail">
        <aside className="admin-sidebar">
          <div className="admin-sidebar__head">
            <span>{totalItems} conversations</span>
            <span>
              Page {page} / {Math.max(totalPages, 1)}
            </span>
          </div>

          <div className="admin-chat-list">
            {!loading &&
              items.map((chat) => {
                const isActive = chat.id === selectedChatId

                return (
                  <button
                    key={chat.id}
                    type="button"
                    className={`admin-chat-card ${isActive ? 'is-active' : ''}`}
                    onClick={() => setSelectedChatId(chat.id)}
                  >
                    <div className="admin-chat-card__top">
                      <strong>{chat.title?.trim() || `Chat #${chat.id}`}</strong>

                      <span className="admin-pill admin-pill--muted">
                        {chat.message_count} msgs
                      </span>
                    </div>

                    <div className="admin-chat-card__meta">
                      <span>Created: {formatDate(chat.created_at)}</span>
                      <span>Updated: {formatDate(chat.updated_at)}</span>
                    </div>
                  </button>
                )
              })}

            {!loading && items.length === 0 && (
              <div className="admin-empty">No conversations found.</div>
            )}
          </div>

          <div className="admin-pagination">
            <button
              type="button"
              className="admin-button admin-button--ghost"
              disabled={!canGoPrev || loading || refreshing}
              onClick={() => setPage((prev) => Math.max(1, prev - 1))}
            >
              Previous
            </button>

            <button
              type="button"
              className="admin-button admin-button--ghost"
              disabled={!canGoNext || loading || refreshing}
              onClick={() => setPage((prev) => prev + 1)}
            >
              Next
            </button>
          </div>
        </aside>

        <section className="admin-detail">
          {selectedChat ? (
            <>
              <div className="admin-detail__header">
                <div>
                  <h3>{selectedChat.title?.trim() || `Chat #${selectedChat.id}`}</h3>
                  <p>Anonymous chat id #{selectedChat.id}</p>
                </div>

                <button
                  type="button"
                  className="admin-button admin-button--danger"
                  onClick={() => handleDeleteChat(selectedChat.id)}
                >
                  Delete chat
                </button>
              </div>

              <div className="admin-detail__meta-grid">
                <div className="admin-detail__meta-card">
                  <span className="admin-detail__label">Created</span>
                  <strong>{formatDate(selectedChat.created_at)}</strong>
                </div>

                <div className="admin-detail__meta-card">
                  <span className="admin-detail__label">Last updated</span>
                  <strong>{formatDate(selectedChat.updated_at)}</strong>
                </div>

                <div className="admin-detail__meta-card">
                  <span className="admin-detail__label">Messages</span>
                  <strong>{selectedChat.message_count}</strong>
                </div>
              </div>

              <div className="admin-detail__placeholder">
                <h4>Conversation detail</h4>
                <p>
                  This panel already shows conversation metadata and timestamps from the
                  admin list endpoint. To render the full message thread here, connect it
                  to an admin chat detail endpoint when that backend route is available.
                </p>
              </div>
            </>
          ) : (
            <div className="admin-empty admin-empty--detail">
              Select a conversation to review its metadata.
            </div>
          )}
        </section>
      </div>
    </section>
  )
}