import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'
import { login as loginApi, getProfile } from '../../../api/auth'
import { useAuth } from '../../../context/AuthContext'
import Input from '../../../components/Input'
import Button from '../../../components/Button'

export default function LoginForm() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [serverError, setServerError] = useState('')
  const [loading, setLoading] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm()

  const onSubmit = async (data) => {
    setServerError('')
    setLoading(true)

    try {
      // Step 1: get the tokens
      const { data: tokens } = await loginApi(data)

      // Step 2: fetch the user's profile so we have their name/email
      const { data: userData } = await getProfile()

      // Step 3: save tokens + user into AuthContext
      login(tokens, userData)

      navigate('/')
    } catch (err) {
      const msg = err.response?.data?.detail
      setServerError(msg || 'Invalid email or password.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">

      <Input
        label="Email address"
        type="email"
        placeholder="you@example.com"
        error={errors.email}
        {...register('email', {
          required: 'Email is required.',
          pattern: { value: /^\S+@\S+\.\S+$/, message: 'Enter a valid email.' },
        })}
      />

      <Input
        label="Password"
        type="password"
        placeholder="••••••••"
        error={errors.password}
        {...register('password', {
          required: 'Password is required.',
          minLength: { value: 8, message: 'Password must be at least 8 characters.' },
        })}
      />

      {serverError && (
        <p className="text-sm text-red-500 text-center">{serverError}</p>
      )}

      <Button type="submit" loading={loading}>
        Sign in
      </Button>

    </form>
  )
}
