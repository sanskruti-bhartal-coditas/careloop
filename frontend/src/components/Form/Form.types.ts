import type { PropsWithChildren } from "react";
import type { UseFormReturn } from "react-hook-form";


export interface FormProps extends PropsWithChildren{
    onSubmit: (data: any) => void,
    methods: UseFormReturn<any, any, any>
    className?: string
}