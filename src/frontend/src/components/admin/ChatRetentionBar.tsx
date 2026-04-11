import { useMemo, useState } from 'react'
import { apiRequest } from '../../lib/api'
import type { ChatRetentionCleanupResponse } from '../../types/admin'

type Props = {
  token: string | null
  onCleanupSuccess?: (deletedCount: number) => void
}

const MIN_DAYS = 1
const MAX_DAYS = 3650
const DEFAULT_DAYS = 30

function clampDays(value: number) {
  if (Number.isNaN(value)) return DEFAULT_DAYS
  return Math.min(Math.max(value, MIN_DAYS), MAX_DAYS)
}

export default function ChatRetentionBar({
  token,
  onCleanupSuccess,
}: Props) {
  const [days, setDays] = useState(DEFAULT_DAYS)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const isDisabled = useMemo(() => !token || loading, [token, loading])

  const handleDaysChange = (value: string) => {
    const parsed = Number(value)
    setDays(clampDays(parsed))
  }

  const handleCleanup = async () => {
    if (isDisabled) return

    const safeDays = clampDays(days)

    setLoading(true)
    setError(null)
    setMessage(null)

    try {
      const data = await apiRequest<ChatRetentionCleanupResponse>(
        `/admin/chats/expired?older_than_days=${safeDays}`,
        {
          method: 'DELETE',
          token,
        }
      )

      if (data.deleted_count === 0) {
        setMessage(`No expired chats found older than ${safeDays} days.`)
      } else if (data.deleted_count === 1) {
        setMessage(`Deleted 1 expired chat older than ${safeDays} days.`)
      } else {
        setMessage(`Deleted ${data.deleted_count} expired chats older than ${safeDays} days.`)
      }

      onCleanupSuccess?.(data.deleted_count)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Cleanup failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="admin-retention">
      <div className="admin-retention__copy">
        <h3>Chat retention cleanup</h3>
        <p>Delete anonymous chats older than the selected number of days.</p>
      </div>

      <div className="admin-retention__controls">
        <label className="admin-field">
          <span>Older than</span>
          <input
            type="number"
            min={MIN_DAYS}
            max={MAX_DAYS}
            step={1}
            value={days}
            onChange={(event) => handleDaysChange(event.target.value)}
            onBlur={() => setDays((prev) => clampDays(prev))}
            disabled={isDisabled}
          />
        </label>

        <button
          type="button"
          className="admin-button admin-button--danger"
          onClick={handleCleanup}
          disabled={isDisabled}
        >
          {loading ? 'Cleaning up...' : 'Delete expired chats'}
        </button>
      </div>

      {message && (
        <p className="admin-feedback admin-feedback--success">
          {message}
        </p>
      )}

      {error && (
        <p className="admin-feedback admin-feedback--error">
          {error}
        </p>
      )}
    </div>
  )
}