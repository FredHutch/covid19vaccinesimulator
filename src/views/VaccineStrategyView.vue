<script setup>
import { storeToRefs } from "pinia";
import { useRouter, useRoute } from "vue-router";
import GeneralUtility from "../lib/GeneralUtility.mjs";
import InputNumber from 'primevue/inputnumber';
import { DateTime } from "luxon";
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
import Card from 'primevue/card';
import Panel from 'primevue/panel';
import Fieldset from 'primevue/fieldset';
import voca from 'voca';
import Calendar from 'primevue/calendar';

import AllocationMethodList from "../components/AllocationMethodList.vue";
import { useStrategiesStore } from '../stores/strategies';

import {fulldoseLessThanTotalMsg, fulldoseMoreThanTotalMsg, boosterLessThanTotalMsg, boosterMoreThanTotalMsg, lessThan100Msg, moreThan100Msg} from "../content/variable";


/*
import { useRegsionStore } from '@/stores/region';
const regionStore = useRegsionStore();
const { region, variant, infectiousnessLevel} = storeToRefs(regionStore);
*/

/*
import { useInfectionStatusStore } from "@/stores/infection-status";
const isStore = useInfectionStatusStore();
const { infectionStatusByAgeGroup } = storeToRefs(isStore);
*/



/*
import { useVaccinationStatusStore } from "@/stores/vaccination-status";
const vaccinationStore = useVaccinationStatusStore();
const { vaccinationStatusByAgeGroup} = storeToRefs(vaccinationStore);
*/

/*
import { useVaccineSelectionStore } from '@/stores/vaccine-selection';
const vaccineStore = useVaccineSelectionStore();
const { vaccine1, vaccine2, vaccine3} = storeToRefs(vaccineStore);
*/


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

let regionParameters = currentStrategy["regionParameters"];
let infectionStatusByAgeGroup = currentStrategy["regionParameters"]["infectionStatus"];

let vaccineList = currentStrategy["vaccineParameters"]["vaccineList"];
//let vaccineAvailability = vaccineList;

let vaccinationStatusByAgeGroup = currentStrategy["vaccineParameters"]["vaccinationStatusByAgeGroup"];

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

const updateSimulationParameters = () => {
  console.log(`updateSimulationParameters`);
  strategiesStore.updateSimulationParametersByStrategyIndex(strategyIndex);
}

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

  let newData = [...infectionStatusByAgeGroup];

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
    newData[2][groupName] = 100 - newData[0][groupName] - newData[1][groupName];
  }


  infectionStatusByAgeGroup = newData;

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
  await sleep(200);
  router.push("/vaccine-plan-period");
};




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

const convertVaccineTypeLabel = (name) => {
  if (name == "Full dose") {
    return "Primary series"
  }
  else {
    return name;
  }
}


const group1Total = computed(() => {
  let propertyName = "group1";
  let items = infectionStatusByAgeGroup;
  return (
    items[0][propertyName] + items[1][propertyName] + items[2][propertyName]
  );
});

const group2Total = computed(() => {
  let propertyName = "group2";
  let items = infectionStatusByAgeGroup;
  return (
    items[0][propertyName] + items[1][propertyName] + items[2][propertyName]
  );
});

const group3Total = computed(() => {
  let propertyName = "group3";
  let items = infectionStatusByAgeGroup;
  return (
    items[0][propertyName] + items[1][propertyName] + items[2][propertyName]
  );
});

const group4Total = computed(() => {
  let propertyName = "group4";
  let items = infectionStatusByAgeGroup;
  return (
    items[0][propertyName] + items[1][propertyName] + items[2][propertyName]
  );
});


const infectedByAgeGroup = computed(() => {
  return infectionStatusByAgeGroup.filter((data) => {
    return data['category'] != "Uninfected";
  });
});

const group5Total = computed(() => {
  let propertyName = "group5";
  let items = infectionStatusByAgeGroup;
  return (
    items[0][propertyName] + items[1][propertyName] + items[2][propertyName]
  );
});


const checkGroupTotal = (data, groupName, newValue) => {
  let validTotal = false;

  let result = 0;

  Object.keys(data).forEach((key) => {
    if (key == groupName) {
      result += newValue;
    }
    else {
      result += data[groupName];
    }
  });

  validTotal = result == 100;

  return validTotal;
}

