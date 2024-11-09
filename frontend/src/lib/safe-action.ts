import { createSafeActionClient } from "next-safe-action";

import { DEFAULT_ERR_MSG, status } from "@/utils/http";

export const actionClient = createSafeActionClient({
    defaultValidationErrorsShape: "flattened",
    handleServerError(e) {
        console.error(`Unhandled server action error: ${e}`);

        return {
            error: { message: DEFAULT_ERR_MSG },
            status: status.INTERNAL_SERVER_ERROR,
        };
    },
});
