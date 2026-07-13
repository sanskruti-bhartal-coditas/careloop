import type { ButtonHTMLAttributes } from "react";

type Variant = 'primary' | 'secondary' | 'tertiary' | 'success' | 'error'

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement>{
  variant?:Variant
}