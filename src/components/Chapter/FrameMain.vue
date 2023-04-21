<script setup lang="ts">
import ChapterItem from "./ChapterDir.vue";
import type { Ref } from "vue";
import { ref, watchEffect, inject, type PropType } from "vue";
import { projectIDKey } from "../../InjectionKeys";

import { getChapters, addChapters } from "../../RequestAPI";

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
        <div>
            <input
                class="leftnav-text"
                v-model="chapNametoAdd"
                v-show="ChapetrsDisplay"
                placeholder="enter chapter name"
            />
            <button
                class="leftnav-text"
                v-show="ChapetrsDisplay"
                style="width: 30%"
                @click="
                    async () => {
                        await addChapters(projectID, chapNametoAdd);
                        getChapters(projectID).then((res: string[]) => {
                            if (res) ChapterList = res;
                            ChapetrsDisplay = true;
                        });
                    }
                "
            >
                New Chapter
            </button>
        </div>
        <ChapterItem
            v-show="ChapetrsDisplay"
            v-for="item in ChapterList"
            :key="item"
            :name="item"
            :item-call-back="prop.itemCallBack"
            :chapNameFromLib="item"
            >{{ item }}
        </ChapterItem>
    </div>
</template>

<style>
.leftnav-text {
    display: inline;
    flex-direction: row;
    /* padding: 0.5rem; */
    border-bottom: 5px solid rgba(0, 90, 27, 0.507);
    width: 70%;
    height: 100%;
    vertical-align: top;
}

.leftnav-button {
    display: inline;
    flex-direction: row;
    /* padding: 0.5rem; */
    border-bottom: 5px solid rgba(0, 90, 27, 0.507);
    width: 30%;
    height: 100%;
}
</style>
