<script setup lang="ts"></script>

<template>
    <div class="file-item">
        <slot>unknown file name</slot>
    </div>
</template>

<style>
.file-item {
    text-align: left;
    color: black;
    padding-left: 10%;
    font-size: large;
}

.file-item:hover {
    background: yellow;
}
</style>
