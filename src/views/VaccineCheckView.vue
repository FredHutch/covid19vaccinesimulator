<script setup>

import { storeToRefs } from 'pinia'
import { useRouter, useRoute } from 'vue-router';
import MySlider from "../components/MySlider.vue";
import Button from 'primevue/button';
import Divider from "primevue/divider";
import Footer from "../components/Footer.vue";
import Header from "../components/Header.vue";
import SideBar from "../components/SideBar.vue";
import MySelectButton from "../components/MySelectButton.vue";

/*
import { useVaccineSelectionStore } from '@/stores/vaccine-selection';
const vaccineStore = useVaccineSelectionStore();
const { vaccine1, vaccine2, vaccine3,  vaccine1Usage, vaccine2Usage, vaccine3Usage} = storeToRefs(vaccineStore);
*/


import { useStrategiesStore } from '../stores/strategies';
const strategiesStore = useStrategiesStore();
const { strategyList, selectedStrategyIndex } = storeToRefs(strategiesStore);
// let currentStrategy = strategyList.value[selectedStrategyIndex.value];

// this works
// weird... it didn't work sometime?!?
//strategiesStore.addStrategy();


let strategyIndex = selectedStrategyIndex.value;
const route = useRoute();

/*
if(route.query.strategy != undefined){
    strategyIndex = Number(route.query.strategy);
    strategiesStore.selectStrategy(strategyIndex);
}
*/
let currentStrategy = strategyList.value[strategyIndex];

let vParameters = currentStrategy["vaccineParameters"];



function onVaccine1SelectionChange(newData) {
    console.log(`onVaccine1SelectionChange: ${JSON.stringify(newData)}`);
    vParameters["vaccineList"][0]["usage"] = newData;

    /*
    vaccineStore.$patch({
        vaccine1Usage: newData
    });
    */
    
}

function onVaccine2SelectionChange(newData) {
    console.log(`onVaccine2SelectionChange: ${JSON.stringify(newData)}`);
    vParameters["vaccineList"][1]["usage"] = newData;
    vaccineStore.$patch({
        vaccine2Usage: newData
    });
    
}

function onVaccine3SelectionChange(newData) {
    console.log(`onVaccine3SelectionChange: ${JSON.stringify(newData)}`);
    vParameters["vaccineList"][2]["usage"] = newData;

    /*
    vaccineStore.$patch({
        vaccine3Usage: newData
    });
    */
    
}

//console.log(props.foo)

const vaccinationTypes = [
    {name: 'Primary series', value: "full dose"},
    {name: 'Booster', value: "booster"},
];

const router = useRouter();
const onNextClick = (event) => {
  router.push('/vaccination-by-age?group=1')
};

</script>

<template>

    <div class="grid">

        <div class="col-2">
            <div class="mt-7"></div>
            <div class="sticky top-0"><SideBar></SideBar></div>
        </div>
        <div class="col ml-4">
            <div class="sticky top-0"><Header></Header></div>
            <h1>Vaccination Status Check</h1>
            <Divider class="fh-divider-primary"></Divider>
            <div class="grid">
                <div class="col">
                    <h3>Has "{{vParameters["vaccineList"][0].name}}" been used for the following?</h3>
                    <MySelectButton @change="onVaccine1SelectionChange" :options="vaccinationTypes"></MySelectButton>

                    <h3>Has "{{vParameters["vaccineList"][1].name}}" been used for the following?</h3>
                    <MySelectButton @change="onVaccine2SelectionChange" :options="vaccinationTypes"></MySelectButton>
                    <h3>Has "{{vParameters["vaccineList"][2].name}}" been used for the following?</h3>
                    <MySelectButton @change="onVaccine3SelectionChange" :options="vaccinationTypes"></MySelectButton>

                </div>
            </div>
            <div>
                <div class="flex justify-content-center mt-4 mb-4">
                    <Button label="Next" class="p-button-lg fh-button-primary"  @click="onNextClick"></Button>
                </div>
                <Divider class="fh-divider-primary"></Divider>
                <Footer></Footer>
            </div>
        </div>
        <div class="col-2"></div>
    </div>
</template>