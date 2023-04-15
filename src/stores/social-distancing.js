import { defineStore } from 'pinia'
import { ref } from 'vue';

export const useSocialDistancingStore = defineStore('social-distancing', () => {
  const homeSCLevel = ref(1);
  const workSCLevel = ref(1);
  const schoolSCLevel = ref(1);
  const otherSCLevel = ref(1);

  return { homeSCLevel, workSCLevel, schoolSCLevel, otherSCLevel};
})