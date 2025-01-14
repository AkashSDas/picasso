import { FadingHero } from "@/components/hero/FadingHero";
import { HowItWorksExample } from "@/components/hero/HowItWorksExample";

export default function HomePage(): React.JSX.Element {
    return (
        <main>
            <FadingHero />
            <HowItWorksExample />
        </main>
    );
}
