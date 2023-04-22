<script setup lang="ts">
import { reactive, ref, defineEmits, type PropType, onMounted } from "vue";
import { ElementType, type Character, type EditorElement } from "@/FrameDef";
let prevX: number = 0;
let prevY: number = 0;
const currX = ref(0);
const currY = ref(0);
const htmlElement = ref<HTMLElement | null>(null);
const editDisplay = ref(false);
let dragStart = false;
const props = defineProps({
    element: {
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

const emits = defineEmits<{
    (e: "updateElement", index: number, el: EditorElement): void;
}>();

const currElement = ref<EditorElement>();
const dialog_input = ref<HTMLElement | null>(null);

onMounted(() => {
    currElement.value = props.element;
    currX.value = props.element.xCoord;
    currY.value = props.element.yCoord;
});
function onDrag(event: MouseEvent): void {
    if (dragStart && htmlElement.value && htmlElement.value.parentElement) {
        currX.value =
            ((htmlElement.value.offsetLeft + (event.clientX - prevX)) /
                htmlElement.value.parentElement.clientWidth) *
            100;
        currY.value =
            ((htmlElement.value.offsetTop + (event.clientY - prevY)) /
                htmlElement.value.parentElement.clientHeight) *
            100;
        prevY = event.clientY;
        prevX = event.clientX;
    }
}
</script>

<template>
    <div
        class="editor-element"
        ref="htmlElement"
        style="position: absolute; z-index: 0"
        :style="{ top: currY + '%', left: currX + '%' }"
        @mousedown.prevent="
            dragStart = true;
            (prevX = $event.clientX), (prevY = $event.clientY);
        "
        @mousemove.prevent="
            onDrag($event);
            dialog_input?.focus();
        "
        @mouseup.prevent="dragStart = false"
        @mouseleave.prevent="dragStart = false"
    >
        <img
            :src="currElement?.content"
            alt="image"
            v-if="currElement?.type == ElementType.Image"
        />
        <div
            class="editor-element-dialog"
            v-if="currElement?.type == ElementType.Text"
            style="display: flex; align-items: center; justify-content: center"
            @dblclick="
                editDisplay = !editDisplay;
                $emit('updateElement', index, currElement);
            "
        >
            <span v-show="!editDisplay"> {{ currElement.content }}</span>
            <input
                ref="dialog_input"
                v-show="editDisplay"
                type="text"
                v-model="currElement.content"
                style="width: 100%; height: 100%"
            />
        </div>
    </div>
</template>

<style>
.editor-element:hover {
    z-index: 0;
    outline: 2px #000 dashed;
}
.editor-element-dialog {
    height: 10rem;
    width: 80rem;
    font-size: x-large;
    background-color: burlywood;
    border: solid;
    border-radius: 1rem;
}
</style>
