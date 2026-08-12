import React from 'react'

export default function Register() {
  return (
    <section className="page register">
      <div className="container card">
        <h2>Create your Phony Bank account</h2>
        <p className="subtext">This demo uses fake information and does not create a real account.</p>

        <form className="login-form">
          <label>
            Name
            <input name="name" />
          </label>
          <label>
            Email
            <input type="email" name="email" />
          </label>
          <label>
            Password
            <input type="password" name="password" />
          </label>
          <button type="submit">Create account</button>
        </form>
      </div>
    </section>
  )
}
