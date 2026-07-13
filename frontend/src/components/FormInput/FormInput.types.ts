import type { FieldValues, Path, RegisterOptions } from "react-hook-form";
import type { InputProps } from "../Input/Input.types";

export interface FormInputProps<T extends FieldValues> extends Omit<InputProps, 'name'> {
  name: Path<T>,
  label: string,
  rules?: RegisterOptions<T, Path<T>>;
}