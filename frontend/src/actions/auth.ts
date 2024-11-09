"use server";

import { cookies } from "next/headers";
import { z } from "zod";
import { zfd } from "zod-form-data";

import {
    emailLoginApiAuthLoginEmailPost200Response as login200Response,
    emailLoginApiAuthLoginEmailPost400Response as login400Response,
    emailSignupApiAuthSignupEmailPost201Response as signup201Response,
    emailSignupApiAuthSignupEmailPost400Response as signup400Response,
    emailSignupApiAuthSignupEmailPost409Response as signup409Response,
} from "@/gen/endpoints/authentication/authentication";
import { actionClient } from "@/lib/safe-action";
import { ACCESS_TOKEN_COOKIE_NAME, DEFAULT_ERR_MSG, status } from "@/utils/http";

// ======================================
// Form Data Schemas
// ======================================

const EmailSignupSchema = zfd.formData({
    username: zfd.text(z.string().min(3).max(255)),
    email: zfd.text(z.string().email()),
});

const EmailLoginSchema = zfd.formData({
    email: zfd.text(z.string().email()),
});

// ======================================
// Server Actions
// ======================================

export const signup = actionClient
    .schema(EmailSignupSchema)
    .action(async function signupAction({ parsedInput: body }) {
        const res = await fetch(`${process.env.BACKEND_URL}/api/auth/signup/email`, {
            method: "post",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });

        const payload = await res.json();

        try {
            switch (res.status) {
                case status.CREATED: {
                    const data = await signup201Response.parseAsync(payload);
                    return { data, status: status.CREATED };
                }
                case status.BAD_REQUEST: {
                    const data = await signup400Response.parseAsync(payload);
                    return { data, status: status.BAD_REQUEST };
                }
                case status.CONFLICT: {
                    const data = await signup409Response.parseAsync(payload);
                    return { data, status: status.CONFLICT };
                }
                default: {
                    console.dir({ message: `Failed to signup ${res.status}`, payload });

                    return {
                        data: { message: DEFAULT_ERR_MSG },
                        status: status.INTERNAL_SERVER_ERROR,
                    };
                }
            }
        } catch (e) {
            console.dir({
                reason: "Backend returned an unknown response",
                message: `Failed to signup ${res.status}`,
                payload,
            });

            return {
                data: { message: DEFAULT_ERR_MSG },
                status: status.INTERNAL_SERVER_ERROR,
            };
        }
    });

export const login = actionClient
    .schema(EmailLoginSchema)
    .action(async function loginAction({ parsedInput: body }) {
        const res = await fetch(`${process.env.BACKEND_URL}/api/auth/login/email`, {
            method: "post",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });

        const payload = await res.json();

        try {
            switch (res.status) {
                case status.OK: {
                    const data = await login200Response.parseAsync(payload);
                    return { data, status: status.OK };
                }
                case status.BAD_REQUEST: {
                    const data = await login400Response.parseAsync(payload);
                    return { data, status: status.BAD_REQUEST };
                }
                default: {
                    console.dir({ message: `Failed to login ${res.status}`, payload });

                    return {
                        data: { message: DEFAULT_ERR_MSG },
                        status: status.INTERNAL_SERVER_ERROR,
                    };
                }
            }
        } catch (e) {
            console.dir({
                reason: "Backend returned an unknown response",
                message: `Failed to login ${res.status}`,
                payload,
            });

            return {
                data: { message: DEFAULT_ERR_MSG },
                status: status.INTERNAL_SERVER_ERROR,
            };
        }
    });

export const logout = actionClient.action(async function logoutAction(): Promise<void> {
    await fetch(`${process.env.BACKEND_URL}/api/auth/logout`);

    const cookieStore = await cookies();
    cookieStore.delete(ACCESS_TOKEN_COOKIE_NAME);
});
