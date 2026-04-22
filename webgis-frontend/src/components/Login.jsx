import { useState } from 'react'
import api from '../services/api'
import './Login.css'

function Login() {
  const [isLogin, setIsLogin] = useState(true)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')

  const handleRegister = async (e) => {
    e.preventDefault()
    try {
      await api.post('/register', { email, password })
      setMessage('Register berhasil. Silakan login.')
      setIsLogin(true)
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Register gagal')
    }
  }

  const handleLogin = async (e) => {
    e.preventDefault()
    try {
      const form = new URLSearchParams()
      form.append('username', email)
      form.append('password', password)

      const res = await api.post('/login', form)
      localStorage.setItem('token', res.data.access_token)
      window.location.href = '/'
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Login gagal')
    }
  }

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={isLogin ? handleLogin : handleRegister}>
        <h2>{isLogin ? 'Login' : 'Register'}</h2>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">
          {isLogin ? 'Login' : 'Register'}
        </button>

        {message && <p>{message}</p>}

        <p
          style={{ cursor: 'pointer', color: 'blue' }}
          onClick={() => {
            setIsLogin(!isLogin)
            setMessage('')
          }}
        >
          {isLogin ? 'Belum punya akun? Register' : 'Sudah punya akun? Login'}
        </p>
      </form>
    </div>
  )
}

export default Login