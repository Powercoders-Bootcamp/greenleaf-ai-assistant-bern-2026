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
  return (
    <div className="chat-input">
      <div className="chat-input__field-wrap">
        <input
          value={input}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              onSend()
            }
          }}
          placeholder="Ask about holidays, leave, policy, or internal process..."
          disabled={loading}
          className="chat-input__field"
        />
      </div>

      <button
        onClick={onSend}
        disabled={loading || !input.trim()}
        className="chat-input__button"
        aria-label="Send message"
        title="Send message"
      >
        {loading ? (
          <span className="chat-input__button-text">Sending...</span>
        ) : (
          <>
            <span className="chat-input__button-icon">➜</span>
            <span className="chat-input__button-text">Send</span>
          </>
        )}
      </button>
    </div>
  )
}