<script setup>

import { storeToRefs } from 'pinia'
import { useRouter, useRoute } from 'vue-router';
import MySlider from "../components/MySlider.vue";
import Button from 'primevue/button';
import Divider from "primevue/divider";
import Footer from "../components/Footer.vue";
import Header from "../components/Header.vue";
import SideBar from "../components/SideBar.vue";

/*
import { useSocialDistancingStore } from '@/stores/social-distancing';
const scStore = useSocialDistancingStore();


const { homeSCLevel, workSCLevel, schoolSCLevel, otherSCLevel} = storeToRefs(scStore);
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

let sdParameters = currentStrategy["regionParameters"]["socialDistancing"];


function onHomeSCLevelChange(newData) {
    console.log(`onHomeSCLevelChange: ${JSON.stringify(newData)}`);
    sdParameters.homeSCLevel = newData;

    /*
    scStore.$patch({
        homeSCLevel: newData
    });
    */
}

function onWorkSCLevelChange(newData) {
    console.log(`onWorkSCLevelChange: ${JSON.stringify(newData)}`);
    sdParameters.workSCLevel = newData;
    /*
    scStore.$patch({
        workSCLevel: newData
    });
    */
}

function onSchoolSCLevelChange(newData) {
    console.log(`onSchoolSCLevelChange: ${JSON.stringify(newData)}`);
    sdParameters.schoolSCLevel = newData;

    /*
    scStore.$patch({
        schoolSCLevel: newData
    });
    */
}

function onOtherSCLevelChange(newData) {
    console.log(`onOtherSCLevelChange: ${JSON.stringify(newData)}`);
    sdParameters.otherSCLevel = newData;

    /*
    scStore.$patch({
        otherSCLevel: newData
    });
    */
}

const router = useRouter();
const onNextClick = (event) => {
  router.push('/infection-status')
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
            <h1>Social Distancing</h1>
            <Divider class="fh-divider-primary"></Divider>
            <div class="grid">
                <div class="col">
                    <h3>Are people practicing social distancing at home?</h3>
                    <MySlider :min="0" :max="1" :step="0.05" :initial="sdParameters.homeSCLevel" minLabl="Not at all" maxLabel="Fully" @change="onHomeSCLevelChange"></MySlider>

                    <h3>Are people practicing social distancing at work?</h3>
                    <MySlider :min="0" :max="1" :step="0.05" :initial="sdParameters.workSCLevel" minLabl="Not at all" maxLabel="Fully" @change="onWorkSCLevelChange"></MySlider>

                    <h3>Are people practicing social distancing at school?</h3>
                    <MySlider :min="0" :max="1" :step="0.05" :initial="sdParameters.schoolSCLevel" minLabl="Not at all" maxLabel="Fully" @change="onSchoolSCLevelChange"></MySlider>

                    <h3>Are people practicing social distancing at other locations?</h3>
                    <MySlider :min="0" :max="1" :step="0.05" :initial="sdParameters.otherSCLevel" minLabl="Not at all" maxLabel="Fully" @change="onOtherSCLevelChange"></MySlider>
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