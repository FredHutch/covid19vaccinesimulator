<script setup>
import { storeToRefs } from "pinia";
import { useRouter, useRoute } from "vue-router";
import { ref, watchEffect, computed, onMounted, reactive, Fragment } from "vue";
import Button from "primevue/button";
import Divider from "primevue/divider";
import Footer from "../components/Footer.vue";
import Header from "../components/Header.vue";
import SideBar from "../components/SideBar.vue";
import Chart from "primevue/chart";
import { useToast } from "primevue/usetoast";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import ColumnGroup from "primevue/columngroup"; //optional for column grouping
import Row from "primevue/row";
import ProgressSpinner from "primevue/progressspinner";
import ProgressBar from "primevue/progressbar";
import { useStrategiesStore } from "../stores/strategies";
import Card from "primevue/card";

import { colorList } from "../content/variable";

import { ageGroupList } from "../content/variable";
import { DateTime } from "luxon";
import GeneralUtility from "../lib/GeneralUtility.mjs";
import Decimal from "decimal.js";
import { sampleSimulationOutcome } from "../content/variable";

const toast = useToast();

const strategiesStore = useStrategiesStore();
const {
  strategyList,
  updateStrategySimulatedOutcomeByIndex,
  selectedStrategyIndex,
  addDuplicateOfCurrentStrategy,
  selectStrategy,
  duplicateStrategyByIndex,
  removeStrategyByIndex,
  clearSimulatedOutcomeByIndex,
} = storeToRefs(strategiesStore);

// PHP
//const API_URL = `http://localhost/VaccineAllocator/service.php`;

// Flask
//const API_URL = `http://127.0.0.1:5000/simulation`;
const API_URL = `/simulation`;

let tempStrategy = {
  default_params: [0.8, 0.25, 0.01],
  immunity_params: [0.2, 0.1],
  initial_conditions_params: [0, 0.0001],
  location_params: [10000, 0.12, 100],
  vaccine_allocation_params: [0.5, 0.3],
  vaccine_efficacy_params: [0.4, 0.7],
};

/*
const simulatedOutcome = ref({
  cases: {},
  deaths: {},
});
*/

/*
cumulativeNumberOfDeaths: 101.0,
peakHospitalization: 12.0,
*/

const simulatedOutcome = ref({
  cumulativeNumberOfDeaths: 0,
  peakHospitalization: 0,
  deathTimeSeries: {},
  hospitalizationTimeSeries: {},
  infectionTimeSeries: {},
  symptomaticInfectionTimeSeries: {},
});

const router = useRouter();
const onNextClick = (event) => {
  router.push("/vaccine-selection");
};

const onEditClick = (index) => {
  strategiesStore.selectStrategy(index);
  router.push("/vaccine-strategy");
};

const onDuplicateClick = (index) => {
  strategiesStore.duplicateStrategyByIndex(index);
  //strategiesStore.strategiesStore(strategyList.value.length);
};

const onRemoveClick = (index) => {
  if (index == 0 && strategyList.value.length == 1) {
    strategiesStore.resetStrategyList();
    toast.add({
      severity: "success",
      summary: "Success",
      detail: "Remove the only strategy. Will add a placeholder.",
      life: 3000,
    });
  } else {
    strategiesStore.removeStrategyByIndex(index);

    toast.add({
      severity: "success",
      summary: "Success",
      detail: "Strategy successfully removed",
      life: 3000,
    });
  }
};

