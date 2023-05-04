<script setup lang="ts">
import {
    inject,
    onMounted,
    provide,
    reactive,
    ref,
    watchEffect,
    type Ref,
    getCurrentInstance,
} from "vue";
import Draggable from "./DraggableItem.vue";
import { Character, type FrameBack, Frame } from "@/FrameDef";
import type { EditorElement } from "@/FrameDef";
import { editorElementsKey, frameIDKey, projectIDKey, editorBackgroundKey } from "@/InjectionKeys";
import { getFrame } from "@/RequestAPI";
import { Diaglog } from "@/FrameDef";

const frameID = inject(frameIDKey) as Ref<number | undefined>;
const projectID = inject(projectIDKey) as Ref<string | undefined>;
let editorElements: Array<EditorElement> = inject(editorElementsKey) as Array<EditorElement>;
const editorBackground = inject(editorBackgroundKey) as Ref<string | undefined>;
const editor = ref<HTMLInputElement | null>(null);
const selected = ref(-1);
let frame: Frame = new Frame();
function updateFrame(index: number, el: EditorElement) {
    console.log(editorElements);
    editorElements[index] = el;
    console.log(editorElements[index].content);
}

const props = defineProps({
    scale: {
        type: Number,
        required: true,
    },
});

const test = () => {
    console.log(selected.value);
    selected.value = -1;
};

const instance = getCurrentInstance();
watchEffect(async () => {
    if (frameID.value !== undefined && projectID.value !== undefined) {
        console.log("updating frame...");
        const fb = await getFrame(frameID.value, projectID.value);
        editorBackground.value = fb.background;
        while (editorElements.length != 0) editorElements.pop();
        console.log("clear frame: ", editorElements);
        for (const name in fb.character) {
            let newImage = new Image();
            newImage.onload = () => {
                let char: Character = new Character();
                char.content = name;
                char.h = fb.character[name].height;
                char.w = fb.character[name].width;
                char.xCoord = fb.character[name].x;
                char.yCoord = fb.character[name].y;
                editorElements.push(char);
            };
            newImage.src = name;
        }
        if (fb.dialog === "") return;
        const d = new Diaglog();
        d.content = fb.dialog;
        d.h = fb.background_attr.height;
        d.w = fb.background_attr.width;
        d.xCoord = fb.background_attr.x;
        d.yCoord = fb.background_attr.y;
        editorElements.push(d);
        console.log(editorElements);
        instance?.proxy?.$forceUpdate();
    }
});
</script>

<template>
    <div
        id="editor-view"
        ref="editor"
        :style="{ width: props.scale * 1920 + 'px', height: props.scale * 1080 + 'px' }"
        @click="test"
    >
        <Draggable
            @update-element="updateFrame"
            @contextmenu.prevent="editorElements.splice(index, 1)"
            @dblclick.stop="selected = index"
            v-for="(char, index) in editorElements"
            :key="char.content"
            :element="char"
            :update-call-back="(newElement: EditorElement, idx: number): void=> {
                editorElements[idx] = newElement;
            }"
            :scale="props.scale"
            :selected="selected == index"
            :index="index"
        ></Draggable>
    </div>
</template>

<style>
#editor-view {
    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;
    z-index: 1;
    position: absolute;
    background-color: white;
}
</style>
