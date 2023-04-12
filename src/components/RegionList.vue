<script setup>
import { ref } from 'vue';
import Dropdown from 'primevue/dropdown';
import { regionList } from '../content/variable';

const emit = defineEmits(['change']);

const selectedRegion = ref();

const regions = ref(regionList);

// TW data
/*
0 -  20: 3921489
20 - 49: 10057596
50 - 64: 5237628
65 - 74: 2521788
  >= 75: 1457677

3921489 + 10057596 + 5237628 + 2521788 + 1457677 = 23196178
*/

function onSelectionChange(event){
    emit('change', event.value)
}
</script>

<template>
    <Dropdown v-model="selectedRegion" @change="onSelectionChange" :options="regions" optionLabel=name :filter="true"
        placeholder="Select a Region" :showClear="false">
        <template #value="slotProps">
            <div class="region-item" v-if="slotProps.value">
                <!--
                <img src="https://www.primefaces.org/wp-content/uploads/2020/05/placeholder.png" />
                -->
                <div>{{ slotProps.value.name }}</div>
            </div>
            <span v-else>
                {{ slotProps.placeholder }}
            </span>
        </template>
        <template #option="slotProps">
            <div class="region-item">
                <!--
                <img src="https://www.primefaces.org/wp-content/uploads/2020/05/placeholder.png" />
                -->
                <div>{{ slotProps.option.name }}</div>
            </div>
        </template>
    </Dropdown>


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
