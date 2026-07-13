import styles from "./FormSelect.module.scss";
import { Controller, useForm, type FieldValues } from "react-hook-form";
import FormField from "../FormField/FormField";
import { multipleClass } from "../../utils/multipleClass";
import type { FormSelectProps } from "./FormSelect.types";

const FormSelect = <T extends FieldValues>({
  label,
  name,
  className,
  options,
  rules,
  ...props
}: FormSelectProps<T>) => {
  const { control } = useForm<T>();

  return (
    <Controller
      name={name}
      control={control}
      rules={rules}
      render={({ field, fieldState: { error } }) => (
        <FormField label={label} error={error?.message} htmlFor={name}>
          <select
            defaultValue="disabled"
            id={name}
            {...field}
            {...props}
            className={multipleClass(["formSelect", className ?? ""])}
          >
            
          </select>
        </FormField>
      )}
    />
  )
}

export default FormSelect;