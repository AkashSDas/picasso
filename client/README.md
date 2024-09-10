# Picasso Frontend

## Testing

To avoid the following error:

```bash
> jest "--watchAll=false"

 PASS  src/__tests__/pages/page.spec.tsx
 FAIL  src/__tests__/e2e/example.spec.ts
  ● Test suite failed to run

    Playwright Test needs to be invoked via 'pnpm exec playwright test' and excluded from Jest test runs.
    Creating one directory for Playwright tests and one for Jest is the recommended way of doing it.
```

Jest test files are named as `<thing>.test.ts` and Playwright files are named as `<thing>.spec.ts`.
