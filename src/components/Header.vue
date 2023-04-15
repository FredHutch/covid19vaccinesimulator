<script setup>
import { storeToRefs } from "pinia";
import { systemName } from "../content/variable";
import { useStrategiesStore } from '../stores/strategies';
import Toolbar from 'primevue/toolbar';
import Button from 'primevue/button';
const strategiesStore = useStrategiesStore();
const { strategyList, selectedStrategyIndex, addDuplicateOfCurrentStrategy, selectStrategy, duplicateStrategyByIndex } = storeToRefs(strategiesStore);

// :displayStrategyIndex="true"
const props = defineProps({
    displayStrategyIndex: {
        type: Boolean,
        default: true
    }
});


</script>
<template>
<div class="card z-5 bg-bluegray-50">
        <div class="mt-2">
    
    <router-link to="/">{{systemName}}</router-link>
    <span v-if="displayStrategyIndex">: Strategy {{selectedStrategyIndex + 1}}</span>
</div>
</div>

</template>
