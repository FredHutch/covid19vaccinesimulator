<script setup>
import { storeToRefs } from "pinia";
import { useRouter, useRoute } from "vue-router";
import { watch } from 'vue';
import GeneralUtility from "../lib/GeneralUtility.mjs";
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
import InputNumber from "primevue/inputnumber";

import Calendar from 'primevue/calendar';

import { ref, computed, onMounted, reactive } from "vue";


import { DateTime } from 'luxon';

import { useStrategiesStore } from '../stores/strategies';
import { useAgeGroupStore } from "@/stores/age-group";



import { useVaccineSelectionStore } from '@/stores/vaccine-selection';




//import { useVaccinationStatusStore } from "@/stores/vaccination-status";

/*
const vaccineStore = useVaccineSelectionStore();
const { vaccine1, vaccine2, vaccine3, vaccineAvailability} = storeToRefs(vaccineStore);
console.log(`vaccine1: ${JSON.stringify(vaccine1)}`);
console.log(`vaccine2: ${vaccine2}`);
console.log(`vaccine3: ${vaccine3}`);
*/

const ageGroupStore = useAgeGroupStore();
const { groupIndexLabelMap} = storeToRefs(ageGroupStore);


//import { useStrategiesStore } from '../stores/strategies';
const strategiesStore = useStrategiesStore();
const { strategyList, selectedStrategyIndex } = storeToRefs(strategiesStore);
// let currentStrategy = strategyList.value[selectedStrategyIndex.value];

// this works
// weird... it didn't work sometime?!?
//strategiesStore.addStrategy();

let strategyIndex = selectedStrategyIndex.value;

/*
if(route.query.strategy != undefined){
    strategyIndex = Number(route.query.strategy);
    strategiesStore.selectStrategy(strategyIndex);
}
*/
let currentStrategy = strategyList.value[strategyIndex];

let vaccineList = currentStrategy["vaccineParameters"]["vaccineList"];

let vaccinationStatusByAgeGroup =
  currentStrategy["vaccineParameters"]["vaccinationStatusByAgeGroup"];


let vaccineAvailability = vaccineList;


strategiesStore.$subscribe((mutation, state) => {
  console.log(`strategiesStore.$subscribe: state change`);
  /*
  // import { MutationType } from 'pinia'
  mutation.type // 'direct' | 'patch object' | 'patch function'
  // same as cartStore.$id
  mutation.storeId // 'cart'
  // only available with mutation.type === 'patch object'
  mutation.payload // patch object passed to cartStore.$patch()
  */

  updateSimulationParameters();

})

// URL: work if enter URL direclty, but not with roouter

const router = useRouter();
const route = useRoute();

/*
let groupIndex = ref(1);

let urlParams = new URLSearchParams(window.location.search);
let groupIndex = ref(1);
groupIndex = urlParams.get('group') != undefined && urlParams.get('group').length > 0? Number(urlParams.get('group')): 1;
*/

//groupIndex = Number(route.query.group);

let groupIndex = computed(() => {
  return route.query.group != undefined? Number(route.query.group): 1;
});

let onlyGroupName = computed(() => {
  return `group${groupIndex.value}`;
});
console.log(`query params: group: ${groupIndex.value}`);






/*
let groupIndex = ref(1);
groupIndex = Number(route.params.groupIndex);
//let groupIndex = Number(route.params.groupIndex);

let onlyGroupName = `group${groupIndex}`;
*/
/*
const onlyGroupName = computed(() => {
  return `group${groupIndex}`;
});
*/

//
console.log(`groupIndex: ${groupIndex}`);
console.log(`onlyGroupName: ${onlyGroupName}`);

console.log(`onlyGroupName.value: ${onlyGroupName.value}`);

console.log(`onlyGroupName.value type: ${typeof onlyGroupName.value}`);


watch(
    () => route.query.group,
    async newGroupIndex => {

      console.log(`groupIndex (before assignment): ${groupIndex.value}`);
      
      //groupIndex = newGroupIndex;
      /*
      onlyGroupName = `group${groupIndex}`;
      */
      //console.log(`new groupIndex: ${groupIndex}`);
      console.log(`new onlyGroupName (before assignment): ${onlyGroupName.value}`);
    }
)



const onNextClick = (event) => {
  router.push({ path: '/vaccine-plan-period'});
};





const combinedColumns = reactive([
  { field: "category", header: "Category" },
  { field: "number", header: "Number" },
  { field: "date", header: "Available on" },
  { field: "rate", header: "Vaccination rate" }
]);



// 
const sortedVaccineAvailability = computed(() => {

  console.log(`sortedVaccineAvailability: ${JSON.stringify(vaccineAvailability)}`);
  return vaccineAvailability.slice();
  
  // disable sorting for now
  /*
  .sort((a, b) => {
    return b["date"].getTime() - a["date"].getTime();
  } );
  */
});


