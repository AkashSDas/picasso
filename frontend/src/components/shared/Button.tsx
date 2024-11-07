import { Slot } from "@radix-ui/react-slot";
import { type VariantProps, cva } from "class-variance-authority";
import { type ButtonHTMLAttributes, forwardRef } from "react";

import { cn } from "@/utils/styles";

const variants = cva(
    "inline-flex font-head items-center justify-center gap-2 whitespace-nowrap rounded-full text-sm font-medium transition-colors focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
    {
        variants: {
            variant: {
                default: `border border-neutral-600/70 bg-neutral-700/70 backdrop-blur-sm hover:bg-neutral-700/40 hover:border-neutral-600/40`,
                brand: "bg-pink-500 text-neutral-50 hover:bg-pink-900/90",
                ghost: "border bg-transparent border-transparent backdrop-blur-sm hover:bg-neutral-700/70 hover:border-neutral-600/70",
            },
            size: {
                default: "h-9 px-6",
                icon: "h-9 w-9",
                lg: "h-10 px-6 text-base",
            },
        },
        defaultVariants: {
            variant: "default",
            size: "default",
        },
    },
);

type Props = ButtonHTMLAttributes<HTMLButtonElement> &
    VariantProps<typeof variants> & {
        asChild?: boolean;
    };

const Button = forwardRef<HTMLButtonElement, Props>(function (
    { className, variant, size, asChild = false, ...props },
    ref,
): React.JSX.Element {
    const Comp = asChild ? Slot : "button";

    return (
        <Comp
            className={cn(variants({ variant, size, className }))}
            ref={ref}
            {...props}
        />
    );
});

Button.displayName = "Button";

export { Button };
