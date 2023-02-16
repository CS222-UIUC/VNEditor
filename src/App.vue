

<script>

import Toolbar from "./components/Toolbar.vue";
import Navbar from "./components/Navbar.vue"
import FileUploadArea from "./components/UploadArea.vue"
import Editor from "./components/Editor.vue"

export default {
  data() {
    return {
      fileUploadAreaDisplay: false
    }
  },
  components: {
    Toolbar,
    Navbar,
    FileUploadArea,
    Editor,
  },

}
</script>


<template>
  <Navbar >

  </Navbar>
  <main id="main-editor" class="grid-item" @clcik="fileUploadAreaDisplay = true" @dragenter="fileUploadAreaDisplay = true" @dragexit="fileUploadAreaDisplay = false">
    <FileUploadArea :fileUploadAreaDisplay="true" />
  </main>
  <div id="preview-sidebar" class="grid-item">this is sidebar 1</div>
  <div id="toolbar-sidebar" class="grid-item">
    
  </div>
  <footer id="footer" class="grid-item">this is footer</footer>
  

</template>


<style>

.grid-item {
  text-align: center;
  
}

#main-editor {
  background: azure;
  display: flex;
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