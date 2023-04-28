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

const instance = getCurrentInstance();
watchEffect(async () => {
    console.log(frameID.value !== undefined);
    console.log("aaaaaaaaaaaaaaaaaaaa?");
    if (frameID.value !== undefined && projectID.value !== undefined) {
        console.log("updating frame...");
        const fb = await getFrame(frameID.value, projectID.value);
        editorBackground.value = fb.background;
        for (let i = 0; i < editorElements.length; ++i) editorElements.pop();
        for (let i = 0; i < fb.chara.length; ++i) {
            const c = new Character();
            c.content = fb.chara[i];
            c.xCoord = fb.chara_pos[i].x;
            c.yCoord = fb.chara_pos[i].y;
            editorElements.push(c);
        }
        const d = new Diaglog();
        d.content = fb.dialog;
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
    >
        <Draggable
            @update-element="updateFrame"
            v-for="(char, index) in editorElements"
            :key="char.content"
            :element="char"
            :update-call-back="(newElement: EditorElement, idx: number): void=> {
                editorElements[idx] = newElement;
            }"
            :scale="props.scale"
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
