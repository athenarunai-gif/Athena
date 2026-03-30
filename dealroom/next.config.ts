import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Allow larger file uploads (50MB)
  experimental: {
    serverActions: {
      bodySizeLimit: '52mb',
    },
  },
};

export default nextConfig;
