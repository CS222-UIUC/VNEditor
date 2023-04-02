<script setup lang="ts">
import ChapterItem from "./ChapterDir.vue";
import type { Ref } from "vue";
import { ref, watchEffect, inject, type PropType } from "vue";
import { projectIDKey } from "../InjectionKeys";

import { getChapters } from "../RequestAPI";

var ChapetrsDisplay = ref(false); // control display the scene of the corresopnding chapter, used once current project deleted
const ChapterList = ref<string[]>([]);

const prop = defineProps({
    itemCallBack: {
        type: Function as PropType<(event: MouseEvent) => void>,
        default: () => console.log("CallBack undefined"),
    },
});

const projectID = inject(projectIDKey) as Ref<string | undefined>;
watchEffect(() => {
    // call back method update the chapter to display once projectID received
    if (projectID.value)
        getChapters(projectID.value).then((res: string[]) => {
            if (res) ChapterList.value = res;
        });
});
</script>

<template>
    <div>
        <ChapterItem
            v-for="item in ChapterList"
            :key="item"
            :name="item"
            :item-call-back="prop.itemCallBack"
            :chaptername="item"
            >{{ item }}
        </ChapterItem>
    </div>
</template>
