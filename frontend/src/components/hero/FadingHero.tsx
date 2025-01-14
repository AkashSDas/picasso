"use client";

import { Wand2 } from "lucide-react";
import Image from "next/image";

import { Button } from "../shared/Button";

const slides: { imgURL: string; gradientStart: string }[] = [
    {
        imgURL: "/images/slide1.png",
        gradientStart: "#612315",
    },
];

export function FadingHero() {
    return (
        <section className="relative">
            {/* Header Gradient with Fade-in Animation */}
            <div className="fixed -z-10 top-[-100px] w-[1833px] h-[568px] bg-gradient-to-b from-[#612315]/40 to-transparent animate-fadeIn" />

            <div className="rounded-xl h-[360px] lg:h-[583px] shadow-2xl relative mx-4 md:mx-16 overflow-hidden mt-8 border-[1.5px] border-neutral-50/10 animate-slideIn">
                <div className="flex z-20 flex-col absolute bottom-10 left-10 gap-8">
                    <h2 className="text-3xl md:text-[80px] font-head text-white">
                        Picasso
                    </h2>

                    <p className="text-white/90 font-medium max-w-[554px]">
                        Experience the magic of Neural Style Transfer with Picasso. Turn
                        your everyday photos and videos into stunning works of art
                        inspired by famous styles and unique designs.
                    </p>

                    <Button
                        size="lg"
                        variant="brand"
                        className="h-14 rounded-md w-fit px-28"
                    >
                        <Wand2 />
                        Try Now
                    </Button>
                </div>

                <div className="absolute top-0 h-full z-10 w-full bg-gradient-to-r from-neutral-950/90 to-transparent" />

                {/* Image Fade-in Animation */}
                <Image
                    src={slides[0].imgURL}
                    layout="fill"
                    priority
                    alt="slide"
                    className="object-cover animate-fadeIn"
                />
            </div>
        </section>
    );
}
