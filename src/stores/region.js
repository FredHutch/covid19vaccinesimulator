import { defineStore } from 'pinia'
import { ref } from 'vue';

export const useRegionStore = defineStore('region', () => {
  const region = ref("");
  const variant = ref("");
  const infectiousnessLevel = ref(1);

  return { region, variant, infectiousnessLevel };
})