const allGroupValid = computed(() => {
  console.log(`group1Total: ${group1Total.value}, group2Total: ${group2Total.value}, group3Total: ${group3Total.value}, group4Total: ${group4Total.value}, group5Total: ${group5Total.value}`);
  // what I need to check is all the allocation (primary + booster) is equal to or less than the allocated proportion
  return group1Total.value == 100 && group2Total.value == 100 && group3Total.value == 100 && group4Total.value == 100 && group5Total.value == 100;
});


const vaccine1Total = computed(() => {
  let allocation = vaccineList[0].allocation;

  // version 2: use other properties
  return computeAllocationTotal(allocation);


  // version 1: calculate directly
  /*
 let total = 0;
 
  for(let i = 1; i <= 5; i++ ){
      let groupName = `group${i}`;
      total += allocation[0][groupName];
      total += allocation[1][groupName];
  }
  return total;
  */
});

// vaccine.allocation
const extractFulldoseAllocation = (allocationList) => {
  return allocationList.filter((oneAllocation) => {
    return oneAllocation.category == "Full dose";
  });
};

const extractBoosterAllocation = (allocationList) => {
  return allocationList.filter((oneAllocation) => {
    return oneAllocation.category == "Booster";
  }).map((oneAllocation) => {
    return oneAllocation.primaryMatching;
  })[0];
}


const computeAllocationTotal = (allocationList) => {
  // version 2:
  return GeneralUtility.sumNumbersAsDecimal([computeAllocationFulldoseTotal(allocationList), computeAllocationBoosterTotal(allocationList)]);


  // version 1
  /*
  let allocation = allocationList;
  let total = 0;

  for(let i = 1; i <= 5; i++ ){
      let groupName = `group${i}`;
      total += allocation[0][groupName];
      total += allocation[1][groupName];
  }
  return total;
  */
};

const computeAllocationFulldoseTotal = (allocationList) => {
  let allocation = allocationList;
  let total = 0;


  let numList = [];

  for (let i = 1; i <= 5; i++) {
    let groupName = `group${i}`;
    //total += allocation[0][groupName];

    numList.push(allocation[0][groupName]);
  }
  total = GeneralUtility.sumNumbersAsDecimal(numList);

  //console.log(`computeAllocationFulldoseTotal: ${total}`);

  return total;
};

const computeAllocationBoosterTotal = (allocationList) => {
  let allocation = allocationList;
  let total = 0;
  let numList = [];

  for (let i = 1; i <= 5; i++) {
    let groupName = `group${i}`;
    // allocation[1] -> supposedly booster
    allocation[1]["primaryMatching"].forEach((matching) => {
      //total += matching[groupName];
      numList.push(matching[groupName]);
    });

  }

  total = GeneralUtility.sumNumbersAsDecimal(numList);

  //console.log(`computeAllocationBoosterTotal: ${total}`);
  return total;
};


const vaccinatedBeforeNewVaccineByGroupList = computed((vaccinePlaceHolder) => {

  let result = [0, 0, 0, 0, 0];

  /*
  result = Object.keys(vaccinationStatusByAgeGroup).map((groupName, index) => {
    let groupSize = region.value.populationList == undefined? 0: region.value.populationList[index];
    
    let vaccineInfoList = vaccinationStatusByAgeGroup[groupName].filter((vaccineInfo) => {
      return vaccineInfo.category == vaccinePlaceHolder;
    });

    console.log(`vaccinatedBeforeNewVaccineByGroupList.vaccineInfoList (${vaccinePlaceHolder}): ${vaccineInfoList}`);

    let proportion = vaccinationStatusByAgeGroup[groupName].filter((vaccineInfo) => {
      return vaccineInfo.category == vaccinePlaceHolder;
    })[0]["fulldose"];

    
    vaccinationStatusByAgeGroup[groupName].filter((vaccineInfo) => {
      return vaccineInfo.category == vaccinePlaceHolder;
    });
    
    return Math.floor(proportion/100 * groupSize);
  });
  */


  return result;

});

const vaccinatedUnBoostedTotalAfterNewVaccineByGroupList = computed(() => {

  let result = [0, 0, 0, 0, 0];

  result = vaccinatedTotalAfterNewVaccineByGroupList.value.map((vNum, index) => {
    let bNum = boostedTotalAfterNewVaccineByGroupList.value[index];
    return vNum - bNum;
  });

  return result;

});

