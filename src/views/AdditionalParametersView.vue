<script setup>
import { storeToRefs } from "pinia";
import { useRouter, useRoute } from "vue-router";
import GeneralUtility from "../lib/GeneralUtility.mjs";
import { ref, computed, onMounted, reactive } from "vue";
import { FilterMatchMode } from "primevue/api";

import MySlider from "../components/MySlider.vue";
import Button from "primevue/button";
import Divider from "primevue/divider";
import Footer from "../components/Footer.vue";
import Header from "../components/Header.vue";
import SideBar from "../components/SideBar.vue";

import DataTable from "primevue/datatable";
import Column from "primevue/column";
import ColumnGroup from "primevue/columngroup"; //optional for column grouping
import Row from "primevue/row";
import InputText from "primevue/inputtext";
import InputNumber from "primevue/inputnumber";
import Card from "primevue/card";
import Fieldset from "primevue/fieldset";
import Accordion from 'primevue/accordion';
import AccordionTab from 'primevue/accordiontab';
import { ageGroupList } from "../content/variable";
/*
import { useInfectionStatusStore } from "@/stores/infection-status";
const isStore = useInfectionStatusStore();
const { infectionStatusByAgeGroup } = storeToRefs(isStore);
*/

import { useStrategiesStore } from "../stores/strategies";
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

//let vaccineList = currentStrategy["vaccineParameters"]["vaccineList"];

//let isParameters = currentStrategy["regionParameters"]["infectionStatus"];

//let fParameters = currentStrategy["fixedParameters"];

function onInfectionStatusChange(event) {
  let { data, newValue, field } = event;

  /*
  {
    "category": "Uninfected",
    "group1": 34,
    "group2": 34,
    "group3": 34,
    "group4": 34,
    "group5": 34
  }, 
  group2, 
  50
  */

  console.log(`onInfectionStatusChange: ${JSON.stringify(data)}`);

  //let newData = [...infectionStatusByAgeGroup.value];
  let newData = [...strategyList.value[strategyIndex].regionParameters.infectionStatus];

  newData = newData.map((item) => {
    if (item["category"] == data["category"]) {
      return data;
    } else {
      return item;
    }
  });

  // now, calibrate the uninfected
  for (let i = 1; i < 6; i++) {
    let groupName = `group${i}`;
    newData[2][groupName] = 100 - newData[0][groupName] - newData[1][groupName];
  }

  strategyList.value[strategyIndex].regionParameters.infectionStatus = newData;

  /*
  isStore.$patch({
    infectionStatusByAgeGroup: newData,
  });
  */
}

const router = useRouter();
const onNextClick = (event) => {
  router.push("/result");
};

// <20, 20-49, 50-64, 65-74, >=75
const columns = reactive([
  { field: "category", header: "Category" },
  { field: "group1", header: "< 20" },
  { field: "group2", header: "20 - 49" },
  { field: "group3", header: "50 - 64" },
  { field: "group4", header: "65 - 74" },
  { field: "group5", header: ">= 75" },
]);

