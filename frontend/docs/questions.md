# Questions

## Metadata and Static Files location in Nextjs App Router: Right way /app or /public?

`public` dir is optional and therefore docs suggest to put favicon and other metadata inside `/app` dir. If using `/public` dir then those files can be put there along with other static assets. **NOTE** that `public` dir should be in the root of your project event if you're using `/src` dir.

- [Github Discussion](https://github.com/vercel/next.js/discussions/50593)
