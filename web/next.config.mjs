/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: "standalone", // slim runtime image for Docker
  images: { remotePatterns: [{ protocol: "https", hostname: "**" }] }, // Google avatars
};

export default nextConfig;
