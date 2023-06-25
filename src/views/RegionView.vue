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

import InputNumber from 'primevue/inputnumber';
import Slider from "primevue/slider";
import { useRouter, useRoute } from 'vue-router';
//import { useRegsionStore } from '@/stores/region';
import { storeToRefs } from 'pinia';
import Message from 'primevue/message';

import { watchEffect } from "vue";

import { useStrategiesStore } from '../stores/strategies';
const strategiesStore = useStrategiesStore();
const { strategyList, selectedStrategyIndex, updateRegionParametersByStrategyIndex } = storeToRefs(strategiesStore);
// let currentStrategy = strategyList.value[selectedStrategyIndex.value];

// this works
// weird... it didn't work sometime?!?
//strategiesStore.addStrategy();


let strategyIndex = selectedStrategyIndex.value;
const route = useRoute();

import { systemName } from "../content/variable";
import { useHead } from "@unhead/vue";
useHead({
  title: `Region ${strategyList[strategyIndex] != undefined && strategyList[strategyIndex]["regionParameters"].region != undefined? ` - ${strategyList[strategyIndex]["regionParameters"].region.name}`: ""} | ${systemName}`,
  /*
  meta: [
    { name: 'description', content: 'Learn more about us.' },
  ],
  */
})

/*
if(route.query.strategy != undefined){
    strategyIndex = Number(route.query.strategy);
    strategiesStore.selectStrategy(strategyIndex);
}
*/
let currentStrategy = strategyList.value[strategyIndex];

let regionParameters = currentStrategy["regionParameters"];




//const regionStore = useRegsionStore();
//const { region, variant, infectiousnessLevel} = storeToRefs(regionStore);

const router = useRouter();
const onNextClick = (event) => {
  router.push('/social-distancing')
};

watchEffect(async () => {
  // this effect will run immediately and then
  // re-run whenever currentBranch.value changes

  window.scrollTo({top: 0, behavior: 'smooth'});

});

function onRegionChnage(newRegion) {
    console.log(`onRegionChnage: ${JSON.stringify(newRegion)}`);
    console.log(`onRegionChnage: currentStrategy ${JSON.stringify(currentStrategy)}`);
    //setRegion(newRegion);


    // version 2: 
    regionParameters.region = newRegion;

    strategiesStore.updateRegionParametersByStrategyIndex(strategyIndex);


    // version 1:
    /*
    regionStore.$patch({
        region: newRegion
    });
    */
}

function onVariantChnage(newData) {
    console.log(`onVariantChnage: ${JSON.stringify(newData)}`);
    //setRegion(newRegion);

    // version 2: 
    regionParameters.variant = newData;

    // version 1:
    /*
    regionStore.$patch({
        variant: newData
    });
    */
}


//<MySlider :min="1" :max="10" :step="1" :initial="1" @change="onInfectiousnessLevelChnage"></MySlider>
/*
function onInfectiousnessLevelChnage(newData) {
    console.log(`onInfectiousnessLevelChnage: ${JSON.stringify(newData)}`);
    //setRegion(newRegion);

    regionStore.$patch({
        infectiousnessLevel: newData
    });
}
*/

</script>

<template>
    <div class="grid">
        <div class="col-2">
            <div class="mt-7"></div>
            <div class="sticky top-0"><SideBar></SideBar></div>
            

        </div>
        <div class="col ml-4">
            <div class="sticky top-0"><Header></Header></div>
            
            <h1>Region</h1>
            <Divider class="fh-divider-primary"></Divider>
            <div class="grid">
                
                <div class="col">
                    <h2>Selected region: {{ strategyList[strategyIndex]["regionParameters"].region != undefined? strategyList[strategyIndex]["regionParameters"].region.name: "" }}</h2>
                    <div class="mt-4">
                        <RegionList @change="onRegionChnage"></RegionList>
                    </div>
                    <div class="mt-4">Population size: {{strategyList[strategyIndex]["regionParameters"].region != undefined && strategyList[strategyIndex]["regionParameters"].region.populationList != undefined? strategyList[strategyIndex]["regionParameters"].region.populationList.reduce((a,b) => a + b, 0).toLocaleString(undefined): "?"}}</div>
                    <div  class="hidden">
                        <h3>Most prominent variant: {{strategyList[strategyIndex]["regionParameters"].variant.name}} </h3>
                        <div>
                            <VariantList  @change="onVariantChnage"></VariantList>
                        </div>
                    </div>
                    
                    <h3>Basic reproduction number: {{strategyList[strategyIndex]["regionParameters"].infectiousnessLevel}} </h3>
                    <InputNumber  v-model="strategyList[strategyIndex]['regionParameters'].infectiousnessLevel" :allowEmpty="false" :min="0" :max="100" :minFractionDigits="2" :maxFractionDigits="2"/>
                    <Message severity="error" v-if="strategyList[strategyIndex]['regionParameters'].infectiousnessLevel <= 0"  :closable="false"> Reproduction number needs to be a positive number.</Message>
                    <p class="mt-6">The basic reproduction number (R_0) is defined as the average number of secondary cases an infected individual will generate in a fully susceptible population.</p>
                    <p>NOTE: This is different from the Effective Reproductive number, which measures the average number of secondary cases per infectious case in a population made up of both susceptible and non-susceptible hosts.</p>
                    <p>Based on the following article (*), we recommend:</p>
                    <ul>
                        <li>R0 = 2 for ancestral strain</li>
                        <li>R0 = 4 for alpha</li>
                        <li>R0 = 6 for delta</li>
                        <li>R0 = 12 for omicron and subsequent strains</li>
                    </ul>
                    <p>[*] Moore, S., Hill, E.M., Dyson, L. et al. <em>Retrospectively modeling the effects of increased global vaccine sharing on the COVID-19 pandemic</em>. Nat Med (2022). <a href="https://doi.org/10.1038/s41591-022-02064-y" target="_blank">https://doi.org/10.1038/s41591-022-02064-y</a></p>
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