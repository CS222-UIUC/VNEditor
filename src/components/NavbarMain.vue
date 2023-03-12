<script lang="ts">
//import item from "../components/NavbarItem.vue";
//find botton file
//https://bootstrap-vue.org/docs/components/button
</script>

<script setup lang="ts">
let counta: number = 0;
let countb: number = 0;
let countc: number = 0;
let countd: number = 0;
function botA() {
    counta++;
}
function botB() {
    countb++;
}
function botC() {
    countc++;
}
function botD() {
    countd++;
}
</script>

<template>
    <div>
        <div class="navbar-section" id="header-left">aaa</div>
        <div class="navbar-section" id="header-mid">aaa</div>
        <div class="navbar-section" id="header-right">aaa</div>
    </div>
</template>

<style>
.navbar-section {
    height: max-content;
}

#header {
    display: flex;
    flex-direction: row;
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
