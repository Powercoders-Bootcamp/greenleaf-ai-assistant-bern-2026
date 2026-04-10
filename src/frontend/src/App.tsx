import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import './App.css'
import ChatInput from './components/ChatInput'
import ChatWindow from './components/ChatWindow'
import LeafScene from './components/LeafScene'
import AdminPanel from './components/admin/AdminPanel'
import AuthShell from './components/auth/AuthShell'
import {
  clearAuthSession,
  getStoredToken,
  getStoredUser,
  persistAuthSession,
} from './lib/auth'
import type { AuthMode, AuthUser } from './types/auth'
import type { Message } from './types/chat'

const API_BASE_URL = 'http://localhost:8000'
const CHAT_API_URL = `${API_BASE_URL}/chat`
const LOGIN_API_URL = `${API_BASE_URL}/auth/login`

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

export default function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [chatId, setChatId] = useState<number | null>(null)

  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [lastSubmittedQuestion, setLastSubmittedQuestion] = useState<string | null>(null)

  const [authMode, setAuthMode] = useState<AuthMode>('login')
  const [authEmail, setAuthEmail] = useState('')
  const [authPassword, setAuthPassword] = useState('')
  const [authConfirmPassword, setAuthConfirmPassword] = useState('')
  const [authLoading, setAuthLoading] = useState(false)
  const [authError, setAuthError] = useState<string | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [authUser, setAuthUser] = useState<AuthUser | null>(null)
  const [view, setView] = useState<'chat' | 'admin'>('chat')

  const endRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    const storedToken = getStoredToken()
    const storedUser = getStoredUser()

    if (storedToken && storedUser) {
      setToken(storedToken)
      setAuthUser(storedUser)
    }
  }, [])

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [messages, loading])

  const [currentTime, setCurrentTime] = useState(() => formatTime())

  useEffect(() => {
    const interval = window.setInterval(() => {
      setCurrentTime(formatTime())
    }, 1000 * 30)

    return () => window.clearInterval(interval)
  }, [])

  const isAuthenticated = Boolean(token && authUser)
  const isAdmin = authUser?.role?.toLowerCase() === 'admin'

  const statusText = useMemo(() => {
    if (loading) return 'Checking policy context'
    if (error) return 'Connection issue'
    return 'Connected to internal knowledge'
  }, [loading, error])

  const handleAuthSubmit = useCallback(async () => {
    setAuthError(null)

    const email = authEmail.trim()
    const password = authPassword.trim()
    const confirmPassword = authConfirmPassword.trim()

    if (!email) {
      setAuthError('Please enter your email.')
      return
    }

    if (authMode !== 'forgot-password' && !password) {
      setAuthError('Please enter your password.')
      return
    }

    if (authMode === 'register' && password !== confirmPassword) {
      setAuthError('Passwords do not match.')
      return
    }

    setAuthLoading(true)

    try {
      await new Promise((resolve) => setTimeout(resolve, 700))

      if (authMode === 'forgot-password') {
        setAuthError('Password reset flow is not connected to backend yet.')
        return
      }

      if (authMode === 'register') {
        setAuthError('Registration is admin-managed. Please ask an admin to create your account.')
        return
      }

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
          ? (data as { access_token?: string; user?: AuthUser; detail?: string })
          : {}

      if (!response.ok || !safeData.access_token || !safeData.user) {
        throw new Error(
          safeData.detail || `Authentication failed with status ${response.status}`
        )
      }

      persistAuthSession(safeData.access_token, safeData.user)
      setToken(safeData.access_token)
      setAuthUser(safeData.user)
      setView('chat')

      setAuthPassword('')
      setAuthConfirmPassword('')
      setAuthMode('login')
    } catch (err) {
      const message =
        err instanceof Error ? err.message : 'Could not sign in right now.'
      setAuthError(message)
    } finally {
      setAuthLoading(false)
    }
  }, [authMode, authEmail, authPassword, authConfirmPassword])

  const handleLogout = useCallback(() => {
    clearAuthSession()
    setToken(null)
    setAuthUser(null)
    setAuthEmail('')
    setAuthPassword('')
    setAuthConfirmPassword('')
    setAuthMode('login')
    setChatId(null)
    setMessages([])
    setView('chat')
  }, [])

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
          throw new Error(
            safeData.detail || `Request failed with status ${response.status}`
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
    [chatId, input, loading, token]
  )

  const handleSend = useCallback(() => {
    void sendMessage()
  }, [sendMessage])

  const handlePreset = useCallback(
    (text: string) => {
      setInput(text)
      void sendMessage(text)
    },
    [sendMessage]
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

  if (!isAuthenticated) {
    return (
      <main className="app-shell">
        <div className="ambient ambient-1" />
        <div className="ambient ambient-2" />

        <AuthShell
          mode={authMode}
          email={authEmail}
          password={authPassword}
          confirmPassword={authConfirmPassword}
          loading={authLoading}
          error={authError}
          success={null}
          onModeChange={setAuthMode}
          onEmailChange={setAuthEmail}
          onPasswordChange={setAuthPassword}
          onConfirmPasswordChange={setAuthConfirmPassword}
          onSubmit={handleAuthSubmit}
        />
      </main>
    )
  }

  return (
    <main className="app-shell">
      <div className="ambient ambient-1" />
      <div className="ambient ambient-2" />

      <section className="chat-page">
        <header className="chat-header">
          <div className="chat-hero">
            <div className="brand-mark" aria-hidden="true">
              <LeafScene loading={loading} />
            </div>

            <div className="chat-header__copy">
              <p className="eyebrow">
                {view === 'admin' ? 'Admin workspace' : 'Internal AI Assistant'}
              </p>
              <h1>{view === 'admin' ? 'Admin Panel' : 'Beat-Bot'}</h1>
              <p className="subtext">
                {view === 'admin'
                  ? 'Review anonymous chat history, retention settings and managed users.'
                  : 'Fast answers for internal policies, holidays, handbook questions, and common internal rules.'}
              </p>
            </div>
          </div>

          <div className="chat-header__actions">
            <div className="chat-header__actions-row">
              {isAdmin && (
                <>
                  <button
                    type="button"
                    className={`chat-card__action-button ${view === 'chat' ? 'is-active' : ''}`}
                    onClick={() => setView('chat')}
                  >
                    Assistant
                  </button>
                  <button
                    type="button"
                    className={`chat-card__action-button ${view === 'admin' ? 'is-active' : ''}`}
                    onClick={() => setView('admin')}
                  >
                    Admin Panel
                  </button>
                </>
              )}

              <div
                className={`status-badge ${loading && view === 'chat' ? 'is-loading' : ''} ${
                  error && view === 'chat' ? 'is-error' : ''
                }`}
                aria-live="polite"
              >
                <span className="status-dot" />
                {view === 'admin' ? 'Admin access enabled' : statusText}
              </div>

              <button type="button" className="logout-button" onClick={handleLogout}>
                Logout
              </button>
            </div>
          </div>

          <div className="context-bar">
            <span>Basel • {currentTime}</span>
            <span>{isAdmin ? 'Admin access' : 'User access'}</span>
          </div>
        </header>

        {view === 'admin' ? (
          <section className="chat-card">
            <div className="chat-card__body chat-card__body--admin">
              <AdminPanel token={token} />
            </div>
          </section>
        ) : (
          <section className="chat-card">
            <div className="chat-card__top">
              <div className="chat-card__title-wrap">
                <h2>Chat</h2>
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
        )}
      </section>
    </main>
  )
}