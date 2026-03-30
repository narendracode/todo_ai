import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  webpack(config, { isServer }) {
    // @event-calendar packages are pre-compiled Svelte components.
    // Strip the "svelte" export condition so webpack resolves the compiled
    // "default" entry (index.js) instead of raw .svelte.js sources.
    config.resolve.conditionNames = config.resolve.conditionNames?.filter(
      (c: string) => c !== "svelte"
    ) ?? ["import", "module", "default"];

    // On the client side, ensure svelte resolves its "browser" runtime
    // (not the SSR build) so SvelteComponent properly initialises $$.
    if (!isServer) {
      config.resolve.conditionNames = [
        "browser",
        ...config.resolve.conditionNames.filter((c: string) => c !== "browser"),
      ];
    }

    return config;
  },
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "lh3.googleusercontent.com",
      },
    ],
  },
};

export default nextConfig;
