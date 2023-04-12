<script setup>
import { ref } from "vue";

import Dropdown from "primevue/dropdown";

import { vaccineList } from "../content/variable";

const emit = defineEmits(["change", "input"]);

const props = defineProps(["editable"]);

//console.log(props.foo)

//const sliderValue = ref(props.initial);

const selectedVaccine = ref();

const vaccines = ref(vaccineList);

/*
const vaccines = ref([
  { name: "None", code: "NONE", type: "pre-defined" },
  {
    name: "COMIRNATY (Pfizer/BioNTech)",
    code: "COMIRNATY",
    type: "pre-defined",
  },
  { name: "VAXZEVRIA (AstraZeneca)", code: "VAXZEVRIA", type: "pre-defined" },
  { name: "COVISHIELD", code: "COVISHIELD", type: "pre-defined" },
  { name: "JANSEN (Johnson & Johnson)", code: "JANSEN", type: "pre-defined" },
  { name: "SPIKEVAX (Moderna)", code: "SPIKEVAX", type: "pre-defined" },
  { name: "VERO CELL", code: "VERO CELL", type: "pre-defined" },
  { name: "CORONAVAC (Sinovac)", code: "CORONAVAC", type: "pre-defined" },
  { name: "COVOVAX", code: "COVOVAX", type: "pre-defined" },
  { name: "NUVAXOVID (Novavax)", code: "NUVAXOVID", type: "pre-defined" },
  { name: "CONVIDECIA (CanSino)", code: "CONVIDECIA", type: "pre-defined" },
  // "customized"
  {
    name: "(Enter vaccine name here)",
    code: "(customized)",
    type: "customized",
  },
]);
*/

function onSelectionChange(event) {
  emit("change", event.value);
}

function onInputChange(event) {
  console.log(`onInputChange: ${event.target.value}`);
  emit("input", event.target.value);
}
</script>

<template>
  <!--
     optionValue="code"
-->
  <Dropdown
    v-model="selectedVaccine"
    @change="onSelectionChange"
    @input="onInputChange"
    :options="vaccines"
    optionLabel="name"
    placeholder="Select a vaccine"
    :editable="props.editable"
  />
</template>

<style lang="scss" scoped>
.p-dropdown {
  width: 14rem;
}

.region-item {
  img {
    width: 17px;
    margin-right: 0.5rem;
  }
}
</style>
