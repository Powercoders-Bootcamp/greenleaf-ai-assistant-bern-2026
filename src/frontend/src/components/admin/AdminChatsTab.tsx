import { useCallback, useEffect, useMemo, useState } from 'react'
import { apiRequest } from '../../lib/api'
import type {
  AdminChatDetail,
  AdminChatItem,
  AdminChatMessage,
  AdminChatPageResponse,
} from '../../types/admin'

type Props = {
  token: string | null
}

type SortOption =
  | 'updated_desc'
  | 'updated_asc'
  | 'created_desc'
  | 'created_asc'
  | 'messages_desc'

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

function getMessageAuthor(message: AdminChatMessage) {
  if (message.sender_type === 'user') return 'Employee'
  if (message.sender_type === 'assistant') return 'Beat-Bot'
  return 'System'
}

export default function AdminChatsTab({ token }: Props) {
  const [items, setItems] = useState<AdminChatItem[]>([])
  const [selectedChatDetail, setSelectedChatDetail] = useState<AdminChatDetail | null>(null)
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(10)
  const [totalPages, setTotalPages] = useState(1)
  const [totalItems, setTotalItems] = useState(0)
  const [selectedChatId, setSelectedChatId] = useState<number | null>(null)

  const [loading, setLoading] = useState(false)
  const [refreshing, setRefreshing] = useState(false)
  const [detailLoading, setDetailLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [detailError, setDetailError] = useState<string | null>(null)

  const [search, setSearch] = useState('')
  const [sortBy, setSortBy] = useState<SortOption>('updated_desc')
  const [dateFrom, setDateFrom] = useState('')
  const [dateTo, setDateTo] = useState('')
  const [mobileFiltersOpen, setMobileFiltersOpen] = useState(false)
  const [mobileDateFiltersOpen, setMobileDateFiltersOpen] = useState(false)

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
        const params = new URLSearchParams({
          page: String(page),
          page_size: String(pageSize),
        })

        if (dateFrom) {
          params.set('date_from', `${dateFrom}T00:00:00`)
        }

        if (dateTo) {
          params.set('date_to', `${dateTo}T23:59:59`)
        }

        const data = await apiRequest<AdminChatPageResponse>(
          `/admin/chats?${params.toString()}`,
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
    [dateFrom, dateTo, page, pageSize, syncSelection, token]
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
        const data = await apiRequest<AdminChatDetail>(`/admin/chats/${selectedChatId}`, {
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
    const filtered = items.filter((chat) => matchesSearch(chat, search))
    return sortChats(filtered, sortBy)
  }, [items, search, sortBy])

  const selectedChat = useMemo(
    () =>
      visibleItems.find((item) => item.id === selectedChatId) ??
      items.find((item) => item.id === selectedChatId) ??
      null,
    [items, selectedChatId, visibleItems]
  )

  const hasSelectedThread = Boolean(
    selectedChatDetail && selectedChatDetail.messages.length > 0
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

      if (selectedChatId === chatId) {
        setSelectedChatDetail(null)
      }

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
  const hasFilters =
    Boolean(search.trim()) ||
    sortBy !== 'updated_desc' ||
    Boolean(dateFrom) ||
    Boolean(dateTo)

  return (
    <section className="admin-tab admin-chats-tab">
      <div className="admin-tab__header">
        <div>
          <h2>Anonymous chats</h2>
          <p>Review chat metadata, timestamps, and conversation volume.</p>
        </div>
      </div>

      <section className="admin-filter-card">
        <div className="admin-filter-card__mobile-toggle">
          <button
            type="button"
            className="admin-button admin-button--ghost admin-button--compact"
            aria-expanded={mobileFiltersOpen}
            onClick={() => setMobileFiltersOpen((prev) => !prev)}
          >
            <span>Search and filters</span>
            <span aria-hidden="true">{mobileFiltersOpen ? '−' : '+'}</span>
          </button>
        </div>

        <div className={`admin-filter-card__body ${mobileFiltersOpen ? 'is-open' : ''}`}>
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

            <div className="admin-toolbar__mobile-toggle">
              <button
                type="button"
                className="admin-button admin-button--ghost admin-button--compact"
                aria-expanded={mobileDateFiltersOpen}
                onClick={() => setMobileDateFiltersOpen((prev) => !prev)}
              >
                <span>Date filters</span>
                <span aria-hidden="true">{mobileDateFiltersOpen ? '−' : '+'}</span>
              </button>
            </div>

            <div
              className={`admin-toolbar__date-filters ${
                mobileDateFiltersOpen ? 'is-open' : ''
              }`}
            >
              <label className="admin-field admin-field--compact">
                <span>Updated from</span>
                <input
                  type="date"
                  value={dateFrom}
                  onChange={(event) => {
                    setDateFrom(event.target.value)
                    setPage(1)
                  }}
                />
              </label>

              <label className="admin-field admin-field--compact">
                <span>Updated to</span>
                <input
                  type="date"
                  value={dateTo}
                  onChange={(event) => {
                    setDateTo(event.target.value)
                    setPage(1)
                  }}
                />
              </label>
            </div>

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
                  setDateFrom('')
                  setDateTo('')
                  setPage(1)
                }}
              >
                Reset filters
              </button>
            )}
          </div>
        </div>
      </section>

      {loading && <p className="admin-feedback">Loading conversations...</p>}
      {error && <p className="admin-feedback admin-feedback--error">{error}</p>}

      <div className="admin-master-detail">
        <aside className="admin-sidebar">
          <div className="admin-sidebar__head">
            <span>{totalItems} conversations total</span>
          </div>

          <div className="admin-sidebar__summary">
            <label className="admin-sidebar__page-size">
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
                <option value={50}>50</option>
              </select>
            </label>

            <div className="admin-sidebar__pagination">
              <button
                type="button"
                className="admin-page-link"
                disabled={!canGoPrev || loading || refreshing}
                onClick={() => setPage((prev) => Math.max(1, prev - 1))}
                aria-label="Previous page"
              >
                <span aria-hidden="true">‹</span>
              </button>

              <span className="admin-sidebar__page-indicator">
                Page {page} of {Math.max(totalPages, 1)}
              </span>

              <button
                type="button"
                className="admin-page-link"
                disabled={!canGoNext || loading || refreshing}
                onClick={() => setPage((prev) => prev + 1)}
                aria-label="Next page"
              >
                <span aria-hidden="true">›</span>
              </button>
            </div>
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

                      <span
                        className="admin-msg-count"
                        aria-label={`${chat.message_count} messages`}
                      >
                        <span aria-hidden="true">💬</span>
                        {chat.message_count}
                      </span>
                    </div>

                    <div className="admin-chat-card__meta">
                      <span>ID: #{chat.id}</span>
                      <span>Created: {formatDate(chat.created_at)}</span>
                      <span>Updated: {formatDate(chat.updated_at)}</span>
                    </div>

                    <div className="admin-chat-card__footer">
                      <span className="admin-chat-card__recency">
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

              {!hasSelectedThread && (
                <div className="admin-inspector-grid">
                  <div className="admin-detail__placeholder">
                    <h4>Conversation overview</h4>
                    <p>
                      This panel now shows the masked thread stored for the selected
                      anonymous chat. Message bodies are still privacy-safe and are shown
                      without exposing direct user identifiers.
                    </p>
                  </div>

                  <div className="admin-detail__placeholder">
                    <h4>Privacy scope</h4>
                    <p>
                      Anonymous chat review is intentionally limited. The current admin API
                      exposes retention-safe metadata only and does not return direct user
                      identifiers.
                    </p>
                  </div>
                </div>
              )}

              <section className="admin-thread-panel">
                <div className="admin-thread-panel__header">
                  <div>
                    <h4>Conversation thread</h4>
                    <p>Masked message history for admin review.</p>
                  </div>

                  {detailLoading && (
                    <span className="admin-thread-panel__loading">Loading...</span>
                  )}
                </div>

                {detailError && (
                  <p className="admin-feedback admin-feedback--error">{detailError}</p>
                )}

                {!detailLoading &&
                  !detailError &&
                  selectedChatDetail?.messages.length === 0 && (
                    <div className="admin-empty">
                      No messages have been stored for this conversation yet.
                    </div>
                  )}

                {!detailError &&
                  selectedChatDetail &&
                  selectedChatDetail.messages.length > 0 && (
                    <div className="admin-thread-view">
                      {selectedChatDetail.messages.map((message) => {
                        const isUser = message.sender_type === 'user'

                        return (
                          <article
                            key={message.id}
                            className={`admin-thread-message ${
                              isUser
                                ? 'admin-thread-message--user'
                                : 'admin-thread-message--assistant'
                            }`}
                          >
                            <div className="admin-thread-message__meta">
                              <strong>{getMessageAuthor(message)}</strong>
                              <span>{formatThreadTimestamp(message.created_at)}</span>
                            </div>

                            <div className="admin-thread-message__bubble">
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
            <div className="admin-empty admin-empty--detail">
              Select a conversation to review its metadata.
            </div>
          )}
        </section>
      </div>
    </section>
  )
}