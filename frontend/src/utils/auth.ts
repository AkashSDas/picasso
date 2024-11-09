import "server-only";

import { cookies } from "next/headers";

import { getLoggedInUserProfileApiAuthMeGet200Response as loggedInUser200Response } from "@/gen/endpoints/authentication/authentication";

import { status } from "./http";

export async function getLoggedInUser() {
    // Even though this request is for an internal route, but theres no /external/api/auth/me
    // in our app so the request will be redirected to process.env.BACKEND_URL/api/auth/me
    // (more info at next.config.mjs).
    //
    // If you get a type error: URL is invalid then make sure you add the absolute url,
    // relative paths are only available in client side, because it's relative to the document.
    // but theres no document in the server.

    const res = await fetch(`${process.env.FRONTEND_URL}/external/api/auth/me`, {
        headers: {
            // You should send the cookies manually with the requests that are sent
            // from server side, so that the cookies reaches the middleware.ts. Put in
            // mind that this makes this route dynamic, meaning that next will pre-render
            // it on each request because we are using a function from next/headers
            Cookie: (await cookies()).toString(),
        },
    });

    try {
        switch (res.status) {
            case status.OK: {
                const payload = await res.json();
                const data = await loggedInUser200Response.parseAsync(payload);
                return {
                    user: data.user,
                    isLoggedIn: true,
                };
            }
            default: {
                console.dir({
                    message: `Failed to get user info ${res.status}`,
                });
            }
        }
    } catch (e) {
        console.dir({
            error: e,
            reason: "Backend returned an unknown response",
            message: `Failed to get user info ${res.status}`,
        });
    }

    return {
        user: null,
        isLoggedIn: false,
    };
}
