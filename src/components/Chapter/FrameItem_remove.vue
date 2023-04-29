<script setup lang="ts">
import { removeFrame } from "../../RequestAPI";
import { projectIDKey } from "../../InjectionKeys";
import { watch, type Ref } from "vue";
import { inject, ref } from "vue";

const projectID = inject(projectIDKey) as Ref<string | undefined>;
var removed: Ref<boolean> = ref(false);

watch(removed, () => {
    console.log("removed" + prop.FrameName);
});

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

function remove_frame() {
    // console.log("next two line are chapname and frame name");
    // console.log(prop.ChapterName);
    // console.log(prop.FrameName);
    removed.value = true;
    if (projectID.value) {
        removeFrame(projectID.value, prop.FrameId).then((res: boolean) => {
            console.log("removed result");
            console.log(res);
        });
    }
}
</script>

<template>
    <div class="frame-item-remove" v-show="!removed.valueOf()" @click="remove_frame">
        <slot>unknown scene</slot>
    </div>
</template>

<style>
.frame-item-remove {
    text-align: center;
    color: black;
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
