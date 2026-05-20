// Reusable button — pass variant="outline" for the secondary style
export default function Button({ children, variant = 'primary', loading = false, ...props }) {
  const base = 'w-full py-2.5 px-4 rounded-lg font-medium text-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer'

  const styles = {
    primary: `${base} bg-blue-600 text-white hover:bg-blue-700`,
    outline: `${base} border border-gray-300 text-gray-700 hover:bg-gray-50`,
  }

  return (
    <button className={styles[variant]} disabled={loading || props.disabled} {...props}>
      {loading ? 'Please wait...' : children}
    </button>
  )
}
