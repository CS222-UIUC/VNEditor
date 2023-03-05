<script>
import FileItem from "./FileItem.vue";
import IconDownArrow from "./icons/IconDownArrow.vue";
export default {
    data() {
        return {
            fileDisplay: true,
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
            <IconDownArrow />
        </div>
        <Transition name="drop">
            <div class="file-content-wrapper" v-show="fileDisplay">
                <FileItem></FileItem>
                <FileItem></FileItem>
                <FileItem></FileItem>
                <FileItem></FileItem>
            </div>
        </Transition>
    </div>
</template>

<style>
.file-wrapper {
    display: flex;
    flex-direction: column;
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
    flex: row;
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
    transition: max-height 0.25s;
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
</style>