const onExportClick = (index) => {
  console.log(`onExportClick: strategy ${index}`);
  let strategy = strategyList.value[index];
  // strategy and result

  let resultMatrix = [];

  if(strategy.simulatedOutcome.resultMatrix != undefined){
    resultMatrix = strategy.simulatedOutcome.resultMatrix;
  }

  const fileString = `data:text/csv;chatset=utf-8,${encodeURIComponent(
    GeneralUtility.convertListOfListToXSVString(resultMatrix, ",")
  )}`;

  // simulation only
  /*
  const fileString = `data:text/json;chatset=utf-8,${encodeURIComponent(
    JSON.stringify(strategy.simulatedOutcome, null, 2)
  )}`;
  */

  /*
  const fileString = `data:text/json;chatset=utf-8,${encodeURIComponent(
    JSON.stringify(strategy.simulatedOutcome)
  )}`;
  */

  console.log(`onExportClick: fileString: ${fileString}`);

  // approach 1 (does not actully download file)

  const link = document.createElement("a");

  //link.href = URL.createObjectURL(fileString);
  link.href = fileString;

  let filePrefix = "strategy";

  let timeString = DateTime.now().toISO();

  let regionName = strategy.regionParameters.region.name;

  let fileName = `${filePrefix}_${
    index + 1
  }_for_${regionName}_result_${timeString}.csv`;

  console.log(`onExportClick: fileName: ${fileName}`);

  link.setAttribute("download", fileName);

  console.log(`onExportClick: setAttribute: download ${fileName}`);

  link.click();

  // it seems like everything after this is not working....
  console.log(`onExportClick: after click!`);

  //window.open(link.href)

  URL.revokeObjectURL(link.href);
  toast.add({
    severity: "success",
    summary: "Success",
    detail: "Simulation result successfully exported!",
    life: 3000,
  });

  // approach 2
  // actually, this doesn't work exactly well, the file is not formatted as json
  /*
  const data = fileString; //JSON.stringify(this.arr)
  const blob = new Blob([data], {type: 'text/plain'})
  const e = document.createEvent('MouseEvents'),

  a = document.createElement('a');

  let filePrefix = "strategy";

  let timeString = DateTime.now().toISO();

  let regionName = strategy.regionParameters.region.name;


  a.download = `${filePrefix}_${index+1}_for_${regionName}_${timeString}.json`;
  a.href = window.URL.createObjectURL(blob);
  a.dataset.downloadurl = ['text/json', a.download, a.href].join(':');
  e.initEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
  a.dispatchEvent(e);
  a.click();
  */
};

/*
const sampleLabels = [...Array(sampleResponse["cases"].length).keys()];

const combinedColumns = reactive([
  { field: "category", header: "Category" },
  { field: "fulldose", header: "Primary" },
  { field: "booster", header: "Booster" },
]);

const basicData2 = ref({
  labels: sampleLabels,
  datasets: [
    {
      label: "First Dataset",
      data: sampleResponse["cases"],
      fill: false,
      borderColor: "#42A5F5",
      tension: 0.4,
    },
    {
      label: "Second Dataset",
      data: sampleResponse["deaths"],
      fill: false,
      borderColor: "#FFA726",
      tension: 0.4,
    },
  ],
});
*/

const basicData = ref({
  labels: ["January", "February", "March", "April", "May", "June", "July"],
  datasets: [
    {
      label: "First Dataset",
      data: [65, 59, 80, 81, 56, 55, 40],
      fill: false,
      borderColor: "#42A5F5",
      tension: 0.4,
    },
    {
      label: "Second Dataset",
      data: [28, 48, 40, 19, 86, 27, 90],
      fill: false,
      borderColor: "#FFA726",
      tension: 0.4,
    },
  ],
});

const basicOptions = ref({
  plugins: {
    legend: {
      labels: {
        color: "#495057",
      },
    },
    colors: {
      enabled: true,
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
      suggestedMax: 5000000,
    },
  },
});

