<script setup lang="ts"></script>

<template>
    <div class="navbar-item">
        <slot name="el"></slot>
    </div>
</template>

<style>
.navbar-item {
    height: max-content;
    margin-left: 2%;
    margin-top: auto;
    margin-bottom: auto;
}
</style>
