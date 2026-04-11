type Props = {
  email: string
  loading?: boolean
  error?: string | null
  success?: string | null
  onEmailChange: (value: string) => void
  onSubmit: () => void
}

export default function ForgotPasswordForm({
  email,
  loading = false,
  error = null,
  success = null,
  onEmailChange,
  onSubmit,
}: Props) {
  return (
    <div className="auth-card__body">
      <div className="auth-card__heading">
        <h2>Reset password</h2>
        <p>Enter your email and we will send password reset instructions.</p>
      </div>

      {error && <div className="auth-error">{error}</div>}
      {success && <div className="auth-success">{success}</div>}

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

      <button
        className="auth-submit"
        type="button"
        onClick={onSubmit}
        disabled={loading}
      >
        {loading ? 'Please wait...' : 'Send reset link'}
      </button>
    </div>
  )
}