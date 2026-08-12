import React from 'react'
import { NavLink } from 'react-router-dom'
import './Header.css'

export default function Header({ user, onLogout }) {
  return (
    <header className="site-header">
      <div className="container">
        <div className="brand-group">
          <h1 className="brand">Phony Bank</h1>
          <p className="tagline">Banking made playful with fake data.</p>
        </div>

        <nav className="menu">
          <NavLink to="/" end className={({ isActive }) => (isActive ? 'active' : '')}>
            Home
          </NavLink>
          <NavLink to="/about" className={({ isActive }) => (isActive ? 'active' : '')}>
            About
          </NavLink>
          <NavLink to="/contact" className={({ isActive }) => (isActive ? 'active' : '')}>
            Contact
          </NavLink>
          {user ? (
            <>
              <NavLink to="/dashboard" className={({ isActive }) => (isActive ? 'active' : '')}>
                Dashboard
              </NavLink>
              {user.role === 'admin' && (
                <NavLink to="/admin" className={({ isActive }) => (isActive ? 'active' : '')}>
                  Admin
                </NavLink>
              )}
              <button type="button" className="logout-button" onClick={onLogout}>
                Logout
              </button>
            </>
          ) : (
            <>
              <NavLink to="/login" className={({ isActive }) => (isActive ? 'active' : '')}>
                Login
              </NavLink>
              <NavLink to="/register" className={({ isActive }) => (isActive ? 'active' : '')}>
                Register
              </NavLink>
            </>
          )}
        </nav>
      </div>
    </header>
  )
}
