type Props = {
  mode: 'login' | 'register'
  email: string
  password: string
  confirmPassword?: string
  loading?: boolean
  error?: string | null
  onEmailChange: (value: string) => void
  onPasswordChange: (value: string) => void
  onConfirmPasswordChange?: (value: string) => void
  onSubmit: () => void
}

export default function AuthForm({
  mode,
  email,
  password,
  confirmPassword = '',
  loading = false,
  error = null,
  onEmailChange,
  onPasswordChange,
  onConfirmPasswordChange,
  onSubmit,
}: Props) {
  const isRegister = mode === 'register'

  return (
    <div className="auth-card__body">
      <div className="auth-card__heading">
        <h2>{isRegister ? 'Create account' : 'Sign in'}</h2>
        <p>
          {isRegister
            ? 'Create your account to access the internal assistant.'
            : 'Access internal policies, handbook answers, and protected tools.'}
        </p>
      </div>

      {error && <div className="auth-error">{error}</div>}

      <label className="auth-field">
        <span>Email</span>
        <input
          type="email"
          placeholder="you@greenleaf.ch"
          value={email}
          onChange={(e) => onEmailChange(e.target.value)}
          disabled={loading}
        />
      </label>

      <label className="auth-field">
        <span>Password</span>
        <input
          type="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => onPasswordChange(e.target.value)}
          disabled={loading}
        />
      </label>

      {isRegister && onConfirmPasswordChange && (
        <label className="auth-field">
          <span>Confirm password</span>
          <input
            type="password"
            placeholder="Repeat your password"
            value={confirmPassword}
            onChange={(e) => onConfirmPasswordChange(e.target.value)}
            disabled={loading}
          />
        </label>
      )}

      <button
        className="auth-submit"
        type="button"
        onClick={onSubmit}
        disabled={loading}
      >
        {loading ? 'Please wait...' : isRegister ? 'Create account' : 'Sign in'}
      </button>
    </div>
  )
}