<script setup lang="ts">
import { ref, provide } from "vue";

import Toolbar from "./components/ToolbarMain.vue";
import Navbar from "./components/NavbarMain.vue";
import FileUploadArea from "./components/UploadArea.vue";

var fileUploadAreaDisplay = ref(false);

provide("host_name", "http://127.0.0.1:8000/");
</script>

<template>
    <Navbar> </Navbar>
    <main
        id="main-editor"
        class="grid-item"
        @clcik="fileUploadAreaDisplay = true"
        @dragenter="fileUploadAreaDisplay = true"
        @dragexit="fileUploadAreaDisplay = false"
    >
        <FileUploadArea :display="fileUploadAreaDisplay" />
    </main>
    <div id="preview-sidebar" class="grid-item">this is sidebar 1 {{ fileUploadAreaDisplay }}</div>
    <div id="toolbar-sidebar" class="grid-item">
        <Toolbar />
    </div>
    <footer id="footer" class="grid-item">this is footer</footer>
</template>

<style>
.grid-item {
    text-align: center;
}

#main-editor {
    background: azure;
    display: flex;
    flex-direction: column;
}

#preview-sidebar {
    background-color: cadetblue;
}

#toolbar-sidebar {
    background-color: #efffdb;
    display: flex;
    flex-direction: column;
}

#header {
    background-color: rgb(80, 140, 231);
    color: white;
}

#footer {
    background-color: brown;
}
</style>
