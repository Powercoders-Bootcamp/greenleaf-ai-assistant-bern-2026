import { useCallback, useEffect, useMemo, useState } from 'react'
import { apiRequest } from '../../lib/api'
import type { AdminChatItem, AdminChatPageResponse } from '../../types/admin'
import ChatRetentionBar from './ChatRetentionBar'

type Props = {
  token: string | null
}

type SortOption = 'updated_desc' | 'updated_asc' | 'created_desc' | 'created_asc' | 'messages_desc'

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

function matchesSearch(chat: AdminChatItem, query: string) {
  const normalizedQuery = query.trim().toLowerCase()

  if (!normalizedQuery) return true

  const title = String(chat.title ?? '').toLowerCase()
  const idText = String(chat.id)
  const messageCountText = String(chat.message_count)

  return (
    title.includes(normalizedQuery) ||
    idText.includes(normalizedQuery) ||
    messageCountText.includes(normalizedQuery)
  )
}

function sortChats(items: AdminChatItem[], sort: SortOption) {
  const next = [...items]

  next.sort((a, b) => {
    const updatedA = new Date(a.updated_at).getTime()
    const updatedB = new Date(b.updated_at).getTime()
    const createdA = new Date(a.created_at).getTime()
    const createdB = new Date(b.created_at).getTime()

    switch (sort) {
      case 'updated_asc':
        return updatedA - updatedB

      case 'created_desc':
        return createdB - createdA

      case 'created_asc':
        return createdA - createdB

      case 'messages_desc':
        return b.message_count - a.message_count

      case 'updated_desc':
      default:
        return updatedB - updatedA
    }
  })

  return next
}

function getRecencyLabel(updatedAt: string) {
  const updated = new Date(updatedAt).getTime()

  if (Number.isNaN(updated)) return 'Unknown'

  const diffMs = Date.now() - updated
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
  const diffDays = Math.floor(diffHours / 24)

  if (diffHours < 1) return 'Updated recently'
  if (diffHours < 24) return `Updated ${diffHours}h ago`
  if (diffDays === 1) return 'Updated yesterday'
  return `Updated ${diffDays}d ago`
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

  const [search, setSearch] = useState('')
  const [sortBy, setSortBy] = useState<SortOption>('updated_desc')

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

  const visibleItems = useMemo(() => {
    const filtered = items.filter((chat) => matchesSearch(chat, search))
    return sortChats(filtered, sortBy)
  }, [items, search, sortBy])

  const selectedChat = useMemo(
    () => visibleItems.find((item) => item.id === selectedChatId) ?? items.find((item) => item.id === selectedChatId) ?? null,
    [items, selectedChatId, visibleItems]
  )

  useEffect(() => {
    if (visibleItems.length === 0) {
      return
    }

    if (!selectedChatId) {
      setSelectedChatId(visibleItems[0].id)
      return
    }

    const existsInVisible = visibleItems.some((item) => item.id === selectedChatId)

    if (!existsInVisible) {
      setSelectedChatId(visibleItems[0].id)
    }
  }, [selectedChatId, visibleItems])

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
  const hasFilters = Boolean(search.trim()) || sortBy !== 'updated_desc'

  return (
    <section className="admin-tab admin-chats-tab">
      <div className="admin-tab__header">
        <div>
          <h2>Anonymous chats</h2>
          <p>
            Review chat metadata, timestamps, retention state and conversation volume.
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

      <div className="admin-toolbar">
        <label className="admin-field admin-field--search">
          <span>Search</span>
          <input
            type="text"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search by title, chat id or message count"
          />
        </label>

        <label className="admin-field admin-field--compact">
          <span>Sort by</span>
          <select
            value={sortBy}
            onChange={(event) => setSortBy(event.target.value as SortOption)}
          >
            <option value="updated_desc">Recently updated</option>
            <option value="updated_asc">Oldest updated</option>
            <option value="created_desc">Recently created</option>
            <option value="created_asc">Oldest created</option>
            <option value="messages_desc">Most messages</option>
          </select>
        </label>

        {hasFilters && (
          <button
            type="button"
            className="admin-button admin-button--ghost"
            onClick={() => {
              setSearch('')
              setSortBy('updated_desc')
            }}
          >
            Reset filters
          </button>
        )}
      </div>

      {loading && <p className="admin-feedback">Loading conversations...</p>}
      {error && <p className="admin-feedback admin-feedback--error">{error}</p>}

      <div className="admin-master-detail">
        <aside className="admin-sidebar">
          <div className="admin-sidebar__head">
            <span>{totalItems} conversations total</span>
            <span>
              Page {page} / {Math.max(totalPages, 1)}
            </span>
          </div>

          <div className="admin-sidebar__summary">
            <span>{visibleItems.length} visible on this page</span>
            <span>{pageSize} per page</span>
          </div>

          <div className="admin-chat-list">
            {!loading &&
              visibleItems.map((chat) => {
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
                      <span>ID: #{chat.id}</span>
                      <span>Created: {formatDate(chat.created_at)}</span>
                      <span>Updated: {formatDate(chat.updated_at)}</span>
                    </div>

                    <div className="admin-chat-card__footer">
                      <span className="admin-pill admin-pill--soft">
                        {getRecencyLabel(chat.updated_at)}
                      </span>
                    </div>
                  </button>
                )
              })}

            {!loading && visibleItems.length === 0 && (
              <div className="admin-empty">
                {items.length === 0
                  ? 'No conversations found.'
                  : 'No conversations match the current filters.'}
              </div>
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

              <div className="admin-inspector-grid">
                <div className="admin-detail__placeholder">
                  <h4>Conversation overview</h4>
                  <p>
                    This chat is available in the admin list endpoint and can be reviewed
                    through metadata such as title, message count, creation time and last
                    update.
                  </p>
                </div>

                <div className="admin-detail__placeholder">
                  <h4>Retention and privacy</h4>
                  <p>
                    Anonymous chat review is intentionally limited. The current admin API
                    exposes retention-safe metadata only and does not return the full
                    message thread or direct identifiers.
                  </p>
                </div>
              </div>

              <div className="admin-detail__placeholder">
                <h4>What you can do here</h4>
                <p>
                  Use this panel to inspect activity patterns, review stale conversations,
                  identify chats with unusually high message counts and apply retention
                  cleanup when needed.
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