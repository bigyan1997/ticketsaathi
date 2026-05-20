import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'
import { register as registerApi, login as loginApi, getProfile } from '../../../api/auth'
import { useAuth } from '../../../context/AuthContext'
import Input from '../../../components/Input'
import Button from '../../../components/Button'

export default function RegisterForm() {
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
      // Step 1: create the account
      await registerApi(data)

      // Step 2: immediately log them in so they don't have to fill the form again
      const { data: tokens } = await loginApi({
        email: data.email,
        password: data.password,
      })

      // Step 3: fetch profile and save to context
      const { data: userData } = await getProfile()
      login(tokens, userData)

      navigate('/')
    } catch (err) {
      const errors = err.response?.data
      // Django returns field-level errors as an object, e.g. { email: ["already exists"] }
      if (errors && typeof errors === 'object') {
        const first = Object.values(errors)[0]
        setServerError(Array.isArray(first) ? first[0] : first)
      } else {
        setServerError('Something went wrong. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">

      <Input
        label="Full name"
        type="text"
        placeholder="Bigyan Karki"
        error={errors.full_name}
        {...register('full_name', {
          required: 'Full name is required.',
          minLength: { value: 2, message: 'Name must be at least 2 characters.' },
        })}
      />

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
        Create account
      </Button>

    </form>
  )
}
