<script setup>
import { storeToRefs } from "pinia";
import { useRouter, useRoute } from "vue-router";
import Message from 'primevue/message';
import MySlider from "../components/MySlider.vue";
import Button from "primevue/button";
import Divider from "primevue/divider";
import Footer from "../components/Footer.vue";
import Header from "../components/Header.vue";
import SideBar from "../components/SideBar.vue";
import MySelectButton from "../components/MySelectButton.vue";
import Timeline from 'primevue/timeline';
import Chart from 'primevue/chart';
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import ColumnGroup from "primevue/columngroup"; //optional for column grouping
import Row from "primevue/row";
import InputText from "primevue/inputtext";
import Calendar from 'primevue/calendar';

import { ref, computed, onMounted, reactive, watch } from "vue";

import GeneralUtility from "../lib/GeneralUtility.mjs";

import { DateTime } from 'luxon';


import { useStrategiesStore } from '../stores/strategies';

//import { useStrategiesStore } from '../stores/strategies';
const strategiesStore = useStrategiesStore();
const { strategyList, selectedStrategyIndex } = storeToRefs(strategiesStore);
// let currentStrategy = strategyList.value[selectedStrategyIndex.value];

// this works
// weird... it didn't work sometime?!?
//strategiesStore.addStrategy();

let strategyIndex = selectedStrategyIndex.value;

let currentStrategy = strategyList.value[strategyIndex];

let simulationInterval = currentStrategy["simulationInterval"];

let needsLongerPeriodMsg = "Too few days for the simulation. Please lengthen the simulation period long enough to cover the arrival of the first vaccine and the number of days needed to apply all vaccines.";






// URL: work if enter URL direclty, but not with roouter

const router = useRouter();
const route = useRoute();




const onNextClick = (event) => {
  router.push({ path: '/additional-parameters'});
};

const onCalendarInput = (event) => {
  console.log(`onCalendarInput: ${event}`);
};

const onCalendarDateSelect = (event) => {
  console.log(`onCalendarDateSelect: ${event}`);

  let { data, newValue, index } = event;

  console.log(`onCalendarDateSelect: ${JSON.stringify(data, null, 2)}, ${index}, ${newValue}`);

  let newInterval = [...data];
  newInterval[index] = newValue; //DateTime.fromJSDate(newValue).startOf("day").toJSDate();

  currentStrategy["simulationInterval"] = newInterval;


  // version 2, use  GeneralUtility
  currentStrategy["simulationDays"]  = GeneralUtility.diffDateByUnits(newInterval[0], newInterval[1], "days");

};

const onCalendarHide = (event) => {
  console.log(`onCalendarHide`);
};


const isPeriodValid = computed(() => {

  //simulationInterval

  let dateDaysList = strategiesStore.getValidVaccineDateDaysListByStrategyIndex(strategyIndex);

  console.log(`isPeriodValid: simulationInterval: ${simulationInterval}`);

  let result = GeneralUtility.hasEnoughSimulationPeriod(simulationInterval[0], simulationInterval[1], dateDaysList);

  console.log(`isPeriodValid: ${result}`);

  return result;
});

// calculateStartAndEndWithDateAndDaysList

//let needsLongerPeriodMsg = "Too few days for the simulation. Please lengthen the simulation period long enough to cover the arrival of the first vaccine and the number of days needed to apply all vaccines.";

const recommendedPeriodMsg = computed(() => {

//simulationInterval

let dateDaysList = strategiesStore.getValidVaccineDateDaysListByStrategyIndex(strategyIndex);

let expectedInterval = GeneralUtility.calculateStartAndEndWithDateAndDaysList(dateDaysList);


let startDateTime = DateTime.fromJSDate(expectedInterval[0]);
let endDateTime = DateTime.fromJSDate(expectedInterval[1]);

let result = `The period should cover days between ${startDateTime.toFormat('yyyy-LL-dd')} and ${endDateTime.toFormat('yyyy-LL-dd')}.`;

return result;
});


</script>

<template>
  <div class="grid">
    <div class="col-2">
      <div class="mt-7"></div>
      <div class="sticky top-0"><SideBar></SideBar></div>
    </div>
    <div class="col ml-4">
      <div class="sticky top-0"><Header></Header></div>
      
      <h1>Period for Simulation</h1>
      <Divider class="fh-divider-primary"></Divider>
      <div>We will use our model and your input to estimate how vaccine allocation impacts the spread of COVID. Indicate the start date and end date for simulation.</div>
      <br />
      <div class="grid">

        <div class="col flex justify-content-end">
          Start date:&nbsp;<Calendar :id="0" v-model="simulationInterval[0]" dateFormat="yy-mm-dd" :touchUI="true"

            @input="onCalendarInput"

            @date-select="onCalendarDateSelect({data: simulationInterval, newValue: simulationInterval[0], index: 0})"

            @hide="onCalendarHide"

            />
        </div>
        <div class="col">
          End date:&nbsp;<Calendar :id="0" v-model="simulationInterval[1]" dateFormat="yy-mm-dd" :touchUI="true"

            @input="onCalendarInput"

            @date-select="onCalendarDateSelect({data: simulationInterval, newValue: simulationInterval[1], index: 1})"

            @hide="onCalendarHide"

            />
        </div>
      </div>

      <div>
          <Message severity="warn" v-if="false" :closable="false">{{fulldoseLessThanTotalMsg}}</Message>
          <Message severity="error" v-if="!isPeriodValid" :closable="false">{{needsLongerPeriodMsg}} {{recommendedPeriodMsg}} </Message>
      </div>

      <div>
        <div class="flex justify-content-center mt-4 mb-4">
          <Button
            label="Next"
            class="p-button-lg fh-button-primary"
            @click="onNextClick"
          ></Button>
        </div>
        <Divider class="fh-divider-primary"></Divider>
        <Footer></Footer>
      </div>
    </div>
    <div class="col-2"></div>
  </div>
</template>


<!--
  <div class="col" style="padding-right: 0px;">
          <table style="width:100%; border-collapse:collapse;">
            <thead>
            <tr style="height:75px; background-color:#F8F9FA;" class="fh-table-header">
              <th style="width:50%; text-align: left;">Start date</th>
              <th style="width:50%; text-align: left;">End date</th>
            </tr>
            </thead>
            <tbody>
            <tr style="height:75px">
              <td><Calendar :id="0" v-model="simulationInterval[0]" dateFormat="yy-mm-dd" :touchUI="true"

                @input="onCalendarInput"
                
                @date-select="onCalendarDateSelect({data: simulationInterval, newValue: simulationInterval[0], index: 0})"
                
                @hide="onCalendarHide"
                
                /></td>
              <td><Calendar :id="0" v-model="simulationInterval[1]" dateFormat="yy-mm-dd" :touchUI="true"

                @input="onCalendarInput"
                
                @date-select="onCalendarDateSelect({data: simulationInterval, newValue: simulationInterval[1], index: 1})"
                
                @hide="onCalendarHide"
                
                /></td>
            </tr>
            </tbody>
          </table>
        </div>  
  
  
-->