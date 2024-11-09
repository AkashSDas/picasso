import { cookies } from "next/headers";
import { redirect } from "next/navigation";

import {
    completeEmailLoginApiAuthLoginEmailTokenGet200Response as completeLogin200Response,
    completeEmailLoginApiAuthLoginEmailTokenGet400Response as completeLogin400Response,
} from "@/gen/endpoints/authentication/authentication";
import {
    ACCESS_TOKEN_COOKIE_NAME,
    LOGIN_ERROR_MSG_QUERY_NAME,
    status,
} from "@/utils/http";

// As of NextJS 15 cookies can only be set inside Server actions and Route handlers
// and having this logic in a server action is not working because it will behave like
// a normal async function when directly called inside a component
//
//  error: ReadonlyRequestCookiesError: Cookies can only be modified in a Server Action or Route Handler. Read more: https://nextjs.org/docs/app/api-reference/functions/cookies#cookiessetname-value-options
export async function GET(
    _request: Request,
    opts: { params: Promise<{ magicLinkToken: string }> },
) {
    const [cookieStore, params] = await Promise.all([cookies(), opts.params]);
    const token = params.magicLinkToken;

    const res = await fetch(`${process.env.BACKEND_URL}/api/auth/login/email/${token}`);
    const payload = await res.json();

    let redirectPath: "/" | `/login?${typeof LOGIN_ERROR_MSG_QUERY_NAME}=${string}` =
        "/";

    try {
        switch (res.status) {
            case status.OK: {
                const data = await completeLogin200Response.parseAsync(payload);

                cookieStore.set(ACCESS_TOKEN_COOKIE_NAME, data.accessToken, {
                    httpOnly: true,
                    secure: process.env.NODE_ENV === "production",
                    sameSite: "lax",
                    maxAge: 6 * 60, // 6 minutes
                    path: "/",
                });

                redirectPath = "/";
                break;
            }
            case status.BAD_REQUEST: {
                const data = await completeLogin400Response.parseAsync(payload);
                redirectPath = `/login?${LOGIN_ERROR_MSG_QUERY_NAME}=${data.message}`;
                break;
            }
            default: {
                console.dir({
                    message: `Failed to complete magic link login ${res.status}`,
                    payload,
                });

                redirectPath = `/login?${LOGIN_ERROR_MSG_QUERY_NAME}=Internal Server Error`;
                break;
            }
        }
    } catch (e) {
        console.dir({
            error: e,
            reason: "Backend returned an unknown response",
            message: `Failed to complete magic link login ${res.status}`,
            payload,
        });

        redirectPath = `/login?error-message=Internal Server Error`;
    }

    redirect(redirectPath);
}
