<script>
import ToolbarDir from "./ToolbarDir.vue";
import IconMusic from "./icons/IconMusic.vue";
export default {
    data() {
        return {
            fileUploadAreaDisplay: false,
        };
    },
    components: {
        ToolbarDir,
        IconMusic,
    },
};
</script>

<template>
    <ToolbarDir>
        <template #dir-icon>
            <IconMusic />
        </template>
    </ToolbarDir>
    <ToolbarDir>
        <template #dir-icon>
            <IconMusic />
        </template>
    </ToolbarDir>
</template>
