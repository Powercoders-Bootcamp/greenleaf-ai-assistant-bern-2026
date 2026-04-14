type Props = {
  email: string
  password: string
  loading?: boolean
  error?: string | null
  onEmailChange: (value: string) => void
  onPasswordChange: (value: string) => void
  onSubmit: () => void
}

export default function AuthForm({
  email,
  password,
  loading = false,
  error = null,
  onEmailChange,
  onPasswordChange,
  onSubmit,
}: Props) {
  return (
    <div className="auth-card__body">
      <div className="auth-card__heading">
        <h2>Sign in</h2>
        <p>
          Access internal policies, handbook answers, and protected tools.
          Account creation and password recovery are handled by your administrator.
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

      <button
        className="auth-submit"
        type="button"
        onClick={onSubmit}
        disabled={loading}
      >
        {loading ? 'Please wait...' : 'Sign in'}
      </button>
    </div>
  )
}