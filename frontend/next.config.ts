import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  basePath: process.env.GITHUB_ACTIONS === "true" ? "/staymate-ai" : "",
  images: {
    unoptimized: true,
  },
};

export default nextConfig;