const getDynamicOptions = (dataName) => {
  let defaultOption = {
    plugins: {
      legend: {
        labels: {
          color: "#495057",
        },
      },
      colors: {
        enabled: true,
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

  // now, scan the simulationOutcome
  let simulationOutcomeDataList = strategyList.value.map((strategy, sIndex) => {
    return strategy["simulatedOutcome"][dataName]["datasets"];
  });

  // now, based on the dataName, calculate the max and min, and find hte max(abs())
  let dataMax = new Decimal(Number.MIN_VALUE);
  let dataMin = new Decimal(Number.MAX_VALUE);

  simulationOutcomeDataList.forEach((datasets) => {
    console.log(`datasets: ${JSON.stringify(datasets)}`);

    if (datasets != undefined) {
      datasets.forEach((datasetObj) => {
        console.log(
          `datasetObj: [${typeof datasetObj}] ${JSON.stringify(datasetObj)}`
        );

        let numMax = Decimal.max(...datasetObj.data);
        let numMin = Decimal.min(...datasetObj.data);

        if (numMax.greaterThan(dataMax)) {
          dataMax = numMax;
        }

        if (numMin.lessThan(dataMin)) {
          dataMin = numMin;
        }
      });
    }
  });

  defaultOption["scales"]["y"]["suggestedMin"] = 0;

  let numZero = Decimal.max(new Decimal(3), new Decimal(dataMax.sd(true) - 2));

  defaultOption["scales"]["y"]["suggestedMax"] = dataMax
    .plus(1 * new Decimal(10).pow(numZero))
    .ceil()
    .toNumber();

  console.log(
    `getDynamicOptions(${dataName}): ${JSON.stringify(defaultOption)}`
  );

  return defaultOption;
};

let dynamicOptions = computed(() => {
  return getDynamicOptions;
});

let chartOptionsMap = ref({});

let excludeList = ["cumulativeNumberOfDeaths", "peakHospitalization"];

let includeList = [
  "deathTimeSeries",
  "hospitalizationTimeSeries",
  "symptomaticInfectionTimeSeries",
  "infectionTimeSeries",
];

let pageLoadTime = DateTime.now();
console.log(`simulatedOutcomeLastUpdateTime - pageLoadTime: ${pageLoadTime}`);

const querySimulatedOutcomeForAStrategy = async (tempStrategy) => {
  const url = `${API_URL}`; //+ new URLSearchParams({input_parameters: JSON.stringify(currentStrategy.value)});

  let queryResponse = await fetch(url, {
    //mode: "no-cors",
    method: "POST",
    cache: "no-cache",
    headers: new Headers({
      "Content-Type": "application/json",
    }),
    body: JSON.stringify(tempStrategy), // JSON.stringify(tempStrategy), // JSON.stringify(currentStrategy.value)
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not OK");
        //toast.add({severity:'warn', summary: 'Warn Message', detail:'The simulation service is temporarily available. Please check back later.', life: 3000});
      }
      return response.json();
    })

    .then((data) => {
      //console.log("Success:", data);

      // through API
      let response = data;

      // updateStrategySimulatedOutcomeByIndex

      let newSimulatedOutcome = {};

      Object.keys(response).forEach((key) => {
        console.log(`watchEffect - response[${key}]`);

        if (key == "cumulativeNumberOfDeaths") {
          newSimulatedOutcome[key] = response[key];
          console.log(`watchEffect - response[${key}]: ${response[key]}`);
          //strategy.simulatedOutcome[key] = response[key];
        } else if (key == "peakHospitalization") {
          newSimulatedOutcome[key] = response[key];
          console.log(`watchEffect - response[${key}]: ${response[key]}`);
          //strategy.simulatedOutcome[key] = response[key];
        } else if (key == "index") {
          newSimulatedOutcome[key] = response[key];
          console.log(`watchEffect - response[${key}]: ${response[key]}`);
          //strategy.simulatedOutcome[key] = response[key];
        } else if (key == "resultMatrix") {
          newSimulatedOutcome[key] = response[key];
          console.log(`watchEffect - response[${key}]: ${response[key]}`);
          //strategy.simulatedOutcome[key] = response[key];
        }  
        else {
          // strategy.simulatedOutcome[key]

          newSimulatedOutcome[key] = {
            labels: [...Array(response[key][0].length).keys()],
            datasets: response[key].map((oneSeries, index) => {
              return {
                label: ageGroupList[index]["header"], // `Group ${index}`,
                data: oneSeries,
                fill: false,
                backgroundColor: colorList[index],
                //borderColor: "#42A5F5",
                tension: 0.4,
              };
            }),
          };
        }
      });

      return newSimulatedOutcome;

      /*
        // now, update the simulatedOutcome
        let strategyIndex = newSimulatedOutcome["index"];
        console.log(`simulatedOutcome for strategy [${strategyIndex}]: cumulativeNumberOfDeaths: ${newSimulatedOutcome["cumulativeNumberOfDeaths"]}`);
        strategiesStore.updateStrategySimulatedOutcomeByIndex(strategyIndex, newSimulatedOutcome);
        */
    })
    .catch((error) => {
      console.error("Error:", error);

      return sampleSimulationOutcome;
      // should consider do this elsewhere
      /*
      toast.add({
        severity: "warn",
        summary: "Warn Message",
        detail:
          "The simulation service is temporarily available. Please check back later.",
        life: 3000,
      });
      */
      //return sampleResponseComplex;
    });

  return queryResponse;
};

const needUpdate = (simulatedOutcomeLastUpdateTimeString, sIndex) => {
  if (simulatedOutcomeLastUpdateTimeString != undefined) {
    let updateTime = DateTime.fromISO(simulatedOutcomeLastUpdateTimeString);

    // there is simulatedOutcome
    //let diffHours = updateTime.diff(pageLoadTime, 'hours').toObject()["hours"];

    let diffTime = updateTime.diff(pageLoadTime).toObject()["milliseconds"];

    console.log(
      `simulatedOutcomeLastUpdateTime [${sIndex}] - diffTime: ${diffTime}`
    );

    if (diffTime >= 0) {
      // //=> { hours: 12168.75 })
      // last update time is older than page load time, so no need to query
      console.log(
        `simulatedOutcomeLastUpdateTime [${sIndex}] is greater [${diffTime}]: no need to query`
      );
      return "updated";
    } else {
      console.log(
        `simulatedOutcomeLastUpdateTime [${sIndex}] is not qreater [${diffTime}]: need to query`
      );
      return "need update";
    }
  } else {
    console.log(
      `simulatedOutcomeLastUpdateTime [${sIndex}] == undefined: need to query`
    );
    return "need update";
  }
};

const strategySimulationStatusList = computed(() => {
  let statusList = strategyList.value.map((strategy, sIndex) => {
    return needUpdate(strategy["simulatedOutcomeLastUpdateTime"], sIndex);

    /*
    if (strategy["simulatedOutcomeLastUpdateTime"] != undefined) {
      let updateTime = DateTime.fromISO(
        strategy["simulatedOutcomeLastUpdateTime"]
      );

      // there is simulatedOutcome
      //let diffHours = updateTime.diff(pageLoadTime, 'hours').toObject()["hours"];

      let diffTime = updateTime.diff(pageLoadTime).toObject()["milliseconds"];

      console.log(
        `simulatedOutcomeLastUpdateTime [${sIndex}] - diffTime: ${diffTime}`
      );

      if (diffTime >= 0) {
        // //=> { hours: 12168.75 })
        // last update time is older than page load time, so no need to query
        console.log(
          `simulatedOutcomeLastUpdateTime [${sIndex}] is greater [${diffTime}]: no need to query`
        );
        return "updated";
      } else {
        console.log(
          `simulatedOutcomeLastUpdateTime [${sIndex}] is not qreater [${diffTime}]: need to query`
        );
        return "need update";
      }
    } else {
      console.log(
        `simulatedOutcomeLastUpdateTime [${sIndex}] == undefined: need to query`
      );
      return "need update";
    }
    */
  });

  console.log(`strategySimulationStatusList: ${JSON.stringify(statusList)}`);

  return statusList;
});

const querySimulatedOutcomeForStrategyList = async () => {
  const url = `${API_URL}`; //+ new URLSearchParams({input_parameters: JSON.stringify(currentStrategy.value)});

  let strategyIndexSimulationOutcomeMap = {};

  let simulationFailedCount = 0;

  for (let i = 0; i < strategyList.value.length; i++) {
    let strategy = strategyList.value[i];
    let sIndex = i;

    let strategyStatus = needUpdate(
      strategy["simulatedOutcomeLastUpdateTime"],
      sIndex
    );

    console.log(
      `simulatedOutcomeLastUpdateTime for strategy [${sIndex}].simulatedOutcomeLastUpdateTime: ${strategy["simulatedOutcomeLastUpdateTime"]}`
    );

    console.log(
      `querySimulatedOutcomeForStrategyList strategyStatus: ${JSON.stringify(
        strategyStatus
      )}`
    );

    // version 2
    if (strategyStatus == "updated") {
      console.log(
        `querySimulatedOutcomeForStrategyList [${sIndex}]:[${strategyStatus}] is updated so no need to query.`
      );

      continue;
    }

    console.log(
      `querySimulatedOutcomeForStrategyList [${sIndex}]:[${strategyStatus}] need to query.`
    );

    // version 1
    /*
    if(strategy["simulatedOutcomeLastUpdateTime"] != undefined){

      let updateTime = DateTime.fromISO(strategy["simulatedOutcomeLastUpdateTime"]);

      // there is simulatedOutcome
      //let diffHours = updateTime.diff(pageLoadTime, 'hours').toObject()["hours"];

      let diffTime = updateTime.diff(pageLoadTime).toObject()["milliseconds"];

      console.log(`simulatedOutcomeLastUpdateTime [${sIndex}] - diffTime: ${diffTime}`);

      if( diffTime >= 0){
        // //=> { hours: 12168.75 })
        // last update time is older than page load time, so no need to query
        console.log(`simulatedOutcomeLastUpdateTime [${sIndex}] is greater [${diffTime}]: no need to query`);
        return;
      }
      else{
        console.log(`simulatedOutcomeLastUpdateTime [${sIndex}] is not qreater [${diffTime}]: need to query`);
      }
    }
    else {
      console.log(`simulatedOutcomeLastUpdateTime [${sIndex}] == undefined: need to query`);
    }
    */

    strategy["index"] = sIndex;

    let tempStrategy = JSON.parse(JSON.stringify(strategy));

    delete tempStrategy.simulatedOutcome;

    let msgList = GeneralUtility.validateStrategy(tempStrategy, i);

    if (msgList.length > 0) {
      msgList.forEach((msg) => {
        // msg
        toast.add({
          severity: "warn",
          summary: "Warn Message",
          detail: msg,
          life: 3000,
        });
      });

      // invalid format, avoid the query
      console.log(`Strategy ${i} is invalid. Avoid Query`);
      continue;
    }

    let newSimulatedOutcome = await querySimulatedOutcomeForAStrategy(
      tempStrategy
    );

    console.log(`newSimulatedOutcome: ${newSimulatedOutcome}`);

    // now, update the simulatedOutcome
    if (
      newSimulatedOutcome != undefined &&
      newSimulatedOutcome["index"] != undefined
    ) {
      let strategyIndex = newSimulatedOutcome["index"];

      console.log(
        `newSimulatedOutcome for strategy [${strategyIndex}]: ${newSimulatedOutcome}`
      );

      strategyIndexSimulationOutcomeMap[strategyIndex] = newSimulatedOutcome;

      /*
      strategiesStore.updateStrategySimulatedOutcomeByIndex(
        strategyIndex,
        newSimulatedOutcome
      );
      */
    } else {
      simulationFailedCount++;
    }
  }

  if (simulationFailedCount > 0) {
    toast.add({
      severity: "warn",
      summary: "Warn Message",
      detail:
        "The simulation service is temporarily unavailable. Please check back later.",
      life: 3000,
    });
  }

  // now, update the strategy
  // in the best case, I should just have one function that will do all the updating
  Object.keys(strategyIndexSimulationOutcomeMap).forEach((sIndex) => {
    strategiesStore.updateStrategySimulatedOutcomeByIndex(
      sIndex,
      strategyIndexSimulationOutcomeMap[sIndex]
    );
  });
};

watchEffect(async () => {
  // this effect will run immediately and then
  // re-run whenever currentBranch.value changes
  console.log(
    `watchEffect!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!`
  );

  window.scrollTo({ top: 0, behavior: "smooth" });

  await querySimulatedOutcomeForStrategyList();
});

const convertVaccineLabel = (placholderName, vaccineList) => {
  console.log(`convertVaccineLabel: ${placholderName}`);

  console.log(`convertVaccineLabel vaccine1.name: ${vaccineList[0].name}`);

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
    default:
      result = "";
      break;
  }

  if (result == undefined || result == "") {
    result = placholderName;
  }

  console.log(`convertVaccineLabel result: ${result}`);

  return result;
};

const extractProportionFromAllocation = (allocation, category) => {
  console.log(
    `extractProportionFromAllocation allocation: ${allocation}, category: ${category}`
  );

  let result = "";

  switch (category) {
    case "fulldose":
      result = allocation[0].proportion;
      break;
    case "booster":
      result = allocation[1].proportion;
      break;
    default:
      result = "";
      break;
  }

  console.log(`extractProportionFromAllocation result: ${result}`);

  return result;
};

const mapPropertyToLabel = (propertyName) => {
  console.log(`mapPropertyToLabel: ${propertyName}`);

  let result = "";

  switch (propertyName) {
    case "cumulativeNumberOfDeaths":
      result = "Cumulative number of deaths over the simulation period";
      break;
    case "peakHospitalization":
      result = "Maximum number of hospitalized individuals";
      break;
    case "hospitalizationTimeSeries":
      result = "Number of hospitalized people";
      break;
    case "infectionTimeSeries":
      result = "Number of infected people";
      break;
    case "symptomaticInfectionTimeSeries":
      result = "Number of symptomatic infections";
      break;
    case "deathTimeSeries":
      result = "Cumulative number of deaths";
      break;
    default:
      result = "";
      break;
  }

  console.log(`extractProportionFromAllocation result: ${result}`);

  return result;
};

// <Chart type="bar" :data="basicData" :options="basicOptions" />
</script>

<template>
  <div class="grid">
    <div class="col-2">
      <div class="mt-7"></div>
      <div class="sticky top-0"><SideBar></SideBar></div>
    </div>
    <div class="col ml-4">
      <div class="sticky top-0">
        <Header :displayStrategyIndex="false"></Header>
      </div>

      <h1>
        Result <spam class="hidden">(page load time:{{ pageLoadTime }})</spam>
      </h1>
      <Divider class="fh-divider-primary"></Divider>
      <h2>Vaccination Strategy Simulated Outcome:</h2>
      <div class="grid">
        <div
          class="col-5 m-3"
          v-for="(strategy, index) in strategyList"
          :key="index"
        >
          <div>
            <h3>Strategy {{ index + 1 }}</h3>
            <h3>Region: {{ strategy["regionParameters"].region.name }}</h3>
            <h4>
              Population size:
              {{
                strategy["regionParameters"].region != undefined &&
                strategy["regionParameters"].region.populationList != undefined
                  ? strategy["regionParameters"].region.populationList
                      .reduce((a, b) => a + b, 0)
                      .toLocaleString(undefined)
                  : "?"
              }}
            </h4>
            <div class="hidden">
              Last simulated time:
              {{ strategy["simulatedOutcomeLastUpdateTime"] }}
            </div>
            <ProgressBar
              mode="indeterminate"
              style="height: 0.5em"
              v-if="strategySimulationStatusList[index] != 'updated'"
            />
            <DataTable
              :value="strategy.vaccineParameters.vaccineList"
              responsiveLayout="scroll"
            >
              <Column
                v-for="col of combinedColumns"
                :field="col.field"
                :header="col.header"
                :key="col.field"
                style="width: 18%"
              >
                <template #body="slotProps">
                  <div v-if="col.field == 'category'">
                    {{
                      convertVaccineLabel(
                        slotProps.data.category,
                        strategy.vaccineParameters.vaccineList
                      )
                    }}
                  </div>
                  <div v-if="col.field != 'category'">
                    {{
                      extractProportionFromAllocation(
                        slotProps.data.allocation,
                        slotProps.field
                      )
                    }}
                  </div>
                </template>
              </Column>
            </DataTable>
          </div>
          <div>
            <h4
              v-for="(excludeName, excludeIndex) in excludeList"
              v-bind:key="excludeIndex"
            >
              {{
                strategy["simulatedOutcome"] != undefined &&
                strategy["simulatedOutcome"][excludeName] != undefined
                  ? `${mapPropertyToLabel(excludeName)}: ${
                      strategy["simulatedOutcome"][excludeName]
                    }`
                  : `${mapPropertyToLabel(excludeName)}:`
              }}
            </h4>
          </div>

          <div class="grid">
            <div class="col">
              <div
                v-for="(propertyName, propertyIndex) in includeList"
                v-bind:key="propertyIndex"
              >
                <h4>{{ mapPropertyToLabel(propertyName) }}:</h4>
                <div>
                  <Chart
                    v-if="
                      strategy['simulatedOutcome'] != undefined &&
                      strategy['simulatedOutcome'][propertyName] != undefined
                    "
                    type="line"
                    :data="strategy['simulatedOutcome'][propertyName]"
                    :options="dynamicOptions(propertyName)"
                  ></Chart>
                </div>
              </div>
            </div>
          </div>
          <div class="flex justify-content-center mt-4 mb-4">
            <Button
              label="Edit"
              class="p-button-info"
              @click="onEditClick(index)"
            ></Button>
            &nbsp;
            <Button
              label="Duplicate"
              class="p-button-success"
              @click="onDuplicateClick(index)"
            ></Button>
            &nbsp;
            <Button
              label="Remove"
              class="p-button-danger"
              @click="onRemoveClick(index)"
            ></Button>
            &nbsp;
            <Button
              label="Export"
              class="p-button-secondary"
              @click="onExportClick(index)"
              >Export Result</Button
            >
          </div>
        </div>
      </div>
      <div>
        <Divider class="fh-divider-primary"></Divider>
        <Footer></Footer>
      </div>
    </div>
    <div class="col-2"></div>
  </div>
</template>
