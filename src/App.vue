<script setup lang="ts">
import { ref, provide, inject, reactive } from "vue";
import { getUrl } from "./RequestAPI";
import Toolbar from "./components/Toolbar/ToolbarMain.vue";
import Navbar from "./components/Navbar/NavbarMain.vue";
import FileUploadArea from "./components/UploadArea.vue";
import Framebar from "./components/Chapter/FrameMain.vue";
import { editorElementsKey, hostNameKey, projectIDKey, projectNameKey } from "./InjectionKeys";
import EditorMain from "./components/EditorMain.vue";
import { Character } from "./FrameDef";
import type { EditorElement } from "./FrameDef";
const fileUploadAreaDisplay = ref(false);
// tool bar display below
const editorBackground = ref("https://images.pexels.com/photos/255379/pexels-photo-255379.jpeg");
const editorMusic = ref("");
// edn
// preview bra const below
// end
const projectID = ref<string | undefined>(undefined);
const projectName = ref<string | undefined>(undefined);
const editorElements: EditorElement[] = reactive([]);
provide(hostNameKey, "http://127.0.0.1:8000/");
provide(projectIDKey, projectID);
provide(projectNameKey, projectName);
provide(editorElementsKey, editorElements);
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
function addNewCharacter(event: MouseEvent) {
    const el: Element = event.target as Element;
    if (projectID.value) {
        let char: Character = new Character();
        char.imageUrl = getUrl(`resources/character/${el.innerHTML}`, {
            task_id: projectID.value,
        });

        editorElements.push(char);
        console.log(editorElements);
    }
}
</script>

<template>
    <Navbar id="header"> </Navbar>
    <div id="main-editor">
        <EditorMain
            class="edit-area"
            @clcik="fileUploadAreaDisplay = true"
            @dragenter="fileUploadAreaDisplay = true"
            @dragexit="fileUploadAreaDisplay = false"
            :style="{ 'background-image': 'url(' + editorBackground + ')' }"
        >
            <FileUploadArea :display="fileUploadAreaDisplay" />
        </EditorMain>
    </div>
    <Framebar id="preview-sidebar" class="grid-item"> </Framebar>
    <Toolbar
        id="toolbar-sidebar"
        class="grid-item"
        :background-call-back="setEditorBackground"
        :music-call-back="setEditorMusic"
        :character-call-back="addNewCharacter"
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

.edit-area {
    text-align: center;
    aspect-ratio: 16 / 9;
    width: 150vh;
    overflow: scroll;
}

#main-editor {
    display: flex;
    flex-direction: column;
}

#preview-sidebar {
    background-color: cadetblue;
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: scroll;
}

#toolbar-sidebar {
    background-color: #efffdb;
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
}

#header {
    background-color: rgb(80, 140, 231);
    color: white;
}

#footer {
    background-color: brown;
}
</style>
