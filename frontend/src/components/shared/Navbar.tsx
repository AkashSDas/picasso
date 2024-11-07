import { MenuIcon } from "lucide-react";
import Link from "next/link";

import { cn } from "@/utils/styles";

import { Button } from "./Button";

// TODO: temp variable (later on get it from backend)
const isLoggedIn = false;

export function Navbar(): React.JSX.Element {
    return (
        <nav className="h-14 px-4 md:px-16 flex items-center justify-between bg-neutral-100/[0.02]">
            <span className="font-head text-xl">Picasso</span>

            <Button variant="default" size="icon" className="flex md:hidden">
                <MenuIcon />
            </Button>

            <div
                className={cn(
                    "hidden md:flex items-center gap-2",
                    isLoggedIn ? "hidden" : "",
                )}
            >
                <Link href="/login">
                    <Button variant="ghost">Login</Button>
                </Link>

                <Link href="/signup">
                    <Button variant="brand">signup</Button>
                </Link>
            </div>
        </nav>
    );
}
