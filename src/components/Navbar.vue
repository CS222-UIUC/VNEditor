<script>
//import item from "../components/NavbarItem.vue";
//find botton file
//https://bootstrap-vue.org/docs/components/button 
</script>

<template>
  <ul>
    <li><b-button>A</b-button></li>
    <li><b-button>B</b-button></li>
    <li><b-button>C</b-button></li>
    <li><b-button>D</b-button></li>
  </ul>
</template>

<style>

ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    background-color: #333;
}

li {
    float: left;
}

li b-button {
    display: block;
    color: white;
    text-align: center;
    padding: 14px 16px;
    text-decoration: none;
}

li b-button:hover {
    background-color: #111;
}
</style>


