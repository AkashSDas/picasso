"use client";

import { type PropsWithChildren } from "react";

import { Toaster } from "./Toaster";

export function RootProviders(props: PropsWithChildren<unknown>): React.JSX.Element {
    return (
        <>
            {props.children}
            <Toaster />
        </>
    );
}
