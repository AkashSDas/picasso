import * as VisuallyHidden from "@radix-ui/react-visually-hidden";
import { MenuIcon } from "lucide-react";
import Link from "next/link";

import { getLoggedInUser } from "@/utils/auth";
import { cn } from "@/utils/styles";

import { Button } from "./Button";
import { LogoutButton } from "./LogoutButton";
import {
    Sheet,
    SheetClose,
    SheetContent,
    SheetFooter,
    SheetTitle,
    SheetTrigger,
} from "./Sheet";

export async function Navbar(): Promise<React.JSX.Element> {
    const { isLoggedIn } = await getLoggedInUser();

    return (
        <nav className="h-14 px-4 md:px-16 flex items-center justify-between bg-neutral-100/[0.02]">
            <Link href="/">
                <span className="font-head text-xl">Picasso</span>{" "}
            </Link>

            <Sheet>
                <SheetTrigger asChild>
                    <Button variant="default" size="icon" className="flex md:hidden">
                        <MenuIcon />
                    </Button>
                </SheetTrigger>

                <SheetContent>
                    <VisuallyHidden.Root>
                        <SheetTitle>Menu</SheetTitle>
                    </VisuallyHidden.Root>

                    <SheetFooter className="flex w-full flex-row gap-2">
                        <SheetClose asChild className={cn(isLoggedIn ? "hidden" : "")}>
                            <Link href="/login" className="w-full">
                                <Button variant="default" className="w-full">
                                    Login
                                </Button>
                            </Link>
                        </SheetClose>

                        <SheetClose asChild className={cn(isLoggedIn ? "hidden" : "")}>
                            <Link href="/signup" className="w-full">
                                <Button variant="brand" className="w-full">
                                    Signup
                                </Button>
                            </Link>
                        </SheetClose>

                        <SheetClose asChild className={cn(!isLoggedIn ? "hidden" : "")}>
                            <LogoutButton />
                        </SheetClose>
                    </SheetFooter>
                </SheetContent>
            </Sheet>

            <div className={cn("hidden md:flex items-center gap-2")}>
                <Link href="/login" className={cn(isLoggedIn ? "md:hidden" : "")}>
                    <Button variant="ghost">Login</Button>
                </Link>

                <Link href="/signup" className={cn(isLoggedIn ? "md:hidden" : "")}>
                    <Button variant="brand">Signup</Button>
                </Link>

                <span className={cn(!isLoggedIn ? "md:hidden" : "")}>
                    <LogoutButton />
                </span>
            </div>
        </nav>
    );
}
