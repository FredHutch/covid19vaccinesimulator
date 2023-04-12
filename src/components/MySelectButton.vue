<script setup>
import { ref } from 'vue';

import Dropdown from 'primevue/dropdown';
import SelectButton from 'primevue/selectbutton';

const emit = defineEmits(['change']);

const props = defineProps(["options"]);

//console.log(props.foo)

//const sliderValue = ref(props.initial);

const selectedOptions = ref();

const paymentOptions = ref([
    {name: 'Option 1', value: 1},
    {name: 'Option 2', value: 2},
    {name: 'Option 3', value: 3}
]);
function onSelectionChange(event){
    emit('change', event.value)
}

</script>

<template>
<!--
     optionValue="code"
-->
<SelectButton v-model="selectedOptions" @change="onSelectionChange" :options="props.options" optionLabel="name" multiple />

</template>

<style lang="scss" scoped>

</style>
