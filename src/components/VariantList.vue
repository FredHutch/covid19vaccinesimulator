<script setup>
import { ref } from 'vue';

import Dropdown from 'primevue/dropdown';

const emit = defineEmits(['change']);

const selectedVariant = ref();

const variants = ref([
    { name: 'Delta', code: 'delta' },
    { name: 'Omicron', code: 'omicron' },
]);

function onSelectionChange(event){
    emit('change', event.value)
}
</script>

<template>
<!--
     optionValue="code"
-->
<Dropdown v-model="selectedVariant" @change="onSelectionChange" :options="variants" optionLabel="name" placeholder="Select a Variant" />

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
