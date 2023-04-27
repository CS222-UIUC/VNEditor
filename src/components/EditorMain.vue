<script setup lang="ts">
import { inject, onMounted, provide, reactive, ref } from "vue";
import Draggable from "./DraggableItem.vue";
import { Character } from "@/FrameDef";
import type { EditorElement } from "@/FrameDef";
import { editorElementsKey } from "@/InjectionKeys";

let elements: Array<EditorElement> = inject(editorElementsKey) as Array<EditorElement>;

const editor = ref<HTMLInputElement | null>(null);

function updateFrame(index: number, el: EditorElement) {
    console.log(elements);
    elements[index] = el;
    console.log(elements[index].content);
}

const props = defineProps({
    scale: {
        type: Number,
        required: true,
    },
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
            v-for="(char, index) in elements"
            :key="index"
            :element="char"
            :update-call-back="(newElement: EditorElement, idx: number): void=> {
                elements[idx] = newElement;
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
