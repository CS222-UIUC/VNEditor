<script setup lang="ts">
import item from "../components/NavbarItem.vue";
import drop from "../components/dropDownList.vue";
import { getProjects, removeProject, initProject } from "../RequestAPI";
import { projectIDKey } from "../InjectionKeys";
import { inject, ref } from "vue";
import type { Ref } from "vue";
// let counta: number = 0;
// let countb: number = 0;
// let countc: number = 0;
// let countd: number = 0;
// function botA() {
//     counta++;
// }
// function botB() {
//     countb++;
// }
// function botC() {
//     countc++;
// }
// function botD() {
//     countd++;
// }
const id = inject(projectIDKey) as Ref<string>;
let projectsDropDisplay = ref(false);
let s: string = "testing_name";
</script>

<template>
    <div>
        <div class="navbar-section" id="header-left"></div>
        <div class="navbar-section" id="header-mid" style="">
            <item>
                <template #el>
                    <button class="navbar-button" @click="initProject(s)">Create Project</button>
                </template>
            </item>
            <item>
                <template #el>
                    <button class="navbar-button" @click="removeProject(id)">Delete Project</button>
                </template>
            </item>
            <item>
                <template #el>
                    <div style="dispay: flex">
                        <button
                            class="navbar-button"
                            @focus="projectsDropDisplay = true"
                            @blur="projectsDropDisplay = false"
                            @click="getProjects"
                        >
                            Open Project
                        </button>
                        <drop :display-control="projectsDropDisplay"></drop>
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
