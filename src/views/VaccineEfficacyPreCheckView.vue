<script setup>
import { ref } from 'vue';
import { storeToRefs } from 'pinia'
import { useRouter, useRoute } from 'vue-router';
import MySlider from "../components/MySlider.vue";
import Button from 'primevue/button';
import Divider from "primevue/divider";
import RadioButton from 'primevue/radiobutton';
import Footer from "../components/Footer.vue";
import Header from "../components/Header.vue";
import SideBar from "../components/SideBar.vue";
import MySelectButton from "../components/MySelectButton.vue";

import MyRadioButtonGroup from '../components/MyRadioButtonGroup.vue';

import { useVaccineSelectionStore } from '@/stores/vaccine-selection';
const vaccineStore = useVaccineSelectionStore();
const { vaccine1, vaccine2, vaccine3,  vaccine1Usage, vaccine2Usage, vaccine3Usage, vaccine1HasEfficacyData, vaccine2HasEfficacyData, vaccine3HasEfficacyData} = storeToRefs(vaccineStore);



function onVaccine1SelectionChange(newData) {
    console.log(`onVaccine1SelectionChange: ${JSON.stringify(newData)}`);
    
    vaccineStore.$patch({
        vaccine1HasEfficacyData: newData.value
    });
    
}

function onVaccine2SelectionChange(newData) {
    console.log(`onVaccine2SelectionChange: ${JSON.stringify(newData)}`);
    
    vaccineStore.$patch({
        vaccine2HasEfficacyData: newData.value
    });
    
}

function onVaccine3SelectionChange(newData) {
    console.log(`onVaccine3SelectionChange: ${JSON.stringify(newData)}`);
    
    vaccineStore.$patch({
        vaccine3HasEfficacyData: newData.value
    });
    
}

const options = ref([
    {name: 'Yes', key : "yes"},
    {name: 'No', key: "no"},
]);

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
            <h1>Vaccination Effectiveness Screening</h1>
            <Divider class="fh-divider-primary"></Divider>
            <div class="grid">
                <div class="col">
                    <h3>Do you have localized/regional data about the efficacy of "{{vaccine1.name}}"?</h3>
                    <MyRadioButtonGroup @change="onVaccine1SelectionChange" :options="options" :initialSelection="options[1]"></MyRadioButtonGroup>
                    <h3>Do you have localized/regional data about the efficacy of "{{vaccine2.name}}"?</h3>
                    <MyRadioButtonGroup @change="onVaccine2SelectionChange" :options="options" :initialSelection="options[1]"></MyRadioButtonGroup>
                    <h3>Do you have localized/regional data about the efficacy of "{{vaccine3.name}}"?</h3>
                    <MyRadioButtonGroup @change="onVaccine3SelectionChange" :options="options" :initialSelection="options[1]"></MyRadioButtonGroup>
                    <p>We understand that oftentimes it might be difficult to obtain such data. If you choose "No," we will provide default parameters to the best of our knowledge.</p>
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