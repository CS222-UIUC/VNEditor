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
            red: "cred",
            // start of left
            ulleft: "ulleft",
            headerleft: "lileft",
            buttonleft: "butleft",
            //end of left part
            ulcentral: "ulcent",
            listcent: "licent",
            butttoncent: "butcent",
            //end of central part
            ulright: "ulright",
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
        // botA() {
        //   this.counta++;
        // },
        // botB() {
        //   this.countb++;
        // },
        // botC() {
        //   this.countc++;
        // },
        // botD() {
        //   this.countd++;
        // },
    },
};
</script>

<template>
    <ul :id="ulleft">
        <li :id="headerleft"><b-button :id="buttonleft" @click="botA">A</b-button></li>
        <li :id="headerleft"><b-button :id="buttonleft" @click="botB">B</b-button></li>
        <li :id="headerleft"><b-button :id="buttonleft" @click="botC">C</b-button></li>
        <li :id="headerleft"><b-button :id="buttonleft" @click="botD">D</b-button></li>
    </ul>

    <ul :id="ulcentral">
        <li :id="listcent"><b-button :id="butttoncent">Cen</b-button></li>
        <li :id="listcent"><b-button :id="butttoncent">Cen</b-button></li>
        <li :id="listcent"><b-button :id="butttoncent">Cen</b-button></li>
        <li :id="listcent"><b-button :id="butttoncent">Cen</b-button></li>
        <p>
            test click counta,b,c,d {{ counta }}, {{ countb }}, {{ countc }},
            {{ countd }}
        </p>
    </ul>

    <ul :id="ulright">
        <p :class="red">something to implement</p>
    </ul>
</template>

<style>
#ulleft {
    list-style-type: none;
    margin: 0;
    padding: 0;
    min-height: 50px;
    overflow: hidden;
    overflow-y: scroll;
    background-color: #333;
}
#lileft {
    float: left;
}
#butleft {
    display: block;
    color: white;
    margin: 0;
    text-align: center;
    padding-top: 16px;
    padding-right: 20px;
    padding-bottom: 20px;
    padding-left: 20px;
    text-decoration: none;
}
#butleft:hover {
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
