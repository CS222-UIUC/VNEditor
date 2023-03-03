<script>
export default {};
</script>

<template>
  <Transition>
    <div id="file-upload-area" v-show="$parent.fileUploadAreaDisplay">
      <h2>
        <b style="opacity: 1"> Drag files here to upload </b>
      </h2>
    </div>
  </Transition>
</template>

<style>
#file-upload-area:-moz-drag-over {
  color: aliceblue;
  background-color: rgb(100, 100, 100);
  border-color: azure;
}
#file-upload-area {
  transition-property: all;
  transition-duration: 2s;
  justify-content: center;
  align-items: center;
  display: flex;
  border-radius: 2%;
  border-style: dashed;
  border-width: 10px;
  border-color: rgb(50, 50, 50);
  background-color: rgba(100, 100, 100, 0.5);
  position: absolute;
  width: 80%;
  height: 80%;
  top: 10%;
  left: 10%;
}
.v-enter-active,
.v-leave-active {
  transition: opacity 0.1s ease;
}
.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
