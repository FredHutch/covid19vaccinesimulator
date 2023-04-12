import { defineStore } from 'pinia'
import { ref } from 'vue';

export const useAgeGroupStore = defineStore('age-group', () => {

    const groupIndexLabelMap = ref({
        1: "under 20",
        2: "between 20 to 49",
        3: "between 50 to 64",
        4: "between 65 to 74",
        5: "over (including) 75",
    });

  return { groupIndexLabelMap};
})