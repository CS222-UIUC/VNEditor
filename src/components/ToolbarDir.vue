<script>
import FileItem from "./FileItem.vue";
import IconDownArrow from "./icons/IconDownArrow.vue";
export default {
    data() {
        return {
            fileDisplay: false,
            files: ["file1", "file2", "file3"],
        };
    },
    components: {
        IconDownArrow,
        FileItem,
    },
};
</script>

<template>
    <div class="file-wrapper">
        <div class="file-icon-wrapper" @click="fileDisplay = !fileDisplay">
            <slot name="dir-icon"></slot>
            <slot name="dir-name"></slot>
            <IconDownArrow :class="{ 'down-rotated': !fileDisplay, 'up-rotated': fileDisplay }" />
        </div>
        <Transition name="drop">
            <div class="file-content-wrapper" v-show="fileDisplay">
                <FileItem v-for="item in files" :key="item">{{ item }}</FileItem>
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
