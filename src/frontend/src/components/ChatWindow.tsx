import type { Message } from '../types/chat'
import MessageBubble from './MessageBubble'
import './ChatWindow.css'

type Props = {
  messages: Message[]
  loading: boolean
  error: string | null
}

export default function ChatWindow({ messages, loading, error }: Props) {
  const hasOnlyGreeting =
    messages.length === 1 && messages[0]?.role === 'assistant'

  return (
    <div className="chat-window">
      {hasOnlyGreeting && !loading && !error && (
        <div className="chat-empty-state">
          <div className="chat-empty-state__icon">✦</div>
          <h3>Start the conversation</h3>
          <p>
            Try asking about holidays, leave requests, company policy, or internal rules.
          </p>

          <div className="chat-empty-state__chips">
            <span>Is May 1st 2026 a holiday?</span>
            <span>What is the holiday policy?</span>
            <span>How many vacation days do I have?</span>
          </div>
        </div>
      )}

      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}

      {loading && (
        <div className="chat-window__typing">
          <span />
          <span />
          <span />
          <p>Assistant is thinking...</p>
        </div>
      )}

      {error && <div className="chat-window__error">{error}</div>}
    </div>
  )
}