<script setup lang="ts">
import { ref, inject, watchEffect, type PropType } from "vue";
import type { Ref } from "vue";
import FileItem from "./FileItem.vue";
import IconDownArrow from "./icons/IconDownArrow.vue";
import { projectIDKey } from "../InjectionKeys";
import { getResources, uploadFiles, Rtype } from "../RequestAPI";

var fileDisplay = ref(false);
var enterCount = ref(0);
const files = ref<string[]>([]);
const props = defineProps({
    fileType: {
        type: String as PropType<Rtype>,
        default: Rtype.background,
    },
    itemCallBack: {
        type: Function as PropType<(event: MouseEvent) => void>,
        default: () => console.log("CallBack undefined"),
    },
});
const projectID = inject(projectIDKey) as Ref<string | undefined>;

watchEffect(() => {
    getResources(projectID.value, props.fileType).then((res: string[]) => {
        if (res) files.value = res;
    });
});

function handleFilesDrop(event: DragEvent): void {
    event.preventDefault();
    enterCount.value = 0;
    if (event.dataTransfer?.files) {
        let formData: FormData = new FormData();
        let names: string[] = [];
        Array.from(event.dataTransfer.files).forEach((f: File) => {
            formData.append("file", f);
            names.push(f.name);
        });
        (async () => {
            console.log("upload");
            const success: boolean = await uploadFiles(projectID.value, props.fileType, formData);
            console.log(success);
            if (success) files.value.push(...names);
            console.log(files);
        })();
    }
}
</script>

<template>
    <div
        class="file-wrapper"
        :class="{ 'upload-area': enterCount > 0 }"
        @dragenter.prevent.stop="
            enterCount++;
            fileDisplay = true;
        "
        @dragexit.prevent.stop="enterCount--"
        @drop.prevent.stop="handleFilesDrop"
    >
        <div class="file-icon-wrapper" @click="fileDisplay = !fileDisplay">
            <slot name="dir-icon"></slot>
            <slot name="dir-name"></slot>
            <IconDownArrow :class="{ 'down-rotated': !fileDisplay, 'up-rotated': fileDisplay }" />
        </div>
        <Transition name="drop">
            <div class="file-content-wrapper" v-show="fileDisplay">
                <FileItem
                    @click="itemCallBack($event)"
                    v-for="item in files"
                    :key="item"
                    :name="item"
                    >{{ item }}</FileItem
                >
            </div>
        </Transition>
    </div>
</template>

<style>
.file-wrapper {
    display: flex;
    flex-direction: column;
    padding: 0.5rem;
    border-bottom: 5px solid red;
}

.upload-area {
    background-color: beige;
}

.file-icon-wrapper > svg {
    margin-top: auto;
    width: 2rem;
    height: 2rem;
}

.file-icon-wrapper {
    overflow: hidden;
    text-align: left;
    display: flex;
    flex-direction: row;
    font-size: x-large;
}

.file-icon-wrapper:hover {
    text-align: left;
    background: red;
}

svg:last-child {
    margin-left: auto;
}

.file-content-wrapper {
    max-height: 20rem;
}

.drop-enter-active,
.drop-leave-active {
    transition: max-height 0.25s ease;
    overflow: hidden;
}
.drop-enter-to,
.drop-leave-from {
    max-height: 20rem;
}

.drop-enter-from,
.drop-leave-to {
    max-height: 0;
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
