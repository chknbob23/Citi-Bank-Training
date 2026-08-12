import React from 'react'
import './Footer.css'

export default function Footer() {
  const today = new Date().toLocaleDateString()
  return (
    <footer className="site-footer">
      <div className="container">
        <span>{today}</span>
        <span>© {new Date().getFullYear()} Bank UI. All rights reserved.</span>
      </div>
    </footer>
  )
}
