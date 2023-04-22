<script setup lang="ts">
import { removeChapters } from "../../RequestAPI";
import { projectIDKey } from "../../InjectionKeys";
import type { Ref } from "vue";
import { inject, ref } from "vue";

const removed: Ref<boolean> = ref(false);
const prop = defineProps({
    chapNameFromLib: {
        type: String,
        required: true,
    },
});
const projectID = inject(projectIDKey) as Ref<string | undefined>;

function removechapter() {
    if (projectID.value) {
        removeChapters(projectID.value, prop.chapNameFromLib).then((res: boolean) => {
            removed.value = res;
        });
    }
}
</script>

<template>
    <div class="chapter-item-remove">
        <div v-show="!removed" class="chapter-name" @click="removechapter">
            <!-- <slot dir-icon="dir-icon"></slot> -->
            <slot>No chapter exist</slot>
        </div>
    </div>
</template>
<style>
.chapter-item-remove {
    display: flex;
    color: black;
    flex-direction: column;
    padding: 0.5rem;
    border-bottom: 5px solid rgba(0, 90, 27, 0.507);
    width: 100%;
}
.chapter-name {
    overflow: hidden;
    text-align: left;
    display: flex;
    flex-direction: row;
    font-size: x-large;
}
.chapter-name:hover {
    text-align: left;
    text-decoration: line-through;
    text-decoration-thickness: 5px;
    background: rgb(45, 102, 34);
}
</style>
