import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import Page from "../../app/page";
import { describe, expect, it } from "@jest/globals";

describe("Page", () => {
    it("renders a heading", () => {
        render(<Page />);

        const heading = screen.getByRole("heading", { level: 1 });

        expect(heading).toBeInTheDocument();
    });
});
