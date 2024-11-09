"use client";

import * as SheetPrimitive from "@radix-ui/react-dialog";
import { type VariantProps, cva } from "class-variance-authority";
import { X } from "lucide-react";
import Link from "next/link";
import {
    type ComponentPropsWithoutRef,
    type ElementRef,
    type HTMLAttributes,
    forwardRef,
} from "react";

import { cn, tw } from "@/utils/styles";

const Sheet = SheetPrimitive.Root;
const SheetTrigger = SheetPrimitive.Trigger;
const SheetClose = SheetPrimitive.Close;
const SheetPortal = SheetPrimitive.Portal;

const SheetOverlay = forwardRef<
    ElementRef<typeof SheetPrimitive.Overlay>,
    ComponentPropsWithoutRef<typeof SheetPrimitive.Overlay>
>(function ({ className, ...props }, ref) {
    return (
        <SheetPrimitive.Overlay
            className={cn(
                tw`inset-0 fixed z-50 bg-neutral-950/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0`,
                className,
            )}
            {...props}
            ref={ref}
        />
    );
});

SheetOverlay.displayName = SheetPrimitive.Overlay.displayName;

const variants = cva(
    cn(
        tw`fixed z-50 gap-4 transition ease-in-out bg-neutral-900/70 border-neutral-800/70 backdrop-blur-sm shadow-[-16px_16px_32px_0px_rgba(0,0,0,0.1)]`,
        tw`data-[state=closed]:duration-300 data-[state=open]:duration-500 data-[state=open]:animate-in data-[state=closed]:animate-out`,
    ),
    {
        variants: {
            side: {
                top: tw`inset-x-0 shadow-lg top-0 border-b data-[state=closed]slide-out-to-top data-[state=open]:slide-in-from-top`,
                bottom: tw`inset-x-0 bottom-0 border-t data-[state=closed]:slide-out-to-bottom data-[state=open]:slide-in-from-bottom`,
                left: tw`inset-y-0 left-0 h-full w-3/4 border-r data-[state=closed]:slide-out-to-left data-[state=open]:slide-in-from-left sm:max-w-sm`,
                right: tw`inset-y-0 right-0 h-full w-3/4 border-l data-[state=closed]:slide-out-to-right data-[state=open]:slide-in-from-right sm:max-w-sm`,
            },
        },
        defaultVariants: {
            side: "right",
        },
    },
);

type SheetContentProps = ComponentPropsWithoutRef<typeof SheetPrimitive.Content> &
    VariantProps<typeof variants>;

const SheetContent = forwardRef<
    ElementRef<typeof SheetPrimitive.Content>,
    SheetContentProps
>(function ({ side = "right", className, children, ...props }, ref) {
    return (
        <SheetPortal>
            <SheetOverlay />
            <SheetPrimitive.Content
                ref={ref}
                className={cn(variants({ side }), className)}
                {...props}
            >
                <div className="flex items-center justify-between h-12 gap-2 px-4 border-b md:h-14 md:px-8 bg-neutral-900/70 border-b-neutral-800/70 backdrop-blur-sm">
                    <SheetClose asChild>
                        <Link href="/">
                            <span className="font-head text-base">Picasso</span>
                        </Link>
                    </SheetClose>

                    <SheetPrimitive.Close className="rounded-full focus:outline-none bg-neutral-700/70 border transition-all border-neutral-600/70 backdrop-blur-sm flex justify-center items-center w-8 h-8 disabled:pointer-events-none data-[state=open]:bg-transparent hover:bg-neutral-700/40 hover:border-neutral-600/40">
                        <X className="w-4 h-4" />
                        <span className="sr-only">Close</span>
                    </SheetPrimitive.Close>
                </div>

                <div className="p-6">{children}</div>
            </SheetPrimitive.Content>
        </SheetPortal>
    );
});

SheetContent.displayName = SheetPrimitive.Content.displayName;

function SheetHeader({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
    return (
        <div
            className={cn(
                "flex flex-col space-y-2 text-center sm:text-left",
                className,
            )}
            {...props}
        />
    );
}

SheetHeader.displayName = "SheetHeader";

function SheetFooter({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
    return (
        <div
            className={cn(
                "flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2",
                className,
            )}
            {...props}
        />
    );
}

SheetFooter.displayName = "SheetFooter";

const SheetTitle = forwardRef<
    ElementRef<typeof SheetPrimitive.Title>,
    ComponentPropsWithoutRef<typeof SheetPrimitive.Title>
>(function ({ className, ...props }, ref) {
    return (
        <SheetPrimitive.Title
            ref={ref}
            className={cn("text-lg font-semibold text-neutral-100", className)}
            {...props}
        />
    );
});

SheetTitle.displayName = SheetPrimitive.Title.displayName;

const SheetDescription = forwardRef<
    ElementRef<typeof SheetPrimitive.Description>,
    ComponentPropsWithoutRef<typeof SheetPrimitive.Description>
>(function ({ className, ...props }, ref) {
    return (
        <SheetPrimitive.Description
            ref={ref}
            className={cn("text-sm text-neutral-400", className)}
            {...props}
        />
    );
});

SheetDescription.displayName = SheetPrimitive.Description.displayName;

export {
    Sheet,
    SheetPortal,
    SheetOverlay,
    SheetTrigger,
    SheetClose,
    SheetContent,
    SheetHeader,
    SheetFooter,
    SheetTitle,
    SheetDescription,
};