function onVaccinationStatusChange(event) {
  let { data, newValue, field } = event;

  console.log(`onVaccinationStatusChange: ${JSON.stringify(data, null, 2)}, ${field}, ${newValue}`);

  console.log(`onVaccinationStatusChange vaccinationStatusByAgeGroup.value[onlyGroupName]: ${JSON.stringify(vaccinationStatusByAgeGroup.value[onlyGroupName.value])}`);


  console.log(`onVaccinationStatusChange vaccinationStatusByAgeGroup.value: ${JSON.stringify(vaccinationStatusByAgeGroup.value)}`);



  console.log(`onVaccinationStatusChange vaccinationStatusByAgeGroup.value type: ${typeof vaccinationStatusByAgeGroup.value}`);



  let newData = {...(vaccinationStatusByAgeGroup.value)};

  console.log(`onVaccinationStatusChange vaccinationStatusByAgeGroup newData (before change): ${JSON.stringify(newData, null, 2)}`);

  newData[onlyGroupName.value] = newData[onlyGroupName.value].map((item) => {
    if( item["category"] == data["category"]){
      return data;
    }
    else{
      return item;
    }
  });

  // now, calibrate the uninfected
  for(let i = 1; i < 6; i++){
    newData[onlyGroupName.value][3][field] = 100 - newData[onlyGroupName.value][0][field] - newData[onlyGroupName.value][1][field] - newData[onlyGroupName.value][2][field];
  }


  console.log(`onVaccinationStatusChange newData (after change): ${JSON.stringify(newData)}`);

  vaccinationStore.$patch({
      vaccinationStatusByAgeGroup: newData,
  });

}

const onCellEditComplete = (event) => {
  let { data, newValue, field } = event;

  console.log(`onCellEditComplete: ${JSON.stringify(data, null, 2)}, ${field}, ${newValue}`);
  console.log(`onCellEditComplete typeof newValue: ${typeof newValue}`);

  switch (field) {
    case "number":
      if (GeneralUtility.isPositiveInteger(newValue)) {
        console.log(`${newValue} is a positive integer`);
        data[field] = Number(newValue);
        //onVaccinationStatusChange(event);
      }
      else {
        console.log(`${newValue} is not a positive integer`);
        event.preventDefault();
      }
      break;
    case "date":
      console.log(`onCellEditComplete date: ${newValue}`);
     
      //console.log(`onCellEditComplete date: ${DateTime.fromJSDate(newValue).toISODate()}`);
      //data[field] = DateTime.fromJSDate(newValue).toISODate();

      data[field] = newValue;

            /*
      if (GeneralUtilityisPositiveInteger(newValue)) {
        //data[field] = Number(newValue);
        //onVaccinationStatusChange(event);
      }
      else 
      */
      //event.preventDefault();
      break;
    default:
      //if (newValue.trim().length > 0) data[field] = newValue;
      //else event.preventDefault();
      break;
  }
};

const onCalendarInput = (event) => {
  console.log(`onCalendarInput: ${event}`);
};



const onCalendarHide = (event) => {
  console.log(`onCalendarHide`);
};

const updateSimulationParameters = () => {
  console.log(`updateSimulationParameters`);
  strategiesStore.updateSimulationParametersByStrategyIndex(strategyIndex);
}

const onCalendarDateSelect = (event) => {
  console.log(`onCalendarDateSelect: new value: ${event.value}`);
  onCellEditComplete(event);

  //updateSimulationParameters();
};

const onNumberInput = (event) => {
  console.log(`onNumberInput: new value: ${event.value}`);
  //updateSimulationParameters();
};