const vaccinatedTotalAfterNewVaccineByGroupList = computed(() => {
  let vaccinatedAfterNewVaccine = regionParameters.region.populationList != undefined ? regionParameters.region.populationList : [0, 0, 0, 0, 0];

  vaccinatedAfterNewVaccine = vaccinatedAfterNewVaccine.map((num, index) => {
    let result = num - unvaccinatedTotalAfterNewVaccineByGroupList.value[index];
    //console.log(`vaccinatedTotalAfterNewVaccineByGroupList: ${num} - ${unvaccinatedTotalAfterNewVaccineByGroupList.value[index]} = ${result}`);
    return result;
  });

  return vaccinatedAfterNewVaccine;
});

const unvaccinatedTotalAfterNewVaccineByGroupList = computed(() => {

  let unvaccinatedAfterNewVaccine = [0, 0, 0, 0, 0];

  // before the new vaccine
  let originalUnvaccinated = unvaccinatedTotalByGroupList;

  // after the newly allocated vaccine
  let vaccinatedWithNewVaccine = vaccinatedWithNewVaccineByGroupList;

  unvaccinatedAfterNewVaccine = originalUnvaccinated.value.map((num, index) => {
    //console.log(`unvaccinatedTotalAfterNewVaccineByGroupList[${index}]: ${num} - ${vaccinatedWithNewVaccine.value[index]}`);
    return num - vaccinatedWithNewVaccine.value[index];
  });


  return unvaccinatedAfterNewVaccine;
});

const vaccinatedWithNewVaccineByGroupList = computed(() => {
  // this is about fulldose/primary series
  // vaccineList

  let vaccinatedWithNewVaccine = [0, 0, 0, 0, 0];

  vaccineList.forEach((allocationInfo) => {
    let vaccineNumber = allocationInfo.number;
    let fulldoseAllocation = allocationInfo.allocation[0];
    for (let i = 1; i <= 5; i++) {
      let groupName = `group${i}`;
      //console.log(`vaccinatedWithNewVaccine[${i - 1}]: minus ${vaccineNumber} * ${fulldoseAllocation.proportion} * ${fulldoseAllocation[groupName]}`);
      let newVaccineNumber = vaccineNumber * fulldoseAllocation[groupName] * 0.01;

      // let newVaccineNumber = vaccineNumber * fulldoseAllocation.proportion * 0.01 * fulldoseAllocation[groupName] * 0.01;

      vaccinatedWithNewVaccine[i - 1] += newVaccineNumber != null ? Math.floor(newVaccineNumber) : 0;

      //console.log(`vaccinatedWithNewVaccine[${i - 1}]: ${vaccinatedWithNewVaccine[i - 1]}`);
    }
  });

  //console.log(`vaccinatedWithNewVaccine: ${vaccinatedWithNewVaccine}`);
  return vaccinatedWithNewVaccine;
});


const unvaccinatedTotalByGroupList = computed(() => {

  let knownUnvaccinated = Object.keys(vaccinationStatusByAgeGroup).map((groupName, index) => {
    //console.log(`unvaccinatedTotalByGroupList: index : ${index}`);
    //console.log(`unvaccinatedTotalByGroupList: region : ${JSON.stringify(regionParameters)}`);
    //console.log(`unvaccinatedTotalByGroupList: region.populationList : ${regionParameters.region.populationList}`);
    return Math.floor(vaccinationStatusByAgeGroup[groupName][3]["fulldose"] / 100 * (regionParameters.region.populationList == undefined ? 0 : regionParameters.region.populationList[index]));
  });

  return knownUnvaccinated;
});


const boostedTotalAfterNewVaccineByGroupList = computed(() => {

  let boostedAfterNewVaccine = regionParameters.region.populationList != undefined ? regionParameters.region.populationList : [0, 0, 0, 0, 0];



  boostedAfterNewVaccine = boostedAfterNewVaccine.map((num, index) => {
    let result = num - unboostedTotalAfterNewVaccineByGroupList.value[index];
    //console.log(`boostedTotalAfterNewVaccineByGroupList: ${num} - ${unboostedTotalAfterNewVaccineByGroupList.value[index]} = ${result}`);
    return result;
  });

  return boostedAfterNewVaccine;

});


const unboostedTotalAfterNewVaccineByGroupList = computed(() => {

  let unboostedAfterNewVaccine = [0, 0, 0, 0, 0];

  // before the new vaccine
  let originalUnboosted = unboostedTotalByGroupList;

  // after the newly allocated vaccine
  let boostedWithNewVaccine = boostedWithNewVaccineByGroupList;

  unboostedAfterNewVaccine = originalUnboosted.value.map((num, index) => {
    //console.log(`unboostedTotalAfterNewVaccineByGroupList[${index}]: ${num} - ${boostedWithNewVaccine.value[index]}`);
    return num - boostedWithNewVaccine.value[index];
  });


  return unboostedAfterNewVaccine;
});

