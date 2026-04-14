import LeafScene from '../LeafScene'
import AuthForm from './AuthForm'
import './AuthShell.css'

type Props = {
  email: string
  password: string
  loading?: boolean
  error?: string | null
  onEmailChange: (value: string) => void
  onPasswordChange: (value: string) => void
  onSubmit: () => void
}

export default function AuthShell({
  email,
  password,
  loading = false,
  error = null,
  onEmailChange,
  onPasswordChange,
  onSubmit,
}: Props) {
  return (
    <section className="auth-shell">
      <div className="auth-shell__brand">
        <div className="auth-shell__mark" aria-hidden="true">
          <LeafScene loading={loading} variant="auth" />
        </div>

        <div>
          <p className="auth-shell__eyebrow">Secure Access</p>
          <h1 className="auth-shell__title">Beat-Bot</h1>
          <p className="auth-shell__subtitle">
            Secure internal assistant for policies, rules, and company knowledge.
          </p>
        </div>
      </div>

      <div className="auth-card">
        <div className="auth-card__tabs">
          <button
            className="auth-card__tab auth-card__tab--active"
            type="button"
          >
            Sign in
          </button>
        </div>

        <AuthForm
          email={email}
          password={password}
          loading={loading}
          error={error}
          onEmailChange={onEmailChange}
          onPasswordChange={onPasswordChange}
          onSubmit={onSubmit}
        />
      </div>
    </section>
  )
}