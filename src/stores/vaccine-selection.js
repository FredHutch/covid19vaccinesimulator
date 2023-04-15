import { defineStore } from 'pinia'
import { ref } from 'vue';
import { DateTime, Interval } from 'luxon';

export const useVaccineSelectionStore = defineStore('vaccine-selection', () => {
  const vaccine1 = ref({});
  const vaccine2 = ref({});
  const vaccine3 = ref({});

  const vaccine1Usage = ref([]);
  const vaccine2Usage = ref([]);
  const vaccine3Usage = ref([]);


  const vaccine1HasEfficacyData = ref("no");
  const vaccine2HasEfficacyData = ref("no");
  const vaccine3HasEfficacyData = ref("no");


  const vaccine1EfficacyData = ref([
    {
      category: "Infection",
      fulldose: 30,
      booster: 30
    },
    {
      category: "Symptomatic infection",
      fulldose: 30,
      booster: 30
    },
    {
      category: "Hospitalization",
      fulldose: 30,
      booster: 30
    },
    {
      category: "Infection after 6 months (wanned)",
      fulldose: 30,
      booster: 30
    },
    {
      category: "Symptomatic infection after 6 months (wanned)",
      fulldose: 30,
      booster: 30
    },
    {
      category: "Hospitalization after 6 months (wanned)",
      fulldose: 30,
      booster: 30
    },
  ]);
  const vaccine2EfficacyData = ref([
    {
      category: "Infection",
      fulldose: 30,
      booster: 30
    },
    {
      category: "Symptomatic infection",
      fulldose: 30,
      booster: 30
    },
    {
      category: "Hospitalization",
      fulldose: 30,
      booster: 30
    },
    {
      category: "Infection after 6 months (wanned)",
      fulldose: 30,
      booster: 30
    },
    {
      category: "Symptomatic infection after 6 months (wanned)",
      fulldose: 30,
      booster: 30
    },
    {
      category: "Hospitalization after 6 months (wanned)",
      fulldose: 30,
      booster: 30
    },
  ]);
  const vaccine3EfficacyData = ref([
    {
      category: "Infection",
      fulldose: 30,
      booster: 30
    },
    {
      category: "Symptomatic infection",
      fulldose: 30,
      booster: 30
    },
    {
      category: "Hospitalization",
      fulldose: 30,
      booster: 30
    },
    {
      category: "Infection after 6 months (wanned)",
      fulldose: 30,
      booster: 30
    },
    {
      category: "Symptomatic infection after 6 months (wanned)",
      fulldose: 30,
      booster: 30
    },
    {
      category: "Hospitalization after 6 months (wanned)",
      fulldose: 30,
      booster: 30
    },
  ]);

  let nowDate =DateTime.utc().startOf('day');
  let jsDate = nowDate.toJSDate();
  let nowDateString = nowDate.toISODate();

  let simulationInterval = ref([jsDate, nowDate.plus({months: 6}).toJSDate()]);

  const vaccineAvailability = ref([
    {
      category: "Vaccine 1",
      number: 0,
      date: jsDate, //nowDateString
      allocation: [
        {
          category: "Full dose",
          proportion: 100,
          group1: 0,
          group2: 0,
          group3: 0,
          group4: 0,
          group5: 0,
        },
        {
          category: "Booster",
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
            }
          ]
        },
      ]
    },
    {
      category: "Vaccine 2",
      number: 0,
      date: jsDate, //nowDateString
      allocation: [
        {
          category: "Full dose",
          proportion: 100,
          group1: 0,
          group2: 0,
          group3: 0,
          group4: 0,
          group5: 0,
        },
        {
          category: "Booster",
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
            }
          ]
        },
      ]

    },
    {
      category: "Vaccine 3",
      number: 0,
      date: jsDate, //nowDateString
      allocation: [
        {
          category: "Full dose",
          proportion: 100,
          group1: 0,
          group2: 0,
          group3: 0,
          group4: 0,
          group5: 0,
        },
        {
          category: "Booster",
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
            }
          ]
        },
      ]
    }
  ]);

  return { vaccine1, vaccine2, vaccine3, vaccine1Usage, vaccine2Usage, vaccine3Usage, vaccine1HasEfficacyData, vaccine2HasEfficacyData, vaccine3HasEfficacyData, vaccine1EfficacyData, vaccine2EfficacyData, vaccine3EfficacyData, vaccineAvailability, simulationInterval};
})