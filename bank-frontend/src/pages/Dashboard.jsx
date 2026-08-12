import React from 'react'

function getCustomerName(customer) {
  if (customer.userName) return customer.userName
  if (customer.name) return customer.name
  const parts = [customer.first_name, customer.last_name, customer.lastName, customer.firstName]
    .filter(Boolean)
  return parts.join(' ') || customer.email || 'Unnamed Customer'
}

function getAccountNumber(customer) {
  return customer.accountId || customer.account_id || customer.accountNumber || customer.account || '•••• ••••'
}

function getAccountType(customer) {
  return customer.accountType || customer.type || 'Checking'
}

function getBalance(customer) {
  const value = customer.balance ?? customer.account_balance ?? customer.accountBalance ?? 0
  const normalized = typeof value === 'string'
    ? Number(value.replace(/[^0-9.-]/g, ''))
    : Number(value)
  return Number.isFinite(normalized) ? normalized : 0
}

export default function Dashboard({ user, customers }) {
  const totalBalance = customers.reduce((sum, customer) => sum + getBalance(customer), 0)

  return (
    <section className="page dashboard">
      <div className="container">
        <div className="dashboard-hero card">
          <div>
            <p className="eyebrow">Phony Bank</p>
            <h2>Welcome back, {user?.name || 'Valued Customer'}</h2>
            <p>{user?.role === 'admin' ? 'Below is a snapshot of all customers loaded from your MongoDB-backed API.' : 'Below is your account data loaded from your MongoDB-backed API.'}</p>
          </div>
          <div className="dashboard-summary">
            <div>
              <span>Total accounts</span>
              <strong>{customers.length}</strong>
            </div>
            <div>
              <span>Combined balance</span>
              <strong>${totalBalance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</strong>
            </div>
          </div>
        </div>

        <div className="account-grid">
          {customers.slice(0, 4).map((customer, index) => (
            <article key={customer.id ?? index} className="account-card card">
              <p className="account-name">{getCustomerName(customer)}</p>
              <p className="account-type">{getAccountType(customer)}</p>
              <p className="account-number">{getAccountNumber(customer)}</p>
              <p className="account-balance">
                ${getBalance(customer).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </p>
            </article>
          ))}
        </div>

        <div className="table-card card">
          <h3>Customer account roster</h3>
          <div className="table-scroll">
            <table className="customer-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Account</th>
                  <th>Type</th>
                  <th>Balance</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {customers.map((customer, index) => (
                  <tr key={customer.id ?? index}>
                    <td>{getCustomerName(customer)}</td>
                    <td>{getAccountNumber(customer)}</td>
                    <td>{getAccountType(customer)}</td>
                    <td>${getBalance(customer).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                    <td>{customer.status || customer.account_status || 'Active'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  )
}
