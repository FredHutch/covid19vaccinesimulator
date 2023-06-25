<script setup>
import Fieldset from "primevue/fieldset";
import Button from "primevue/button";
import Divider from "primevue/divider";
import Footer from "../components/Footer.vue";

import { useRouter, useRoute } from "vue-router";
import Checkbox from "primevue/checkbox";
import SelectButton from "primevue/selectbutton";

import { systemName } from "../content/variable";
import { ref } from "vue";

import { storeToRefs } from "pinia";
import { useStrategiesStore } from "../stores/strategies";
import { useToast } from "primevue/usetoast";




const strategiesStore = useStrategiesStore();
const {
  usePresetStrategyList,
  usePresetStrategyByIndex,
  clearStrategyList,
  resetStrategyList,
} = storeToRefs(strategiesStore);

const toast = useToast();

let checked = ref(false);

const router = useRouter();
const onStartClick = (event) => {
  router.push("/region");
};

import { useHead } from "@unhead/vue";
useHead({
  title: `${systemName}: a COVID-19 Vaccine Allocation Comparison Tool`,
  /*
  meta: [
    { name: 'description', content: 'Learn more about us.' },
  ],
  */
})


// @click="onPresetSelectionClick"
/*
const onPresetSelectionClick = (event) => {
  console.log(`onPresetSelectionClick: ${event}`);
  //checked = !checked;

};
*/

const options = ref([
  { label: "None", value: 0 },
  { label: "Afghanistan (Boosters first)", value: 1 },
  { label: "Afghanistan (Primary series first)", value: 2 },
  { label: "Haiti (Boosters first)", value: 3 },
  { label: "Haiti (Primary series first)", value: 4 },
]);

const selectedPreset = ref(options.value[0]);
strategiesStore.resetStrategyList();

const onPresetSelectionButtonChange = (event) => {
  console.log(
    `onPresetSelectionButtonChange: selection ${JSON.stringify(event.value)}`
  );

  /*
  console.log(
    `onPresetSelectionButtonChange: selection ${JSON.stringify(
      event.value
    )}, selectedPreset: ${JSON.stringify(selectedPreset)}`
  );
  */

  /*
  onPresetSelectionButtonChange: selection {"label":"Afghanistan","value":1}, selectedPreset: {"__v_isShallow":false,"dep":{"w":0,"n":0},"__v_isRef":true,"_rawValue":{"label":"Afghanistan","value":1},"_value":{"label":"Afghanistan","value":1}}
  */

  let newValue = event.value;

  let presetIndex = newValue.value;

  if (presetIndex == 0) {
    //clear it and use the default
    strategiesStore.resetStrategyList();
    toast.add({
      severity: "success",
      summary: "Success",
      detail: "Strategies successfully reseted!",
      life: 3000,
    });
  } else {
    strategiesStore.usePresetStrategyByIndex(presetIndex - 1);
    toast.add({
      severity: "success",
      summary: "Success",
      detail: "Preset strategies successfully applied!",
      life: 3000,
    });
  }

  /*
  if( newValue ){
    strategiesStore.clearStrategyList();
    strategiesStore.usePresetStrategyList();
    toast.add({severity:'success', summary: 'Success', detail:'Preset strategies successfully applied!', life: 3000});

  }
  else{
    // clear it
    strategiesStore.resetStrategyList();
    toast.add({severity:'success', summary: 'Success', detail:'Strategies successfully reseted!', life: 3000});
  }
  */
};

strategiesStore.$subscribe((mutation, state) => {
  console.log(`strategiesStore.$subscribe: state change`);

  if (
    mutation.events != undefined &&
    (mutation.events.key == "rate" || mutation.events.key == "number")
  ) {
    updateSimulationParameters();
  }
});

const updateSimulationParameters = () => {
  console.log(`updateSimulationParameters`);
  strategiesStore.updateSimulationParametersByStrategyIndex(0);
};

const onPresetSelectionInputChange = (newValue) => {
  console.log(`onPresetSelectionInputChange: checked ${newValue}`);

  if (newValue) {
    strategiesStore.clearStrategyList();
    strategiesStore.usePresetStrategyList();
    toast.add({
      severity: "success",
      summary: "Success",
      detail: "Preset strategies successfully applied!",
      life: 3000,
    });
  } else {
    // clear it
    strategiesStore.resetStrategyList();
    toast.add({
      severity: "success",
      summary: "Success",
      detail: "Strategies successfully reseted!",
      life: 3000,
    });
  }
};
</script>

<template>
  <div class="grid">
    <div class="col-2"></div>
    <div class="col">
      <h1 class="text-7xl text-center">
        {{ systemName }}: a COVID-19 Vaccine Allocation Comparison Tool
      </h1>
      <div>
        <Fieldset legend="Purpose">
          <div>
            The purpose of this tool is to compare different vaccination
            strategies when different vaccine products are available. The user
            can provide up to three vaccine products with product-specific
            quantities, effectiveness, vaccination rates and availability
            together with an allocation strategy. The vaccine allocation tool
            will then simulate the SARS-CoV-2 transmission dynamics in a chosen
            population stratified in 5 age groups, and report the number of
            cases, hospitalizations, and deaths over the period of choice.
          </div>
        </Fieldset>
        <Fieldset legend="Data/Parameters">
          <div>
            In the following pages, you will be able to input region-specific
            data and parameters, including the percentage of the population
            previously infected, those who are currently infected and current
            social distancing interventions. In addition, you will be able to
            incorporate vaccination data from up to three different vaccines,
            including percentage of the population previously vaccinated and/or
            boosted. You will then be requested to input data for the
            vaccination strategies that you want to model, and compare the
            results.
          </div>
        </Fieldset>
        <div class="flex justify-content-center mt-4 mb-4">
          <Button
            label="Start"
            class="p-button-lg fh-button-primary"
            @click="onStartClick"
          ></Button>
        </div>
        <div class="flex justify-content-center mt-4 mb-4 align-content-center">
          <div class="card flex justify-content-center">
            <label>Load example: </label>&ensp;&ensp;
            <SelectButton
              v-model="selectedPreset"
              :options="options"
              optionLabel="label"
              dataKey="value"
              aria-labelledby="custom"
              @change="onPresetSelectionButtonChange"
            >
              <template #option="slotProps">
                {{ slotProps.option.label }}
              </template>
            </SelectButton>
          </div>

          <br />
          <br />
          <div class="hidden">
            <div class="hidden flex align-items-center">
              <Checkbox
                inputId="binary"
                v-model="checked"
                :binary="true"
                @input="onPresetSelectionInputChange"
              />&ensp;
              <label for="binary">Load example: Chad</label>
            </div>
          </div>
        </div>
        <Divider class="fh-divider-primary"></Divider>
        <Footer></Footer>
      </div>
    </div>
    <div class="col-2"></div>
  </div>
</template>

<style scoped lang="scss">
::v-deep(.p-fieldset) {
  .p-fieldset-legend-text {
    font-size: 1.5em;
  }
}
</style>
