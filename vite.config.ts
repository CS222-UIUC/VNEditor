import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueJsx from "@vitejs/plugin-vue-jsx";
import volarJS from "@volar-plugins/vetur";
// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue(), vueJsx(), volarJS()],
    resolve: {
        alias: {
            "@": fileURLToPath(new URL("./src", import.meta.url)),
        },
    },
});
