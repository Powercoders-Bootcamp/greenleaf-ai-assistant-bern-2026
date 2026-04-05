import type { Message } from '../types/chat'
import './MessageBubble.css'

type Props = {
  message: Message
}

export default function MessageBubble({ message }: Props) {
  const isUser = message.role === 'user'

  return (
    <div className={`message-row ${isUser ? 'message-row--user' : 'message-row--assistant'}`}>
      <div className="message-head">
        {!isUser && <div className="message-avatar">GL</div>}

        <div className="message-head__meta">
          <span className="message-author">{isUser ? 'You' : 'Assistant'}</span>
          <span className="message-time">{message.timestamp}</span>
        </div>
      </div>

      <div className={`message-bubble ${isUser ? 'message-bubble--user' : 'message-bubble--assistant'}`}>
        {message.content}
      </div>
    </div>
  )
}