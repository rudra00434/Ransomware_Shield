/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                threat: {
                    critical: '#FF2D55',
                    high: '#FF6B35',
                    medium: '#FFD60A',
                    low: '#30D158',
                    clean: '#32ADE6',
                },
                dark: {
                    900: '#0A0E1A',
                    800: '#0F1629',
                    700: '#1A2238'
                }
            },
        },
    },
    plugins: [],
}
