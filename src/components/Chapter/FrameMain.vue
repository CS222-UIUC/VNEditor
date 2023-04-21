<script setup lang="ts">
import ChapterItem from "./ChapterDir.vue";
import type { Ref } from "vue";
import { ref, watchEffect, inject, type PropType } from "vue";
import { projectIDKey } from "../../InjectionKeys";

import { getChapters, addChapters } from "../../RequestAPI";

var ChapetrsDisplay = ref(false); // control display the scene of the corresopnding chapter, used once current project deleted
var AddNewChapterDisplay = ref(false);
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
            AddNewChapterDisplay.value = true;
        });
    chapNametoAdd;
});
</script>

<template>
    <div>
        <div v-show="ChapetrsDisplay">
            <button
                style="
                    display: inline;
                    flex-direction: row;
                    /* padding: 0.5rem; */
                    border-bottom: 5px solid rgba(0, 90, 27, 0.507);
                    width: 100%;
                    height: 100%;
                    vertical-align: top;
                "
                v-show="AddNewChapterDisplay"
                @click="AddNewChapterDisplay = !AddNewChapterDisplay"
            >
                New Chapter
            </button>
            <input
                class="leftnav-text"
                v-model="chapNametoAdd"
                v-show="!AddNewChapterDisplay"
                placeholder="enter chapter name"
            />
            <button
                class="leftnav-text"
                v-show="!AddNewChapterDisplay"
                style="width: 25%"
                @click="
                    async () => {
                        await addChapters(projectID, chapNametoAdd);
                        getChapters(projectID).then((res: string[]) => {
                            if (res) {
                                ChapterList = res;
                                AddNewChapterDisplay = !AddNewChapterDisplay;
                                ChapetrsDisplay = true;
                            }
                        });
                    }
                "
            >
                Done
            </button>
            <button
                class="leftnav-text"
                v-show="!AddNewChapterDisplay"
                style="width: 25%"
                @click="AddNewChapterDisplay = true"
            >
                Cancel
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
    width: 50%;
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
