import { useCallback, useEffect, useMemo, useState } from 'react'
import { apiRequest } from '../../lib/api'
import './UserChatHistory.css'

type HistoryChatItem = {
  id: number
  title: string | null
  created_at: string
  updated_at: string
  message_count: number
}

type HistoryMessage = {
  id: number
  chat_id: number
  sender_type: 'user' | 'assistant' | 'system'
  content_masked: string
  created_at: string
}

type HistoryChatDetail = {
  id: number
  title: string | null
  created_at: string
  updated_at: string
  message_count?: number
  messages: HistoryMessage[]
}

type HistoryChatPageResponse = {
  items: HistoryChatItem[]
  page: number
  page_size: number
  total_items: number
  total_pages: number
}

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

function formatThreadTimestamp(value: string) {
  const date = new Date(value)

  if (Number.isNaN(date.getTime())) {
    return value
  }

  return date.toLocaleString([], {
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
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

function getMessageAuthor(message: HistoryMessage) {
  if (message.sender_type === 'user') return 'You'
  if (message.sender_type === 'assistant') return 'Beat-Bot'
  return 'System'
}

function matchesSearch(chat: HistoryChatItem, query: string) {
  const normalizedQuery = query.trim().toLowerCase()

  if (!normalizedQuery) return true

  const title = String(chat.title ?? '').toLowerCase()
  const idText = String(chat.id)

  return title.includes(normalizedQuery) || idText.includes(normalizedQuery)
}

export default function UserChatHistory({ token }: Props) {
  const [items, setItems] = useState<HistoryChatItem[]>([])
  const [selectedChatId, setSelectedChatId] = useState<number | null>(null)
  const [selectedChatDetail, setSelectedChatDetail] = useState<HistoryChatDetail | null>(null)

  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(10)
  const [totalPages, setTotalPages] = useState(1)
  const [totalItems, setTotalItems] = useState(0)

  const [loading, setLoading] = useState(false)
  const [refreshing, setRefreshing] = useState(false)
  const [detailLoading, setDetailLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [detailError, setDetailError] = useState<string | null>(null)

  const [search, setSearch] = useState('')

  const syncSelection = useCallback(
    (nextItems: HistoryChatItem[]) => {
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
        const params = new URLSearchParams({
          page: String(page),
          page_size: String(pageSize),
        })

        const data = await apiRequest<HistoryChatPageResponse>(
          `/history?${params.toString()}`,
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
        setError(err instanceof Error ? err.message : 'Failed to load chat history.')
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

  useEffect(() => {
    if (!token || !selectedChatId) {
      setSelectedChatDetail(null)
      setDetailError(null)
      return
    }

    let cancelled = false

    const fetchDetail = async () => {
      setSelectedChatDetail(null)
      setDetailLoading(true)
      setDetailError(null)

      try {
        const data = await apiRequest<HistoryChatDetail>(`/history/${selectedChatId}`, {
          token,
        })

        if (!cancelled) {
          setSelectedChatDetail(data)
        }
      } catch (err) {
        if (!cancelled) {
          setSelectedChatDetail(null)
          setDetailError(
            err instanceof Error ? err.message : 'Failed to load conversation detail.'
          )
        }
      } finally {
        if (!cancelled) {
          setDetailLoading(false)
        }
      }
    }

    void fetchDetail()

    return () => {
      cancelled = true
    }
  }, [selectedChatId, token])

  const visibleItems = useMemo(() => {
    return items.filter((chat) => matchesSearch(chat, search))
  }, [items, search])

  const selectedChat = useMemo(
    () =>
      visibleItems.find((item) => item.id === selectedChatId) ??
      items.find((item) => item.id === selectedChatId) ??
      null,
    [items, selectedChatId, visibleItems]
  )

  useEffect(() => {
    if (visibleItems.length === 0) return

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

  const canGoPrev = page > 1
  const canGoNext = page < totalPages

  return (
    <section className="history-tab">
      <div className="history-tab__header">
        <div>
          <h2>Your chat history</h2>
          <p>Review your previous conversations with Beat-Bot.</p>
        </div>

        <div className="history-tab__actions">
          <button
            type="button"
            className="history-button history-button--ghost"
            onClick={handleRefresh}
            disabled={loading || refreshing}
          >
            {refreshing ? 'Refreshing...' : 'Refresh'}
          </button>
        </div>
      </div>

      <section className="history-filter-card">
        <div className="history-toolbar">
          <label className="history-field history-field--search">
            <span>Search</span>
            <input
              type="text"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search by title or chat id"
            />
          </label>
        </div>
      </section>

      {loading && <p className="history-feedback">Loading conversations...</p>}
      {error && <p className="history-feedback history-feedback--error">{error}</p>}

      <div className="history-master-detail">
        <aside className="history-sidebar">
          <div className="history-sidebar__head">
            <span>{totalItems} conversations total</span>
          </div>

          <div className="history-sidebar__summary">
            <label className="history-sidebar__page-size">
              <span>Per page</span>
              <select
                value={pageSize}
                onChange={(event) => {
                  setPageSize(Number(event.target.value))
                  setPage(1)
                }}
              >
                <option value={5}>5</option>
                <option value={10}>10</option>
                <option value={20}>20</option>
                <option value={30}>30</option>
              </select>
            </label>

            <div className="history-sidebar__pagination">
              <button
                type="button"
                className="history-page-link"
                disabled={!canGoPrev || loading || refreshing}
                onClick={() => setPage((prev) => Math.max(1, prev - 1))}
                aria-label="Previous page"
              >
                <span aria-hidden="true">‹</span>
              </button>

              <span className="history-sidebar__page-indicator">
                Page {page} of {Math.max(totalPages, 1)}
              </span>

              <button
                type="button"
                className="history-page-link"
                disabled={!canGoNext || loading || refreshing}
                onClick={() => setPage((prev) => prev + 1)}
                aria-label="Next page"
              >
                <span aria-hidden="true">›</span>
              </button>
            </div>
          </div>

          <div className="history-chat-list">
            {!loading &&
              visibleItems.map((chat) => {
                const isActive = chat.id === selectedChatId

                return (
                  <button
                    key={chat.id}
                    type="button"
                    className={`history-chat-card ${isActive ? 'is-active' : ''}`}
                    onClick={() => setSelectedChatId(chat.id)}
                  >
                    <div className="history-chat-card__top">
                      <strong>{chat.title?.trim() || `Chat #${chat.id}`}</strong>

                      <span className="history-msg-count">
                        💬 {chat.message_count}
                      </span>
                    </div>

                    <div className="history-chat-card__meta">
                      <span>ID: #{chat.id}</span>
                      <span>Created: {formatDate(chat.created_at)}</span>
                      <span>Updated: {formatDate(chat.updated_at)}</span>
                    </div>

                    <div className="history-chat-card__footer">
                      <span className="history-pill history-pill--soft">
                        {getRecencyLabel(chat.updated_at)}
                      </span>
                    </div>
                  </button>
                )
              })}

            {!loading && visibleItems.length === 0 && (
              <div className="history-empty">
                {items.length === 0
                  ? 'No conversations found yet.'
                  : 'No conversations match the current search.'}
              </div>
            )}
          </div>
        </aside>

        <section className="history-detail">
          {selectedChat ? (
            <>
              <div className="history-detail__header">
                <div>
                  <h3>{selectedChat.title?.trim() || `Chat #${selectedChat.id}`}</h3>
                  <p>Your private conversation history</p>
                </div>
              </div>

              <div className="history-detail__meta-grid">
                <div className="history-detail__meta-card">
                  <span className="history-detail__label">Created</span>
                  <strong>{formatDate(selectedChat.created_at)}</strong>
                </div>

                <div className="history-detail__meta-card">
                  <span className="history-detail__label">Last updated</span>
                  <strong>{formatDate(selectedChat.updated_at)}</strong>
                </div>

                <div className="history-detail__meta-card">
                  <span className="history-detail__label">Messages</span>
                  <strong>{selectedChat.message_count}</strong>
                </div>
              </div>

              <section className="history-thread-panel">
                <div className="history-thread-panel__header">
                  <div>
                    <h4>Conversation thread</h4>
                    <p>Your saved messages and assistant replies.</p>
                  </div>

                  {detailLoading && (
                    <span className="history-pill history-pill--muted">Loading...</span>
                  )}
                </div>

                {detailError && (
                  <p className="history-feedback history-feedback--error">{detailError}</p>
                )}

                {!detailLoading &&
                  !detailError &&
                  selectedChatDetail?.messages.length === 0 && (
                    <div className="history-empty">
                      No messages have been stored for this conversation yet.
                    </div>
                  )}

                {!detailError &&
                  selectedChatDetail &&
                  selectedChatDetail.messages.length > 0 && (
                    <div className="history-thread-view">
                      {selectedChatDetail.messages.map((message) => {
                        const isUser = message.sender_type === 'user'

                        return (
                          <article
                            key={message.id}
                            className={`history-thread-message ${
                              isUser
                                ? 'history-thread-message--user'
                                : 'history-thread-message--assistant'
                            }`}
                          >
                            <div className="history-thread-message__meta">
                              <strong>{getMessageAuthor(message)}</strong>
                              <span>{formatThreadTimestamp(message.created_at)}</span>
                            </div>

                            <div className="history-thread-message__bubble">
                              {message.content_masked}
                            </div>
                          </article>
                        )
                      })}
                    </div>
                  )}
              </section>
            </>
          ) : (
            <div className="history-empty history-empty--detail">
              Select a conversation to review it.
            </div>
          )}
        </section>
      </div>
    </section>
  )
}