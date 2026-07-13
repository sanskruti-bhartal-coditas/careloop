import { Controller, useFormContext, type FieldValues } from "react-hook-form"
import type { FormInputProps } from "./FormInput.types"
import FormField from "../FormField/FormField";
import Input from "../../components/Input/Input";

const FormInput = <T extends FieldValues>({ label, name, rules, ...props }: FormInputProps<T>) => {
    const { control } = useFormContext<T>();
    
    return (
        <Controller
            name={name}
            control={control}
            rules={rules}
            render={({ field, fieldState: { error } }) =>
                <FormField
                    label={label}
                    error={error?.message}
                    htmlFor={name}
                >
                    <Input id={name} {...field} {...props} />
                </FormField>
            }
        />
    )
}

export default FormInput;