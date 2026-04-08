import type { RefObject } from 'react'
import type { Message } from '../types/chat'
import './ChatWindow.css'
import MessageBubble from './MessageBubble'

type Props = {
  messages: Message[]
  loading: boolean
  error: string | null
  onSendPreset: (text: string) => void
  bottomRef?: RefObject<HTMLDivElement | null>
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
  bottomRef,
}: Props) {
  const hasStartedConversation = messages.length > 0

  return (
    <div className="chat-window">
      {!hasStartedConversation && !loading && !error && (
        <div className="chat-empty-state">
          <div className="chat-empty-state__icon">✦</div>

          <h3>Start the conversation</h3>
          <p>Ask about holidays, internal rules, or company policies.</p>

          <div className="chat-empty-state__chips">
            {SUGGESTIONS.map((text) => (
              <button
                key={text}
                type="button"
                onClick={() => onSendPreset(text)}
                className="chat-chip"
              >
                {text}
              </button>
            ))}
          </div>
        </div>
      )}

      {hasStartedConversation && (
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
    )}

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

      {error && (
        <div className="chat-error">
          <div className="chat-error__icon">⚠</div>
          <div className="chat-error__content">
            <p className="chat-error__title">Unable to retrieve answer</p>
            <span className="chat-error__message">{error}</span>
          </div>
        </div>
      )}

      <div ref={bottomRef} aria-hidden="true" />
    </div>
  )
}