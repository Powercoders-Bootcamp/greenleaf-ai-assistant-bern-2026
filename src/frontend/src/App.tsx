import { useEffect, useMemo, useRef, useState } from 'react'
import ChatInput from './components/ChatInput'
import ChatWindow from './components/ChatWindow'
import type { Message } from './types/chat'
import './App.css'

function formatTime(date = new Date()) {
  return date.toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  })
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: crypto.randomUUID(),
      role: 'assistant',
      content:
        'Hello! Ask me something about GreenLeaf policies, holidays, or internal rules.',
      timestamp: formatTime(),
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const endRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const statusText = useMemo(() => {
    if (loading) return 'Thinking...'
    if (error) return 'Backend issue'
    return 'Ready'
  }, [loading, error])

  const handleSend = async () => {
    if (!input.trim() || loading) return

    const userText = input.trim()

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: userText,
      timestamp: formatTime(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setError(null)
    setLoading(true)

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userText }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data?.detail || `Request failed with status ${response.status}`)
      }

      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: data.reply || 'No reply received from server.',
        timestamp: formatTime(),
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : 'Could not get a response from the backend.'

      console.error(error)
      setError(message)

      const assistantErrorMessage: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: `Sorry, backend error: ${message}`,
        timestamp: formatTime(),
      }

      setMessages((prev) => [...prev, assistantErrorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="app-shell">
      <div className="ambient ambient-1" />
      <div className="ambient ambient-2" />

      <section className="chat-page">
        <header className="chat-header">
          <div>
            <p className="eyebrow">Internal AI Assistant</p>
            <h1>GreenLeaf Assistant</h1>
            <p className="subtext">
              Fast answers for internal policies, holidays, and handbook questions.
            </p>
          </div>

          <div className={`status-badge ${loading ? 'is-loading' : ''} ${error ? 'is-error' : ''}`}>
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
          </div>

          <div className="chat-card__body">
            <ChatWindow messages={messages} loading={loading} error={error} />
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