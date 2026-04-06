import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import ChatInput from './components/ChatInput'
import ChatWindow from './components/ChatWindow'
import LeafScene from './components/LeafScene'
import type { Message } from './types/chat'
import './App.css'

const API_URL = 'http://127.0.0.1:8000/chat'

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
  const [messages, setMessages] = useState<Message[]>([
    createMessage(
      'assistant',
      'Hello! Ask me something about GreenLeaf policies, holidays, internal rules, or handbook-related questions.'
    ),
  ])

  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [lastSubmittedQuestion, setLastSubmittedQuestion] = useState<string | null>(null)

  const endRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const statusText = useMemo(() => {
    if (loading) return 'Checking policy context'
    if (error) return 'Connection issue'
    return 'Connected to internal knowledge'
  }, [loading, error])

  const sendMessage = useCallback(
    async (rawText?: string) => {
      const textToSend = (rawText ?? input).trim()

      if (!textToSend || loading) return

      const userMessage = createMessage('user', textToSend)

      setMessages((prev) => [...prev, userMessage])
      setInput('')
      setError(null)
      setLoading(true)
      setLastSubmittedQuestion(textToSend)

      try {
        const response = await fetch(API_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: textToSend }),
        })

        let data: unknown = null

        try {
          data = await response.json()
        } catch {
          data = null
        }

        const safeData =
          typeof data === 'object' && data !== null
            ? (data as { reply?: string; detail?: string })
            : {}

        if (!response.ok) {
          throw new Error(
            safeData.detail || `Request failed with status ${response.status}`
          )
        }

        const assistantReply =
          safeData.reply?.trim() || 'No reply received from server.'

        setMessages((prev) => [...prev, createMessage('assistant', assistantReply)])
      } catch (err) {
        const message =
          err instanceof Error
            ? err.message
            : 'Could not get a response from the backend.'

        console.error(err)
        setError(message)

        setMessages((prev) => [
          ...prev,
          createMessage(
            'assistant',
            `Sorry, I could not reach the backend right now.\n\nReason: ${message}`
          ),
        ])
      } finally {
        setLoading(false)
      }
    },
    [input, loading]
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

  return (
    <main className="app-shell">
      <div className="ambient ambient-1" />
      <div className="ambient ambient-2" />

      <section className="chat-page">
        <header className="chat-header">
  <div className="context-bar">
    <span>Zurich • 16:32</span>
    <span>Internal assistant ready</span>
  </div>

  <div className="brand-mark" aria-hidden="true">
    <LeafScene loading={loading} />
  </div>

  <div>
    <p className="eyebrow">Internal AI Assistant</p>
    <h1>GreenLeaf Assistant</h1>
    <p className="subtext">
      Fast answers for internal policies, holidays, handbook questions,
      and common internal rules.
    </p>
  </div>

  <div
    className={`status-badge ${loading ? 'is-loading' : ''} ${
      error ? 'is-error' : ''
    }`}
    aria-live="polite"
  >
    <span className="status-dot" />
    {statusText}
  </div>
</header>

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
                disabled={messages.length <= 1}
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
            />
            <div ref={endRef} />
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
      </section>
    </main>
  )
}