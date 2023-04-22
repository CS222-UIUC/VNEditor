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
</script>

<template>
    <div ref="editor">
        <Draggable
            @update-element="updateFrame"
            v-for="(char, index) in elements"
            :key="index"
            :element="char"
            :update-call-back="(newElement: EditorElement, idx: number): void=> {
                elements[idx] = newElement;
            }"
            :index="index"
        ></Draggable>
    </div>
</template>

<style>
#main-editor {
    background-image: url(https://images.pexels.com/photos/255379/pexels-photo-255379.jpeg);
    background-position: center;
    background-repeat: no-repeat;
    z-index: 1;
}
</style>
