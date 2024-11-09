export default async function CompleteMagicLinkLoginPage(props: {
    params: Promise<{ magicLinkToken: string }>;
}): Promise<void> {
    const token = (await props.params).magicLinkToken;

    await fetch(`/login/${token}`);
}
