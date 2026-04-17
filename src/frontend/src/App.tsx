import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import './App.css'
import ChatInput from './components/ChatInput'
import ChatWindow from './components/ChatWindow'
import LeafScene from './components/LeafScene'
import AdminPanel from './components/admin/AdminPanel'
import AuthShell from './components/auth/AuthShell'
import UserChatHistory from './components/history/UserChatHistory'
import { AUTH_EXPIRED_EVENT } from './lib/api'
import {
  clearAuthSession,
  getStoredToken,
  getStoredUser,
  persistAuthSession,
} from './lib/auth'
import type { AuthResponse, AuthUser } from './types/auth'
import type { Message } from './types/chat'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:10000'
const CHAT_API_URL = `${API_BASE_URL}/chat`
const LOGIN_API_URL = `${API_BASE_URL}/auth/login`
const ADMIN_CHAT_MODE_SESSION_KEY = 'greenleaf:admin-chat-mode'

type ViewMode = 'chat' | 'admin' | 'history'
type ChatMode = 'production' | 'debug'

type LogoutModalProps = {
  open: boolean
  onCancel: () => void
  onConfirm: () => void
}

function formatTime(date = new Date()) {
  return date.toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  })
}

function createMessage(role: Message['role'], content: string): Message {
  return {
    id: crypto.randomUUID(),
    role,
    content,
    timestamp: formatTime(),
  }
}

function getHeaderContent(view: ViewMode) {
  if (view === 'admin') {
    return {
      eyebrow: 'Admin workspace',
      title: 'Admin Panel',
      description: 'Manage chats, retention and users.',
      subtextClass: 'app-header__subtext app-header__subtext--compact',
      leafVariant: 'auth' as const,
      brandClass: 'brand-mark--admin',
      pageClass: 'app-header--admin',
    }
  }

  if (view === 'history') {
    return {
      eyebrow: 'Personal workspace',
      title: 'Chat History',
      description: 'Review your previous conversations with the assistant.',
      subtextClass: 'subtext',
      leafVariant: 'default' as const,
      brandClass: 'brand-mark--chat',
      pageClass: 'app-header--chat',
    }
  }

  return {
    eyebrow: 'Internal AI Assistant',
    title: 'Beat-Bot',
    description:
      'Fast answers for internal policies, holidays, handbook questions, and common internal rules.',
    subtextClass: 'subtext',
    leafVariant: 'default' as const,
    brandClass: 'brand-mark--chat',
    pageClass: 'app-header--chat',
  }
}

