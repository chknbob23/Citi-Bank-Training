import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function Login({ onLogin, loading, error }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (event) => {
    event.preventDefault()
    const success = await onLogin({ email, password })
    if (success) {
      navigate('/dashboard')
    }
  }

  return (
    <section className="page login">
      <div className="container card">
        <h2>Sign in to Phony Bank</h2>
        <p className="subtext">Sign in as admin or as a customer to view account information from your MongoDB-backed API.</p>

        <form onSubmit={handleSubmit} className="login-form">
          <label>
            Email or username
            <input
              type="text"
              name="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
            />
          </label>

          <label>
            Password
            <input
              type="password"
              name="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />
          </label>

          <button type="submit" disabled={loading}>
            {loading ? 'Loading accounts...' : 'Sign in'}
          </button>

          {error && <p className="form-error">{error}</p>}
        </form>
      </div>
    </section>
  )
}
