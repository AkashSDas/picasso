import { ArrowUpRightIcon, EqualIcon, PlusIcon } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

import { Button } from "../shared/Button";

export function HowItWorksExample() {
    return (
        <section className="my-24 flex flex-col justify-center gap-8 w-full animate-slideIn">
            <h2 className="text-3xl md:text-4xl font-head text-white text-center">
                How it works?
            </h2>

            <div className="flex items-center gap-4 mx-16 relative">
                <ExampleImage imgURL="/images/input-img1.png" label="Images/Video" />

                <div className="border z-20 border-neutral-600/40 font-head bg-neutral-700/90 backdrop:blur-md absolute bottom-1/2 right-1/3 translate-x-1/2 translate-y-1/2 px-4 h-9 flex justify-center items-center rounded-full">
                    <EqualIcon />
                </div>

                <ExampleImage imgURL="/images/filter-img1.png" label="Filter" />

                <div className="border z-20 border-neutral-600/40 font-head bg-neutral-700/90 backdrop:blur-md absolute bottom-1/2 left-1/3 -translate-x-1/2 translate-y-1/2 px-4 h-9 flex justify-center items-center rounded-full">
                    <PlusIcon />
                </div>

                <ExampleImage imgURL="/images/output-img1.png" label="Result" />
            </div>

            <Link
                target="_blank"
                className="w-fit mx-auto"
                href="https://www.tensorflow.org/tutorials/generative/style_transfer"
            >
                <Button>
                    Read More <ArrowUpRightIcon />
                </Button>
            </Link>
        </section>
    );
}

function ExampleImage(props: {
    imgURL: string;
    label: string;
    rightIcon?: React.ReactNode;
}) {
    return (
        <div className="relative flex flex-col justify-center min-h-60 w-full overflow-hidden rounded-xl">
            <div className="absolute inset-0 z-0 flex flex-col items-center justify-center">
                {[1, 2, 3].map((_idx, index) => (
                    <div
                        key={index}
                        className="relative min-h-48 w-full mb-4 last:mb-0"
                    >
                        <Image
                            src={props.imgURL}
                            layout="fill"
                            priority
                            alt={`Image`}
                            className="object-cover rounded-xl"
                        />
                    </div>
                ))}
            </div>

            <div className="absolute inset-0 z-10 bg-gradient-to-b from-neutral-900/60 via-transparent to-neutral-900/60 pointer-events-none" />

            <div className="border z-20 border-neutral-600/40 font-head bg-neutral-700/80 backdrop:blur-md absolute bottom-4 left-1/2 -translate-x-1/2 px-4 h-9 flex justify-center items-center rounded-full">
                {props.label}
            </div>
        </div>
    );
}
