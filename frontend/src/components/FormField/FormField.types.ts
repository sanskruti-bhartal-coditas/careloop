import type { PropsWithChildren } from "react";

export interface FormFieldProps extends PropsWithChildren {
    label: string,
    error? :string,
    htmlFor?: string
}