const convertVaccineLabel = (placholderName) => {
  console.log(`convertVaccineLabel: ${placholderName}`);

  let result = "";

  switch(placholderName){
    case "Vaccine 1":
      result =  vaccineList[0].name;
      break;
    case "Vaccine 2":
      result =  vaccineList[1].name;
      break;
    case "Vaccine 3":
      result =  vaccineList[2].name;
      break;
    default:
      result =  "";
      break;
  }

  if (result == undefined || result == ""){
    result = placholderName;
  }

  console.log(`convertVaccineLabel result: ${result}`);

  return result;
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
      
      <h1>Vaccine Availablity Timeline</h1>
      <Divider class="fh-divider-primary"></Divider>
      <div class="grid">
        <div class="col" style="padding-right: 0px;">
          <DataTable
            :value="strategyList[strategyIndex].vaccineParameters.vaccineList"
            editMode="cell"
            @cell-edit-complete="onCellEditComplete"
            responsiveLayout="scroll"
          >
            <Column
              v-for="col of combinedColumns"
              :field="col.field"
              :header="col.header"
              :key="col.field"
              style="width: 18%"
              headerClass="fh-table-header"
            >
              <template  v-if="col.field == 'category'" #body="slotProps">
                <div>{{ convertVaccineLabel(slotProps.data.category)}}</div>
              </template>
              <template  v-else-if="col.field == 'number'" #body="slotProps">
                <div><InputNumber @input="onNumberInput" :allowEmpty="false" mode="decimal" :min="0"  v-model="slotProps.data[slotProps.field]" /></div>
              </template>
              <template  v-else-if="col.field == 'date'" #body="slotProps">
                <div>
                  <Calendar :id="0" v-model="slotProps.data[slotProps.field]" dateFormat="yy-mm-dd" :touchUI="true"

                  @input="onCalendarInput"

                  @date-select="onCalendarDateSelect({data: vaccineAvailability[0], newValue: vaccineAvailability[0]['date'], field: 'date'})"

                  @hide="onCalendarHide"

                  ></Calendar>

                </div>
              </template>
              <template  v-else-if="col.field == 'rate'" #body="slotProps">
                <div><InputNumber @input="onNumberInput"  mode="decimal" :allowEmpty="false" :min="0" v-model="slotProps.data[slotProps.field]" /></div>
              </template>
            </Column>
          </DataTable>
          
        </div>
      </div>
      <br />
        <br />
        <div>* A course of vaccine is defined to be the required number of doses to be considered fully vaccinated with a primary series vaccination or boosted. For example, you need 2 doses of the COMIRNATY (Pfizer/BioNTech) vaccine for the primary series but only one dose for the CONVIDECIA (CanSino) vaccine. Boosters are assumed to be a single dose per course.</div>

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
  <table style="width:100%; border-collapse:collapse;" class="hidden">
            <thead>
            <tr style="height:75px; background-color:#F8F9FA;" class="fh-table-header">
              <th style="width:25%; text-align: left;">Category</th>
              <th style="width:25%; text-align: left;">Number(*)</th>
              <th style="width:25%; text-align: left;">Available on</th>
              <th style="width:25%; text-align: left;">Vaccination Rate</th>
            </tr>
            </thead>
            <tbody>
            <tr style="height:75px">
              <td>{{convertVaccineLabel(vaccineAvailability[0]["category"])}}</td>
              <td><InputNumber @input="onNumberInput" :allowEmpty="false" mode="decimal" :allowEmpty="false" :min="0"  v-model="vaccineAvailability[0]['number']" /></td>
              <td><Calendar :id="0" v-model="vaccineAvailability[0]['date']" dateFormat="yy-mm-dd" :touchUI="true"

                @input="onCalendarInput"
                
                @date-select="onCalendarDateSelect({data: vaccineAvailability[0], newValue: vaccineAvailability[0]['date'], field: 'date'})"
                
                @hide="onCalendarHide"
                
                ></Calendar></td>
                <td><InputNumber @input="onNumberInput"  mode="decimal" :allowEmpty="false" :min="0" v-model="vaccineAvailability[0]['rate']" /></td>
            </tr>
            <tr style="height:75px">
              <td>{{convertVaccineLabel(vaccineAvailability[1]["category"])}}</td>
              <td><InputNumber @input="onNumberInput" :allowEmpty="false" mode="decimal" :min="0"  v-model="vaccineAvailability[1]['number']" /></td>
              <td><Calendar :id="1" v-model="vaccineAvailability[1]['date']" dateFormat="yy-mm-dd" :touchUI="true"

                @input="onCalendarInput"
                
                @date-select="onCalendarDateSelect({data: vaccineAvailability[1], newValue: vaccineAvailability[1]['date'], field: 'date'})"
                
                @hide="onCalendarHide"
                
                /></td>
                <td><InputNumber @input="onNumberInput" :allowEmpty="false" mode="decimal" :min="0"  v-model="vaccineAvailability[1]['rate']" /></td>
            </tr>
            <tr style="height:75px">
              <td>{{convertVaccineLabel(vaccineAvailability[2]["category"])}}</td>
              <td><InputNumber @input="onNumberInput" :allowEmpty="false" mode="decimal" :min="0"  v-model="vaccineAvailability[2]['number']" /></td>
              <td><Calendar :id="2" v-model="vaccineAvailability[2]['date']" dateFormat="yy-mm-dd" :touchUI="true"

                @input="onCalendarInput"
                
                @date-select="onCalendarDateSelect({data: vaccineAvailability[2], newValue: vaccineAvailability[2]['date'], field: 'date'})"
                
                @hide="onCalendarHide"
                
                /></td>
                <td><InputNumber @input="onNumberInput" :allowEmpty="false" mode="decimal" :min="0"  v-model="vaccineAvailability[2]['rate']" /></td>
            </tr>
            </tbody>
          </table>
-->