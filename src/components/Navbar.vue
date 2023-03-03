<script lang="ts">
//import item from "../components/NavbarItem.vue";
//find botton file
//https://bootstrap-vue.org/docs/components/button
export default {
  data() {
    return {
      counta: 0,
      countb: 0,
      countc: 0,
      countd: 0,
    };
  },
  methods: {
    botA() {
      // update component state
      this.counta++;
    },
    botB() {
      // update component state
      this.countb++;
    },
    botC() {
      // update component state
      this.countc++;
    },
    botD() {
      // update component state
      this.countd++;
    },
  },

  watch: {
    botA() {
      this.counta++;
    },
    botB() {
      this.countb++;
    },
    botC() {
      this.countc++;
    },
    botD() {
      this.countd++;
    },
  },
};
</script>

<template>
  <ul>
    <li><b-button @click="botA">A</b-button></li>
    <li><b-button @click="botB">B</b-button></li>
    <li><b-button @click="botC">C</b-button></li>
    <li><b-button @click="botD">D</b-button></li>
  </ul>
  <p>
    test click counta,b,c,d {{ counta }}, {{ countb }}, {{ countc }},
    {{ countd }}
  </p>
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
