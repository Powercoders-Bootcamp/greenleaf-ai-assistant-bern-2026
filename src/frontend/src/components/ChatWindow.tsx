import { useMemo } from 'react'
import type { Message } from '../types/chat'
import MessageBubble from './MessageBubble'
import './ChatWindow.css'

type Props = {
  messages: Message[]
  loading: boolean
  error: string | null
  onSendPreset: (text: string) => void
}

const SUGGESTIONS = [
  'Is May 1st 2026 a holiday?',
  'What is the holiday policy?',
  'How many vacation days do I have?',
]

export default function ChatWindow({
  messages,
  loading,
  error,
  onSendPreset,
}: Props) {
  const hasOnlyGreeting =
    messages.length === 1 && messages[0]?.role === 'assistant'

  const lastAssistantIndex = useMemo(() => {
    return [...messages]
      .reverse()
      .findIndex((m) => m.role === 'assistant')
  }, [messages])

  return (
    <div className="chat-window">
      {/* EMPTY STATE */}
      {hasOnlyGreeting && !loading && !error && (
        <div className="chat-empty-state">
          <div className="chat-empty-state__icon">✦</div>

          <h3>Start the conversation</h3>
          <p>
            Ask about holidays, internal rules, or company policies.
          </p>

          {/* SMART SUGGESTIONS */}
          <div className="chat-empty-state__chips">
            {SUGGESTIONS.map((text) => (
              <button
                key={text}
                onClick={() => onSendPreset(text)}
                className="chat-chip"
              >
                {text}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* MESSAGES */}
      <div className="chat-thread">
        {messages.map((message, index) => {
          const isLastAssistant =
            message.role === 'assistant' &&
            index === messages.length - 1

          return (
            <MessageBubble
              key={message.id}
              message={message}
              isLatest={isLastAssistant}
            />
          )
        })}
      </div>

      {/* THINKING STATE */}
      {loading && (
        <div className="chat-thinking">
          <div className="chat-thinking__bubble">
            <div className="chat-thinking__dots">
              <span />
              <span />
              <span />
            </div>
            <p>Analyzing internal knowledge...</p>
          </div>
        </div>
      )}

      {/* ERROR */}
      {error && (
        <div className="chat-error">
          <div className="chat-error__icon">⚠</div>
          <div className="chat-error__content">
            <p className="chat-error__title">
              Unable to retrieve answer
            </p>
            <span className="chat-error__message">{error}</span>
          </div>
        </div>
      )}
    </div>
  )
}