const boostedWithNewVaccineByGroupList = computed(() => {
  // this is about fulldose/primary series
  // vaccineList

  let boostedWithNewVaccine = [0, 0, 0, 0, 0];



  // wait... there are three types of vaccine

  vaccineList.forEach((allocationInfo) => {
    let vaccineNumber = allocationInfo.number;
    let boosterAllocation = allocationInfo.allocation[1];
    let boostedProportion = [0, 0, 0, 0, 0];

    for (let i = 1; i <= 5; i++) {
      let groupName = `group${i}`;

      boosterAllocation["primaryMatching"].forEach((matching, index) => {
        boostedProportion[i - 1] += matching[groupName];
      });

      //console.log(`boostedWithNewVaccine[${allocationInfo.category}][${groupName}]: minus ${vaccineNumber} * ${boostedProportion[i - 1]}%`);

      let newVaccineNumber = vaccineNumber * boostedProportion[i - 1] * 0.01;

      boostedWithNewVaccine[i - 1] += newVaccineNumber != null ? Math.floor(newVaccineNumber) : 0;

      //console.log(`accinatedWithNewVaccine[${i - 1}]: ${boostedWithNewVaccine[i - 1]}`);
    }
  });

  //console.log(`vaccinatedWithNewVaccineByGroupList: ${boostedWithNewVaccine}`);
  return boostedWithNewVaccine;
});


const unboostedTotalByGroupList = computed(() => {

  let knownUnboosted = Object.keys(vaccinationStatusByAgeGroup).map((groupName, index) => {
    /*
    console.log(`unboostedTotalByGroupList: index : ${index}`);
    console.log(`unboostedTotalByGroupList: region : ${JSON.stringify(regionParameters)}`);
    console.log(`unboostedTotalByGroupList: region.populationList : ${regionParameters.region.populationList}`);
    */
    return Math.floor(vaccinationStatusByAgeGroup[groupName][3]["booster"] / 100 * (regionParameters.region.populationList == undefined ? 0 : regionParameters.region.populationList[index]));
  });

  return knownUnboosted;
});

/*
const vaccine1FulldoseAllocation = computed(() => {
    let allocation = vaccineList[0].allocation.filter((oneAllocation) => {
      return oneAllocation.category == "Full dose";
    });
    return allocation;
});
*/

const vaccine1FulldoseTotal = computed(() => {
  let allocation = vaccineList[0].allocation;
  let total = 0;

  for (let i = 1; i <= 5; i++) {
    let groupName = `group${i}`;
    total += allocation[0][groupName];
    //total += allocation[1][groupName];
  }
  //console.log(`vaccine1FulldoseTotal: ${total}`);
  return total;
});

const vaccine1BoosterTotal = computed(() => {
  let allocation = vaccineList[0].allocation;
  let total = 0;

  for (let i = 1; i <= 5; i++) {
    let groupName = `group${i}`;
    //total += allocation[0][groupName];
    total += allocation[1][groupName];
  }
  return total;
});

const vaccine2Total = computed(() => {
  let allocation = vaccineList[1].allocation;

  // version 2: use other properties
  return computeAllocationTotal(allocation);

  /*
 let total = 0;
 
  for(let i = 1; i <= 5; i++ ){
      let groupName = `group${i}`;
      total += allocation[0][groupName];
      total += allocation[1][groupName];
  }
  return total;
  */
});



const vaccine3Total = computed(() => {
  let allocation = vaccineList[2].allocation;

  // version 2: use other properties
  return computeAllocationTotal(allocation);

  /*
 let total = 0;
 
  for(let i = 1; i <= 5; i++ ){
      let groupName = `group${i}`;
      total += allocation[0][groupName];
      total += allocation[1][groupName];
  }
  return total;
  */
});


const allAllocationValid = computed(() => {
  //console.log(`vaccine1Total: ${vaccine1Total.value}, vaccine2Total: ${vaccine2Total.value}, vaccine3Total: ${vaccine3Total.value}`);
  //return vaccine1Total.value <= 100 && vaccine2Total.value <= 100 && vaccine3Total.value <= 100;

  return vaccineList.every((oneAvailability) => {
    return computeAllocationFulldoseTotal(oneAvailability.allocation) <= oneAvailability.allocation[0].proportion && computeAllocationBoosterTotal(oneAvailability.allocation) <= oneAvailability.allocation[1].proportion;
  });
});

