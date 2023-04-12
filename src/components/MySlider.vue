<script setup>
import { ref } from 'vue';
import Slider from "primevue/slider";

const emit = defineEmits(['change']);


const props = defineProps(['min', 'max', 'step', 'initial', "minLabl", "maxLabel"])

//console.log(props.foo)

const sliderValue = ref(props.initial);

function onSelectionChange(value) {
    emit('change', value)
}
</script>

<template>
    <div class="flex align-items-center">
        <div class="text-xl text-center" style="width: 120px;">{{minLabl != undefined && minLabl != ""? minLabl: props.min}}</div>
        <Slider v-model="sliderValue" @change="onSelectionChange" :min="props.min" :max="props.max" :step="props.step" class="mt-2" style="width: 300px;"></Slider>
        <div class="text-xl text-center" style="width: 120px;">{{maxLabel != undefined && maxLabel != ""? maxLabel: props.max}}</div>
    </div>

</template>

<style lang="scss" scoped>
</style>
