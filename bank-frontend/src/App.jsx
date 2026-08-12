import React, { useState } from 'react'
import axios from 'axios'
import { Routes, Route, Navigate } from 'react-router-dom'
import Header from './components/HeaderComponent/Header'
import Footer from './components/FooterComponent/Footer'
import Home from './pages/Home'
import About from './pages/About'
import Contact from './pages/Contact'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Admin from './pages/Admin'
import './App.css'

function normalizeEmail(value) {
  return (value || '').toString().trim().toLowerCase()
}

function getEmailFromCustomer(customer) {
  return normalizeEmail(customer.email || customer.username || customer.user_name || '')
}

function ProtectedRoute({ user, children }) {
  return user ? children : <Navigate to="/login" replace />
}

export default function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0)
  const [loginError, setLoginError] = useState('')
  const [loading, setLoading] = useState(false)

  const getUser = () => {
    const stored = sessionStorage.getItem('phonybank_user')
    return stored ? JSON.parse(stored) : null
  }

  const getCustomers = () => {
    const stored = sessionStorage.getItem('phonybank_customers')
    return stored ? JSON.parse(stored) : []
  }

  const user = getUser()
  const customers = getCustomers()

  const handleLogin = async ({ email, password }) => {
    setLoginError('')
    setLoading(true)

    try {
      const response = await axios.get('http://127.0.0.1:5000/api/v1/customers')
      const apiPayload = response.data
      const maybeList = apiPayload?.data ?? apiPayload?.customers ?? apiPayload
      const customerList = Array.isArray(maybeList) ? maybeList : []

      if (normalizeEmail(email) === 'admin' && password === '123') {
        sessionStorage.setItem('phonybank_customers', JSON.stringify(customerList))
        sessionStorage.setItem('phonybank_user', JSON.stringify({ email, name: 'Admin', role: 'admin' }))
        setRefreshTrigger(r => r + 1)
        return true
      }

      const customer = customerList.find((item) => getEmailFromCustomer(item) === normalizeEmail(email))
      if (!customer) {
        setLoginError('Customer not found. Please check your email address.')
        return false
      }

      if (customer.password && customer.password !== password) {
        setLoginError('Invalid password. Please try again.')
        return false
      }

      sessionStorage.setItem('phonybank_customers', JSON.stringify([customer]))
      sessionStorage.setItem('phonybank_user', JSON.stringify({
        email,
        name: customer.name || `${customer.first_name || ''} ${customer.last_name || ''}`.trim() || email,
        role: 'customer',
      }))
      setRefreshTrigger(r => r + 1)
      return true
    } catch (error) {
      setLoginError('Unable to reach the customer API. Please make sure the backend is running and accessible at http://127.0.0.1:5000.')
      return false
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    sessionStorage.removeItem('phonybank_user')
    sessionStorage.removeItem('phonybank_customers')
    setRefreshTrigger(r => r + 1)
  }

  const handleRefresh = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/v1/customers')
      const apiPayload = response.data
      const maybeList = apiPayload?.data ?? apiPayload?.customers ?? apiPayload
      const customerList = Array.isArray(maybeList) ? maybeList : []
      sessionStorage.setItem('phonybank_customers', JSON.stringify(customerList))
      setRefreshTrigger(r => r + 1)
    } catch (error) {
      console.error('Failed to refresh customers:', error)
    }
  }

  return (
    <div className="app-root">
      <Header user={user} onLogout={handleLogout} />

      <main className="app-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/login" element={<Login onLogin={handleLogin} loading={loading} error={loginError} />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute user={user}>
                <Dashboard user={user} customers={customers} />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin"
            element={
              user?.role === 'admin' ? (
                <Admin customers={customers} onRefresh={handleRefresh} />
              ) : (
                <Navigate to="/dashboard" replace />
              )
            }
          />
        </Routes>
      </main>

      <Footer />
    </div>
  )
}
