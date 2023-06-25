<script setup>
import { storeToRefs } from "pinia";
import { useRouter, useRoute } from "vue-router";
import GeneralUtility from "../lib/GeneralUtility.mjs";
import { ref, computed, onMounted, reactive } from "vue";
import { FilterMatchMode } from "primevue/api";
import Message from 'primevue/message';
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
import voca from 'voca';
/*
import { useInfectionStatusStore } from "@/stores/infection-status";
const isStore = useInfectionStatusStore();
const { infectionStatusByAgeGroup } = storeToRefs(isStore);
*/

import { propor0to100OutOfScopeMsg } from "../content/variable";


import { useStrategiesStore } from '../stores/strategies';

import { Decimal } from 'decimal.js';

const strategiesStore = useStrategiesStore();
const { strategyList, selectedStrategyIndex } = storeToRefs(strategiesStore);
// let currentStrategy = strategyList.value[selectedStrategyIndex.value];

// this works
// weird... it didn't work sometime?!?
//strategiesStore.addStrategy();


let strategyIndex = selectedStrategyIndex.value;
const route = useRoute();

import { systemName } from "../content/variable";
import { useHead } from "@unhead/vue";
useHead({
  title: `Infection Prevalence | ${systemName}`,
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

let isParameters = currentStrategy["regionParameters"]["infectionStatus"];





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
    }
    else {
      return item;
    }
  });

  // now, calibrate the uninfected
  for (let i = 1; i < 6; i++) {
    let groupName = `group${i}`;

    updateUninfected(groupName);

    // verion 1
    /*
    // Decimal('1.1').add('2.2').toNumber()

    // newData[2][groupName] = new Decimal(100).minus(new Decimal(newData[0][groupName])).minus(new Decimal(newData[1][groupName])).toNumber();


    newData[2][groupName] = GeneralUtility.minusNumbersAsDecimal(
      100,
      GeneralUtility.sumNumbersAsDecimal([
      newData[0][groupName],
      newData[1][groupName]
      ])
    );
    */
  }


  //strategyList.value[strategyIndex].regionParameters.infectionStatus = newData;

  /*
  isStore.$patch({
    infectionStatusByAgeGroup: newData,
  });
  */


}

const router = useRouter();

