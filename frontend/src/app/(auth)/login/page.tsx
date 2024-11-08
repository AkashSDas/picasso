"use client";

import { useAction } from "next-safe-action/hooks";

import { login } from "@/actions/auth";
import { Button } from "@/components/shared/Button";
import { Input } from "@/components/shared/Input";
import { Label } from "@/components/shared/Label";
import { Loader } from "@/components/shared/Loader";
import { useToast } from "@/hooks/toast";
import { status } from "@/utils/http";

export default function LoginPage(): React.JSX.Element {
    const { toast } = useToast();

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
        </main>
    );
}
