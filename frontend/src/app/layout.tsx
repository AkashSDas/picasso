import type { Metadata } from "next";
import localFont from "next/font/local";

import { Navbar } from "@/components/shared/Navbar";
import { RootProviders } from "@/components/shared/RootProviders";

import "./globals.css";

const geistSans = localFont({
    src: "../../public/fonts/GeistVF.woff",
    variable: "--font-geist-sans",
    weight: "100 900",
});

const geistMono = localFont({
    src: "../../public/fonts/GeistMonoVF.woff",
    variable: "--font-geist-mono",
    weight: "100 900",
});

const cubano = localFont({
    src: "../../public/fonts/Cubano.ttf",
    variable: "--font-cubano",
    weight: "400",
    preload: true,
});

export const metadata: Metadata = {
    title: "Picasso",
    description: "Apply filters to images and videos using AI",
};

export default function RootLayout(
    props: Readonly<{ children: React.ReactNode }>,
): React.JSX.Element {
    return (
        <html lang="en">
            <body
                className={`${geistSans.variable} ${geistMono.variable} ${cubano.variable} antialiased`}
            >
                <Navbar />
                <RootProviders>{props.children}</RootProviders>
            </body>
        </html>
    );
}
