<script setup lang="ts">
import ToolbarDir from "./ToolbarDir.vue";
import IconMusic from "./icons/IconMusic.vue";

defineProps({
    backgroundCallBack: {
        type: Function,
        default: () => console.log("CallBack undefined"),
    },
});
</script>

<template>
    <div>
        <ToolbarDir file-type="background">
            <template #dir-icon>
                <IconMusic />
            </template>
            <template #dir-name>
                <div>Background</div>
            </template>
        </ToolbarDir>
        <ToolbarDir file-type="music">
            <template #dir-icon>
                <IconMusic />
            </template>
            <template #dir-name>
                <div>Music</div>
            </template>
        </ToolbarDir>
        <ToolbarDir file-type="character">
            <template #dir-icon>
                <IconMusic />
            </template>
            <template #dir-name>
                <div>Character</div>
            </template>
        </ToolbarDir>
    </div>
</template>
