<script setup>
import { storeToRefs } from "pinia";
import { useRouter, useRoute } from "vue-router";
import GeneralUtility from "../lib/GeneralUtility.mjs";
import MySlider from "../components/MySlider.vue";
import Button from "primevue/button";
import Divider from "primevue/divider";
import Footer from "../components/Footer.vue";
import Header from "../components/Header.vue";
import SideBar from "../components/SideBar.vue";
import MySelectButton from "../components/MySelectButton.vue";
import Chart from "primevue/chart";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import ColumnGroup from "primevue/columngroup"; //optional for column grouping
import Row from "primevue/row";
import InputText from "primevue/inputtext";
import InputNumber from "primevue/inputnumber";
import Skeleton from "primevue/skeleton";
import ProgressBar from "primevue/progressbar";
import { ref, computed, onMounted, reactive, watch, nextTick } from "vue";
import voca from "voca";

import Message from "primevue/message";
import { propor0to100OutOfScopeMsg, proporSumOver100Msg } from "../content/variable";

import { useStrategiesStore } from "../stores/strategies";

//import { useVaccineSelectionStore } from '@/stores/vaccine-selection';
//import { useVaccinationStatusStore } from "@/stores/vaccination-status";

import { useAgeGroupStore } from "@/stores/age-group";

/*
const vaccineStore = useVaccineSelectionStore();
const { vaccine1, vaccine2, vaccine3} = storeToRefs(vaccineStore);

console.log(`vaccine1: ${JSON.stringify(vaccine1)}`);
console.log(`vaccine2: ${vaccine2}`);
console.log(`vaccine3: ${vaccine3}`);
*/

/*
const vaccinationStore = useVaccinationStatusStore();
const { vaccinationStatusByAgeGroup} = storeToRefs(vaccinationStore);
*/

const ageGroupStore = useAgeGroupStore();
const { groupIndexLabelMap } = storeToRefs(ageGroupStore);

const nextButtonRef = ref(null);

//import { useStrategiesStore } from '../stores/strategies';
const strategiesStore = useStrategiesStore();
const { strategyList, selectedStrategyIndex } = storeToRefs(strategiesStore);
// let currentStrategy = strategyList.value[selectedStrategyIndex.value];

// this works
// weird... it didn't work sometime?!?
//strategiesStore.addStrategy();

let strategyIndex = selectedStrategyIndex.value;

let showProgress = false;
/*
if(route.query.strategy != undefined){
    strategyIndex = Number(route.query.strategy);
    strategiesStore.selectStrategy(strategyIndex);
}
*/
let currentStrategy = strategyList.value[strategyIndex];

//let vaccineList = currentStrategy["vaccineParameters"]["vaccineList"];

let vaccinationStatusByAgeGroup =
  currentStrategy["vaccineParameters"]["vaccinationStatusByAgeGroup"];

// URL: work if enter URL direclty, but not with roouter

const router = useRouter();
const route = useRoute();
import { systemName } from "../content/variable";
import { useHead } from "@unhead/vue";
useHead({
  title: `Previously Vaccinated by Age | ${systemName}`,
  /*
  meta: [
    { name: 'description', content: 'Learn more about us.' },
  ],
  */
});
/*
let groupIndex = ref(1);

let urlParams = new URLSearchParams(window.location.search);
let groupIndex = ref(1);
groupIndex = urlParams.get('group') != undefined && urlParams.get('group').length > 0? Number(urlParams.get('group')): 1;
*/

//groupIndex = Number(route.query.group);

