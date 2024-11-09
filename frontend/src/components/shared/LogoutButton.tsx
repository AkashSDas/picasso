"use client";

import { useAction } from "next-safe-action/hooks";
import { redirect } from "next/navigation";

import { logout } from "@/actions/auth";

import { Button } from "./Button";
import { Loader } from "./Loader";

export function LogoutButton() {
    const { executeAsync, isExecuting } = useAction(logout);

    return (
        <Button
            className="w-full"
            onClick={async () => {
                await executeAsync();

                // Keeping it here instead of onSettled because redirect should be
                // called outside try/catch
                redirect("/");
            }}
            disabled={isExecuting}
        >
            {isExecuting ? <Loader sizeInPx={18} /> : "Logout"}
        </Button>
    );
}
