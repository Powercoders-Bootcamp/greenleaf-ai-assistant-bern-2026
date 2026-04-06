import { useState } from 'react'
import type { Message } from '../types/chat'
import './MessageBubble.css'

type Props = {
  message: Message
  isLatest?: boolean
}

export default function MessageBubble({ message, isLatest = false }: Props) {
  const isUser = message.role === 'user'
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    if (isUser) return

    try {
      await navigator.clipboard.writeText(message.content)
      setCopied(true)

      window.setTimeout(() => {
        setCopied(false)
      }, 1200)
    } catch (error) {
      console.error('Copy failed:', error)
    }
  }

  const lines = message.content.split('\n').filter(Boolean)

  return (
    <div className={`message-row ${isUser ? 'message-row--user' : 'message-row--assistant'}`}>
      <div className="message-head">
        {!isUser && (
          <div className="message-avatar" aria-hidden="true">
            GL
          </div>
        )}

        <div className="message-head__meta">
          <span className="message-author">{isUser ? 'You' : 'GreenLeaf AI'}</span>
          <span className="message-time">{message.timestamp}</span>
          {!isUser && isLatest && <span className="message-badge">Latest answer</span>}
        </div>

        {!isUser && (
          <button
            type="button"
            className="message-copy"
            onClick={handleCopy}
            aria-label="Copy answer"
            title="Copy answer"
          >
            {copied ? 'Copied' : 'Copy'}
          </button>
        )}
      </div>

      <div className={`message-bubble ${isUser ? 'message-bubble--user' : 'message-bubble--assistant'}`}>
        {lines.length > 0 ? (
          lines.map((line, index) => (
            <p key={`${message.id}-${index}`} className="message-line">
              {line}
            </p>
          ))
        ) : (
          <p className="message-line">{message.content}</p>
        )}
      </div>
    </div>
  )
}