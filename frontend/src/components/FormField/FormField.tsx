import type { FormFieldProps } from "./FormField.types"
import styles from "./FormField.module.scss"

const FormField = ({ label, children, error, htmlFor }: FormFieldProps) => {
  return (
    <div>
      <label htmlFor={htmlFor}>{label}</label>

      {children}

      {error &&
        <div className={styles.errorMessage}>
          {error}
        </div>}

    </div>
  )
}

export default FormField