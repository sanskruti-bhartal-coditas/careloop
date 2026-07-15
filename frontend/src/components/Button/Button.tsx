import styles from "./Button.module.scss"
import { multipleClass } from "../../utils/multipleClass"
import type { ButtonProps } from "./Button.types"

const Button = ({ variant = 'primary', children, className, ...props }: ButtonProps) =>{
  return(
    <button className={multipleClass([styles.button, styles[variant], className??"" ])} {...props}>
      {children}
    </button>
  )
}

export default Button;