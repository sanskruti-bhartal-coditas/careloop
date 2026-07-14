import { multipleClass } from "../../utils/multipleClass";
import styles from "./Input.module.scss";
import type { InputProps } from "./Input.types";

const Input = ({className, ...props}:InputProps) =>{
  return(
    <input className={multipleClass([styles.input, className??""])} {...props} />
  )
}

export default Input;