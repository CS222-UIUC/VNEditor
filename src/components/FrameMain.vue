<script setup lang="ts">
import ChapterItem from "./ChapterDir.vue";
import type { Ref } from "vue";
import { ref, watchEffect, inject, type PropType } from "vue";
import { projectIDKey } from "../InjectionKeys";

import { getChapters, addChapters } from "../RequestAPI";

var ChapetrsDisplay = ref(false); // control display the scene of the corresopnding chapter, used once current project deleted
const ChapterList = ref<string[]>([]);
var chapNametoAdd = "";

const prop = defineProps({
    itemCallBack: {
        type: Function as PropType<(event: MouseEvent) => void>,
        default: () => console.log("CallBack undefined"),
    },
});

const projectID = inject(projectIDKey) as Ref<string | undefined>;
watchEffect(() => {
    // call back method update the chapter to display once projectID received
    ChapetrsDisplay.value = false;
    if (projectID.value)
        getChapters(projectID.value).then((res: string[]) => {
            if (res) ChapterList.value = res;
            ChapetrsDisplay.value = true;
        });
    chapNametoAdd;
});
</script>

<template>
    <div>
        <input
            class="chapter-button"
            v-model="chapNametoAdd"
            v-show="ChapetrsDisplay"
            placeholder="enter chapter name"
        />
        {{ chapNametoAdd }}
        <button
            class="chapter-button"
            v-show="ChapetrsDisplay"
            @click="addChapters(projectID, chapNametoAdd)"
        >
            New Chapter
        </button>
        <ChapterItem
            v-show="ChapetrsDisplay"
            v-for="item in ChapterList"
            :key="item"
            :name="item"
            :item-call-back="prop.itemCallBack"
            chapter-name="asdasds"
            >{{ item }}
        </ChapterItem>
    </div>

</template>

<style>
.chapter-button {
    display: flex;
    flex-direction: column;
    padding: 0.5rem;
    border-bottom: 5px solid rgba(0, 90, 27, 0.507);
    width: 100%;
}
</style>

