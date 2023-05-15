import { defineStore } from "pinia";
import { ref, watch  } from "vue";
import { DateTime, Interval } from "luxon";
import {Decimal} from 'decimal.js';
import GeneralUtility from "../lib/GeneralUtility.mjs";
import { regionNameInfectionMap, vaccineList, presetStrategyList } from "../content/variable.js";



let nowDate = DateTime.utc().startOf("day");
let jsDate = nowDate.toJSDate();
let nowDateString = nowDate.toISODate();

export const useStrategiesStore = defineStore("strategies", () => {
  let selectedStrategyIndex = ref(0);


  // let strategyList = ref([createStrategy(true, true)]);
  let strategyList = ref([createStrategy(false, false)]);

  /*
  watch(strategyList, async (newStrategyList, oldStrategyList) => {
    console.log(`strategyList watch: change`);
  },{ deep: true, immediate: true })
  */

  function addStrategy() {
    let newStrategy = createStrategy();
    strategyList.value.push(newStrategy);
  }

  function usePresetStrategyByIndex(index) {
    console.log(`usePresetStrategyByIndex: index: ${index}`);

    let presetStrategyListCopy = presetStrategyList.map((strategy) => {
      return GeneralUtility.convertStrategyFromJSON(JSON.stringify(strategy));
    });

    setStrategyList([presetStrategyListCopy[index]]);

    selectStrategy(0);

  }

  function usePresetStrategyList() {
    console.log(`usePresetStrategyList`);

    let presetStrategyListCopy = presetStrategyList.map((strategy) => {
      return GeneralUtility.convertStrategyFromJSON(JSON.stringify(strategy));
    });
    
    
    //  GeneralUtility.convertStrategyFromJSON(JSON.stringify(presetStrategyList));

    strategyList.value.push.apply(strategyList.value, presetStrategyListCopy);

  }

  function setStrategyList(newStrategyList) {
    console.log(`setStrategyList`);
    clearStrategyList();

    strategyList.value.push.apply(strategyList.value, newStrategyList);
  }

  function clearStrategyList() {
    console.log(`clearStrategyList`);
    strategyList.value.splice(0, strategyList.value.length);
  }

  function resetStrategyList() {
    console.log(`resetStrategyList`);
    strategyList.value.splice(0, strategyList.value.length);
    strategyList.value.push(createStrategy(false, false));
  }

  function addDuplicateOfCurrentStrategy() {
    console.log(
      `addDuplicateOfCurrentStrategy: selectedStrategyIndex: ${selectedStrategyIndex}, strategyList.value:${
        strategyList.value
      }, strategyList[selectedStrategyIndex]:${
        strategyList.value[selectedStrategyIndex.value]
      }`
    );

    // version 2: function
    duplicateStrategyByIndex(selectedStrategyIndex.value);

    // version 1: code
    /*
    let currentStrategy = strategyList.value[selectedStrategyIndex.value];
    console.log(`addDuplicateOfCurrentStrategy: currentStrategy: ${currentStrategy}`);

    let newStrategy = JSON.parse(JSON.stringify(currentStrategy));

    strategyList.value.push(newStrategy);
    */
  }

  function duplicateStrategyByIndex(index) {
    console.log(`duplicateStrategyByIndex: index: ${index}`);

    let targetStrategy = strategyList.value[index];
    console.log(`duplicateStrategyByIndex: targetStrategy: ${targetStrategy}`);

    
    let newStrategy = GeneralUtility.convertStrategyFromJSON(JSON.stringify(targetStrategy));

    // GeneralUtility.convertStrategyFromJSON

    /*
    let newStrategy = JSON.parse(JSON.stringify(targetStrategy));

    // remember to set the simulationInterval
    newStrategy["simulationInterval"][0] = DateTime.fromISO(
      newStrategy["simulationInterval"][0]
    ).toJSDate();
    newStrategy["simulationInterval"][1] = DateTime.fromISO(
      newStrategy["simulationInterval"][1]
    ).toJSDate();

    */

    strategyList.value.push(newStrategy);
  }

  function removeStrategyByIndex(index) {
    console.log(`removeStrategyByIndex: index: ${index}`);

    let oneElementList = strategyList.value.splice(index, 1);

    // If only one element is removed, an array of one element is returned.

    if( selectedStrategyIndex.value == index ){
      selectStrategy(0);
    }

  }

  function updateStrategySimulatedOutcomeByIndex(index, simulatedOutcome) {
    console.log(`updateStrategySimulatedOutcomeByIndex: index: ${index}`);

    strategyList.value[index]["simulatedOutcome"] = simulatedOutcome;
    strategyList.value[index]["simulatedOutcomeLastUpdateTime"] = DateTime.now().toISO();

    console.log(`updateStrategySimulatedOutcomeByIndex[${index}]: simulatedOutcome: ${JSON.stringify(simulatedOutcome)}`);


    console.log(`updateStrategySimulatedOutcomeByIndex[${index}]: cumulativeNumberOfDeaths: ${simulatedOutcome["cumulativeNumberOfDeaths"]}`);

  }



  function clearSimulatedOutcomeByIndex(index) {
    console.log(`clearSimulatedOutcomeByIndex: index: ${index}`);

    strategyList.value[index]["simulatedOutcome"] = {
      cases: {},
      deaths: {},
    };
  }

  function selectStrategy(sIndex) {
    console.log(
      `selectStrategy: ${sIndex}, strategyList.length: ${strategyList.value.length}`
    );
    if (sIndex < strategyList.value.length) {
      console.log(`selectStrategy: ${sIndex} < ${strategyList.value.length}`);
      selectedStrategyIndex.value = sIndex;
    }
  }

  function generateEfficacyDataTtemplate(vaccineCode) {

    let selectedInfoList = vaccineList.filter((vaccineInfo) => {
      return vaccineInfo.code == vaccineCode;
    });

    if(selectedInfoList.length > 0){
      return selectedInfoList[0].efficacyData;
    }
    
    // else

    return [
      {
        category: "Infection",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Symptomatic infection",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Hospitalization",
        fulldose: 0,
        booster: 0,
      },
      /*
      {
        category: "Infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Symptomatic infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Hospitalization after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      */
    ];
  }

  function generateAvailabilityDataTtemplate(defaultOrNot=false) {
    return {
      //category: "Vaccine 1",
      number: defaultOrNot? 1000000: 0,
      date: jsDate, //nowDateString
      rate: defaultOrNot? 100000: 0,
      allocation: [
        {
          category: "Full dose",
          date: jsDate,
          proportion: 100,
          group1: 100,
          group2: 0,
          group3: 0,
          group4: 0,
          group5: 0,
        },
        {
          category: "Booster",
          date: jsDate,
          proportion: 0,
          group1: 0,
          group2: 0,
          group3: 0,
          group4: 0,
          group5: 0,
          primaryMatching: [
            {
              primary: "Vaccine 1",
              group1: 0,
              group2: 0,
              group3: 0,
              group4: 0,
              group5: 0,
            },
            {
              primary: "Vaccine 2",
              group1: 0,
              group2: 0,
              group3: 0,
              group4: 0,
              group5: 0,
            },
            {
              primary: "Vaccine 3",
              group1: 0,
              group2: 0,
              group3: 0,
              group4: 0,
              group5: 0,
            },
          ],
        },
      ],
    };
  }

  function getValidVaccineDateDaysListByStrategyIndex(index, defaultStartDate){
    console.log(`getValidVaccineDateDaysListByStrategyIndex: ${index}, defaultStartDate: ${defaultStartDate}`);
    let stategy = strategyList.value[index];

    let vaccineList = stategy["vaccineParameters"]["vaccineList"];

    let validVaccineList = vaccineList.filter((vInfo) => {
      return vInfo.type != "";
    });


    // date, number/rate
    let dateDaysList = [];

    // version 2: a date for a primary/booster for each vaccine
    for(let i = 0; i < validVaccineList.length; i++){

      let vInfo = validVaccineList[i];
      
      console.log(`getValidVaccineDateDaysListByStrategyIndex: number: ${vInfo["number"]}, rate: ${vInfo["rate"]}`);

      vInfo.allocation.forEach((allocationInfo) => {
        let allocatedNumber = GeneralUtility.multiplyNumbersAsDecimal(vInfo["number"], GeneralUtility.divideNumbersAsDecimal(allocationInfo.proportion, 100));

        let calculatedDays = 0;

        if(vInfo["number"] != undefined && vInfo["rate"] != undefined && vInfo["rate"] > 0 && allocatedNumber > 0){
          calculatedDays  = Math.ceil(allocatedNumber/vInfo["rate"]) + 1;
          dateDaysList.push({startDate: allocationInfo.date, days: calculatedDays});
        }
      });

    }

    if( dateDaysList.length == 0){
      dateDaysList.push({startDate: defaultStartDate, days: 1});
    }

    // version 1: a date for a vaccine
    /*
    let dateDaysList = validVaccineList.map((vInfo) => {

      console.log(`getValidVaccineDateDaysListByStrategyIndex: date: ${vInfo.date}, number: ${vInfo["number"]}, rate: ${vInfo["rate"]}`);


      let calculatedDays = 0;

      if(vInfo["number"] != undefined && vInfo["rate"] != undefined && vInfo["rate"] > 0){
        calculatedDays  = Math.ceil(vInfo["number"]/vInfo["rate"]) + 1;
      }

      return {startDate: vInfo.date, days: calculatedDays};

    });
    */

    return dateDaysList;
  }

  function updateSimulationParametersByStrategyIndex(index){
    console.log(`updateSimulationParametersByStrategyIndex: ${index}`);

    //strategyList.value[index]["regionParameters"]["infectionStatus"] = generateInfectionStatusList(strategyList.value[index]["regionParameters"]["region"]["name"]);

    /*
    let stategy = strategyList.value[index];

    let vaccineList = stategy["vaccineParameters"]["vaccineList"];

    let validVaccineList = vaccineList.filter((vInfo) => {
      return vInfo.type != "";
    });


    // date, number/rate

    let dateDaysList = validVaccineList.map((vInfo) => {
      console.log(`updateSimulationParametersByStrategyIndex: date: ${vInfo.date}, number: ${vInfo["number"]}, rate: ${vInfo["rate"]}`);
      return {startDate: vInfo.date, days: Math.ceil(vInfo["number"]/vInfo["rate"])}
    });

    */

    let stategy = strategyList.value[index];

    let dateDaysList = getValidVaccineDateDaysListByStrategyIndex(index, strategy.simulationInterval[0]);

    console.log(`updateSimulationParametersByStrategyIndex: dateDaysList: ${JSON.stringify(dateDaysList)}`);

    let startEndResult = GeneralUtility.calculateStartAndEndWithDateAndDaysList(dateDaysList);

    console.log(`updateSimulationParametersByStrategyIndex: startEndResult: ${startEndResult}`);

    let recommendedStartDate = startEndResult[0];
    let recommendedEndDate = startEndResult[1];

    let selectedStartDate = recommendedStartDate;
    let selectedEndDate = recommendedEndDate;


    // update: simulationInterval:Array[2]
    // Constraint 1: the start date should be no later than the recommended one
    let simulationInterval = stategy["simulationInterval"];

    if( GeneralUtility.diffDateByUnits(simulationInterval[0], recommendedStartDate, "seconds") > 0  ){
      selectedStartDate = simulationInterval[0];
    }

    // Constraint 2: the end date should be no earlier than the recommended one
    if( GeneralUtility.diffDateByUnits(simulationInterval[1], recommendedEndDate, "seconds") < 0  ){
      selectedEndDate = simulationInterval[0];
    }

    // try only updating it if one of the date change

    if(GeneralUtility.diffDateByUnits(simulationInterval[0], selectedStartDate, "days") != 0 || GeneralUtility.diffDateByUnits(simulationInterval[1], selectedEndDate, "days") != 0
    ){
      stategy["simulationInterval"] = [selectedStartDate, selectedEndDate];
      console.log(`updateSimulationParametersByStrategyIndex: simulationInterval: ${simulationInterval}`);
    }
    
    

    // update: simulationDays:180
    let simulationDays = GeneralUtility.diffDateByUnits(selectedStartDate, selectedEndDate, "days");

    if( simulationDays != stategy["simulationDays"]){
      stategy["simulationDays"] = simulationDays;
      console.log(`updateSimulationParametersByStrategyIndex: simulationDays: ${simulationDays}`);
    }
    
  }

  function updateRegionParametersByStrategyIndex(index){
    strategyList.value[index]["regionParameters"]["infectionStatus"] = generateInfectionStatusList(strategyList.value[index]["regionParameters"]["region"]["name"]);
  }

  function generateInfectionStatusList(regionName){
    let infectedNumber = new Decimal(0);
    let totalNumber = new Decimal(100);

    if(regionNameInfectionMap[regionName] != undefined){
      infectedNumber = new Decimal(regionNameInfectionMap[regionName]);
    }

    // else, return a typical one

    return [
      {
        category: "Previously Infected",
        group1: infectedNumber.toNumber(),
        group2: infectedNumber.toNumber(),
        group3: infectedNumber.toNumber(),
        group4: infectedNumber.toNumber(),
        group5: infectedNumber.toNumber(),
      },
      {
        category: "Currently Infected",
        group1: 0,
        group2: 0,
        group3: 0,
        group4: 0,
        group5: 0,
      },
      {
        category: "Uninfected",
        group1: totalNumber.minus(infectedNumber).toNumber(),
        group2: totalNumber.minus(infectedNumber).toNumber(),
        group3: totalNumber.minus(infectedNumber).toNumber(),
        group4: totalNumber.minus(infectedNumber).toNumber(),
        group5: totalNumber.minus(infectedNumber).toNumber()
      }
    ];
  }

  function createStrategy(defaultRegion=false, defaultVaccine=false) {
    // version 1: JS Object
    let startDate = jsDate;
    let endDate = nowDate.plus({ days: 180 }).toJSDate(); // nowDate.plus({months: 6}).toJSDate();

    return {
      simulationInterval: [startDate, endDate],
      simulationDays: GeneralUtility.diffDateByUnits(startDate, endDate, "days"),
      simulatedOutcome: {
        cases: {},
        deaths: {},
      },
      regionParameters: {
        region: defaultRegion? {
          code: "AFG",
          name: "Afghanistan",
          populationList: [20910291, 14533976, 2452836, 757309, 273929]
        }: "",
        variant: "",
        infectiousnessLevel: 3,
        socialDistancing: {
          homeSCLevel: 0,
          workSCLevel: 0,
          schoolSCLevel: 0,
          otherSCLevel: 0,
        },
        infectionStatus: defaultRegion? generateInfectionStatusList("Afghanistan"): generateInfectionStatusList("")
      },
      vaccineParameters: {
        vaccineList: [
          {
            category: "Vaccine 1",
            name: defaultVaccine? "COMIRNATY (Pfizer/BioNTech)":"",
            code: defaultVaccine? "COMIRNATY":"",
            type: "pre-defined",
            usage: [],
            ...generateAvailabilityDataTtemplate(false),
            efficacyData: generateEfficacyDataTtemplate(defaultVaccine? "COMIRNATY":""),
          },
          {
            category: "Vaccine 2",
            name: "",
            code: "",
            type: "",
            usage: [],
            ...generateAvailabilityDataTtemplate(),
            efficacyData: generateEfficacyDataTtemplate(),
          },
          {
            category: "Vaccine 3",
            name: "",
            code: "",
            type: "",
            usage: [],
            ...generateAvailabilityDataTtemplate(),
            efficacyData: generateEfficacyDataTtemplate(),
          },
        ],
        vaccinationStatusByAgeGroup: {
          group1: [
            {
              category: "Vaccine 1",
              fulldose: 0,
              booster: 0,
            },
            {
              category: "Vaccine 2",
              fulldose: 0,
              booster: 0,
            },
            {
              category: "Vaccine 3",
              fulldose: 0,
              booster: 0,
            },
            {
              category: "Unvaccinated",
              fulldose: 100,
              booster: 100,
            },
          ],
          group2: [
            {
              category: "Vaccine 1",
              fulldose: 0,
              booster: 0,
            },
            {
              category: "Vaccine 2",
              fulldose: 0,
              booster: 0,
            },
            {
              category: "Vaccine 3",
              fulldose: 0,
              booster: 0,
            },
            {
              category: "Unvaccinated",
              fulldose: 100,
              booster: 100,
            },
          ],
          group3: [
            {
              category: "Vaccine 1",
              fulldose: 0,
              booster: 0,
            },
            {
              category: "Vaccine 2",
              fulldose: 0,
              booster: 0,
            },
            {
              category: "Vaccine 3",
              fulldose: 0,
              booster: 0,
            },
            {
              category: "Unvaccinated",
              fulldose: 100,
              booster: 100,
            },
          ],
          group4: [
            {
              category: "Vaccine 1",
              fulldose: 0,
              booster: 0,
            },
            {
              category: "Vaccine 2",
              fulldose: 0,
              booster: 0,
            },
            {
              category: "Vaccine 3",
              fulldose: 0,
              booster: 0,
            },
            {
              category: "Unvaccinated",
              fulldose: 100,
              booster: 100,
            },
          ],
          group5: [
            {
              category: "Vaccine 1",
              fulldose: 0,
              booster: 0,
            },
            {
              category: "Vaccine 2",
              fulldose: 0,
              booster: 0,
            },
            {
              category: "Vaccine 3",
              fulldose: 0,
              booster: 0,
            },
            {
              category: "Unvaccinated",
              fulldose: 100,
              booster: 100,
            },
          ],
        },
      },
      fixedParameters: {
        averageTimeBetweenSymptomOnsetAndHospitalization: 3.8,
        meanDurationInfectiousnessPostSymptoms: 4,
        meanDurationHospitalization: 7,
        meanDurationLatentPeriod: 2,
        meanDurationPreSymptomaticPeriod: 1.5,
        meanDurationNatImmunityAfterInfection: 100,
        meanDurationNatImmunityAfterInfection2: 180,
        meanDurationImmunityWanedVaxHybrid: 100,
        meanDurationPrimaryImmunity: [100, 100, 100],
        meanDurationHybridImmunity: [180, 180, 180],
        meanDurationBoosterImmunity: [180, 180, 180],
        meanDurationBoostedHybridImmunity: [180, 180, 180],
        propSymptomaticInfection: [0.25, 0.4, 0.4, 0.4, 0.4],
        /*
        propSymptomaticInfection:{
          category: "Proportion of symptomatic infections in each age group",
          group1: 0.25,
          group2: 0.4,
          group3: 0.4,
          group4: 0.4,
          group5: 0.4
        },
        */
        relativeInfectiousnessAsymptomaticInfection: 1,
        relativeInfectiousnessHospitalizedInfection: 0,
        relativeInfectiousnessPreSymptomaticInfection: 1,
        relativeSusceptibility: [1,1,1,1,1],
        /*
        relativeSusceptibility:{
          category: "Relative susceptibility",
          group1: 1,
          group2: 1,
          group3: 1,
          group4: 1,
          group5: 1
        },
        */
        VESUSpartiallySus: 0,
        VEDISpartiallySus: 24.7,
        VEHpartiallySus: 74.6,
        VESUSpartiallySusVaccinated: 0,
        VEDISpartiallySusVaccinated: 41,
        VEHpartiallySusVaccinated: 95.3
      },
    };
  }

  return {
    strategyList,
    selectedStrategyIndex,
    setStrategyList,
    usePresetStrategyByIndex,
    usePresetStrategyList,
    clearStrategyList,
    resetStrategyList,
    getValidVaccineDateDaysListByStrategyIndex,
    updateRegionParametersByStrategyIndex,
    updateSimulationParametersByStrategyIndex,
    addDuplicateOfCurrentStrategy,
    selectStrategy,
    duplicateStrategyByIndex,
    removeStrategyByIndex,
    clearSimulatedOutcomeByIndex,
    updateStrategySimulatedOutcomeByIndex
  };
});



/*
durationInfectiousness: 5,
durationLatentPeriod: 2,
durationPresymtomaticPeriod: 1.5,
lengthTimeSymptomOnsetHospitalization: [1, 2, 3, 4, 5],
meanDurationNonicuHospitalization: [1, 2, 3, 4, 5],
meanDurationIcuHospitalization: [1, 2, 3, 4, 5],
proportionSymptomaticInfection: [0.1, 0.2, 0.3, 0.4, 0.5],
proportionSymptomaticInfectionHospitalization: [
  0.1, 0.2, 0.3, 0.4, 0.5,
],
proportionHospitalizationIcu: [0.1, 0.2, 0.3, 0.4, 0.5],
relativeInfectiousnessAsymptomaticInfection: [0.1, 0.2, 0.3, 0.4, 0.5],
relativeInfectiousnessHospitalizedInfection: 0,
relativeInfectiousnessPresymptomaticInfection: 1,
relativeSusceptibility: [1, 1, 1, 1, 1],
waningImmunityInfection: 180,
waningImmunitySymptom: 180,
waningImmunityHospitalization: 1000,
waningTimeFulldose: [100, 120, 150],
waningTimeBooster: [100, 110, 120],
*/