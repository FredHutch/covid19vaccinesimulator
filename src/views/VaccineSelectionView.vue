<script setup>
import Fieldset from 'primevue/fieldset';
import Button from 'primevue/button';
import Divider from "primevue/divider";
import Footer from "../components/Footer.vue";
import Header from "../components/Header.vue";
import SideBar from "../components/SideBar.vue";
import RegionList from "../components/RegionList.vue";
import VariantList from "../components/VariantList.vue";
import MySlider from "../components/MySlider.vue";

import Slider from "primevue/slider";
import { useRouter, useRoute } from 'vue-router';
import { ref } from 'vue';
import { storeToRefs } from 'pinia';
import VaccineList from '../components/VaccineList.vue';

/*
import { useVaccineSelectionStore } from '@/stores/vaccine-selection';
const vaccineStore = useVaccineSelectionStore();
const { vaccine1, vaccine2, vaccine3} = storeToRefs(vaccineStore);
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



const router = useRouter();
const onNextClick = (event) => {
  router.push('/vaccination-by-age')
};


function onVaccine1Chnage(newData) {
    console.log(`onVaccine1Chnage: ${JSON.stringify(newData)}`);
    //setRegion(newRegion);
    vParameters["vaccineList"][0] = {...vParameters["vaccineList"][0], ...newData};
    /*
    vaccineStore.$patch({
        vaccine1: newData
    });
    */
}

function onVaccine1Input(newData) {
    console.log(`onVaccine1Input: ${JSON.stringify(newData)}`);
    // { name: 'Pfizer-BioNTech', code: 'pfizer', type:"pre-defined" },
    

    vParameters["vaccineList"][0] = {...vParameters["vaccineList"][0], name: newData, code: newData.toLowerCase(), type:"customized"};
    // version 1
    //vParameters["vaccineList"][0] = { name: newData, code: newData.toLowerCase(), type:"customized" };


    /*
    vaccineStore.$patch({
        vaccine1: { name: newData, code: newData.toLowerCase(), type:"customized" }
    });
    */
}

function onVaccine2Chnage(newData) {
    console.log(`onVaccine2Chnage: ${JSON.stringify(newData)}`);
    //setRegion(newRegion);
    vParameters["vaccineList"][1] = {...vParameters["vaccineList"][1], ...newData};
    /*
    vaccineStore.$patch({
        vaccine2: newData
    });
    */
}

function onVaccine2Input(newData) {
    console.log(`onVaccine2Input: ${JSON.stringify(newData)}`);
    // { name: 'Pfizer-BioNTech', code: 'pfizer', type:"pre-defined" },
    
    
    vParameters["vaccineList"][1] = {...vParameters["vaccineList"][1], name: newData, code: newData.toLowerCase(), type:"customized"};
    // version 1
    //vParameters["vaccineList"][1] = { name: newData, code: newData.toLowerCase(), type:"customized" };

    /*
    vaccineStore.$patch({
        vaccine2: { name: newData, code: newData.toLowerCase(), type:"customized" }
    });
    */
}

function onVaccine3Chnage(newData) {
    console.log(`onVaccine3Chnage: ${JSON.stringify(newData)}`);
    //setRegion(newRegion);
    vParameters["vaccineList"][2] = {...vParameters["vaccineList"][2], ...newData};

    /*
    vaccineStore.$patch({
        vaccine3: newData
    });
    */
}

function onVaccine3Input(newData) {
    console.log(`onVaccine3Input: ${JSON.stringify(newData)}`);
    // { name: 'Pfizer-BioNTech', code: 'pfizer', type:"pre-defined" },

    vParameters["vaccineList"][2] = {...vParameters["vaccineList"][2], name: newData, code: newData.toLowerCase(), type:"customized"};
    // version 1
    //vParameters["vaccineList"][2] = { name: newData, code: newData.toLowerCase(), type:"customized" };

    /*
    vaccineStore.$patch({
        vaccine3: { name: newData, code: newData.toLowerCase(), type:"customized" }
    });
    */
}



</script>

<template>

    <div class="grid">

        <div class="col-2">
            <div class="mt-7"></div>
            <div class="sticky top-0"><SideBar></SideBar></div>
        </div>
        <div class="col ml-4">
            <div class="sticky top-0"><Header></Header></div>
            
            <h1>Vaccine Options</h1>
            <Divider class="fh-divider-primary"></Divider>
            <p class="mt-6">Indicate vaccines that have been applied and/or those that will be applied.</p>
            <p>You could enter "None" if no additional vaccines are considered. If you cannot find the vaccines in the provided list, feel free to enter the name of another vaccine. You will later be asked to provide effectiveness data for simulation.</p>
               
            <div class="grid">
                
                <div class="col">
                    <h2>{{vParameters["vaccineList"][0].name}}</h2>
                    <div>
                        <VaccineList  @change="onVaccine1Chnage" @input="onVaccine1Input" :editable="true"></VaccineList>
                    </div>
                    <h2>{{vParameters["vaccineList"][1].name}}</h2>
                    <div>
                        <VaccineList  @change="onVaccine2Chnage" @input="onVaccine2Input" :editable="true"></VaccineList>
                    </div>
                    <h2>{{vParameters["vaccineList"][2].name}}</h2>
                    <div>
                        <VaccineList  @change="onVaccine3Chnage" @input="onVaccine3Input" :editable="true"></VaccineList>
                    </div>
                </div>
            </div>
            <div>
                <div class="flex justify-content-center mt-4 mb-4">
                    <Button label="Next" class="p-button-lg fh-button-primary" @click="onNextClick"></Button>
                </div>
                <Divider class="fh-divider-primary"></Divider>
                <Footer></Footer>
            </div>
        </div>
        <div class="col-2"></div>
    </div>
</template>