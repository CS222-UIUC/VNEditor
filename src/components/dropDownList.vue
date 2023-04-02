<script setup lang="ts">
import type { Ref, PropType } from "vue";
defineProps({
    displayControl: {
        type: Boolean,
        default: false,
    },
    itemList: {
        type: Array<string>,
        default: [],
    },
    itemClick: {
        type: Function as PropType<(event: MouseEvent) => void>,
        default: () => {},
    },
});
</script>

<template>
    <div class="dropdown-list" v-show="displayControl">
        <div class="dropdown-item" @click="itemClick" v-for="items in itemList" :key="items">
            {{ items }}
        </div>
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
.dropdown-item {
}
.dropdown-item:hover {
    background-color: rgb(164, 5, 89);
}
</style>
