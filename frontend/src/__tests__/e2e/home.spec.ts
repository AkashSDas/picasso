import { expect, test } from "@playwright/test";

test("should navigate to home page", async ({ page }) => {
    await page.goto("http://localhost:3000/");
    await expect(page).toHaveTitle("Picasso");
});
