import { useEffect, useRef } from 'react'
import './ChatWindow.css'

type Props = {
  input: string
  loading: boolean
  onChange: (value: string) => void
  onSend: () => void
}

export default function ChatInput({
  input,
  loading,
  onChange,
  onSend,
}: Props) {
  const textareaRef = useRef<HTMLTextAreaElement | null>(null)

  useEffect(() => {
    const el = textareaRef.current
    if (!el) return

    el.style.height = '0px'
    const nextHeight = Math.min(el.scrollHeight, 160)
    el.style.height = `${nextHeight}px`
  }, [input])

  return (
    <div className="chat-input">
      <div className="chat-input__field-wrap">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault()
              onSend()
            }
          }}
          placeholder="Ask about holidays, leave, policy, or internal process..."
          disabled={loading}
          className="chat-input__field"
          rows={1}
        />

        <div className="chat-input__helper">
          <span>Enter to send</span>
          <span>Shift + Enter for new line</span>
        </div>
      </div>

      <button
        onClick={onSend}
        disabled={loading || !input.trim()}
        className="chat-input__button"
        aria-label="Send message"
        title="Send message"
        type="button"
      >
        {loading ? (
          <span className="chat-input__button-text">Sending</span>
        ) : (
          <>
            <span className="chat-input__button-icon">↑</span>
            <span className="chat-input__button-text">Send</span>
          </>
        )}
      </button>
    </div>
  )
}