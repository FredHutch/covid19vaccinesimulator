<script setup>
import { ref } from 'vue';
import RadioButton from 'primevue/radiobutton';

const emit = defineEmits(['change']);

const props = defineProps(["options", "initialSelection"]);

const selectedOption = ref(props.initialSelection);

/*
const categories = ref([
            {name: 'Accounting', key: 'A'}, 
            {name: 'Marketing', key: 'M'}, 
            {name: 'Production', key: 'P'}, 
            {name: 'Research', key: 'R'}
]);
*/



function onSelectionChange(event, value){
    console.log(`MyRadioButtonGroup value: ${value}`);
    emit('change', {...event, value: value})
}

</script>

<template>
<!--
<SelectButton v-model="selectedOptions" @change="onSelectionChange" :options="props.options" optionLabel="name" multiple />
-->


<div v-for="option of props.options" :key="option.key" class="field-radiobutton">
    <RadioButton :id="option.key" name="option" :value="option" v-model="selectedOption" @change="onSelectionChange($event, option.key)"/>
    <label :for="option.key">{{option.name}}</label>
</div>

</template>

<style lang="scss" scoped>

</style>
