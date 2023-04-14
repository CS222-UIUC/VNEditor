<script setup lang="ts">
import ToolbarDir from "./ToolbarDir.vue";
import IconMusic from "../icons/IconMusic.vue";
import { Rtype } from "../../RequestAPI";
import type { PropType } from "vue";

const props = defineProps({
    backgroundCallBack: {
        type: Function as PropType<(event: MouseEvent) => void>,
        default: () => console.log("CallBack undefined"),
    },

    musicCallBack: {
        type: Function as PropType<(event: MouseEvent) => void>,
        default: () => console.log("CallBack undefined"),
    },

    characterCallBack: {
        type: Function as PropType<(event: MouseEvent) => void>,
        default: () => console.log("CallBack undefined"),
    },
});
</script>

<template>
    <div>
        <ToolbarDir :file-type="Rtype.background" :item-call-back="props.backgroundCallBack">
            <template #dir-icon>
                <IconMusic />
            </template>
            <template #dir-name>
                <div>Background</div>
            </template>
        </ToolbarDir>
        <ToolbarDir :file-type="Rtype.music" :item-call-back="props.musicCallBack">
            <template #dir-icon>
                <IconMusic />
            </template>
            <template #dir-name>
                <div>Music</div>
            </template>
        </ToolbarDir>
        <ToolbarDir :file-type="Rtype.character" :item-call-back="props.characterCallBack">
            <template #dir-icon>
                <IconMusic />
            </template>
            <template #dir-name>
                <div>Character</div>
            </template>
        </ToolbarDir>
    </div>
</template>
