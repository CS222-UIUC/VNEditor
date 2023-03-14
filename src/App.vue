<script setup lang="ts">
import { ref, provide } from "vue";
import { getUrl } from "./RequestAPI";
import { initProject } from "./RequestAPI";
import Toolbar from "./components/ToolbarMain.vue";
import Navbar from "./components/NavbarMain.vue";
import FileUploadArea from "./components/UploadArea.vue";
import { hostNameKey, projectIDKey } from "./InjectionKeys";
import EditorMain from "./components/EditorMain.vue";

const fileUploadAreaDisplay = ref(false);
const editorBackground = ref("https://images.pexels.com/photos/255379/pexels-photo-255379.jpeg");
const editorMusic = ref("");
const projectID = ref<string | undefined>(undefined);

provide(hostNameKey, "http://127.0.0.1:8000/");
provide(projectIDKey, projectID);

initProject("test").then((res: string | undefined) => {
    if (res) {
        projectID.value = res;
    } else {
        console.log("project init failed");
    }
});

function setEditorBackground(event: MouseEvent) {
    const el: Element = event.target as Element;
    if (projectID.value)
        editorBackground.value = getUrl(`resources/background/${el.innerHTML}`, {
            task_id: projectID.value,
        });
}

function setEditorMusic(event: MouseEvent) {
    const el: Element = event.target as Element;
    if (projectID.value)
        editorMusic.value = getUrl(`resources/music/${el.innerHTML}`, {
            task_id: projectID.value,
        });
}
</script>

<template>
    <Navbar id="header"> </Navbar>
    <EditorMain
        id="main-editor"
        class="grid-item"
        @clcik="fileUploadAreaDisplay = true"
        @dragenter="fileUploadAreaDisplay = true"
        @dragexit="fileUploadAreaDisplay = false"
        :style="{ 'background-image': 'url(' + editorBackground + ')' }"
    >
        <FileUploadArea :display="fileUploadAreaDisplay" />
    </EditorMain>
    <div id="preview-sidebar" class="grid-item">this is sidebar 1 {{ fileUploadAreaDisplay }}</div>
    <Toolbar
        id="toolbar-sidebar"
        class="grid-item"
        :background-call-back="setEditorBackground"
        :music-call-back="setEditorMusic"
    />
    <footer id="footer" class="grid-item">this is footer</footer>
    <audio :src="editorMusic" autoplay loop>
        <p>
            If you are reading this, it is because your browser does not support the audio element.
        </p>
    </audio>
</template>

<style>
.grid-item {
    text-align: center;
}

#main-editor {
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