function LogoutModal({ open, onCancel, onConfirm }: LogoutModalProps) {
  if (!open) return null

  return (
    <div className="logout-modal-backdrop">
      <div
        className="logout-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="logout-modal-title"
        aria-describedby="logout-modal-description"
      >
        <div className="logout-modal__icon" aria-hidden="true">
          ?
        </div>

        <h3 id="logout-modal-title">Log out?</h3>
        <p id="logout-modal-description">
          Are you sure you want to end your current session?
        </p>

        <div className="logout-modal__actions">
          <button
            type="button"
            className="logout-modal__button logout-modal__button--secondary"
            onClick={onCancel}
          >
            Cancel
          </button>

          <button
            type="button"
            className="logout-modal__button logout-modal__button--danger"
            onClick={onConfirm}
          >
            Yes, log out
          </button>
        </div>
      </div>
    </div>
  )
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [chatId, setChatId] = useState<number | null>(null)

  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [lastSubmittedQuestion, setLastSubmittedQuestion] = useState<string | null>(null)

  const [authEmail, setAuthEmail] = useState('')
  const [authPassword, setAuthPassword] = useState('')
  const [authLoading, setAuthLoading] = useState(false)
  const [authError, setAuthError] = useState<string | null>(null)

  const [token, setToken] = useState<string | null>(null)
  const [authUser, setAuthUser] = useState<AuthUser | null>(null)
  const [view, setView] = useState<ViewMode>('chat')
  const [showLogoutModal, setShowLogoutModal] = useState(false)
  const [chatMode, setChatMode] = useState<ChatMode>('production')

  const endRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    const storedToken = getStoredToken()
    const storedUser = getStoredUser()
    const storedChatMode = sessionStorage.getItem(ADMIN_CHAT_MODE_SESSION_KEY)

    if (storedToken && storedUser) {
      setToken(storedToken)
      setAuthUser(storedUser)
    }

    if (storedChatMode === 'debug' || storedChatMode === 'production') {
      setChatMode(storedChatMode)
    }
  }, [])

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [messages, loading])

  const isAuthenticated = Boolean(token && authUser)
  const isAdmin = authUser?.role?.toLowerCase() === 'admin'

  useEffect(() => {
    if (!isAdmin && chatMode !== 'production') {
      sessionStorage.setItem(ADMIN_CHAT_MODE_SESSION_KEY, 'production')
      setChatMode('production')
    }
  }, [chatMode, isAdmin])

  const headerContent = useMemo(() => getHeaderContent(view), [view])

  const handleAuthSubmit = useCallback(async () => {
    setAuthError(null)

    const email = authEmail.trim()
    const password = authPassword.trim()

    if (!email) {
      setAuthError('Please enter your email.')
      return
    }

    if (!password) {
      setAuthError('Please enter your password.')
      return
    }

    setAuthLoading(true)

    try {
      await new Promise((resolve) => globalThis.setTimeout(resolve, 700))

      const response = await fetch(LOGIN_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      })

      let data: unknown = null

      try {
        data = await response.json()
      } catch {
        data = null
      }

      const safeData =
        typeof data === 'object' && data !== null
          ? (data as Partial<AuthResponse> & { detail?: string })
          : {}

      if (!response.ok || !safeData.access_token || !safeData.user) {
        throw new Error(
          safeData.detail || `Authentication failed with status ${response.status}`,
        )
      }

      persistAuthSession({
        access_token: safeData.access_token,
        token_type: safeData.token_type ?? 'bearer',
        user: safeData.user,
      })

      setToken(safeData.access_token)
      setAuthUser(safeData.user)
      setView('chat')
      setAuthPassword('')
    } catch (err) {
      const message =
        err instanceof Error ? err.message : 'Could not sign in right now.'
      setAuthError(message)
    } finally {
      setAuthLoading(false)
    }
  }, [authEmail, authPassword])

  const handleLogout = useCallback(() => {
    clearAuthSession()
    sessionStorage.removeItem(ADMIN_CHAT_MODE_SESSION_KEY)
    setToken(null)
    setAuthUser(null)
    setAuthEmail('')
    setAuthPassword('')
    setChatId(null)
    setMessages([])
    setView('chat')
    setShowLogoutModal(false)
    setChatMode('production')
  }, [])

  const handleToggleChatMode = useCallback(() => {
    if (!isAdmin) return

    setChatMode((currentMode) => {
      const nextMode: ChatMode = currentMode === 'debug' ? 'production' : 'debug'
      sessionStorage.setItem(ADMIN_CHAT_MODE_SESSION_KEY, nextMode)
      return nextMode
    })
  }, [isAdmin])

  useEffect(() => {
    const handleAuthExpired = () => {
      handleLogout()
      setAuthError('Your session expired. Please sign in again.')
    }

    globalThis.addEventListener(AUTH_EXPIRED_EVENT, handleAuthExpired)

    return () => {
      globalThis.removeEventListener(AUTH_EXPIRED_EVENT, handleAuthExpired)
    }
  }, [handleLogout])

  const sendMessage = useCallback(
    async (rawText?: string) => {
      const textToSend = (rawText ?? input).trim()

      if (!textToSend || loading || !token) return

      const userMessage = createMessage('user', textToSend)

      setMessages((prev) => [...prev, userMessage])
      setInput('')
      setError(null)
      setLoading(true)
      setLastSubmittedQuestion(textToSend)

      try {
        const response = await fetch(CHAT_API_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            message: textToSend,
            ...(chatId ? { chat_id: chatId } : {}),
            ...(isAdmin ? { mode: chatMode } : {}),
          }),
        })

        let data: unknown = null

        try {
          data = await response.json()
        } catch {
          data = null
        }

        const safeData =
          typeof data === 'object' && data !== null
            ? (data as { chat_id?: number; reply?: string; detail?: string })
            : {}

        if (response.status === 401) {
          clearAuthSession()
          setToken(null)
          setAuthUser(null)
          setView('chat')
          throw new Error('Your session expired. Please sign in again.')
        }

        if (!response.ok) {
          if (response.status === 409) {
            setChatId(null)
          }

          if (response.status === 403) {
            sessionStorage.setItem(ADMIN_CHAT_MODE_SESSION_KEY, 'production')
            setChatMode('production')
          }

          throw new Error(
            safeData.detail || `Request failed with status ${response.status}`,
          )
        }

        const assistantReply =
          safeData.reply?.trim() || 'No reply received from server.'

        if (typeof safeData.chat_id === 'number') {
          setChatId(safeData.chat_id)
        }

        setMessages((prev) => [...prev, createMessage('assistant', assistantReply)])
      } catch (err) {
        const message =
          err instanceof Error
            ? err.message
            : 'Could not get a response from the backend.'

        console.error(err)
        setError(message)
      } finally {
        setLoading(false)
      }
    },
    [chatId, chatMode, input, isAdmin, loading, token],
  )

  const handleSend = useCallback(() => {
    void sendMessage()
  }, [sendMessage])

  const handlePreset = useCallback(
    (text: string) => {
      setInput(text)
      void sendMessage(text)
    },
    [sendMessage],
  )

  const handleRetry = useCallback(() => {
    if (!lastSubmittedQuestion || loading) return
    void sendMessage(lastSubmittedQuestion)
  }, [lastSubmittedQuestion, loading, sendMessage])

  const handleCopyLastAnswer = useCallback(async () => {
    const lastAssistantMessage = [...messages]
      .reverse()
      .find((message) => message.role === 'assistant')

    if (!lastAssistantMessage?.content) return

    try {
      await navigator.clipboard.writeText(lastAssistantMessage.content)
    } catch (err) {
      console.error('Clipboard copy failed:', err)
    }
  }, [messages])

  const renderWorkspaceSwitch = () => {
    if (isAdmin) {
      return (
        <div className="view-switch" role="tablist" aria-label="Workspace view">
          <button
            type="button"
            role="tab"
            aria-selected={view === 'chat'}
            className={`view-switch__button ${view === 'chat' ? 'is-active' : ''}`}
            onClick={() => setView('chat')}
          >
            Assistant
          </button>

          <button
            type="button"
            role="tab"
            aria-selected={view === 'admin'}
            className={`view-switch__button ${view === 'admin' ? 'is-active' : ''}`}
            onClick={() => setView('admin')}
          >
            Admin Panel
          </button>
        </div>
      )
    }

    return (
      <div className="view-switch" role="tablist" aria-label="Workspace view">
        <button
          type="button"
          role="tab"
          aria-selected={view === 'chat'}
          className={`view-switch__button ${view === 'chat' ? 'is-active' : ''}`}
          onClick={() => setView('chat')}
        >
          Chat
        </button>

        <button
          type="button"
          role="tab"
          aria-selected={view === 'history'}
          className={`view-switch__button ${view === 'history' ? 'is-active' : ''}`}
          onClick={() => setView('history')}
        >
          Chat History
        </button>
      </div>
    )
  }

  const renderMainContent = () => {
    if (view === 'admin') {
      return (
        <section className="admin-card">
          <div className="admin-card__body">
            <AdminPanel
              token={token}
              chatMode={chatMode}
              onToggleChatMode={handleToggleChatMode}
            />
          </div>
        </section>
      )
    }

    if (view === 'history') {
      return (
        <section className="admin-card">
          <div className="admin-card__body">
            <UserChatHistory token={token} />
          </div>
        </section>
      )
    }

    return (
      <section className="chat-card">
        <div className="chat-card__top">
          <div className="chat-card__title-wrap">
            <div className="chat-card__heading-row">
              <h2>Chat</h2>
              <span className="chat-card__mode-badge">
                {isAdmin ? `Admin access · ${chatMode}` : 'User access'}
              </span>
            </div>

            <p>Ask a question and review the response in one clean thread.</p>
          </div>

          <div className="chat-card__actions">
            <button
              type="button"
              className="chat-card__action-button"
              onClick={handleRetry}
              disabled={!lastSubmittedQuestion || loading}
            >
              Retry last
            </button>

            <button
              type="button"
              className="chat-card__action-button"
              onClick={handleCopyLastAnswer}
              disabled={!messages.some((message) => message.role === 'assistant')}
            >
              Copy answer
            </button>
          </div>
        </div>

        <div className="chat-card__body">
          <ChatWindow
            messages={messages}
            loading={loading}
            error={error}
            onSendPreset={handlePreset}
            bottomRef={endRef}
          />
        </div>

        <div className="chat-card__footer">
          <ChatInput
            input={input}
            loading={loading}
            onChange={setInput}
            onSend={handleSend}
          />
        </div>
      </section>
    )
  }

  if (!isAuthenticated) {
    return (
      <main className="app-shell">
        <div className="ambient ambient-1" />
        <div className="ambient ambient-2" />

        <AuthShell
          email={authEmail}
          password={authPassword}
          loading={authLoading}
          error={authError}
          onEmailChange={setAuthEmail}
          onPasswordChange={setAuthPassword}
          onSubmit={handleAuthSubmit}
        />
      </main>
    )
  }

  return (
    <main className="app-shell">
      <div className="ambient ambient-1" />
      <div className="ambient ambient-2" />

      <section className={`chat-page ${view === 'admin' ? 'chat-page--admin' : ''}`}>
        <header className={`app-header ${headerContent.pageClass}`}>
          <div className="app-header__main">
            <div className="app-header__hero">
              <div className={`brand-mark ${headerContent.brandClass}`} aria-hidden="true">
                <LeafScene loading={loading} variant={headerContent.leafVariant} />
              </div>

              <div className="app-header__copy">
                <p className="eyebrow">{headerContent.eyebrow}</p>
                <h1>{headerContent.title}</h1>
                <p className={headerContent.subtextClass}>{headerContent.description}</p>
              </div>
            </div>

            <div className="app-header__controls">
              {renderWorkspaceSwitch()}

              <button
                type="button"
                className="logout-button logout-button--header"
                onClick={() => setShowLogoutModal(true)}
              >
                Logout
              </button>
            </div>
          </div>
        </header>

        {renderMainContent()}
      </section>

      <LogoutModal
        open={showLogoutModal}
        onCancel={() => setShowLogoutModal(false)}
        onConfirm={handleLogout}
      />
    </main>
  )
}
