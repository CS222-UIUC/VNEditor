<script setup lang="ts">
import { removeFrame } from "../../RequestAPI";
import { projectIDKey } from "../../InjectionKeys";
import type { Ref } from "vue";
import { inject, ref } from "vue";

const projectID = inject(projectIDKey) as Ref<string | undefined>;
const removed: Ref<boolean> = ref(false);

const prop = defineProps({
    ChapterName: {
        type: String,
        required: true,
    },
    FrameName: {
        type: String,
        required: true,
    },
});

function remove_frame() {
    // console.log("next two line are chapname and frame name");
    // console.log(prop.ChapterName);
    // console.log(prop.FrameName);
    if (projectID.value) {
        removeFrame(projectID.value, prop.ChapterName, prop.FrameName).then((res: boolean) => {
            removed.value = res;
        });
    }
}
</script>

<template>
    <div class="frame-item-remove" v-show="!removed" @click="remove_frame">
        <slot>unknown scene</slot>
    </div>
</template>

<style>
.frame-item-remove {
    text-align: center;
    width: 100%;
}
.frame-item-remove:hover {
    text-align: center;
    width: 100%;
    text-decoration: line-through;
    text-decoration-thickness: 5px;
    background: rgb(70, 156, 53);
}
</style>
