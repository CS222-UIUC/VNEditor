<script setup lang="ts">
import Toolbar from "./components/Toolbar.vue";
import Navbar from "./components/Navbar.vue"
</script>


<template>
  <Navbar >

  </Navbar>
  <main id="main-editor" class="grid-item">
    This is main editor
  </main>
  <div id="preview-sidebar" class="grid-item">this is sidebar 1</div>
  <div id="toolbar-sidebar" class="grid-item">this is sidebar 2</div>
  <footer id="footer" class="grid-item">this is footer</footer>
  

</template>


<style>

.grid-item {
  text-align: center;
  
}

#main-editor {
  background: azure;
}

#preview-sidebar {
  background-color: cadetblue;
}

#toolbar-sidebar {
  background-color: cadetblue;
}

#header {
  background-color: darkblue;
  color: white;
}

#footer {
  background-color: brown;
}

</style>