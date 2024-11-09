"use client";

import { useAction } from "next-safe-action/hooks";
import { redirect } from "next/navigation";

import { logout } from "@/actions/auth";

import { Button } from "./Button";
import { Loader } from "./Loader";

export function LogoutButton() {
    const { executeAsync, isExecuting } = useAction(logout, {
        onSettled() {
            redirect("/");
        },
    });

    return (
        <Button
            className="w-full"
            onClick={async () => await executeAsync()}
            disabled={isExecuting}
        >
            {isExecuting ? <Loader sizeInPx={18} /> : "Logout"}
        </Button>
    );
}
