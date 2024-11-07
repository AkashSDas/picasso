import { defineConfig } from "orval";

export default defineConfig({
    zod: {
        input: {
            target: "./swagger.json",
        },
        output: {
            mode: "tags-split",
            target: "./src/gen/endpoints",
            schemas: "./src/gen/schemas",
            // fileExtension: ".gen.ts", // TODO: issue with this is that the imports in each are file have extension .ts and not .gen.ts
            baseUrl: "http://localhost:8000",
            client: "zod",
            override: {
                zod: {
                    generateEachHttpStatus: true,
                } as unknown as any,
            },
        },
        hooks: {
            afterAllFilesWrite: [
                // "pnpm lint",
                "prettier --write './src/gen/**/*.{gen.ts,ts}'",
            ],
        },
    },
});