const getVaccineTotal = (index) => {
  switch (index) {
    case 0:
      return vaccine1Total;
    case 1:
      return vaccine2Total;
    case 2:
      return vaccine3Total;
    default:
      return 0;
  }

};


const convertVaccineLabel = (placholderName) => {
  //console.log(`convertVaccineLabel: ${placholderName}`);

  //console.log(`convertVaccineLabel vaccine1.name: ${vaccineList[0].name}`);

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

  //console.log(`convertVaccineLabel result: ${result}`);

  return result;
}

// <20, 20-49, 50-64, 65-74, >=75
const columns = reactive([
  { field: "category", header: "Category" },
  { field: "group1", header: "< 20" },
  { field: "group2", header: "20 - 49" },
  { field: "group3", header: "50 - 64" },
  { field: "group4", header: "65 - 74" },
  { field: "group5", header: ">= 75" },
]);

// <20, 20-49, 50-64, 65-74, >=75
const boosterColumns = reactive([
  { field: "primary", header: "For people who received a primary series with vaccine product:" },
  { field: "group1", header: "< 20" },
  { field: "group2", header: "20 - 49" },
  { field: "group3", header: "50 - 64" },
  { field: "group4", header: "65 - 74" },
  { field: "group5", header: ">= 75" },
]);



