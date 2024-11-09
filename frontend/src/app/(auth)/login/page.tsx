"use client";

import { useAction } from "next-safe-action/hooks";
import Link from "next/link";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useEffect } from "react";

import { login } from "@/actions/auth";
import { Button } from "@/components/shared/Button";
import { Input } from "@/components/shared/Input";
import { Label } from "@/components/shared/Label";
import { Loader } from "@/components/shared/Loader";
import { useToast } from "@/hooks/toast";
import { LOGIN_ERROR_MSG_QUERY_NAME, status } from "@/utils/http";

export default function LoginPage(): React.JSX.Element {
    const { toast } = useToast();

    const router = useRouter();
    const pathname = usePathname();
    const searchParams = useSearchParams();
    const errorMsg = searchParams.get(LOGIN_ERROR_MSG_QUERY_NAME);

    const { executeAsync, isExecuting } = useAction(login, {
        onSuccess({ data }) {
            if (data) {
                const created = data.status === status.OK;

                toast({
                    variant: created ? "success" : "error",
                    title: created ? "Sent Email" : "Failed",
                    description: data.data.message,
                });
            }
        },
        onError() {
            toast({
                variant: "error",
                title: "Failed",
                description: "Something went wrong",
            });
        },
    });

    async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        const form = new FormData(e.currentTarget);
        await executeAsync(form);
    }

    useEffect(
        function checkForLoginErrorMessage() {
            if (errorMsg) {
                // When page is loaded and errorMsg is present it's not showing
                // the toast (not sure why). To resolve this we are using setTimeout
                setTimeout(() => {
                    toast({
                        variant: "error",
                        title: "Failed",
                        description: errorMsg,
                    });

                    // Remove error message from search params

                    const nextSearchParams = new URLSearchParams(
                        searchParams.toString(),
                    );
                    nextSearchParams.delete(LOGIN_ERROR_MSG_QUERY_NAME);

                    router.replace(`${pathname}?${nextSearchParams}`);
                }, 100);
            }
        },
        [errorMsg, searchParams, pathname, router, toast],
    );

    return (
        <main className="mx-auto w-full max-w-md my-10 px-4">
            <h1 className="font-head text-3xl md:text-4xl mb-8">Welcome Back</h1>

            <form onSubmit={onSubmit} className="flex flex-col gap-4">
                <div className="flex flex-col gap-2">
                    <Label htmlFor="email">Email</Label>
                    <Input
                        type="email"
                        required
                        name="email"
                        placeholder="Unique email address"
                    />
                    <div className="text-[12.8px] font-medium text-neutral-400">
                        Login link will be sent to the registered email address
                    </div>
                </div>

                <Button
                    variant="brand"
                    type="submit"
                    disabled={isExecuting}
                    aria-disabled={isExecuting}
                    className="w-full mt-4"
                >
                    {isExecuting ? <Loader /> : "Login"}
                </Button>
            </form>

            <hr className="my-8 border-neutral-800" />

            <p className="text-center text-neutral-400 text-sm font-medium">
                {`Don't have an account? `}
                <Link href="/signup" className="text-blue-500 underline">
                    Signup
                </Link>
            </p>
        </main>
    );
}
