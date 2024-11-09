/**
 * Generated by orval v7.2.0 🍺
 * Do not edit manually.
 * Picasso
 * OpenAPI spec version: 0.1.0
 */
import { z as zod } from "zod";

/**
 * @summary Signup using email and username. Both of them should be unique. This will send magic link for login on the registered email address
 */
export const emailSignupApiAuthSignupEmailPostBodyUsernameMin = 3;

export const emailSignupApiAuthSignupEmailPostBodyUsernameMax = 255;

export const emailSignupApiAuthSignupEmailPostBody = zod.object({
    email: zod.string().email(),
    username: zod
        .string()
        .min(emailSignupApiAuthSignupEmailPostBodyUsernameMin)
        .max(emailSignupApiAuthSignupEmailPostBodyUsernameMax),
});

export const emailSignupApiAuthSignupEmailPost201Response = zod.object({
    message: zod.string(),
});

export const emailSignupApiAuthSignupEmailPost400Response = zod
    .object({
        reason: zod.string(),
        message: zod.string(),
        errors: zod.array(zod.any()),
    })
    .or(
        zod.object({
            reason: zod.string(),
            message: zod.string(),
        }),
    );

export const emailSignupApiAuthSignupEmailPost409Response = zod.object({
    reason: zod.string(),
    message: zod.string(),
});

export const emailSignupApiAuthSignupEmailPost422Response = zod.object({
    detail: zod
        .array(
            zod.object({
                loc: zod.array(zod.string().or(zod.number())),
                msg: zod.string(),
                type: zod.string(),
            }),
        )
        .optional(),
});

export const emailSignupApiAuthSignupEmailPost500Response = zod.object({
    reason: zod.string(),
    message: zod.string(),
});

/**
 * @summary Login using email. This will send magic send magic link for login on the registered email address
 */
export const emailLoginApiAuthLoginEmailPostBody = zod.object({
    email: zod.string().email(),
});

export const emailLoginApiAuthLoginEmailPost200Response = zod.object({
    message: zod.string(),
});

export const emailLoginApiAuthLoginEmailPost400Response = zod
    .object({
        reason: zod.string(),
        message: zod.string(),
        errors: zod.array(zod.any()),
    })
    .or(
        zod.object({
            reason: zod.string(),
            message: zod.string(),
        }),
    );

export const emailLoginApiAuthLoginEmailPost422Response = zod.object({
    detail: zod
        .array(
            zod.object({
                loc: zod.array(zod.string().or(zod.number())),
                msg: zod.string(),
                type: zod.string(),
            }),
        )
        .optional(),
});

export const emailLoginApiAuthLoginEmailPost500Response = zod.object({
    reason: zod.string(),
    message: zod.string(),
});

/**
 * @summary Complete magic link login and then set refresh token and sending access token
 */
export const completeEmailLoginApiAuthLoginEmailTokenGetParams = zod.object({
    token: zod.string(),
});

export const completeEmailLoginApiAuthLoginEmailTokenGet200ResponseUserUsernameMin = 3;

export const completeEmailLoginApiAuthLoginEmailTokenGet200ResponseUserUsernameMax = 255;

export const completeEmailLoginApiAuthLoginEmailTokenGet200Response = zod.object({
    accessToken: zod.string(),
    refreshToken: zod.string(),
    user: zod.object({
        userId: zod.string(),
        username: zod
            .string()
            .min(completeEmailLoginApiAuthLoginEmailTokenGet200ResponseUserUsernameMin)
            .max(completeEmailLoginApiAuthLoginEmailTokenGet200ResponseUserUsernameMax),
        email: zod.string().email(),
        profilePicURL: zod.string().url().min(1),
    }),
});

export const completeEmailLoginApiAuthLoginEmailTokenGet400Response = zod
    .object({
        reason: zod.string(),
        message: zod.string(),
        errors: zod.array(zod.any()),
    })
    .or(
        zod.object({
            reason: zod.string(),
            message: zod.string(),
        }),
    );

export const completeEmailLoginApiAuthLoginEmailTokenGet422Response = zod.object({
    detail: zod
        .array(
            zod.object({
                loc: zod.array(zod.string().or(zod.number())),
                msg: zod.string(),
                type: zod.string(),
            }),
        )
        .optional(),
});

export const completeEmailLoginApiAuthLoginEmailTokenGet500Response = zod.object({
    reason: zod.string(),
    message: zod.string(),
});

/**
 * @summary Refresh access token
 */
export const refreshAccessTokenApiAuthRefreshGet200Response = zod.object({
    accessToken: zod.string(),
});

export const refreshAccessTokenApiAuthRefreshGet400Response = zod
    .object({
        reason: zod.string(),
        message: zod.string(),
        errors: zod.array(zod.any()),
    })
    .or(
        zod.object({
            reason: zod.string(),
            message: zod.string(),
        }),
    );

export const refreshAccessTokenApiAuthRefreshGet401Response = zod.object({
    reason: zod.string(),
    message: zod.string(),
});

export const refreshAccessTokenApiAuthRefreshGet500Response = zod.object({
    reason: zod.string(),
    message: zod.string(),
});

/**
 * @summary Logout user
 */
export const logoutUserApiAuthLogoutGet401Response = zod.object({
    reason: zod.string(),
    message: zod.string(),
});

export const logoutUserApiAuthLogoutGet500Response = zod.object({
    reason: zod.string(),
    message: zod.string(),
});

/**
 * @summary Get current user
 */
export const getLoggedInUserProfileApiAuthMeGet200ResponseUserUsernameMin = 3;

export const getLoggedInUserProfileApiAuthMeGet200ResponseUserUsernameMax = 255;

export const getLoggedInUserProfileApiAuthMeGet200Response = zod.object({
    user: zod.object({
        userId: zod.string(),
        username: zod
            .string()
            .min(getLoggedInUserProfileApiAuthMeGet200ResponseUserUsernameMin)
            .max(getLoggedInUserProfileApiAuthMeGet200ResponseUserUsernameMax),
        email: zod.string().email(),
        profilePicURL: zod.string().url().min(1),
    }),
});

export const getLoggedInUserProfileApiAuthMeGet401Response = zod.object({
    reason: zod.string(),
    message: zod.string(),
});

export const getLoggedInUserProfileApiAuthMeGet500Response = zod.object({
    reason: zod.string(),
    message: zod.string(),
});