/*
let items = reactive([
  {
    category: "Previously Infected",
    group1: 33,
    group2: 33,
    group3: 33,
    group4: 33,
    group5: 33,
  },
  {
    category: "Infected",
    group1: 33,
    group2: 33,
    group3: 33,
    group4: 33,
    group5: 33,
  },
  {
    category: "Uninfected",
    group1: 34,
    group2: 34,
    group3: 34,
    group4: 34,
    group5: 34,
  },
]);
*/
/*
const group1Total = computed(() => {
  let propertyName = "group1";

  //let items = infectionStatusByAgeGroup.value;
  let items = isParameters;
  return (
    items[0][propertyName] + items[1][propertyName] + items[2][propertyName]
  );
});

const group2Total = computed(() => {
  let propertyName = "group2";
  //let items = infectionStatusByAgeGroup.value;
  let items = isParameters;
  return (
    items[0][propertyName] + items[1][propertyName] + items[2][propertyName]
  );
});

const group3Total = computed(() => {
  let propertyName = "group3";
  //let items = infectionStatusByAgeGroup.value;
  let items = isParameters;
  return (
    items[0][propertyName] + items[1][propertyName] + items[2][propertyName]
  );
});

const group4Total = computed(() => {
  let propertyName = "group4";
  //let items = infectionStatusByAgeGroup.value;
  let items = isParameters;
  return (
    items[0][propertyName] + items[1][propertyName] + items[2][propertyName]
  );
});

const group5Total = computed(() => {
  let propertyName = "group5";
  //let items = infectionStatusByAgeGroup.value;
  let items = isParameters;
  return (
    items[0][propertyName] + items[1][propertyName] + items[2][propertyName]
  );
});

const infectedByAgeGroup = computed(() => {
  // version 2
  // isParameters
  return isParameters.filter((data) => {
    return data["category"] != "Uninfected";
  });

});

const checkGroupTotal = (data, groupName, newValue) => {
  let validTotal = false;

  let result = 0;

  Object.keys(data).forEach((key) => {
    if (key == groupName) {
      result += newValue;
    } else {
      result += data[groupName];
    }
  });

  validTotal = result == 100;

  return validTotal;
};

const allGroupValid = computed(() => {
  console.log(
    `group1Total: ${group1Total.value}, group2Total: ${group2Total.value}, group3Total: ${group3Total.value}, group4Total: ${group4Total.value}, group5Total: ${group5Total.value}`
  );
  return (
    group1Total.value == 100 &&
    group2Total.value == 100 &&
    group3Total.value == 100 &&
    group4Total.value == 100 &&
    group5Total.value == 100
  );
});

*/

const ageGroupColumns = computed(() => {
  return ageGroupList.map((ageGroupInfo, index) => {
    // { field: "category", header: "Category" },
    return {field: index, header: ageGroupInfo.header};
  });

  let propertyName = "group1";

  //let items = infectionStatusByAgeGroup.value;
  let items = strategyList.value[strategyIndex].regionParameters.infectionStatus;
  return (
    items[0][propertyName] + items[1][propertyName] + items[2][propertyName]
  );
});

// strategyList.value[selectedStrategyIndex].fixedParameters.propSymptomaticInfection


