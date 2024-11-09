import type { Config } from "tailwindcss";

const config: Config = {
    darkMode: ["class"],
    content: [
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                head: ["var(--font-cubano)"],
                body: ["var(--font-geist-sans)"],
                mono: ["var(--font-geist-mono)"],
            },
            borderRadius: {
                lg: "var(--radius)",
                md: "calc(var(--radius) - 2px)",
                sm: "calc(var(--radius) - 4px)",
            },
            colors: {},
            keyframes: {
                fadeIn: {
                    "0%": { opacity: "0" },
                    "100%": { opacity: "1" },
                },
                slideIn: {
                    "0%": { transform: "translateY(50px)", opacity: "0" },
                    "100%": { transform: "translateY(0)", opacity: "1" },
                },
                slideUpAndRotate: {
                    "0%": {
                        transform: "translateY(130%) rotateX(-40deg)",
                        opacity: "0",
                    },
                    "100%": { transform: "translateY(0) rotateX(0deg)", opacity: "1" },
                },
            },
            animation: {
                fadeIn: "fadeIn 1.5s ease-in-out",
                slideIn: "slideIn 1.2s ease-in-out",
                slideUpAndRotate: `slideUpAndRotate 1s cubic-bezier(0.6, 0.01, 0.05, 0.95) forwards`,
            },
            transitionTimingFunction: {
                cubic: "cubic-bezier(0.6, 0.01, 0.05, 0.95)",
            },
        },
    },
    plugins: [require("tailwindcss-animate"), require("autoprefixer")],
};

export default config;
