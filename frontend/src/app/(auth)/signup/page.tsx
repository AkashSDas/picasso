"use client";

import { useAction } from "next-safe-action/hooks";

import { signup } from "@/actions/auth";
import { Button } from "@/components/shared/Button";
import { Input } from "@/components/shared/Input";
import { Label } from "@/components/shared/Label";
import { Loader } from "@/components/shared/Loader";
import { useToast } from "@/hooks/toast";
import { status } from "@/utils/http";

export default function SignupPage(): React.JSX.Element {
    const { toast } = useToast();

    const { executeAsync, isExecuting } = useAction(signup, {
        onSuccess({ data }) {
            if (data) {
                const created = data.status === status.CREATED;

                toast({
                    variant: created ? "success" : "error",
                    title: created ? "Account Created" : "Failed",
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
            <h1 className="font-head text-3xl md:text-4xl mb-8">New Account</h1>

            <form onSubmit={onSubmit} className="flex flex-col gap-4">
                <div className="flex flex-col gap-2">
                    <Label htmlFor="username">Username</Label>
                    <Input
                        type="text"
                        minLength={3}
                        maxLength={255}
                        required
                        name="username"
                        placeholder="Unique username"
                    />
                </div>

                <div className="flex flex-col gap-2">
                    <Label htmlFor="email">Email</Label>
                    <Input
                        type="email"
                        required
                        name="email"
                        placeholder="Unique email address"
                    />
                </div>

                <Button
                    variant="brand"
                    type="submit"
                    disabled={isExecuting}
                    aria-disabled={isExecuting}
                    className="w-full mt-4"
                >
                    {isExecuting ? <Loader /> : "Signup"}
                </Button>
            </form>
        </main>
    );
}
