"use client";

import "ldrs/lineSpinner";
import { useEffect } from "react";

import { cn } from "@/utils/styles";

export function Loader({
    sizeInPx = 24,
    color = "white",
    variant = "alone",
    className = "",
}: {
    sizeInPx?: number;
    color?: "white";
    variant?: "alone" | "page" | "section";
    className?: string;
}): React.JSX.Element {
    useEffect(() => {
        async function getLoader() {
            const { lineSpinner } = await import("ldrs");
            lineSpinner.register();
        }
        getLoader();
    }, []);

    switch (variant) {
        case "page":
            return (
                <div
                    className={cn(
                        "flex items-center justify-center w-full my-32",
                        className,
                    )}
                >
                    <l-line-spinner
                        size={sizeInPx.toString()}
                        color={color}
                    ></l-line-spinner>
                </div>
            );
        case "section":
            return (
                <div
                    className={cn(
                        "flex items-center justify-center w-full my-12",
                        className,
                    )}
                >
                    <l-line-spinner
                        size={sizeInPx.toString()}
                        color={color}
                    ></l-line-spinner>
                </div>
            );
        default:
            return (
                <l-line-spinner
                    size={sizeInPx.toString()}
                    color={color}
                ></l-line-spinner>
            );
    }
}
