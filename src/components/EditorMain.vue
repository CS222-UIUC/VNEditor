<script setup lang="ts">
import { inject, onMounted, provide, reactive, ref } from "vue";
import Draggable from "./DraggableItem.vue";
import { Character } from "@/FrameDef";
import type { EditorElement } from "@/FrameDef";
import { editorElementsKey } from "@/InjectionKeys";
let elements: Array<EditorElement> = inject(editorElementsKey) as Array<EditorElement>;
const topCoord = ref(0);
const leftCoord = ref(0);
const viewWidth = ref(0);
const viewHeight = ref(0);

const editor = ref<HTMLInputElement | null>(null);
onMounted(() => {
    const rect = editor.value?.getBoundingClientRect();
    topCoord.value = rect?.top as number;
    leftCoord.value = rect?.left as number;
    viewWidth.value = rect?.width as number;
    viewHeight.value = rect?.height as number;
});
</script>

<template>
    <div ref="editor">
        <Draggable
            v-for="(char, index) in elements"
            :key="index"
            :char="char"
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
