import type { AuthMode } from '../../types/auth'
import LeafScene from '../LeafScene'
import AuthForm from './AuthForm'
import './AuthShell.css'
import ForgotPasswordForm from './ForgotPasswordForm'

type Props = {
  mode: AuthMode
  email: string
  password: string
  confirmPassword: string
  loading?: boolean
  error?: string | null
  success?: string | null
  onModeChange: (mode: AuthMode) => void
  onEmailChange: (value: string) => void
  onPasswordChange: (value: string) => void
  onConfirmPasswordChange: (value: string) => void
  onSubmit: () => void
}

export default function AuthShell({
  mode,
  email,
  password,
  confirmPassword,
  loading = false,
  error = null,
  success = null,
  onModeChange,
  onEmailChange,
  onPasswordChange,
  onConfirmPasswordChange,
  onSubmit,
}: Props) {
  const isLogin = mode === 'login'
  const isRegister = mode === 'register'
  const isForgotPassword = mode === 'forgot-password'

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
            className={`auth-card__tab ${isLogin ? 'auth-card__tab--active' : ''}`}
            type="button"
            onClick={() => onModeChange('login')}
          >
            Sign in
          </button>

          <button
            className={`auth-card__tab ${isRegister ? 'auth-card__tab--active' : ''}`}
            type="button"
            onClick={() => onModeChange('register')}
          >
            Register
          </button>

          <button
            className={`auth-card__tab ${isForgotPassword ? 'auth-card__tab--active' : ''}`}
            type="button"
            onClick={() => onModeChange('forgot-password')}
          >
            Reset
          </button>
        </div>

        {isForgotPassword ? (
          <ForgotPasswordForm
            email={email}
            loading={loading}
            error={error}
            success={success}
            onEmailChange={onEmailChange}
            onSubmit={onSubmit}
          />
        ) : (
          <AuthForm
            mode={isRegister ? 'register' : 'login'}
            email={email}
            password={password}
            confirmPassword={confirmPassword}
            loading={loading}
            error={error}
            onEmailChange={onEmailChange}
            onPasswordChange={onPasswordChange}
            onConfirmPasswordChange={onConfirmPasswordChange}
            onSubmit={onSubmit}
          />
        )}

        {!isForgotPassword && (
          <div className="auth-card__footer">
            <button
              className="auth-link"
              type="button"
              onClick={() => onModeChange('forgot-password')}
            >
              Forgot password?
            </button>
          </div>
        )}
      </div>
    </section>
  )
}