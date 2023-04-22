<script setup lang="ts">
import { reactive, ref, type PropType } from "vue";
import type { Character, EditorElement } from "@/FrameDef";
const prevX = ref(0);
const prevY = ref(0);
const currX = ref(0);
const currY = ref(0);
const element = ref<HTMLElement | null>(null);
let dragStart = false;
const props = defineProps({
    char: {
        type: Object as PropType<EditorElement>,
        required: true,
    },
    updateCallBack: {
        type: Function as PropType<(el: EditorElement, idx: number) => void>,
        required: true,
    },
    index: {
        type: Number,
        required: true,
    },
});
function onDrag(event: MouseEvent): void {
    if (dragStart && element.value && element.value.parentElement) {
        currX.value =
            ((element.value.offsetLeft + (event.clientX - prevX.value)) /
                element.value.parentElement.clientWidth) *
            100;
        currY.value =
            ((element.value.offsetTop + (event.clientY - prevY.value)) /
                element.value.parentElement.clientHeight) *
            100;
        prevY.value = event.clientY;
        prevX.value = event.clientX;
    }
}
</script>

<template>
    <div
        class="editor-element"
        ref="element"
        style="position: absolute; z-index: 0"
        :style="{ top: currY + '%', left: currX + '%' }"
        @mousedown.prevent="
            dragStart = true;
            (prevX = $event.clientX), (prevY = $event.clientY);
        "
        @mousemove.prevent="onDrag"
        @mouseup.prevent="dragStart = false"
        @mouseleave.prevent="dragStart = false"
    >
        <img :src="char.imageUrl" alt="image" />
    </div>
</template>

<style>
.editor-element:hover {
    z-index: 0;
    outline: 2px #000 dashed;
}
</style>
