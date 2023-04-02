<script setup lang="ts">
import FrameItem from "./FrameItem.vue";
import type { Ref } from "vue";
import { ref } from "vue";
import type { IFrame } from "@/FrameDef";
const FrameList: Ref<IFrame[]> = ref([]);
const currBranch: Ref<IFrame[]> = ref([]);
function addFrame(idx: Number): boolean {
    return false;
}

function removeFrame(idx: Number): boolean {
    return false;
}

function switchBranch(id: FrameID): boolean {
    return false;
}
</script>

<template>
    <div>
        <FrameItem v-for="item in FrameList" :key="item.id">{{ item }}</FrameItem>
    </div>
</template>