const ageGroupParameters = computed(() => {
  // strategyList.value[strategyIndex].fixedParameters['propSymptomaticInfection'][0]
  // strategyList.value[strategyIndex].fixedParameters['relativeSusceptibility'][0]

  return [
    {
      category: "Proportion of symptomatic infections in each age group",
      group1: strategyList.value[strategyIndex].fixedParameters['propSymptomaticInfection'][0],
      group2: strategyList.value[strategyIndex].fixedParameters['propSymptomaticInfection'][1],
      group3: strategyList.value[strategyIndex].fixedParameters['propSymptomaticInfection'][2],
      group4: strategyList.value[strategyIndex].fixedParameters['propSymptomaticInfection'][3],
      group5: strategyList.value[strategyIndex].fixedParameters['propSymptomaticInfection'][4],
    },
    {
      category: "Relative susceptibility",
      group1: strategyList.value[strategyIndex].fixedParameters['relativeSusceptibility'][0],
      group2: strategyList.value[strategyIndex].fixedParameters['relativeSusceptibility'][1],
      group3: strategyList.value[strategyIndex].fixedParameters['relativeSusceptibility'][2],
      group4: strategyList.value[strategyIndex].fixedParameters['relativeSusceptibility'][3],
      group5: strategyList.value[strategyIndex].fixedParameters['relativeSusceptibility'][4],
    }
  ];



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
      
      <h1>Additional Parameters</h1>
      <Divider class="fh-divider-primary"></Divider>
      <div class="grid">
        <div class="col">
          <Accordion  :activeIndex="0">
            <AccordionTab header="Vaccine">
              <div class="grid">
              <div class="col"></div>
              <div class="col">
                <div class="grid">
                  <div class="col text-lg"><spam style="width: 100px;">{{strategyList[strategyIndex].vaccineParameters.vaccineList[0].name !=  ""?  strategyList[strategyIndex].vaccineParameters.vaccineList[0].name: "Vaccine 1" }}</spam></div>
                  <div class="col text-lg"><spam style="width: 100px;">{{strategyList[strategyIndex].vaccineParameters.vaccineList[1].name !=  ""?  strategyList[strategyIndex].vaccineParameters.vaccineList[1].name: "Vaccine 2" }}</spam></div>
                  <div class="col text-lg"><spam style="width: 100px;">{{strategyList[strategyIndex].vaccineParameters.vaccineList[2].name !=  ""?  strategyList[strategyIndex].vaccineParameters.vaccineList[2].name: "Vaccine 3" }}</spam></div>
                </div>
              </div>
            </div>
            <div class="grid">
              <div class="col">
                Mean duration of vaccine-induced immunity for vaccination with a
                primary series:
              </div>
              <div class="col">
                <div class="grid">
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 100px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0"
                  v-model="strategyList[strategyIndex].fixedParameters['meanDurationPrimaryImmunity'][0]"
                />
                  </div>
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 100px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0"
                  v-model="strategyList[strategyIndex].fixedParameters['meanDurationPrimaryImmunity'][1]"
                />
                  </div>
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 100px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0"
                  v-model="strategyList[strategyIndex].fixedParameters['meanDurationPrimaryImmunity'][2]"
                />
                  </div>
                </div>
                
              </div>
            </div>

            <div class="grid">
              <div class="col">
                Mean duration of immunity for vaccinated individuals with a
                primary series following a SARS-CoV-2 infection:
              </div>

              <div class="col">
                <div class="grid">
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 100px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0"
                  v-model="strategyList[strategyIndex].fixedParameters['meanDurationHybridImmunity'][0]"
                />

                  </div>
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 100px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0"
                  v-model="strategyList[strategyIndex].fixedParameters['meanDurationHybridImmunity'][1]"
                />

                  </div>
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 100px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0"
                  v-model="strategyList[strategyIndex].fixedParameters['meanDurationHybridImmunity'][2]"
                />

                  </div>

                </div>
                
              </div>
            </div>
            <div class="grid">
              <div class="col">
                Mean duration of vaccine-induced immunity for vaccination with a
                booster:
              </div>

              <div class="col">
                <div class="grid">
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 100px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0"
                  v-model="strategyList[strategyIndex].fixedParameters['meanDurationBoosterImmunity'][0]"
                />
                  </div>
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 100px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0"
                  v-model="strategyList[strategyIndex].fixedParameters['meanDurationBoosterImmunity'][1]"
                />
                  </div>
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 100px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0"
                  v-model="strategyList[strategyIndex].fixedParameters['meanDurationBoosterImmunity'][2]"
                />
                  </div>

                </div>
                
              </div>
            </div>

            <div class="grid">
              <div class="col">
                Mean duration of immunity for vaccinated individuals with a
                booster following a SARS-CoV-2 infection:
              </div>

              <div class="col">
                <div class="grid">
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 100px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0"
                  v-model="strategyList[strategyIndex].fixedParameters['meanDurationBoostedHybridImmunity'][0]"
                />
                  </div>
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 100px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0"
                  v-model="strategyList[strategyIndex].fixedParameters['meanDurationBoostedHybridImmunity'][1]"
                />
                  </div>
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 100px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0"
                  v-model="strategyList[strategyIndex].fixedParameters['meanDurationBoostedHybridImmunity'][2]"
                />
                  </div>

                </div>
                
              </div>
            </div>
            </AccordionTab>
            <AccordionTab header="Age-dependent parameters">
              <div class="grid">
              <div class="col"></div>
              <div class="col">
                <div class="grid">
                  <div class="col  text-lg" v-for="(ageGroup, index) in ageGroupList" :key="index">{{ ageGroup.header }}</div>
                </div>
              </div>
              
            </div>
            <div class="grid">
              <div class="col">
                Proportion of symptomatic infections in each age group:
              </div>

              <div class="col">
                <div class="grid">
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 80px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0" :max="1"
                  v-model="strategyList[strategyIndex].fixedParameters['propSymptomaticInfection'][0]"
                />
                  </div>
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 80px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0" :max="1"
                  v-model="strategyList[strategyIndex].fixedParameters['propSymptomaticInfection'][1]"
                />
                  </div>
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 80px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0" :max="1"
                  v-model="strategyList[strategyIndex].fixedParameters['propSymptomaticInfection'][2]"
                />
                  </div>
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 80px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0" :max="1"
                  v-model="strategyList[strategyIndex].fixedParameters['propSymptomaticInfection'][3]"
                />
                  </div>
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 80px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0" :max="1"
                  v-model="strategyList[strategyIndex].fixedParameters['propSymptomaticInfection'][4]"
                />
                  </div>
                </div>
                
              </div>
            </div>
            <div class="grid">
              <div class="col">Relative susceptibility:</div>

              <div class="col">
                <div class="grid">
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 80px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0" :max="1"
                  v-model="strategyList[strategyIndex].fixedParameters['relativeSusceptibility'][0]"
                />
                  </div>
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 80px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0" :max="1"
                  v-model="strategyList[strategyIndex].fixedParameters['relativeSusceptibility'][1]"
                />
                  </div>
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 80px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0" :max="1"
                  v-model="strategyList[strategyIndex].fixedParameters['relativeSusceptibility'][2]"
                />
                  </div>
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 80px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0" :max="1"
                  v-model="strategyList[strategyIndex].fixedParameters['relativeSusceptibility'][3]"
                />
                  </div>
                  <div class="col">
                    <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 80px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0" :max="1"
                  v-model="strategyList[strategyIndex].fixedParameters['relativeSusceptibility'][4]"
                />
                  </div>
                </div>
                
              </div>
            </div>
            </AccordionTab>
            <AccordionTab header="SARS-CoV-2 infection and Natural history">
              <div class="grid">
            <div class="col">
              Average time between symptom onset and hospitalization:
            </div>
            <div class="col">
              <InputNumber
                mode="decimal"
                inputClass="text-1xl"
                inputStyle="width: 100px;"
                :minFractionDigits="0"
                :maxFractionDigits="2"
                :allowEmpty="false" :min="0"
                v-model="
                  strategyList[strategyIndex].fixedParameters[
                    'averageTimeBetweenSymptomOnsetAndHospitalization'
                  ]
                "
              />
            </div>
          </div>
          <div class="grid">
            <div class="col">
              Mean Duration of Infectiousness after developing symptoms:
            </div>

            <div class="col">
              <InputNumber
                mode="decimal"
                inputClass="text-1xl"
                inputStyle="width: 100px;"
                :minFractionDigits="0"
                :maxFractionDigits="2"
                :allowEmpty="false" :min="0"
                v-model="strategyList[strategyIndex].fixedParameters['meanDurationInfectiousnessPostSymptoms']"
              />
            </div>
          </div>
          <div class="grid">
            <div class="col">Mean duration of hospitalization:</div>
            <div class="col">
              <InputNumber
                mode="decimal"
                inputClass="text-1xl"
                inputStyle="width: 100px;"
                :minFractionDigits="0"
                :maxFractionDigits="2"
                :allowEmpty="false" :min="0"
                v-model="strategyList[strategyIndex].fixedParameters['meanDurationHospitalization']"
              />
            </div>
          </div>

          <div class="grid">
            <div class="col">Mean duration of latent period:</div>
            <div class="col">
              <InputNumber
                mode="decimal"
                inputClass="text-1xl"
                inputStyle="width: 100px;"
                :minFractionDigits="0"
                :maxFractionDigits="2"
                :allowEmpty="false" :min="0"
                v-model="strategyList[strategyIndex].fixedParameters['meanDurationLatentPeriod']"
              />
            </div>
          </div>
          <div class="grid">
            <div class="col">Mean duration of pre-symptomatic period:</div>

            <div class="col">
              <InputNumber
                mode="decimal"
                inputClass="text-1xl"
                inputStyle="width: 100px;"
                :minFractionDigits="0"
                :maxFractionDigits="2"
                :allowEmpty="false" :min="0"
                v-model="strategyList[strategyIndex].fixedParameters['meanDurationPreSymptomaticPeriod']"
              />
            </div>
          </div>
          <div class="grid">
            <div class="col">
              Relative infectiousness of asymptomatic infected individuals:
            </div>

            <div class="col">
              <InputNumber
                mode="decimal"
                inputClass="text-1xl"
                inputStyle="width: 100px;"
                :minFractionDigits="0"
                :maxFractionDigits="2"
                :allowEmpty="false" :min="0"
                v-model="
                  strategyList[strategyIndex].fixedParameters['relativeInfectiousnessAsymptomaticInfection']
                "
              />
            </div>
          </div>
          <div class="grid">
            <div class="col">
              Relative infectiousness of hospitalized infected individuals:
            </div>

            <div class="col">
              <InputNumber
                mode="decimal"
                inputClass="text-1xl"
                inputStyle="width: 100px;"
                :minFractionDigits="0"
                :maxFractionDigits="2"
                :allowEmpty="false" :min="0"
                v-model="
                  strategyList[strategyIndex].fixedParameters['relativeInfectiousnessHospitalizedInfection']
                "
              />
            </div>
          </div>
          <div class="grid">
            <div class="col">
              Relative infectiousness of pre-symptomatic infected individuals:
            </div>

            <div class="col">
              <InputNumber
                mode="decimal"
                inputClass="text-1xl"
                inputStyle="width: 100px;"
                :minFractionDigits="0"
                :maxFractionDigits="2"
                :allowEmpty="false" :min="0"
                v-model="
                  strategyList[strategyIndex].fixedParameters['relativeInfectiousnessPreSymptomaticInfection']
                "
              />
            </div>
          </div>
          <div class="grid">
            <div class="col">
              Mean duration of immunity after SARS-CoV-2 infection (first
              phase):
            </div>

            <div class="col">
              <InputNumber
                mode="decimal"
                inputClass="text-1xl"
                inputStyle="width: 100px;"
                :minFractionDigits="0"
                :maxFractionDigits="2"
                :allowEmpty="false" :min="0"
                v-model="strategyList[strategyIndex].fixedParameters['meanDurationNatImmunityAfterInfection']"
              />
            </div>
          </div>
          <div class="grid">
            <div class="col">
              Mean duration of immunity after SARS-CoV-2 infection (second
              phase):
            </div>

            <div class="col">
              <InputNumber
                mode="decimal"
                inputClass="text-1xl"
                inputStyle="width: 100px;"
                :minFractionDigits="0"
                :maxFractionDigits="2"
                :allowEmpty="false" :min="0"
                v-model="strategyList[strategyIndex].fixedParameters['meanDurationNatImmunityAfterInfection2']"
              />
            </div>
          </div>
          <div class="grid">
            <div class="col">
              Mean duration of immunity for waned vaccinated individuals
              following a SARS-CoV-2 infection:
            </div>

            <div class="col">
              <InputNumber
                mode="decimal"
                inputClass="text-1xl"
                inputStyle="width: 100px;"
                :minFractionDigits="0"
                :maxFractionDigits="2"
                :allowEmpty="false" :min="0"
                v-model="strategyList[strategyIndex].fixedParameters['meanDurationImmunityWanedVaxHybrid']"
              />
            </div>
          </div>
            </AccordionTab>
            <AccordionTab header="Protection for partially susceptible individuals">
              <div class="grid">
            <div class="col">
              Protection against infection for partially susceptible
              individuals:
            </div>

            <div class="col">
              <InputNumber
                mode="decimal"
                inputClass="text-1xl"
                inputStyle="width: 100px;"
                :minFractionDigits="0"
                :maxFractionDigits="2"
                :allowEmpty="false" :min="0" :max="100"
                v-model="strategyList[strategyIndex].fixedParameters['VESUSpartiallySus']"
              />
            </div>
          </div>

          <div class="grid">
            <div class="col">
              Protection against symptomatic infection for partially
              susceptible individuals:
            </div>

            <div class="col">
              <InputNumber
                mode="decimal"
                inputClass="text-1xl"
                inputStyle="width: 100px;"
                :minFractionDigits="0"
                :maxFractionDigits="2"
                :allowEmpty="false" :min="0" :max="100"
                v-model="strategyList[strategyIndex].fixedParameters['VEDISpartiallySus']"
              />
            </div>
          </div>

          <div class="grid">
            <div class="col">
              Protection against hospitalization for partially
              susceptible individuals:
            </div>

            <div class="col">
              <InputNumber
                mode="decimal"
                inputClass="text-1xl"
                inputStyle="width: 100px;"
                :minFractionDigits="0"
                :maxFractionDigits="2"
                :allowEmpty="false" :min="0" :max="100"
                v-model="strategyList[strategyIndex].fixedParameters['VEHpartiallySus']"
              />
            </div>
          </div>

            </AccordionTab>
            <AccordionTab header="Protection for partially vaccinated (waned) individuals">
              <div class="grid">
            <div class="col">
              Protection against infection for partially susceptible
              vaccinated individuals:
            </div>

            <div class="col">
              <InputNumber
                mode="decimal"
                inputClass="text-1xl"
                inputStyle="width: 100px;"
                :minFractionDigits="0"
                :maxFractionDigits="2"
                :allowEmpty="false" :min="0"  :max="100"
                v-model="strategyList[strategyIndex].fixedParameters['VESUSpartiallySusVaccinated']"
              />
            </div>
          </div>

          <div class="grid">
            <div class="col">
              Protection against symptomatic infection for partially
              susceptible vaccinated individuals:
            </div>

            <div class="col">
              <InputNumber
                mode="decimal"
                inputClass="text-1xl"
                inputStyle="width: 100px;"
                :minFractionDigits="0"
                :maxFractionDigits="2"
                :allowEmpty="false" :min="0"  :max="100"
                v-model="strategyList[strategyIndex].fixedParameters['VEDISpartiallySusVaccinated']"
              />
            </div>
          </div>

          <div class="grid">
            <div class="col">
              Protection against hospitalization for partially
              susceptible vaccinated individuals:
            </div>

            <div class="col">
              <InputNumber
                mode="decimal"
                inputClass="text-1xl"
                inputStyle="width: 100px;"
                :minFractionDigits="0"
                :maxFractionDigits="2"
                :allowEmpty="false" :min="0"  :max="100"
                v-model="strategyList[strategyIndex].fixedParameters['VEHpartiallySusVaccinated']"
              />
            </div>
          </div>
            </AccordionTab>
          </Accordion>

          <DataTable :value="strategyList[selectedStrategyIndex].fixedParameters.propSymptomaticInfection" editMode="cell" responsiveLayout="scroll"   class="hidden">
              <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field" headerClass="fh-table-header">
                  <template v-if="col.field == 'category'" #body="slotProps">
                    <div>{{ slotProps.data.category }}</div>
                  </template>
                  <template v-else #editor="slotProps">
                    <InputNumber mode="decimal" :minFractionDigits="0" :maxFractionDigits="2" :allowEmpty="false" :min="0"
                      v-model="slotProps.data[slotProps.field]" />
                  </template>
              </Column>
          </DataTable>
          <table style="width: 100%;" class="hidden">
            <tr>
              <th></th>
              <th v-for="(ageGroup, index) in ageGroupList" :key="index">{{ ageGroup.header }}</th>
            </tr>
            <tr>
              <td><h2>Proportion of symptomatic infections in each age group</h2></td>
              <td>
                <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 80px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0"
                  v-model="strategyList[strategyIndex].fixedParameters['propSymptomaticInfection'][0]"
                />
              </td>
              <td>
                <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 80px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0"
                  v-model="strategyList[strategyIndex].fixedParameters['propSymptomaticInfection'][1]"
                />
              </td>
              <td>
                <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 80px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0"
                  v-model="strategyList[strategyIndex].fixedParameters['propSymptomaticInfection'][2]"
                />
              </td>
              <td>
                <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 80px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0"
                  v-model="strategyList[strategyIndex].fixedParameters['propSymptomaticInfection'][3]"
                />
              </td>
              <td>
                <InputNumber
                  mode="decimal"
                  inputClass="text-1xl"
                  inputStyle="width: 80px;"
                  :minFractionDigits="0"
                  :maxFractionDigits="2"
                  :allowEmpty="false" :min="0"
                  v-model="strategyList[strategyIndex].fixedParameters['propSymptomaticInfection'][4]"
                />
              </td>
            </tr>
            <tr>
              <td>16</td>
              <td>14</td>
              <td>10</td>
            </tr>
          </table>
        </div>
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
