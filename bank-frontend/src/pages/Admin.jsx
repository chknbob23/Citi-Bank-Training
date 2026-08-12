import React, { useState } from 'react'
import axios from 'axios'
import '../styles/Admin.css'

const API_BASE = 'http://127.0.0.1:5000/api/v1'

export default function Admin({ customers, onRefresh }) {
  const [activeTab, setActiveTab] = useState('list')
  const [formData, setFormData] = useState({
    userName: '',
    email: '',
    balance: '',
    accountType: 'Checking',
  })
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'balance' ? parseFloat(value) || 0 : value,
    }))
  }

  const handleCreateCustomer = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      const payload = {
        userName: formData.userName,
        email: formData.email,
        balance: formData.balance,
        accountType: formData.accountType,
      }
      await axios.post(`${API_BASE}/customers`, payload)
      setMessage('Customer created successfully!')
      setFormData({ userName: '', email: '', balance: '', accountType: 'Checking' })
      onRefresh()
      setTimeout(() => setActiveTab('list'), 1500)
    } catch (error) {
      setMessage(`Error: ${error.response?.data?.message || error.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteCustomer = async (customerId) => {
    if (!window.confirm('Are you sure you want to delete this customer?')) return

    setLoading(true)
    try {
      await axios.delete(`${API_BASE}/customers/${customerId}`)
      setMessage('Customer deleted successfully!')
      onRefresh()
    } catch (error) {
      setMessage(`Error: ${error.response?.data?.message || error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="page admin">
      <div className="container">
        <h2>Admin Management</h2>
        <p className="admin-subtitle">Manage customer accounts and perform operations</p>

        <div className="admin-tabs">
          <button
            className={`tab-btn ${activeTab === 'list' ? 'active' : ''}`}
            onClick={() => setActiveTab('list')}
          >
            Customers ({customers.length})
          </button>
          <button
            className={`tab-btn ${activeTab === 'create' ? 'active' : ''}`}
            onClick={() => setActiveTab('create')}
          >
            Add Customer
          </button>
        </div>

        {message && <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>{message}</div>}

        {activeTab === 'list' && (
          <div className="admin-section card">
            <h3>Customer List</h3>
            <div className="customers-grid">
              {customers.length === 0 ? (
                <p className="no-data">No customers found</p>
              ) : (
                customers.map((customer) => (
                  <div key={customer.accountId} className="customer-item card">
                    <h4>{customer.userName}</h4>
                    <p><strong>Email:</strong> {customer.email}</p>
                    <p><strong>Account:</strong> {customer.accountId}</p>
                    <p><strong>Type:</strong> {customer.accountType || 'Checking'}</p>
                    <p><strong>Balance:</strong> ${customer.balance?.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
                    <div className="customer-actions">
                      <button
                        className="btn-delete"
                        onClick={() => handleDeleteCustomer(customer.accountId)}
                        disabled={loading}
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {activeTab === 'create' && (
          <div className="admin-section card">
            <h3>Add New Customer</h3>
            <form onSubmit={handleCreateCustomer} className="admin-form">
              <label>
                Username
                <input
                  type="text"
                  name="userName"
                  value={formData.userName}
                  onChange={handleInputChange}
                  required
                />
              </label>
              <label>
                Email
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                />
              </label>
              <label>
                Initial Balance
                <input
                  type="number"
                  name="balance"
                  value={formData.balance}
                  onChange={handleInputChange}
                  step="0.01"
                  required
                />
              </label>
              <label>
                Account Type
                <select name="accountType" value={formData.accountType} onChange={handleInputChange}>
                  <option>Checking</option>
                  <option>Savings</option>
                  <option>Money Market</option>
                  <option>Premium</option>
                </select>
              </label>
              <button type="submit" disabled={loading}>
                {loading ? 'Creating...' : 'Create Customer'}
              </button>
            </form>
          </div>
        )}
      </div>
    </section>
  )
}