let groupIndex = computed(() => {
  return route.query.group != undefined ? Number(route.query.group) : 1;
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
  async (newGroupIndex) => {
    console.log(`groupIndex (before assignment): ${groupIndex.value}`);

    //groupIndex = newGroupIndex;
    /*
      onlyGroupName = `group${groupIndex}`;
      */
    //console.log(`new groupIndex: ${groupIndex}`);
    console.log(
      `new onlyGroupName (before assignment): ${onlyGroupName.value}`
    );
  }
);

function sleep(ms) {
  console.log(`sleep for ${ms}`);
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const onNextClick = async (event) => {
  showProgress = true;
  console.log(`showProgress: ${showProgress}`);
  //await nextTick();

  await sleep(200);
  showProgress = false;
  console.log(`showProgress: ${showProgress}`);
  if (groupIndex.value < 5) {
    router.push({
      path: "/vaccination-by-age",
      query: { group: groupIndex.value + 1 },
    });
    //router.push(`/vaccination-by-age/${groupIndex + 1}`);
  } else {
    // /vaccination-efficacy-precheck
    router.push({ path: "/vaccine-efficacy", query: { vaccine: 1 } });
  }
};

const onMouseLeave = (event) => {
  console.log(`onMouseLeave`);
  // v-on:mouseleave="mouseleave"
};

const combinedColumns = reactive([
  { field: "category", header: "Category" },
  { field: "fulldose", header: "Primary series *" },
  { field: "booster", header: "Booster" },
]);

// strategyList.value[strategyIndex].vaccineParameters.vaccinationStatusByAgeGroup
const vaccinationByAgeGroup = computed(() => {
  return strategyList.value[strategyIndex].vaccineParameters.vaccinationStatusByAgeGroup[onlyGroupName.value].filter((data) => {
    return data["category"] != "Unvaccinated";
  });
});

// group1
const group1PrimaryTotal = computed(() => {
  let propertyName = onlyGroupName.value;

  //let items = infectionStatusByAgeGroup.value;
  let items = strategyList.value[strategyIndex].vaccineParameters.vaccinationStatusByAgeGroup[propertyName];
  //console.log(`items: ${JSON.stringify(items)}`);
  let vaccineType = "fulldose";

  return GeneralUtility.sumNumbersAsDecimal([items[0][vaccineType], items[1][vaccineType], items[2][vaccineType], items[3][vaccineType]]);
});

const group1PrimaryValid = computed(() => {
  let propertyName = onlyGroupName.value;
  let items = strategyList.value[strategyIndex].vaccineParameters.vaccinationStatusByAgeGroup[propertyName];
  let vaccineType = "fulldose";
  return group1PrimaryTotal.value == 100 && items[0][vaccineType] >= 0 && items[1][vaccineType] >= 0 && items[2][vaccineType] >= 0 && items[3][vaccineType] >= 0;

});

const group1BoosterTotal = computed(() => {
  let propertyName = onlyGroupName.value;

  //let items = infectionStatusByAgeGroup.value;
  let items = strategyList.value[strategyIndex].vaccineParameters.vaccinationStatusByAgeGroup[propertyName];
  //console.log(`items: ${JSON.stringify(items)}`);
  let vaccineType = "booster";

  return GeneralUtility.sumNumbersAsDecimal([items[0][vaccineType], items[1][vaccineType], items[2][vaccineType], items[3][vaccineType]]);
});

const group1BoosterValid = computed(() => {
  let propertyName = onlyGroupName.value;
  let items = strategyList.value[strategyIndex].vaccineParameters.vaccinationStatusByAgeGroup[propertyName];
  let vaccineType = "booster";
  return group1BoosterTotal.value == 100 && items[0][vaccineType] >= 0 && items[1][vaccineType] >= 0 && items[2][vaccineType] >= 0 && items[3][vaccineType] >= 0;

});

const group1Valid = computed(() => {
  return group1PrimaryValid.value && group1BoosterValid.value && group1VaccinatedTotal.value <= 100;
});

const group1VaccinatedTotal = computed(() => {
  let propertyName = onlyGroupName.value;

  //let items = infectionStatusByAgeGroup.value;
  let items = strategyList.value[strategyIndex].vaccineParameters.vaccinationStatusByAgeGroup[propertyName];
  //console.log(`items: ${JSON.stringify(items)}`);
  let vaccinePrimary = "fulldose";
  let vaccineBooster = "booster";

  return GeneralUtility.sumNumbersAsDecimal([items[0][vaccinePrimary], items[1][vaccinePrimary], items[2][vaccinePrimary], items[0][vaccineBooster], items[1][vaccineBooster], items[2][vaccineBooster]]);
});


function updateUnvaccinated(field) {
  let newData = { ...strategyList.value[strategyIndex].vaccineParameters.vaccinationStatusByAgeGroup };
  newData[onlyGroupName.value][3][field] = GeneralUtility.minusNumbersAsDecimal(
    100,
    GeneralUtility.sumNumbersAsDecimal([
      newData[onlyGroupName.value][0][field],
      newData[onlyGroupName.value][1][field],
      newData[onlyGroupName.value][2][field],
    ])
  );
  strategyList.value[strategyIndex].vaccineParameters.vaccinationStatusByAgeGroup = newData;
}

function onVaccinationStatusChange(event) {
  let { data, newValue, field } = event;

  console.log(
    `onVaccinationStatusChange: ${JSON.stringify(
      data,
      null,
      2
    )}, ${field}, ${newValue}`
  );

  console.log(
    `onVaccinationStatusChange vaccinationStatusByAgeGroup[onlyGroupName]: ${JSON.stringify(
      strategyList.value[strategyIndex].vaccineParameters.vaccinationStatusByAgeGroup[onlyGroupName.value]
    )}`
  );

  console.log(
    `onVaccinationStatusChange vaccinationStatusByAgeGroup: ${JSON.stringify(
      strategyList.value[strategyIndex].vaccineParameters.vaccinationStatusByAgeGroup
    )}`
  );

  console.log(
    `onVaccinationStatusChange vaccinationStatusByAgeGroup type: ${typeof strategyList.value[strategyIndex].vaccineParameters.vaccinationStatusByAgeGroup}`
  );

  let newData = { ...strategyList.value[strategyIndex].vaccineParameters.vaccinationStatusByAgeGroup };

  console.log(
    `onVaccinationStatusChange vaccinationStatusByAgeGroup newData (before change): ${JSON.stringify(
      newData,
      null,
      2
    )}`
  );

  newData[onlyGroupName.value] = newData[onlyGroupName.value].map((item) => {
    if (item["category"] == data["category"]) {
      return data;
    } else {
      return item;
    }
  });

  // now, calibrate the uninfected

  // use decimal
  newData[onlyGroupName.value][3][field] = GeneralUtility.minusNumbersAsDecimal(
    100,
    GeneralUtility.sumNumbersAsDecimal([
      newData[onlyGroupName.value][0][field],
      newData[onlyGroupName.value][1][field],
      newData[onlyGroupName.value][2][field],
    ])
  );

  /*
  newData[onlyGroupName.value][3][field] = 100 - newData[onlyGroupName.value][0][field] - newData[onlyGroupName.value][1][field] - newData[onlyGroupName.value][2][field];
  */

  // this loop seems unnecessary
  /*
  for(let i = 1; i < 6; i++){
    
  }
  */

  console.log(
    `onVaccinationStatusChange newData (after change): ${JSON.stringify(
      newData
    )}`
  );

  strategyList.value[strategyIndex].vaccineParameters.vaccinationStatusByAgeGroup = newData;

  /*
  vaccinationStore.$patch({
      vaccinationStatusByAgeGroup: newData,
  });
  */
}

/*
const onInputChange = (event, obj, groupName) => {
  console.log(
    `onInputChange: event ${JSON.stringify(event)}, obj: ${JSON.stringify(obj)}`
  );
  //obj.data[obj.field] = event.value;
};
*/

const onInputBlur = (event, obj, groupName) => {
  console.log(`onInputBlur: groupName: ${groupName}`);
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

  let oldValue = strategyList.value[strategyIndex].vaccineParameters.vaccinationStatusByAgeGroup[
    groupName
  ].filter((eInfo) => {
    return eInfo.category == obj.data.category;
  })[0][obj.field];

  if (oldValue != resultValue) {
    strategyList.value[strategyIndex].vaccineParameters.vaccinationStatusByAgeGroup[
      groupName
    ].filter((eInfo) => {
      return eInfo.category == obj.data.category;
    })[0][obj.field] = resultValue;

    updateUnvaccinated(obj.field);

  }


};

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

  /*
  switch (field) {
    case "fulldose":
      if (GeneralUtility.isPositiveNumber(newValue)) {
        data[field] = Number(newValue);
        onVaccinationStatusChange(event);
      }
      else event.preventDefault();
      break;
    case "booster":
      if (GeneralUtility.isPositiveNumber(newValue)) {
        data[field] = Number(newValue);
        onVaccinationStatusChange(event);
      }
      else event.preventDefault();
      break;
    default:
      //if (newValue.trim().length > 0) data[field] = newValue;
      //else event.preventDefault();
      break;
  }
  */
};

const convertVaccineLabel = (placholderName) => {
  //console.log(`convertVaccineLabel: ${placholderName}`);

  //console.log(`convertVaccineLabel vaccine1.name: ${vaccineList[0].name}`);

  let result = "";

  switch (placholderName) {
    case "Vaccine 1":
      result = strategyList.value[strategyIndex].vaccineParameters.vaccineList[0].name;
      break;
    case "Vaccine 2":
      result = strategyList.value[strategyIndex].vaccineParameters.vaccineList[1].name;
      break;
    case "Vaccine 3":
      result = strategyList.value[strategyIndex].vaccineParameters.vaccineList[2].name;
      break;
    default:
      result = "";
      break;
  }

  if (result == undefined || result == "") {
    result = placholderName;
  }

  //console.log(`convertVaccineLabel result: ${result}`);

  return result;
};
const colorList = ["#42A5F5", "#FFA726", "#44A726"];

const basicData = computed(() => {
  return {
    labels: ["Primary series", "Booster"],
    datasets: strategyList.value[strategyIndex].vaccineParameters.vaccinationStatusByAgeGroup[onlyGroupName.value]
      .filter((item) => {
        return convertVaccineLabel(item.category) != "Unvaccinated";
      })
      .map((item, index) => {
        return {
          label: convertVaccineLabel(item.category),
          backgroundColor: colorList[index],
          data: [item.fulldose, item.booster], //vaccinationStatusByAgeGroup[onlyGroupName.value].map((item) => item.fulldose)
        };
      }),
    /*
                datasets: [
                   {
                        label:  "Vaccine 1",
                        backgroundColor: '#42A5F5',
                        data: [60, 25]//vaccinationStatusByAgeGroup[onlyGroupName.value].map((item) => item.fulldose)
                  },
                  {
                      label:  "Vaccine 2",
                      backgroundColor: '#FFA726',
                      data: [10, 25]//vaccinationStatusByAgeGroup[onlyGroupName.value].map((item) => item.fulldose)
                  },
                  {
                      label:  "Vaccine 3",
                      backgroundColor: '#44A726',
                      data: [20, 25]//vaccinationStatusByAgeGroup[onlyGroupName.value].map((item) => item.fulldose)
                  },
                ],
                */
    /*
                labels: vaccinationStatusByAgeGroup[onlyGroupName.value].map((item) => {
                  return convertVaccineLabel(item.category);
                }),
                datasets: [

                    {
                        label: 'Primary series',
                        backgroundColor: '#42A5F5',
                        data: vaccinationStatusByAgeGroup[onlyGroupName.value].map((item) => item.fulldose)
                    },
                    {
                        label: 'Booster',
                        backgroundColor: '#FFA726',
                        data: vaccinationStatusByAgeGroup[onlyGroupName.value].map((item) => item.booster)
                    }
                ]
                */
  };
});

const basicOptions = {
  responsive: true,
  plugins: {
    legend: {
      labels: {
        color: "#495057",
      },
    },
  },
  scales: {
    x: {
      ticks: {
        color: "#495057",
      },
      grid: {
        color: "#ebedef",
      },
    },
    y: {
      ticks: {
        color: "#495057",
      },
      grid: {
        color: "#ebedef",
      },
    },
  },
};
</script>

<template>
  <div class="grid" :key="groupIndex.value">
    <div class="col-2">
      <div class="mt-7"></div>
      <div class="sticky top-0">
        <SideBar></SideBar>
      </div>
    </div>
    <div class="col ml-4">
      <div class="sticky top-0">
        <Header></Header>
      </div>

      <h1>Previously vaccinated by Age</h1>
      <Divider class="fh-divider-primary"></Divider>
      <Skeleton width="100%" height="2rem" v-if="showProgress" />
      <div v-else>
        <h3>
          Group {{ groupIndex }}: people {{ groupIndexLabelMap[groupIndex] }}
        </h3>
        <h3>Primary series vs. Booster</h3>
        <div class="mt-4 text-2xl">
          <strong>* Primary series: People who completed a primary series BUT have not had a booster yet</strong>.
        </div>
        <br />
        <div class="grid">
          <div class="col" style="padding-right: 0px">
            <Chart type="bar" :data="basicData" :options="basicOptions" />
          </div>
          <div class="col" style="padding-right: 0px">
            <DataTable :value="vaccinationByAgeGroup" editMode="cell" @cell-edit-complete="onCellEditComplete"
              responsiveLayout="scroll" @mouseleave="onMouseLeave">
              <Column v-for="col of combinedColumns" :field="col.field" :header="col.header" :key="col.field"
                style="width: 18%" headerClass="fh-table-header">
                <!--
                <template v-if="col.field == 'category'">
                  <div>{{  convertVaccineLabel(field)}}</div>
                </template>
                :ref="refAmount" @keyup="($event) => {this.$ref.refAmount.onInputBlur($event)}"
                -->
                <template v-if="col.field == 'category'" #body="slotProps">
                  <div>{{ convertVaccineLabel(slotProps.data.category) }}</div>
                </template>
                <template v-else #editor="slotProps">
                  <InputNumber :maxFractionDigits="2" :allowEmpty="false" :min="0" :max="100"
                    v-model="slotProps.data[slotProps.field]" @blur="
                        (event) => {
                          onInputBlur(event, slotProps, onlyGroupName);
                        }
                      " />
                </template>
              </Column>

              <div class="hidden">
                <ColumnGroup type="footer">
                  <Row>
                    <Column footer="Unvaccinated" :colspan="1" footerStyle="text-align:left"
                      footerClass="fh-table-footer" />
                    <Column
                      :footer="strategyList[strategyIndex].vaccineParameters.vaccinationStatusByAgeGroup[onlyGroupName][3]['fulldose']"
                      footerClass="fh-table-footer" />
                    <Column :footer="strategyList[strategyIndex].vaccineParameters.vaccinationStatusByAgeGroup[onlyGroupName][3]['booster']
                      " footerClass="fh-table-footer" />

                  </Row>
                </ColumnGroup>
              </div>

            </DataTable>
            <br />
            <br />
            <div class="text-2xl text-center">Unvaccinated: {{ GeneralUtility.minusNumbersAsDecimal(100,
              group1VaccinatedTotal) }} %</div>
            <div>

              <Message severity="error" v-if="group1VaccinatedTotal > 100" :closable="false">{{ proporSumOver100Msg }}
              </Message>
            </div>
          </div>
        </div>
      </div>


      <div>
        <ProgressBar v-if="showProgress" style="height: 0.5em" mode="indeterminate" />
        <div class="flex justify-content-center mt-4 mb-4">
          <Button label="Next" ref="nextButtonRef" :disabled="!group1Valid" class="p-button-lg fh-button-primary"
            @click="onNextClick"></Button>
        </div>
        <Divider class="fh-divider-primary"></Divider>
        <Footer></Footer>
      </div>
    </div>
    <div class="col-2"></div>
  </div>
</template>


/*

*/