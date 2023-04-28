<script setup lang="ts">
/** __vue_virtual_code_placeholder */
// const ChapterName = "";
import { frameIDKey, frameNameKey } from "@/InjectionKeys";
import { inject, type Ref } from "vue";
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

const frameID = inject(frameIDKey) as Ref<number>;
const frameName = inject(frameNameKey) as Ref<string | undefined>;
</script>

<template>
    <div
        class="frame-item"
        @dblclick="
            frameID = prop.FrameId;
            frameName = prop.FrameName;
        "
    >
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
