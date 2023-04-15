<script setup lang="ts">
import FrameItem from "./FrameItem.vue";
import { ref, inject, watchEffect, type PropType } from "vue";
import type { Ref } from "vue";
import IconDownArrow from "./icons/IconDownArrow.vue";
import type { IFrame } from "@/FrameDef";
import { projectIDKey } from "../InjectionKeys";
import { getFrames, addFrame } from "../RequestAPI"; // need to change to needed function

var FramesDisplay = ref(false); // control display the scene of the corresopnding chapter
var FrameCreateDisplay = ref(false);
const FrameList: Ref<IFrame[]> = ref([]);
const chapName: Ref<string> = ref("");
var frameNametoAdd = "";
// function addFrame(idx: Number): boolean {
//     return false;
// }

// function removeFrame(idx: Number): boolean {
//     return false;
// }

// function switchBranch(id: FrameID): boolean {
//     return false;
// }

const projectID = inject(projectIDKey) as Ref<string | undefined>;

function updateChapName(event: MouseEvent) {
    const el = event.target as HTMLElement;
    const name = el.textContent;
    if (name) chapName.value = name;
    FramesDisplay.value = !FramesDisplay.value;
    FrameCreateDisplay.value = false;
}

async function appendNewFrame(chap_name: string, frame_name: string) {
    let result = await addFrame(projectID.value, chap_name, frame_name);
    if (result != "") {
        FrameCreateDisplay.value = !FrameCreateDisplay.value;
    }
}

watchEffect(() => {
    // call back method update the chapter to display once projectID received
    if (projectID.value)
        getFrames(projectID.value, chapName.value).then((res: IFrame[]) => {
            if (res) FrameList.value = res;
            console.log("nextline is chapter name");
            console.log(chapName.value);
            // console.log(" ");
        });
    frameNametoAdd;
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
                <div v-show="!FrameCreateDisplay">
                    <button
                        class="chapter-button"
                        @click="FrameCreateDisplay = !FrameCreateDisplay"
                    >
                        New Frame
                    </button>
                </div>
                <div class="addframe-wrapper" v-show="FrameCreateDisplay">
                    <input
                        class="add-frame-text"
                        v-model="frameNametoAdd"
                        placeholder="enter chapter name"
                    />
                    <button
                        class="add-frame-button"
                        @click="appendNewFrame(chapName, frameNametoAdd)"
                    >
                        Done
                    </button>
                    <button
                        class="add-frame-button"
                        @click="FrameCreateDisplay = !FrameCreateDisplay"
                    >
                        Cancle
                    </button>
                </div>
                <FrameItem v-for="item in FrameList" :key="item.name" :name="item.name"
                    >{{ item.name }}
                </FrameItem>
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

.addframe-wrapper {
    flex-direction: row;
    text-align: left;
}

.chapter-button {
    display: flex;
    flex-direction: column;
    padding: 0.5rem;
    border-bottom: 5px solid rgba(0, 90, 27, 0.507);
    width: 100%;
}

.add-frame-text {
    display: inline;
    flex-direction: row;
    padding: 0.5rem;
    border-bottom: 5px solid rgba(0, 90, 27, 0.507);
    width: 50%;
}
.add-frame-button {
    display: inline;
    flex-direction: row;
    padding: 0.5rem;
    border-bottom: 5px solid rgba(0, 90, 27, 0.507);
    width: 25%;
}
</style>
