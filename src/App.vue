<script setup lang="ts">
import { ref, provide, inject, reactive, onMounted, watchEffect, watch } from "vue";
import { getFrame, getUrl } from "./RequestAPI";
import Toolbar from "./components/Toolbar/ToolbarMain.vue";
import Navbar from "./components/Navbar/NavbarMain.vue";
import FileUploadArea from "./components/UploadArea.vue";
import Framebar from "./components/Chapter/FrameMain.vue";
import {
    editorElementsKey,
    hostNameKey,
    projectIDKey,
    projectNameKey,
    frameIDKey,
    editorBackgroundKey,
    frameNameKey,
} from "@/InjectionKeys";
import EditorMain from "./components/EditorMain.vue";
import { Character, Diaglog, Frame } from "@/FrameDef";
import type { EditorElement } from "@/FrameDef";
const fileUploadAreaDisplay = ref(false);
// tool bar display below
const editorBackground = ref("");
const editorMusic = ref("");
// edn
// preview bra const below
// end
const frameID = ref<number | undefined>(undefined);
const frameName = ref<string | undefined>(undefined);
const projectID = ref<string | undefined>(undefined);
const projectName = ref<string | undefined>(undefined);
let editorElements: EditorElement[] = reactive([]);
const editorScale = ref(1);
provide(hostNameKey, "http://127.0.0.1:8000/");
provide(projectIDKey, projectID);
provide(projectNameKey, projectName);
provide(editorElementsKey, editorElements);
provide(frameIDKey, frameID);
provide(frameNameKey, frameName);
provide(editorBackgroundKey, editorBackground);
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
    console.log(el);
    if (projectID.value) {
        let newImage = new Image();
        const url = getUrl(`resources/character/${el.innerHTML}`, {
            task_id: projectID.value,
        });
        newImage.onload = () => {
            let char: Character = new Character();
            char.content = url;
            char.h = newImage.height;
            char.w = newImage.width;
            editorElements.push(char);
            console.log(editorElements.length);
            console.log(editorElements);
        };
        newImage.src = url;
    }
}

watch(projectID, () => {
    while (editorElements.length != 0) {
        editorElements.pop();
    }
});
// watchEffect(() => {
//     if (projectID.value)
//         while (editorElements.length != 0) {
//             editorElements.pop();
//         }
// });

// function test(event) {
//     console.log("aaaa");
// }

onMounted(() => {
    document.getElementById("app")?.addEventListener("wheel", (event: Event) => {
        const e: WheelEvent = event as WheelEvent;
        if (e.ctrlKey) {
            e.preventDefault();
            editorScale.value += e.deltaY * -0.001;
            console.log(editorScale.value);
        }
    });
});

let forceUpdate = 1;
</script>

<template>
    <Navbar id="header"> </Navbar>
    <div id="main-editor">
        <EditorMain
            class="edit-area"
            @clcik="fileUploadAreaDisplay = true"
            @dragenter="fileUploadAreaDisplay = true"
            @dragexit="fileUploadAreaDisplay = false"
            :scale="editorScale"
            :style="{
                'background-image': 'url(' + editorBackground + ')',
            }"
            :key="forceUpdate"
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

#main-editor {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: gray;
    overflow: auto;
    scrollbar-gutter: stable both-edges;
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
