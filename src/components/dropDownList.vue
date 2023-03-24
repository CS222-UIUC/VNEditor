<script setup lang="ts">
import type { Ref } from "vue";
defineProps({
    displayControl: {
        type: Boolean,
        default: false,
    },
});
</script>

<template>
    <div class="dropdown-list" v-show="displayControl">
        <div class="dropdown-item">aa</div>
        <div class="dropdown-item">aa</div>
        <div class="dropdown-item">aa</div>
    </div>
</template>

<style>
.dropdown-list {
    z-index: 2;
    position: absolute;
    background-color: deeppink;
    width: 100%;
    padding: 5%;
}
</style>
