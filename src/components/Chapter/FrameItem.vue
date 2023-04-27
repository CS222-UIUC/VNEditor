<script setup lang="ts">
/** __vue_virtual_code_placeholder */
// const ChapterName = "";
import { frameIdKey } from "@/InjectionKeys";
const prop = defineProps({
    ChapterName: {
        type: String,
        required: true,
    },
    FrameName: {
        type: String,
        required: true,
    },
    FrameId: {
        type: Number,
        required: true,
    },
});

function displayframe() {}
</script>

<template>
    <div class="frame-item" @dblclick="$emit('displayFrame')">
        <slot>unknown scene</slot>
    </div>
</template>

<style>
.frame-item {
    text-align: center;
    color: black;
    width: 100%;
}
.frame-item:hover {
    text-align: center;
    width: 100%;
    background: rgb(70, 156, 53);
}
</style>