function sleep(ms) {
  console.log(`sleep for ${ms}`);
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const onNextClick = async (event) => {
  console.log(`onNextClick`);
  //showProgress = true;
  //console.log(`showProgress: ${showProgress}`);
  //await nextTick();

  await sleep(200);
  //showProgress = false;
  //console.log(`showProgress: ${showProgress}`);
  router.push("/vaccine-selection");
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

const group1Total = computed(() => {
  let propertyName = "group1";

  //let items = infectionStatusByAgeGroup.value;
  let items = strategyList.value[strategyIndex].regionParameters.infectionStatus;
  return GeneralUtility.sumNumbersAsDecimal([items[0][propertyName], items[1][propertyName], items[2][propertyName]]);
});

const group1Valid = computed(() => {
  let propertyName = "group1";
  let items = strategyList.value[strategyIndex].regionParameters.infectionStatus;
  return group1Total.value == 100 && items[0][propertyName] >= 0 && items[1][propertyName] >= 0 && items[2][propertyName] >= 0;

});

const group2Total = computed(() => {
  let propertyName = "group2";
  //let items = infectionStatusByAgeGroup.value;
  let items = strategyList.value[strategyIndex].regionParameters.infectionStatus;
  return GeneralUtility.sumNumbersAsDecimal([items[0][propertyName], items[1][propertyName], items[2][propertyName]]);
});

const group2Valid = computed(() => {
  let propertyName = "group2";
  let items = strategyList.value[strategyIndex].regionParameters.infectionStatus;
  return group2Total.value == 100 && items[0][propertyName] >= 0 && items[1][propertyName] >= 0 && items[2][propertyName] >= 0;

});

const group3Total = computed(() => {
  let propertyName = "group3";
  //let items = infectionStatusByAgeGroup.value;
  let items = strategyList.value[strategyIndex].regionParameters.infectionStatus;
  return GeneralUtility.sumNumbersAsDecimal([items[0][propertyName], items[1][propertyName], items[2][propertyName]]);
});

const group3Valid = computed(() => {
  let propertyName = "group3";
  let items = strategyList.value[strategyIndex].regionParameters.infectionStatus;
  return group3Total.value == 100 && items[0][propertyName] >= 0 && items[1][propertyName] >= 0 && items[2][propertyName] >= 0;

});

const group4Total = computed(() => {
  let propertyName = "group4";
  //let items = infectionStatusByAgeGroup.value;
  let items = strategyList.value[strategyIndex].regionParameters.infectionStatus;
  return GeneralUtility.sumNumbersAsDecimal([items[0][propertyName], items[1][propertyName], items[2][propertyName]]);
});

const group4Valid = computed(() => {
  let propertyName = "group4";
  let items = strategyList.value[strategyIndex].regionParameters.infectionStatus;
  return group4Total.value == 100 && items[0][propertyName] >= 0 && items[1][propertyName] >= 0 && items[2][propertyName] >= 0;

});

const group5Total = computed(() => {
  let propertyName = "group5";
  //let items = infectionStatusByAgeGroup.value;
  let items = strategyList.value[strategyIndex].regionParameters.infectionStatus;
  return GeneralUtility.sumNumbersAsDecimal([items[0][propertyName], items[1][propertyName], items[2][propertyName]]);
});

const group5Valid = computed(() => {
  let propertyName = "group5";
  let items = strategyList.value[strategyIndex].regionParameters.infectionStatus;
  return group5Total.value == 100 && items[0][propertyName] >= 0 && items[1][propertyName] >= 0 && items[2][propertyName] >= 0;

});




const allGroupValid = computed(() => {
  console.log(`group1Total: ${group1Total.value}, group2Total: ${group2Total.value}, group3Total: ${group3Total.value}, group4Total: ${group4Total.value}, group5Total: ${group5Total.value}`);
  console.log(`group1Valid: ${group1Valid.value}, group2Valid: ${group2Valid.value}, group3Valid: ${group3Valid.value}, group4Valid: ${group4Valid.value}, group5Valid: ${group5Valid.value}`);
  return group1Valid.value && group2Valid.value && group3Valid.value && group4Valid.value && group5Valid.value;
});




const infectedByAgeGroup = computed(() => {
  // version 2
  // strategyList.value[strategyIndex].regionParameters.infectionStatus
  return strategyList.value[strategyIndex].regionParameters.infectionStatus.filter((data) => {
    return data['category'] != "Uninfected";
  });


  // version 1
  /*
  return infectionStatusByAgeGroup.value.filter((data) => {
    return data['category'] != "Uninfected";
  });
  */

});

/*
const checkGroupTotal = (data, groupName, newValue) => {
    let validTotal = false;

    let result = 0;

    Object.keys(data).forEach((key) => {
        if( key == groupName){
            result += newValue;
        }
        else{
            result += data[groupName];
        }
    });

    validTotal = result == 100;

    return validTotal;
}
*/




const onCellEditComplete = (event) => {
  let { data, newValue, field } = event;

  console.log(`onCellEditComplete: ${JSON.stringify(data, null, 2)}, ${field}, ${newValue}`);
  console.log(`onCellEditComplete typeof newValue: ${typeof newValue}`);
  switch (field) {
    case "category":
      break;
    case "group1":
      if (GeneralUtility.isPositiveNumber(newValue)) {
        data[field] = Number(newValue);
        onInfectionStatusChange(event);
      }
      else event.preventDefault();
      break;
    case "group2":
      if (GeneralUtility.isPositiveNumber(newValue)) {
        data[field] = Number(newValue);
        onInfectionStatusChange(event);
      }
      else event.preventDefault();
      break;
    case "group3":
      if (GeneralUtility.isPositiveNumber(newValue)) {
        data[field] = Number(newValue);
        onInfectionStatusChange(event);
      }
      else event.preventDefault();
      break;
    case "group4":
      if (GeneralUtility.isPositiveNumber(newValue)) {
        data[field] = Number(newValue);
        onInfectionStatusChange(event);
      }
      else event.preventDefault();
      break;
    case "group5":
      if (GeneralUtility.isPositiveNumber(newValue)) {
        data[field] = Number(newValue);
        onInfectionStatusChange(event);
      }
      else event.preventDefault();
      break;
    default:
      //if (newValue.trim().length > 0) data[field] = newValue;
      //else event.preventDefault();
      break;
  }

};


function updateUninfected(groupName) {
  let newData = [...strategyList.value[strategyIndex].regionParameters.infectionStatus];
  newData[2][groupName] = GeneralUtility.minusNumbersAsDecimal(
    100,
    GeneralUtility.sumNumbersAsDecimal([
      newData[0][groupName],
      newData[1][groupName]
    ])
  );

  currentStrategy["regionParameters"]["infectionStatus"] = newData;
}


const onInputBlur = (event, obj, groupName) => {
  console.log(`onInputBlur: groupName: ${groupName}`);
  console.log(
    `onInputBlur: data ${JSON.stringify(obj.data)}, field: ${JSON.stringify(
      obj.field
    )}, value: ${event.value}, type: ${typeof event.value}`
  );

  /*
  obj.data[obj.field] = event.value;
  onCellEditComplete({...event, ...obj});
  updateUninfected(groupName);
  */


  let inputValue = Number(voca.replaceAll(event.value, ",", ""));
  let resultValue = 0;

  resultValue = Math.min(Math.max(inputValue, 0), 100);

  console.log(`onInputBlur: inputValue: ${inputValue}, resultValue: ${resultValue}`);

  console.log(`currentStrategy["regionParameters"]["infectionStatus"]: ${JSON.stringify(currentStrategy["regionParameters"]["infectionStatus"])}`);


  let oldValue = currentStrategy["regionParameters"]["infectionStatus"].filter((eInfo) => {
    return eInfo.category == obj.data.category;
  })[0][obj.field];

  if (oldValue != resultValue) {
    currentStrategy["regionParameters"]["infectionStatus"].filter((eInfo) => {
      return eInfo.category == obj.data.category;
    })[0][obj.field] = resultValue;
    // consider only updateUninfected if the value actually change?

    updateUninfected(groupName);


  }





  //updateUninfected(obj.field);
  //onInfectionStatusChange({data: obj.data, field: obj.field, value: event.value});
};

/*
<Column field="category" header="Category"></Column>
<Column field="group1" header="< 10"></Column>
<Column field="group2" header="10 ~ 19"></Column>
<Column field="group3" header="20 ~ 49"></Column>
<Column field="group4" header="50 ~ 64"></Column>
<Column field="group5" header="> 65"></Column>
*/

/*
              <template v-else #editor="{ data, field }">
                  <InputText v-model="data[field]" autofocus />
              </template>
*/

// //:value="items"


/*
            <ColumnGroup type="footer">
              <Row>
                <Column
                  footer="Totals (100):"
                  :colspan="1"
                  footerStyle="text-align:left"
                />
                <Column :footer="group1Total" />
                <Column :footer="group2Total" />
                <Column :footer="group3Total" />
                <Column :footer="group4Total" />
                <Column :footer="group5Total" />
              </Row>
            </ColumnGroup>
*/

</script>

<template>
  <div class="grid">
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


      <h1>Infection Prevalence</h1>
      <Divider class="fh-divider-primary"></Divider>
      <div class="grid">
        <div class="col">
          <h3>Infection status for each age group (in %):</h3>
          <DataTable :value="infectedByAgeGroup" editMode="cell" @cell-edit-complete="onCellEditComplete"
            responsiveLayout="scroll">
            <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field" style="width: 18%"
              headerClass="fh-table-header">
              <template v-if="col.field == 'category'">
                <div>{{ field }}</div>
              </template>
              <template v-if="col.field != 'category'" #editor="slotProps">
                <InputNumber mode="decimal" :minFractionDigits="0" :maxFractionDigits="2" :allowEmpty="false" :min="0"
                  :max="100" v-model="slotProps.data[slotProps.field]" @blur="(event) => {
                      onInputBlur(event, slotProps, slotProps.field);
                    }
                    " />
              </template>
            </Column>
            <ColumnGroup type="footer">
              <Row>
                <Column footer="Uninfected" :colspan="1" footerStyle="text-align:left" footerClass="fh-table-footer" />
                <Column :footer="strategyList[strategyIndex].regionParameters.infectionStatus[2]['group1']"
                  footerClass="fh-table-footer" />
                <Column :footer="strategyList[strategyIndex].regionParameters.infectionStatus[2]['group2']"
                  footerClass="fh-table-footer" />
                <Column :footer="strategyList[strategyIndex].regionParameters.infectionStatus[2]['group3']"
                  footerClass="fh-table-footer" />
                <Column :footer="strategyList[strategyIndex].regionParameters.infectionStatus[2]['group4']"
                  footerClass="fh-table-footer" />
                <Column :footer="strategyList[strategyIndex].regionParameters.infectionStatus[2]['group5']"
                  footerClass="fh-table-footer" />
              </Row>
            </ColumnGroup>

          </DataTable>
          <div>
            <Message severity="error" v-if="!allGroupValid" :closable="false">{{ propor0to100OutOfScopeMsg }}</Message>
          </div>
          <p class="mt-6">Previously infected: People who have been previously infected with any strain of SARS-CoV-2 and
            are not fully susceptible.</p>
          <p class="mt-6">Currently infected: People who are currently infected with SARS-CoV-2 (including asymptomatic,
            mild and hospitalized infections).</p>
          <p class="mt-6">Uninfected: People who have never been infected by SARS-CoV-2.</p>
          <p class="mt-6">Note: If age-specific rates of pre-existing and current infections are not known, give overall
            rates.</p>
          <p class="mt-6">Default previously infected (cumulative infection) rates reflect estimates as of November 2021,
            taken from this article: Barber, Ryan M et al . <em>Estimating global, regional, and national daily and
              cumulative infections with SARS-CoV-2 through Nov 14, 2021: a statistical analysis</em>. The Lancet (2022),
            <a href="https://doi.org/10.1016/S0140-6736(22)00484-6ß"
              target="_blank">https://doi.org/10.1016/S0140-6736(22)00484-6ß</a></p>
        </div>
      </div>

      <div>
        <div class="flex justify-content-center mt-4 mb-4">
          <Button label="Next" class="p-button-lg fh-button-primary" :disabled="!allGroupValid"
            @click="onNextClick"></Button>
        </div>
        <Divider class="fh-divider-primary"></Divider>
        <Footer></Footer>
      </div>
    </div>
    <div class="col-2"></div>
  </div>
</template>
