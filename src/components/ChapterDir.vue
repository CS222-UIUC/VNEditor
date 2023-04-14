<script setup lang="ts">
import FrameItem from "./FrameItem.vue";
import { ref, inject, watchEffect, type PropType } from "vue";
import type { Ref } from "vue";
import IconDownArrow from "./icons/IconDownArrow.vue";
import type { IFrame } from "@/FrameDef";
import { projectIDKey } from "../InjectionKeys";
import { getFrames } from "../RequestAPI"; // need to change to needed function

var FramesDisplay = ref(false); // control display the scene of the corresopnding chapter
const FrameList: Ref<IFrame[]> = ref([]);
const chapName: Ref<string> = ref("");
// function addFrame(idx: Number): boolean {
//     return false;
// }

// function removeFrame(idx: Number): boolean {
//     return false;
// }

// function switchBranch(id: FrameID): boolean {
//     return false;
// }

const props = defineProps({
    ChapterName: {
        type: ref<String>,
    },
    itemCallBack: {
        type: Function as PropType<(event: MouseEvent) => void>,
        default: () => console.log("CallBack in frames undefined"),
    },
});
const projectID = inject(projectIDKey) as Ref<string | undefined>;

function updateChapName(event: MouseEvent) {
    const el = event.target as HTMLElement;
    const name = el.textContent;
    if (name) chapName.value = name;
    FramesDisplay.value = !FramesDisplay.value;
}

watchEffect(() => {
    // call back method update the chapter to display once projectID received
    if (projectID.value)
        getFrames(projectID.value, chapName.value).then((res: IFrame[]) => {
            if (res) FrameList.value = res;
            console.log("nextline is chapter name");
            // console.log(chapName.value);
            console.log(props.ChapterName); // sth wrong with here
            // console.log(" ");
        });
});
</script>

<template>
    <div class="chapter-item">
        <div class="chap-icon-wrapper" @click="updateChapName">
            <!-- <slot dir-icon="dir-icon"></slot> -->
            <slot>No chapter exist</slot>
            <IconDownArrow
                :class="{ 'down-rotated': !FramesDisplay, 'up-rotated': FramesDisplay }"
            />
        </div>
        <Transition name="drop">
            <div class="file-content-wrapper" v-show="FramesDisplay">
                <FrameItem
                    @click="itemCallBack($event)"
                    v-for="item in FrameList"
                    :name="item.name"
                    >{{ item.name }}</FrameItem
                >
            </div>
        </Transition>
    </div>
</template>

<style>
.chapter-item {
    display: flex;
    flex-direction: column;
    padding: 0.5rem;
    border-bottom: 5px solid rgba(0, 90, 27, 0.507);
    width: 100%;
}

/*icon part below*/
.chap-icon-wrapper > svg {
    margin-top: auto;
    width: 2rem;
    height: 2rem;
}

.chap-icon-wrapper {
    overflow: hidden;
    text-align: left;
    display: flex;
    flex-direction: row;
    font-size: x-large;
}

.chap-icon-wrapper:hover {
    text-align: left;
    background: rgb(45, 102, 34);
}

.up-rotated {
    transform: rotate(180deg);
    transition: transform 0.1s;
}

.down-rotated {
    transform: rotate(0deg);
    transition: transform 0.1s;
}
</style>
