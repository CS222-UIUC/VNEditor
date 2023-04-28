<script setup lang="ts">
import item from "./NavbarItem.vue";
import drop from "../DropDownList.vue";
import { getProjects, removeProject, initProject, modifyFrame } from "@/RequestAPI";
import {
    projectIDKey,
    projectNameKey,
    editorBackgroundKey,
    editorElementsKey,
    frameIDKey,
    frameNameKey,
} from "@/InjectionKeys";
import { inject, ref, watch, watchEffect } from "vue";
import type { Ref } from "vue";
import { FrameBack, type EditorElement, ElementType } from "@/FrameDef";

const frameID = inject(frameIDKey) as Ref<number | undefined>;
const frameName = inject(frameNameKey) as Ref<string | undefined>;
const projectID = inject(projectIDKey) as Ref<string | undefined>;
const projectName = inject(projectNameKey) as Ref<string | undefined>;
let editorElements: EditorElement[] = inject(editorElementsKey) as EditorElement[];
const editorBackground = inject(editorBackgroundKey) as Ref<string | undefined>;
const projectsOpenDisplay = ref(false);
const projectsRemoveDisplay = ref(false);
const projectsCreateDisplay = ref(false);
const projectNames: Ref<string[]> = ref([]);

function handleRemove(event: MouseEvent) {
    console.log("aaa");
    const el = event.target as HTMLElement;
    const name = el.innerHTML;
    console.log(name);

    removeProject(name).then((res: boolean) => {
        if (res) updateProject(undefined, undefined);
        const idx = projectNames.value.indexOf(name);
        projectNames.value.splice(idx, 1);
    });
}

function updateProject(newID: string | undefined, newName: string | undefined): void {
    projectID.value = newID;
    projectName.value = newName;
}

function saveFrame() {
    console.log("modifying frame...");
    console.log(editorElements.length);
    let frame = new FrameBack();
    frame.background = editorBackground.value as string;
    for (let i = 0; i < editorElements.length; ++i) {
        const el: EditorElement = editorElements[i];
        console.log(el);
        if (el.type == ElementType.Text) {
            frame.dialog = el.content;
        } else {
            frame.chara.push(el.content);
            frame.chara_pos.push({ x: el.xCoord, y: el.yCoord });
        }
    }
    modifyFrame(frameID.value, projectID.value, frame).then((res: boolean) => {
        if (res) console.log("save successful");
        else console.log("save failed");
    });
}

watch(projectID, () => {
    console.log("change");
    getProjects().then((res: string[]) => {
        projectNames.value = res;
    });
});
</script>

<template>
    <div>
        <div class="navbar-section" id="header-left">
            <item>
                <template #el>
                    <div id="project-title">
                        {{
                            projectName
                                ? "Current Project: " + projectName
                                : "No project has been opened"
                        }}
                    </div>
                </template>
            </item>
            <item>
                <template #el>
                    <div>
                        {{ frameName ? frameName : "No Frame has been opened" }}
                    </div>
                </template>
            </item>
        </div>
        <div class="navbar-section" id="header-mid" style="">
            <item v-show="!projectsCreateDisplay">
                <template #el>
                    <button
                        class="navbar-button"
                        @click="projectsCreateDisplay = !projectsCreateDisplay"
                    >
                        Create Project
                    </button>
                </template>
            </item>
            <item v-show="projectsCreateDisplay">
                <template #el>
                    <input
                        @keyup.enter="
                            (event) => {
                                projectsCreateDisplay = !projectsCreateDisplay;
                                initProject((event.target as HTMLInputElement).value as string).then((res: string | undefined)=> {
                                    if (res)
                                    projectID = res;
                     
                                });
                            }
                        "
                        placeholder="project name"
                        class="navbar-button"
                        style="background-color: white; color: black; height: 2rem"
                    />
                </template>
            </item>
            <item>
                <template #el>
                    <div style="dispay: flex">
                        <button
                            class="navbar-button"
                            @click="
                                async () => {
                                    projectNames = await getProjects();
                                    projectsRemoveDisplay = !projectsRemoveDisplay;
                                }
                            "
                        >
                            Remove Project
                        </button>
                        <drop
                            :display-control="projectsRemoveDisplay"
                            :item-list="projectNames"
                            :item-click="handleRemove"
                        ></drop>
                    </div>
                </template>
            </item>
            <item>
                <template #el>
                    <div style="dispay: flex">
                        <button
                            class="navbar-button"
                            @click="
                                getProjects().then((res: string[]) => {
                                    projectNames = res;
                                });
                                projectsOpenDisplay = !projectsOpenDisplay;
                            "
                        >
                            Open Project
                        </button>
                        <drop
                            :display-control="projectsOpenDisplay"
                            :item-list="projectNames"
                            :item-click="($event) => {
                                initProject(($event.target as HTMLElement).innerHTML).then((res: string | undefined)=>{
                                    if (res) {
                                        updateProject(res, ($event.target as HTMLElement).innerHTML);
                                    }
                                    
                                });
                                
                            }"
                        ></drop>
                    </div>
                </template>
            </item>
            <item>
                <template #el>
                    <div style="dispay: flex">
                        <button class="navbar-button" @click="saveFrame">Save Frame</button>
                    </div>
                </template>
            </item>
        </div>

        <div class="navbar-section" id="header-right">aaa</div>
    </div>
</template>

<style>
#project-title:hover + div {
    display: block;
}

.navbar-button {
    background: transparent;
    width: 6rem;
    color: white;
    border-radius: 5px;
    border-style: none;
    height: 3rem;
    font-size: large;
}

.navbar-button:hover {
    background-color: rgb(7, 63, 194);
}
.navbar-button:focus {
    background-color: rgb(0, 41, 138);
}

.navbar-section {
    height: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
}

#header {
    display: flex;
    flex-direction: row;
    align-items: center;
}

#header-left {
    width: calc(100% * 1 / 8);
    /* 1/8 */
}

#header-mid {
    width: calc(100% * 6 / 8);
    /* 6/8 */
}

#header-right {
    width: calc(100% * 1 / 8);
    /* 1/8 */
}
</style>