const onCellEditComplete = (event) => {
  let { data, newValue, field } = event;

  console.log(`onCellEditComplete: ${JSON.stringify(data, null, 2)}, ${field}, ${newValue}`);
  //console.log(`onCellEditComplete typeof newValue: ${typeof newValue}`);
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


const onStrategyChange = (distributionTool, indexList = [0, 1, 2]) => {
  //console.log(`onStrategyChange: ${JSON.stringify(distributionTool)}`);

  let newVaccineList = distributionTool.distribute(strategyList.value[selectedStrategyIndex.value]["vaccineParameters"]["vaccineList"], indexList);


  //console.log(`newVaccineList: ${JSON.stringify(newVaccineList)}`);

  //  it actually looks orrect up till here


  // reference
  /*
  store.$patch((state) => {
    state.items.push({ name: 'shoes', quantity: 1 })
    state.hasChanged = true
  })
  */

  strategiesStore.$patch((state) => {
    state.strategyList[strategyIndex]["vaccineParameters"]["vaccineList"] = newVaccineList;
  })

  //currentStrategy["vaccineParameters"]["vaccineList"] = newVaccineList;

  //vaccineList = newvaccineList;
  
  /*
  vaccineStore.$patch({
      vaccineAvailability: newvaccineList
  });
  */
  
}

/*
let fulldoseLessThanTotalMsg =  "Not all proportion of the primary series is allocated.";
let fulldoseMoreThanTotalMsg = "Can not allocate more than the available proportion for the primary series. Please reduce the proportion for certain age groups.";


let boosterLessThanTotalMsg = "Not all proportion of the booster is allocated.";
let boosterMoreThanTotalMsg = "Can not allocate more than the available proportion for the booster. Please reduce the proportion for certain age groups.";


const lessThan100Msg = "Not all 100% of vaccine is allocated.";
const moreThan100Msg = "Can not allocate more than 100% of the vaccines. Please reduce the proportion for certain age groups.";
*/

const onInputPercentageChange = (event, index) => {
  console.log(`onInputPercentageChange [${index}]: ${JSON.stringify(event)}`);

  // version 2:
  if( event.value >= 0 && event.value <= 100){
    let newAvailabilityAllocation = [...vaccineList[index].allocation];
    newAvailabilityAllocation = newAvailabilityAllocation.map((allocation, aIndex) => {
      let totalAllowance = 100;
      return aIndex == 0 ? { ...allocation, proportion: event.value } : { ...allocation, proportion: GeneralUtility.minusNumbersAsDecimal(totalAllowance, event.value) }
    });

    vaccineList[index].allocation = newAvailabilityAllocation;
  }
  else if ( event.value > 100){
    let newAvailabilityAllocation = [...vaccineList[index].allocation];
    newAvailabilityAllocation = newAvailabilityAllocation.map((allocation, aIndex) => {
      let totalAllowance = 100;
      return aIndex == 0 ? { ...allocation, proportion: 100 } : { ...allocation, proportion: 0 };
    });

    vaccineList[index].allocation = newAvailabilityAllocation;
  }
  else if ( event.value < 0){
    let newAvailabilityAllocation = [...vaccineList[index].allocation];
    newAvailabilityAllocation = newAvailabilityAllocation.map((allocation, aIndex) => {
      let totalAllowance = 100;
      return aIndex == 0 ? { ...allocation, proportion: 0 } : { ...allocation, proportion: 100 };
    });

    vaccineList[index].allocation = newAvailabilityAllocation;
  }

}


const onInputBlur = (event, obj, vaccineIndex, allocationIndex) => {
  console.log(`onInputBlur: vaccineIndex: ${vaccineIndex}, allocationIndex: ${allocationIndex}`);
  console.log(
    `onInputBlur: data ${JSON.stringify(obj.data)}, field: ${JSON.stringify(
      obj.field
    )}, value: ${event.value}, type: ${typeof event.value}`
  );

  let inputValue = Number(voca.replaceAll(event.value, ",", ""));
  let resultValue = 0;

  resultValue = Math.min(Math.max(inputValue, 0), 100);

  currentStrategy["vaccineParameters"]["vaccineList"][vaccineIndex].allocation[allocationIndex][obj.field] = resultValue;// event.value;

  /*
  //obj.data[obj.field] = event.value;
  console.log(`currentStrategy["regionParameters"]["infectionStatus"]: ${JSON.stringify(currentStrategy["regionParameters"]["infectionStatus"])}`);
  currentStrategy["regionParameters"]["infectionStatus"].filter((eInfo) => {
    return eInfo.category == obj.data.category;
  })[0][obj.field] = Number(event.value);

  */


  //updateUninfected(obj.field);
  //onInfectionStatusChange({data: obj.data, field: obj.field, value: event.value});
};

const onInputBoosterBlur = (event, obj, vaccineIndex, allocationIndex) => {
  console.log(`onInputBoosterBlur: vaccineIndex: ${vaccineIndex}, allocationIndex: ${allocationIndex}`);
  console.log(
    `onInputBoosterBlur: data ${JSON.stringify(obj.data)}, field: ${JSON.stringify(
      obj.field
    )}, value: ${event.value}, type: ${typeof event.value}`
  );

  let inputValue = Number(voca.replaceAll(event.value, ",", ""));
  let resultValue = 0;

  resultValue = Math.min(Math.max(inputValue, 0), 100);

  console.log(`currentStrategy["vaccineParameters"]["vaccineList"][vaccineIndex].allocation[allocationIndex]['primaryMatching']: ${JSON.stringify(currentStrategy["vaccineParameters"]["vaccineList"][vaccineIndex].allocation[allocationIndex]['primaryMatching'])}`);

  currentStrategy["vaccineParameters"]["vaccineList"][vaccineIndex].allocation[allocationIndex]['primaryMatching'].filter((eInfo) => {
    return eInfo.primary == obj.data.primary;
  })[0][obj.field] = resultValue; //Number(event.value);

  /*
  //obj.data[obj.field] = event.value;
  console.log(`currentStrategy["regionParameters"]["infectionStatus"]: ${JSON.stringify(currentStrategy["regionParameters"]["infectionStatus"])}`);
  currentStrategy["regionParameters"]["infectionStatus"].filter((eInfo) => {
    return eInfo.category == obj.data.category;
  })[0][obj.field] = Number(event.value);

  */


  //updateUninfected(obj.field);
  //onInfectionStatusChange({data: obj.data, field: obj.field, value: event.value});
};



const onCalendarInput = (event) => {
  console.log(`onCalendarInput: ${event}`);
};

const onCalendarDateSelect = (event) => {
  console.log(`onCalendarDateSelect: ${event}`);

  let { data, newValue, vaccineIndex, allocationIndex } = event;

  console.log(`onCalendarDateSelect: ${JSON.stringify(data, null, 2)}, ${vaccineIndex}, ${newValue}`);



  // need to update the date property in the allocation



  currentStrategy["vaccineParameters"]["vaccineList"][vaccineIndex]["allocation"][allocationIndex]["date"] = newValue;






  /*
  let newInterval = [...data];
  newInterval[index] = newValue; //DateTime.fromJSDate(newValue).startOf("day").toJSDate();

  currentStrategy["simulationInterval"] = newInterval;


  // version 2, use  GeneralUtility
  currentStrategy["simulationDays"]  = GeneralUtility.diffDateByUnits(newInterval[0], newInterval[1], "days");
  */

};

const onCalendarHide = (event) => {
  console.log(`onCalendarHide`);
};


/*
will be available on {{ DateTime.fromJSDate(vaccine.date).toISODate() }}
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
      
      <h1>Vaccine Allocation Strategy {{ selectedStrategyIndex+1 }}</h1>
      <Divider class="fh-divider-primary"></Divider>
      <Fieldset>
        <template #legend>
          <h3>Summary</h3>
        </template>
        <div>Region: {{ regionParameters.region.name }}</div>
        <div>Population size: {{
          regionParameters.region != undefined && regionParameters.region.populationList !=
            undefined ? regionParameters.region.populationList.reduce((a, b) => a + b, 0).toLocaleString(undefined) : "?"
        }}
        </div>
        <div class="hidden">
          <div>Nubmer of people unvaccinated (before): {{ unvaccinatedTotalByGroupList }}</div>
          <div>Nubmer of people unvaccinated (after ): {{ unvaccinatedTotalAfterNewVaccineByGroupList }}</div>
          <div>Nubmer of people vaccinated (after ): {{ vaccinatedTotalAfterNewVaccineByGroupList }}</div>

          <div>Number of people unboosted (before): {{ unboostedTotalByGroupList }}</div>
          <div>Number of people unboosted (after ): {{ unboostedTotalAfterNewVaccineByGroupList }}</div>
          <div>Number of people boosted (after ): {{ boostedTotalAfterNewVaccineByGroupList }}</div>

          <div>Number of people vaccinated * unboosted (after): {{ vaccinatedUnBoostedTotalAfterNewVaccineByGroupList }}
          </div>
          <div>Number of people vaccinated(1) (after-notworking): {{ vaccinatedBeforeNewVaccineByGroupList }}</div>
          <div>Number of people vaccinated(2) (after-notworking): {{}}</div>
          <div>Number of people vaccinated(3) (after-notworking): {{}}</div>
        </div>
      </Fieldset>
      <Divider class="mt-6" style="opacity: 0"></Divider>
      <div class="grid">
        <div class="col">

          <div v-for="(vaccine, vaccineIndex) in strategyList[strategyIndex].vaccineParameters.vaccineList" :key="vaccineIndex">
            <Fieldset>
              <template #legend>
                <h3>{{ convertVaccineLabel(vaccine.category) }}</h3>
              </template>
              <h4>Total: {{ vaccine.number }} doses</h4>
              <h4 v-show="vaccine.number > 0">
                
                Primary series starts on:&nbsp;<Calendar :id="0" v-model="vaccine.allocation[0].date" dateFormat="yy-mm-dd" :touchUI="true"

                @input="onCalendarInput"

                @date-select="onCalendarDateSelect({data: vaccine.allocation[0], newValue: vaccine.allocation[0].date, vaccineIndex: vaccineIndex, allocationIndex: 0})"

                @hide="onCalendarHide"

                />, 
                Booster starts on:&nbsp;<Calendar :id="1" v-model="vaccine.allocation[1].date" dateFormat="yy-mm-dd" :touchUI="true"

                @input="onCalendarInput"

                @date-select="onCalendarDateSelect({data: vaccine.allocation[1], newValue: vaccine.allocation[1].date,  vaccineIndex: vaccineIndex, allocationIndex: 1})"

                @hide="onCalendarHide"

                />

              </h4>
              <div v-show="vaccine.number > 0">
                <h4>Specify how you plan to allocate these doses (in %): {{ getVaccineTotal(index) }}% allocated</h4>
                <AllocationMethodList @change="(event) => { onStrategyChange(event, [index]) }"></AllocationMethodList>
                <br />
                <br />
                <h4>Primary series</h4>
                <InputNumber v-model="vaccine.allocation[0].proportion" inputClass="text-1xl" mode="decimal"
                  :minFractionDigits="1" :maxFractionDigits="2" :allowEmpty="false" :min="0" :max="100"
                  @input="(event) => { onInputPercentageChange(event, index) }"
                  />&nbsp;% &nbsp;<spam>
                  ({{ computeAllocationFulldoseTotal(vaccine.allocation) }} % used, {{
                    GeneralUtility.minusNumbersAsDecimal(vaccine.allocation[0].proportion,
                      computeAllocationFulldoseTotal(vaccine.allocation))
                  }} % left)</spam>
                <br />
                <br />
                <DataTable :value="[vaccine.allocation[0]]" editMode="cell"
                  @cell-edit-complete="onCellEditComplete" responsiveLayout="scroll">
                  <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field"
                    style="width: 18%" headerClass="fh-table-header">
                    <template v-if="col.field == 'category'" #body="slotProps">
                      <div>{{ convertVaccineTypeLabel(slotProps.data[slotProps.field]) }}</div>
                    </template>
                    <template v-if="col.field != 'category'" #editor="slotProps">
                      <InputNumber mode="decimal" :minFractionDigits="0" :maxFractionDigits="2" :allowEmpty="false" :min="0" :max="100" 
                        v-model="slotProps.data[slotProps.field]" 
                        @blur="
                          (event) => {
                            onInputBlur(event, slotProps, index, 0);
                          }
                        "
                        />
                    </template>
                  </Column>
                </DataTable>
                <div>
                  <Message severity="warn"
                    v-if="computeAllocationFulldoseTotal(vaccine.allocation) < vaccine.allocation[0].proportion"
                    :closable="false">{{ fulldoseLessThanTotalMsg }}</Message>
                  <Message severity="error"
                    v-if="computeAllocationFulldoseTotal(vaccine.allocation) > vaccine.allocation[0].proportion"
                    :closable="false">{{ fulldoseMoreThanTotalMsg }}</Message>
                </div>

                <h4>Booster</h4>
                <h5>Indicate how boosters are allocated for people using different vaccines as their primary series:
                </h5>
                <InputNumber v-model="vaccine.allocation[1].proportion" inputClass="text-1xl" mode="decimal"
                  :minFractionDigits="0" :maxFractionDigits="2" :allowEmpty="false" :min="0"  :max="100" :readonly="true" disabled />&nbsp;% &nbsp;
                <spam>({{ computeAllocationBoosterTotal(vaccine.allocation) }} % used, {{
                  GeneralUtility.minusNumbersAsDecimal(vaccine.allocation[1].proportion,
                    computeAllocationBoosterTotal(vaccine.allocation))
                }} % left)</spam>
                <br />
                <br />
                <DataTable :value="vaccine.allocation[1]['primaryMatching']" editMode="cell"
                  @cell-edit-complete="onCellEditComplete" responsiveLayout="scroll">
                  <Column v-for="col of boosterColumns" :field="col.field" :header="col.header" :key="col.field"
                    style="width: 18%" headerClass="fh-table-header">
                    <template v-if="col.field == 'primary'" #body="slotProps">
                      <div>{{ convertVaccineLabel(slotProps.data[slotProps.field]) }}</div>
                    </template>
                    <template v-if="col.field != 'primary'" #editor="slotProps">
                      <InputNumber mode="decimal" :minFractionDigits="0" :maxFractionDigits="2" :allowEmpty="false" :min="0"  :max="100" 
                        v-model="slotProps.data[slotProps.field]" 
                        @blur="
                          (event) => {
                            onInputBoosterBlur(event, slotProps, index, 1);
                          }
                        "
                        />
                    </template>
                  </Column>
                </DataTable>
                <div>
                  <Message severity="warn"
                    v-if="computeAllocationBoosterTotal(vaccine.allocation) < vaccine.allocation[1].proportion"
                    :closable="false">{{ boosterLessThanTotalMsg }}</Message>
                  <Message severity="error"
                    v-if="computeAllocationBoosterTotal(vaccine.allocation) > vaccine.allocation[1].proportion"
                    :closable="false">{{ boosterMoreThanTotalMsg }}</Message>
                </div>
                <br />
                <div>
                  <Message severity="warn" v-if="computeAllocationTotal(vaccine.allocation) < 100" :closable="false">
                    {{ lessThan100Msg }}</Message>
                  <Message severity="error" v-if="computeAllocationTotal(vaccine.allocation) > 100" :closable="false">
                    {{ moreThan100Msg }}</Message>
                </div>

              </div>
            </Fieldset>
            <Divider class="mt-6" style="opacity: 0"></Divider>


          </div>
        </div>
      </div>

      <div>
        <div class="flex justify-content-center mt-4 mb-4">
          <Button label="Next" class="p-button-lg fh-button-primary" :disabled="!allAllocationValid" @click="onNextClick"></Button>
        </div>
        <Divider class="fh-divider-primary"></Divider>
        <Footer></Footer>
      </div>
    </div>
    <div class="col-2"></div>
  </div>
</template>


