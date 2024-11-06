import { fixupConfigRules, fixupPluginRules } from "@eslint/compat";
import { FlatCompat } from "@eslint/eslintrc";
import js from "@eslint/js";
import tanstackQuery from "@tanstack/eslint-plugin-query";
import typescriptEslint from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";
import prettier from "eslint-plugin-prettier";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";
import globals from "globals";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
    baseDirectory: __dirname,
    recommendedConfig: js.configs.recommended,
    allConfig: js.configs.all,
});

export default [
    {
        ignores: ["**/.next", "**/.eslintrc.json"],
    },
    ...fixupConfigRules(
        compat.extends(
            "next/core-web-vitals",
            "next/typescript",
            "eslint:recommended",
            "prettier",
            "plugin:react/recommended",
            "plugin:@typescript-eslint/recommended",
            "plugin:react-hooks/recommended",
            "plugin:@tanstack/eslint-plugin-query/recommended",
        ),
    ),
    {
        plugins: {
            "@typescript-eslint": fixupPluginRules(typescriptEslint),
            react: fixupPluginRules(react),
            prettier,
            "react-refresh": reactRefresh,
            "react-hooks": fixupPluginRules(reactHooks),
        },

        languageOptions: {
            globals: {
                ...globals.browser,
            },

            parser: tsParser,
        },

        rules: {
            "react-refresh/only-export-components": [
                "warn",
                {
                    allowConstantExport: true,
                },
            ],

            "@typescript-eslint/no-unused-vars": "off",
            "@tanstack/query/exhaustive-deps": "error",
            "@tanstack/query/no-deprecated-options": "off",
            "@tanstack/query/prefer-query-object-syntax": "off",
            "@tanstack/query/stable-query-client": "error",
            "react-hooks/rules-of-hooks": "error",
            "react-hooks/exhaustive-deps": "warn",
            "prettier/prettier": "warn",
            "react/react-in-jsx-scope": "off",

            "react/jsx-filename-extension": [
                1,
                {
                    extensions: [".ts", ".tsx"],
                },
            ],
        },
    },
];
