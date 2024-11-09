import { cookies } from "next/headers";
import { type NextRequest, NextResponse } from "next/server";

import { ACCESS_TOKEN_COOKIE_NAME, status } from "./utils/http";

export default async function middleware(req: NextRequest): Promise<Response> {
    const token = req.cookies.get(ACCESS_TOKEN_COOKIE_NAME)?.value;

    // Clone the request and set the Authorization header if the access token exists
    const headers = new Headers(req.headers);
    if (token) {
        headers.set("Authorization", `Bearer ${token}`);
    }

    // Create the modified request with the updated headers
    const originalRequest = new Request(req.url, {
        method: req.method,
        headers,
        body: req.body,
        redirect: "manual", // Prevent auto-redirects
    });

    let response = await fetch(originalRequest);

    if (response.status !== status.UNAUTHORIZED) {
        return response;
    } else {
        // Handle 401 Unauthorized by refreshing the token

        const refreshResponse = await fetch(
            `${process.env.BACKEND_URL}/api/auth/refresh`,
            {
                credentials: "include",
                headers: { Cookie: req.cookies.toString() },
            },
        );

        if (refreshResponse.status !== status.OK) {
            (await cookies()).delete(ACCESS_TOKEN_COOKIE_NAME);
            return refreshResponse;
        } else {
            const { accessToken: newToken } = await refreshResponse.json();

            headers.set("Authorization", `Bearer ${newToken}`);
            const retryRequest = new Request(req.url, {
                method: req.method,
                headers,
                body: req.body,
                redirect: "manual", // Prevent auto-redirects
            });

            // Retry the original request with the new access token
            response = await fetch(retryRequest);

            // Update the cookie with the new access token
            const cookieResponse = NextResponse.next();
            cookieResponse.cookies.set(ACCESS_TOKEN_COOKIE_NAME, newToken, {
                httpOnly: true,
                secure: process.env.NODE_ENV === "production",
                sameSite: "lax",
                maxAge: 6 * 60, // 6 minutes
                path: "/",
            });

            return cookieResponse;
        }
    }
}

export const config = {
    matcher: [
        // "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
        // "/(api|trpc)(.*)",
        "/(external)(.*)",
    ],
};
