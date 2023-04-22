<script setup lang="ts">
/** __vue_virtual_code_placeholder */
// const ChapterName = "";

const prop = defineProps({
    ChapterName: {
        type: String,
        required: true,
    },
    FrameName: {
        type: String,
        required: true,
    },
});

function displayframe() {
    console.log("next two line are chapname and frame name");
    console.log(prop.ChapterName);
    console.log(prop.FrameName);
}
</script>

<template>
    <div class="frame-item" @dblclick="displayframe">
        <slot>unknown scene</slot>
    </div>
</template>

<style>
.frame-item {
    text-align: center;
    width: 100%;
}
.frame-item:hover {
    text-align: center;
    width: 100%;
    background: rgb(70, 156, 53);
}
</style>
