import { defineStore } from 'pinia'
import { ref } from 'vue';

export const useVaccinationStatusStore = defineStore('vaccination-status', () => {


  const vaccinationStatusByAgeGroup = ref({
    "group1": [
      {
        category: "Vaccine 1",
        fulldose: 0,
        booster: 0
      },
      {
        category: "Vaccine 2",
        fulldose: 0,
        booster: 0
      },
      {
        category: "Vaccine 3",
        fulldose: 0,
        booster: 0
      },
      {
        category: "Unvaccinated",
        fulldose: 100,
        booster: 100
      },
    ],
    "group2": [
      {
        category: "Vaccine 1",
        fulldose: 0,
        booster: 0
      },
      {
        category: "Vaccine 2",
        fulldose: 0,
        booster: 0
      },
      {
        category: "Vaccine 3",
        fulldose: 0,
        booster: 0
      },
      {
        category: "Unvaccinated",
        fulldose: 100,
        booster: 100
      },
    ],
    "group3": [
      {
        category: "Vaccine 1",
        fulldose: 0,
        booster: 0
      },
      {
        category: "Vaccine 2",
        fulldose: 0,
        booster: 0
      },
      {
        category: "Vaccine 3",
        fulldose: 0,
        booster: 0
      },
      {
        category: "Unvaccinated",
        fulldose: 100,
        booster: 100
      },
    ],
    "group4": [
      {
        category: "Vaccine 1",
        fulldose: 0,
        booster: 0
      },
      {
        category: "Vaccine 2",
        fulldose: 0,
        booster: 0
      },
      {
        category: "Vaccine 3",
        fulldose: 0,
        booster: 0
      },
      {
        category: "Unvaccinated",
        fulldose: 100,
        booster: 100
      },
  ],
  "group5": [
    {
      category: "Vaccine 1",
      fulldose: 0,
      booster: 0
    },
    {
      category: "Vaccine 2",
      fulldose: 0,
      booster: 0
    },
    {
      category: "Vaccine 3",
      fulldose: 0,
      booster: 0
    },
    {
      category: "Unvaccinated",
      fulldose: 100,
      booster: 100
    },
]
  });



  return {vaccinationStatusByAgeGroup /*, vaccinationStatusByAgeGroupFullDose, vaccinationStatusByAgeGroupBooster */};
})

  /*
  const homeSCLevel = ref(1);
  const workSCLevel = ref(1);
  const schoolSCLevel = ref(1);
  const otherSCLevel = ref(1);
  */

  /*
  const vaccinationStatusByAgeGroupFullDose = ref([
    {
      category: "Vaccine 1",
      group1: 25,
      group2: 25,
      group3: 25,
      group4: 25,
      group5: 25,
    },
    {
      category: "Vaccine 2",
      group1: 25,
      group2: 25,
      group3: 25,
      group4: 25,
      group5: 25,
    },
    {
      category: "Vaccine 3",
      group1: 25,
      group2: 25,
      group3: 25,
      group4: 25,
      group5: 25,
    },
    {
      category: "Unvaccinated",
      group1: 25,
      group2: 25,
      group3: 25,
      group4: 25,
      group5: 25,
    }
  ]);


  const vaccinationStatusByAgeGroupBooster = ref([
    {
      category: "Vaccine 1",
      group1: 25,
      group2: 25,
      group3: 25,
      group4: 25,
      group5: 25,
    },
    {
      category: "Vaccine 2",
      group1: 25,
      group2: 25,
      group3: 25,
      group4: 25,
      group5: 25,
    },
    {
      category: "Vaccine 3",
      group1: 25,
      group2: 25,
      group3: 25,
      group4: 25,
      group5: 25,
    },
    {
      category: "Unvaccinated",
      group1: 25,
      group2: 25,
      group3: 25,
      group4: 25,
      group5: 25,
    }
  ]);
  */

