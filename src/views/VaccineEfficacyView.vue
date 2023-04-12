<script setup>
import { storeToRefs } from "pinia";
import { useRouter, useRoute } from "vue-router";
import { watch } from "vue";
import GeneralUtility from "../lib/GeneralUtility.mjs";
import MySlider from "../components/MySlider.vue";
import Button from "primevue/button";
import Divider from "primevue/divider";
import Footer from "../components/Footer.vue";
import Header from "../components/Header.vue";
import SideBar from "../components/SideBar.vue";
import MySelectButton from "../components/MySelectButton.vue";

import DataTable from "primevue/datatable";
import Column from "primevue/column";
import ColumnGroup from "primevue/columngroup"; //optional for column grouping
import Row from "primevue/row";
import InputText from "primevue/inputtext";
import InputNumber from "primevue/inputnumber";
import voca from 'voca';

import { ref, computed, onMounted, reactive } from "vue";

import { useAgeGroupStore } from "@/stores/age-group";

import { useStrategiesStore } from "../stores/strategies";

/*
import { useVaccineSelectionStore } from '@/stores/vaccine-selection';
import { useVaccinationStatusStore } from "@/stores/vaccination-status";
*/
/*
const vaccineStore = useVaccineSelectionStore();
const { vaccine1, vaccine2, vaccine3, vaccine1EfficacyData, vaccine2EfficacyData, vaccine3EfficacyData} = storeToRefs(vaccineStore);
*/

const ageGroupStore = useAgeGroupStore();
const { groupIndexLabelMap } = storeToRefs(ageGroupStore);

//const vaccinationStore = useVaccinationStatusStore();
//const { vaccinationStatusByAgeGroup} = storeToRefs(vaccinationStore);

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

let vaccineIndex = computed(() => {
  return route.query.vaccine != undefined ? Number(route.query.vaccine) : 1;
});

console.log(`query params: vaccine: ${route.query.vaccine}`);
console.log(`vaccineIndex: ${vaccineIndex.value}`);

let vaccineInfo = computed(() => {
  console.log(
    `vaccineInfo computed vaccineIndex: ${Number(vaccineIndex.value)}`
  );
  console.log(
    `vaccineInfo computed vaccineList.length: ${vaccineList.length}`
  );
  switch (Number(vaccineIndex.value)) {
    case 1:
      return vaccineList[0];
    case 2:
      return vaccineList[1];
    case 3:
      return vaccineList[2];
    default:
      return;
  }
});

console.log(`vaccineInfo: ${JSON.stringify(vaccineInfo.value)}`);

let vaccineEfficacyData = computed(() => {
  console.log(
    `vaccineEfficacyData computed vaccineIndex: ${vaccineIndex.value}`
  );
  console.log(
    `vaccineEfficacyData computed typeof vaccineIndex.value: ${typeof vaccineIndex.value}`
  );
  console.log(
    `vaccineEfficacyData computed vaccineList.length: ${vaccineList.length}`
  );

  let result = undefined;

  switch (vaccineIndex.value) {
    case 1:
      console.log(`vaccineEfficacyData match: ${vaccineIndex.value}`);
      console.log(`vaccineEfficacyData vaccineList[0]: ${JSON.stringify(vaccineList[0], null, 2)}`);
      console.log(`vaccineEfficacyData vaccineList[0]["efficacyData"]: ${vaccineList[0]["efficacyData"]}`);
      result = vaccineList[0]["efficacyData"];
      break;
    case 2:
      console.log(`vaccineEfficacyData match: ${vaccineIndex.value}`);
      console.log(`vaccineEfficacyData vaccineList[1]: ${JSON.stringify(vaccineList[1], null, 2)}`);
      console.log(`vaccineEfficacyData vaccineList[1]["efficacyData"]: ${vaccineList[1]["efficacyData"]}`);
      result = vaccineList[1]["efficacyData"];
      break;
    case 3:
      console.log(`vaccineEfficacyData match: ${vaccineIndex.value}`);
      console.log(`vaccineEfficacyData vaccineList[2]: ${JSON.stringify(vaccineList[2], null, 2)}`);
      console.log(`vaccineEfficacyData vaccineList[2]["efficacyData"]: ${vaccineList[2]["efficacyData"]}`);
      result = vaccineList[2]["efficacyData"];
      break;
    default:
      console.log(`vaccineEfficacyData no match: ${vaccineIndex.value}`);
      break;
  }

  console.log(`vaccineEfficacyData result: ${result}`);

  return result;
});

