<script setup lang="ts">
import FrameItem from "./FrameItem.vue";
import FrameItemRemove from "./FrameItem_remove.vue";
import { ref, inject, watchEffect, watch } from "vue";
import type { Ref } from "vue";
import IconDownArrow from "../icons/IconDownArrow.vue";
import type { IFrame_left } from "@/FrameDef";
import { projectIDKey } from "../../InjectionKeys";
import { getFramesList, appendFrame } from "../../RequestAPI"; // need to change to needed function
var FramesDisplay = ref(false); // control display the scene of the corresopnding chapter
var FrameCreateDisplay = ref(false);
var FrameDeleteDisplay = ref(false);
const FrameList: Ref<IFrame_left[]> = ref([]);
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
const prop = defineProps({
    chapNameFromLib: {
        type: String,
        required: true,
    },
});
const projectID = inject(projectIDKey) as Ref<string | undefined>;
function updateChapName(event: MouseEvent) {
    // for future change of chapter name
    const el = event.target as HTMLElement;
    const name = el.textContent;
    if (name) chapName.value = name;
    FramesDisplay.value = !FramesDisplay.value;
    FrameCreateDisplay.value = false;
    FrameDeleteDisplay.value = false;
}
async function appendNewFrame(chap_name: string, frame_name: string) {
    let result = await appendFrame(projectID.value, chap_name, frame_name);
    if (result != undefined && result != "") {
        FrameCreateDisplay.value = !FrameCreateDisplay.value;
    }
}
watch(FrameCreateDisplay, () => {
    if (projectID.value)
        getFramesList(projectID.value, prop.chapNameFromLib).then((res: IFrame_left[]) => {
            if (res) FrameList.value = res;
            console.log("nextline is chapNameFromLib");
            // console.log(chapName.value);
            console.log(prop.chapNameFromLib);
        });
});
watch(FrameDeleteDisplay, () => {
    if (projectID.value)
        getFramesList(projectID.value, prop.chapNameFromLib).then((res: IFrame_left[]) => {
            if (res) FrameList.value = res;
            console.log("nextline is chapNameFromLib");
            // console.log(chapName.value);
            console.log(prop.chapNameFromLib);
        });
});

watchEffect(() => {
    // call back method update the chapter to display once projectID received
    FramesDisplay.value = false;
    FrameList.value = [];
    if (projectID.value)
        getFramesList(projectID.value, prop.chapNameFromLib).then((res: IFrame_left[]) => {
            if (res) FrameList.value = res;
            console.log("nextline is chapNameFromLib");
            // console.log(chapName.value);
            console.log(prop.chapNameFromLib);
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
            <div class="drop-wrapper" v-show="FramesDisplay">
                <div v-show="!FrameCreateDisplay && !FrameDeleteDisplay">
                    <button
                        class="chapter-button"
                        @click="FrameCreateDisplay = !FrameCreateDisplay"
                    >
                        New Frame
                    </button>
                    <button
                        class="chapter-button"
                        @click="FrameDeleteDisplay = !FrameDeleteDisplay"
                    >
                        Remove Frame
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
                <div class="addframe-wrapper" v-show="FrameDeleteDisplay">
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
                        @click="FrameDeleteDisplay = !FrameDeleteDisplay"
                    >
                        Done
                    </button>
                </div>
                <div class="frame-list">
                    <FrameItem
                        v-show="!FrameDeleteDisplay"
                        v-for="item in FrameList"
                        :key="item.FrameName"
                        :name="item.FrameName"
                        :ChapterName="prop.chapNameFromLib"
                        :FrameName="item.FrameName"
                        :FrameId="item.id.valueOf()"
                        >{{ item.FrameName }}
                    </FrameItem>
                    <FrameItemRemove
                        v-show="FrameDeleteDisplay"
                        v-for="item in FrameList"
                        :key="item.FrameName"
                        :name="item.FrameName"
                        :ChapterName="prop.chapNameFromLib"
                        :FrameName="item.FrameName"
                        :FrameId="item.id.valueOf()"
                        >{{ item.FrameName }}
                    </FrameItemRemove>
                </div>
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
.drop-wrapper {
    max-height: 200px;
}
/*icon part below*/
.chap-icon-wrapper > svg {
    margin-top: auto;
    width: 2rem;
    height: 2rem;
}
.chap-icon-wrapper {
    overflow: hidden;
    color: black;
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
    height: 40px;
    flex-direction: row;
    text-align: left;
}
.chapter-button {
    display: inline;
    flex-direction: row;
    border-bottom: 6px solid rgba(0, 90, 27, 0.507);
    width: 50%;
    height: 40px;
    vertical-align: bottom;
}
.add-frame-text {
    display: inline;
    flex-direction: row;
    height: 40px;
    border-bottom: 5px solid rgba(0, 90, 27, 0.507);
    width: 50%;
}
.add-frame-button {
    display: inline;
    flex-direction: row;
    border-bottom: 5px solid rgba(0, 90, 27, 0.507);
    height: 40px;
    width: 25%;
}
.frame-list {
    max-height: 160px;
    overflow-y: scroll;
}
</style>
