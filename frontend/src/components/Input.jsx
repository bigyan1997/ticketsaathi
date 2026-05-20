// Reusable input — designed to work with React Hook Form's register()
// Pass error={errors.fieldName} to show validation messages below the input
export default function Input({ label, error, ...props }) {
  return (
    <div className="flex flex-col gap-1">
      {label && (
        <label className="text-sm font-medium text-gray-700">{label}</label>
      )}
      <input
        className={`w-full px-3 py-2.5 rounded-lg border text-sm outline-none transition-colors
          ${error
            ? 'border-red-400 focus:border-red-500'
            : 'border-gray-300 focus:border-blue-500'
          }`}
        {...props}
      />
      {error && (
        <p className="text-xs text-red-500">{error.message}</p>
      )}
    </div>
  )
}
