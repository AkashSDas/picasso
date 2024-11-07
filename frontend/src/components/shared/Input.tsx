import { type InputHTMLAttributes, forwardRef } from "react";

import { cn } from "@/utils/styles";

type Props = InputHTMLAttributes<HTMLInputElement>;

const Input = forwardRef<HTMLInputElement, Props>(function (
    { className, type, ...props },
    ref,
) {
    return (
        <input
            type={type}
            className={cn(
                "flex h-12 w-full font-medium border-b-2 border-b-neutral-600 bg-neutral-700/40 backdrop-blur-sm px-3 py-2 text-base file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-neutral-950 placeholder:text-neutral-500 focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50 md:text-sm",
                className,
            )}
            ref={ref}
            {...props}
        />
    );
});

Input.displayName = "Input";

export { Input };
