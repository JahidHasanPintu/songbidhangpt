import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        green: { DEFAULT: "#006A4E", light: "#008B66", dark: "#004D38" },
        red: { DEFAULT: "#F42A41", light: "#FF4D61", dark: "#C4001F" },
        gold: { DEFAULT: "#D4AF37", light: "#E8C84A", dark: "#A88A1C" },
        bg: { DEFAULT: "#0F1117", secondary: "#1A1D27" },
        surface: { DEFAULT: "#1A1D27", raised: "#22263A" },
        border: { DEFAULT: "#2A2D3A", light: "#3A3D4A" },
        muted: { DEFAULT: "#8B8FA8", faint: "#5A5E72" },
      },
      fontFamily: {
        sans: ["Hind Siliguri", "sans-serif"],
        bangla: ["Noto Serif Bengali", "serif"],
      },
      animation: {
        "fade-in": "fadeIn 0.3s ease-in-out",
        "slide-up": "slideUp 0.3s ease-out",
      },
      keyframes: {
        fadeIn: { "0%": { opacity: "0" }, "100%": { opacity: "1" } },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      boxShadow: {
        glow: "0 0 20px rgba(0, 106, 78, 0.3)",
        card: "0 4px 24px rgba(0, 0, 0, 0.4)",
      },
      maxWidth: { chat: "48rem" },
    },
  },
  plugins: [],
};

export default config;