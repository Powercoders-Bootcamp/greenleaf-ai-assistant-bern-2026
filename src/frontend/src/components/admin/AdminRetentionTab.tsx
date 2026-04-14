import './AdminPanel.css'
import ChatRetentionBar from './ChatRetentionBar'

type Props = {
  token: string | null
}

export default function AdminRetentionTab({ token }: Props) {
  return (
    <section className="admin-tab admin-retention-tab">
      <div className="admin-tab__header">
        <div>
          <h2>Retention</h2>
          <p>
            Manage cleanup rules for expired anonymous chats and control data lifecycle.
          </p>
        </div>
      </div>

      <div className="admin-retention-tab__content">
        <ChatRetentionBar token={token} />
      </div>
    </section>
  )
}