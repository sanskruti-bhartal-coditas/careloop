import type { SelectHTMLAttributes } from "react";
import type { FieldValues, Path, RegisterOptions } from "react-hook-form";

export interface FormSelectProps<T extends FieldValues> extends Omit<SelectHTMLAttributes<HTMLSelectElement>, 'name'> {
    name: Path<T>;
    label: string;
    rules?: RegisterOptions<T, Path<T>>;
    options: { label: string; value: string | number | boolean }[];
}