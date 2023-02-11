<script setup lang="ts">
import item from "../components/NavbarItem.vue"
</script>



<template>
    <header id="header" class="grid-item">
        <item></item>
        <item></item>
        <item></item>
    </header>

</template>



<style>

#header {
    display: flex;
    flex-direction: row;
}

</style>