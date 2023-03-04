<script>
import ToolbarDir from "./ToolbarDir.vue";
import IconMusic from "./icons/IconMusic.vue";
export default {
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
        <template #dir-name>
            <div>Images</div>
        </template>
    </ToolbarDir>
    <ToolbarDir>
        <template #dir-icon>
            <IconMusic />
        </template>
        <template #dir-name>
            <div>Music</div>
        </template>
    </ToolbarDir>
</template>
