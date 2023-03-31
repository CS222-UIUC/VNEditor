<script setup lang="ts">
import item from "../components/NavbarItem.vue";
import drop from "../components/dropDownList.vue";
import { getProjects, removeProject, initProject } from "../RequestAPI";
import { projectIDKey } from "../InjectionKeys";
import { inject, ref } from "vue";
import type { Ref } from "vue";

const id = inject(projectIDKey) as Ref<string>;
let projectsOpenDisplay = ref(false);
let projectsRemoveDisplay = ref(false);
let projectsCreateDisplay = ref(false);
let s: string = "testing_name";
let projectNames: Ref<string[]>;

function handleRemove(event: MouseEvent) {
    console.log("aaa");
    const el = event.target as Element;
    const id = el.getAttribute("project-name");
    console.log(id);
    if (id) {
        removeProject(id); // stupid backend is working on this
    }
}
</script>

<template>
    <div>
        <div class="navbar-section" id="header-left"></div>
        <div class="navbar-section" id="header-mid" style="">
            <item>
                <template #el>
                    <button
                        class="navbar-button"
                        v-show="!projectsCreateDisplay"
                        @click="projectsCreateDisplay = !projectsCreateDisplay"
                    >
                        Create Project
                    </button>
                </template>
            </item>
            <item>
                <template #el>
                    <input
                        v-show="projectsCreateDisplay"
                        @keyup.enter="
                            (event) => {
                                projectsCreateDisplay = !projectsCreateDisplay;
                                initProject((event.target as HTMLInputElement).value as string);
                            }
                        "
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
                                getProjects().then((res: string[]) => {
                                    projectNames = res;
                                });
                                projectsRemoveDisplay = !projectsRemoveDisplay;
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
                        ></drop>
                    </div>
                </template>
            </item>
        </div>

        <div class="navbar-section" id="header-right">aaa</div>
    </div>
</template>

<style>
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