console.log(
  `vaccineEfficacyData: ${JSON.stringify(vaccineEfficacyData.value, null, 2)}`
);

watch(
  () => route.query.vaccine,
  async (newIndex) => {
    console.log(`vaccineIndex (before assignment): ${vaccineIndex.value}`);
  }
);

function sleep(ms) {
  console.log(`sleep for ${ms}`);
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const onNextClick = async (event) => {


  await sleep(200);

  if (vaccineIndex.value < 3) {
    router.push({
      path: "/vaccine-efficacy",
      query: { vaccine: vaccineIndex.value + 1 },
    });
    //router.push(`/vaccination-by-age/${groupIndex + 1}`);
  } else {
    router.push({ path: "/vaccine-availability-timeline" });
  }
};


const combinedColumns = reactive([
  { field: "category", header: "Category" },
  { field: "fulldose", header: "Primary series" },
  { field: "booster", header: "Booster" },
]);

// vaccinationStatusByAgeGroup
/*
const vaccinationByAgeGroup = computed(() => {
  return vaccinationStatusByAgeGroup.value[onlyGroupName.value].filter((data) => {
    return data['category'] != "Unvaccinated";
  });
});
*/



function onVaccineEfficacyChange(event) {
  let { data, newValue, field } = event;

  console.log(
    `onVaccineEfficacyChange: ${JSON.stringify(
      data,
      null,
      2
    )}, ${field}, ${newValue}`
  );

  console.log(
    `onVaccineEfficacyChange vaccineEfficacyData: ${JSON.stringify(
      vaccineEfficacyData.value
    )}`
  );

  console.log(
    `onVaccineEfficacyChange vaccineEfficacyData.value type: ${typeof vaccineEfficacyData.value}`
  );

  let newData = [...vaccineEfficacyData.value];

  console.log(
    `onVaccineEfficacyChange vaccineEfficacyData newData (before change): ${JSON.stringify(
      newData,
      null,
      2
    )}`
  );

  newData = newData.map((item) => {
    if (item["category"] == data["category"]) {
      return data;
    } else {
      return item;
    }
  });

  console.log(
    `onVaccineEfficacyChange newData (after change): ${JSON.stringify(newData)}`
  );

  switch (vaccineIndex.value) {
    case 1:
      vaccineList[0]["efficacyData"] = newData;
      break;
    /*
        vaccineStore.$patch({
            vaccine1EfficacyData: newData,
        });
        
        */
    case 2:
      vaccineList[1]["efficacyData"] = newData;
      break;
      /*
        vaccineStore.$patch({
            vaccine2EfficacyData: newData,
        });
        */
      break;
    case 3:
      vaccineList[2]["efficacyData"] = newData;
      break;
      /*
        vaccineStore.$patch({
            vaccine3EfficacyData: newData,
        });
        */
      break;
    default:
      return;
  }
}

const onCellEditComplete = (event) => {
  let { data, newValue, field } = event;

  console.log(
    `onCellEditComplete: ${JSON.stringify(
      data,
      null,
      2
    )}, ${field}, ${newValue}`
  );
  console.log(`onCellEditComplete typeof newValue: ${typeof newValue}`);

  switch (field) {
    case "fulldose":
      if (GeneralUtility.isPositiveNumber(newValue)) {
        data[field] = Number(newValue);
        onVaccineEfficacyChange(event);
      } else event.preventDefault();
      break;
    case "booster":
      if (GeneralUtility.isPositiveNumber(newValue)) {
        data[field] = Number(newValue);
        onVaccineEfficacyChange(event);
      } else event.preventDefault();
      break;
    default:
      //if (newValue.trim().length > 0) data[field] = newValue;
      //else event.preventDefault();
      break;
  }
};

const convertVaccineLabel = (placholderName) => {
  console.log(`convertVaccineLabel: ${JSON.stringify(placholderName)}`);

  console.log(`vaccine1.name: ${vaccineList[0].name}`);

  let result = "";

  switch (placholderName) {
    case "Vaccine 1":
      result = vaccineList[0].name;
      break;
    case "Vaccine 2":
      result = vaccineList[1].name;
      break;
    case "Vaccine 3":
      result = vaccineList[2].name;
      break;
    case undefined:
      result = "vaccine";
      break;
    default:
      result = "";
      break;
  }

  console.log(`convertVaccineLabel result: ${result}`);

  return result;
};


const onInputBlur = (event, obj, vaccineLabel) => {
  console.log(`onInputBlur: vaccineLabel: ${vaccineLabel}`);
  console.log(
    `onInputBlur: data ${JSON.stringify(obj.data)}, field: ${JSON.stringify(
      obj.field
    )}, value: ${event.value}, type: ${typeof event.value}`
  );
  //obj.data[obj.field] = event.value;


  let inputValue = Number(voca.replaceAll(event.value, ",", ""));
  let resultValue = 0;

  resultValue = Math.min(Math.max(inputValue, 0), 100);

  console.log(
    `onInputBlur: inputValue: ${inputValue}, resultValue: ${resultValue}`
  );



  console.log(`currentStrategy["vaccineParameters"]["vaccineList"][vaccineIndex.value-1]["efficacyData"]: ${JSON.stringify(currentStrategy["vaccineParameters"]["vaccineList"][vaccineIndex.value-1]["efficacyData"])}`);

  currentStrategy["vaccineParameters"]["vaccineList"][vaccineIndex.value - 1]["efficacyData"].filter((eInfo) => {
    return eInfo.category == obj.data.category;
  })[0][obj.field] = resultValue;

};

// <h1>Vaccine Effectiveness (%) for {{convertVaccineLabel(vaccineInfo.value.name)}}</h1>
</script>

<template>
  <div class="grid" :key="vaccineIndex.value">
    <div class="col-2">
      <div class="mt-7"></div>
      <div class="sticky top-0"><SideBar></SideBar></div>
    </div>
    <div class="col ml-4">
      <div class="sticky top-0"><Header></Header></div>
      <h1>
        Vaccine Effectiveness (%) for
        {{ vaccineInfo.name != undefined ? vaccineInfo.name : "vaccine" }}
      </h1>
      <Divider class="fh-divider-primary"></Divider>
      <h3>
        Here is the vaccine effectiveness data to the best of our knowledge. You
        could review, edit, and confirm the default parameters we provide.
      </h3>
      <h3>Primary series vs. Booster</h3>
      <div class="grid">
        <div class="col" style="padding-right: 0px">
          <DataTable
            :value="vaccineEfficacyData"
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
              <!--
              <template v-if="col.field == 'category'">
                <div>{{  convertVaccineLabel(field)}}</div>
              </template>
              -->
              <template v-if="col.field == 'category'">
                <div>{{ field }}</div>
              </template>
              <template v-if="col.field != 'category'" #editor="slotProps">
                <InputNumber mode="decimal" :minFractionDigits="0" :maxFractionDigits="2" :allowEmpty="false" :min="0" :max="100" v-model="slotProps.data[slotProps.field]" 
                @blur="
                      (event) => {
                        onInputBlur(event, slotProps, slotProps.field);
                      }
                    "
                />
              </template>
            </Column>
          </DataTable>
        </div>
        <p>Vaccine effectiveness default values are provided for the major vaccine products for your convenience, but they can be modified as needed. Vaccine boosters were assumed to be as efficacious as primary series vaccination against the ancestral variant. Details about how vaccine effectiveness values were inferred can be found in the companion paper.</p>
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
