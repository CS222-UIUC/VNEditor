<script>
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
        <li><button @click="botA">A</button></li>
        <li><button @click="botB">B</button></li>
        <li><button @click="botC">C</button></li>
        <li><button @click="botD">D</button></li>
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
/*end of left column*/
#ulcent {
    list-style-type: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    overflow-y: scroll;
    background-color: #30aef2;
}

#licent {
    float: left;
}

#butcent {
    display: block;
    color: rgb(0, 0, 0);
    margin: 0;
    text-align: center;
    padding-top: 18px;
    padding-right: 20px;
    padding-bottom: 20px;
    padding-left: 20px;
    text-decoration: none;
}

#butcent:hover {
    background-color: #0a7adc;
}
/*end of central column*/
#ulright {
    list-style-type: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    overflow-y: scroll;
    background-color: #333;
}

/*global setting*/
.cred {
    color: red;
}
</style>
