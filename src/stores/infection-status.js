import { defineStore } from 'pinia'
import { ref } from 'vue';

export const useInfectionStatusStore = defineStore('infection-status', () => {
  /*
  const homeSCLevel = ref(1);
  const workSCLevel = ref(1);
  const schoolSCLevel = ref(1);
  const otherSCLevel = ref(1);
  */

  const infectionStatusByAgeGroup = ref([
    {
      category: "Previously Infected",
      group1: 33,
      group2: 33,
      group3: 33,
      group4: 33,
      group5: 33,
    },
    {
      category: "Currently Infected",
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



  return { infectionStatusByAgeGroup};
})