import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    lib: {
      entry: {
        main: path.resolve(__dirname, 'src/main.ts'),
        preload: path.resolve(__dirname, 'src/preload.ts'),
      },
      name: '5edma',
      fileName: (format, entryName) => {
        if (entryName === 'main') return '[name].js'
        if (entryName === 'preload') return '[name].js'
        return `[name].${format}.js`
      },
      formats: ['es'],
    },
    rollupOptions: {
      external: ['electron'],
    },
  },
})
