<script setup>
import { ref } from 'vue';
import Dropdown from 'primevue/dropdown';

/*
import { useVaccineSelectionStore } from '@/stores/vaccine-selection';
const vaccineStore = useVaccineSelectionStore();
const {vaccineAvailability} = storeToRefs(vaccineStore);
*/



const emit = defineEmits(['change']);

const selectedStrategy = ref();


// long one
const tools = ref([
    {
        name: "Reset Primary Series", 
        code: "rps",
        distribute: (vaccineAvailability, indexList=[0,1,2]) => {
            console.log(`Reset Primary Series for vaccine: ${indexList}: vaccineAvailability: ${vaccineAvailability}`);
            let newAvailability = [...vaccineAvailability];

            newAvailability = newAvailability.map((oneAvailability, index) => {
                let fulldoseAllocation = {...oneAvailability.allocation[0]};
                let boosterAllocation = {...oneAvailability.allocation[1]};

                if (indexList.includes(index)){
                    let totalAllowance = fulldoseAllocation.proportion;
                    let currentAllowance = totalAllowance;

                    for(let i = 1; i <= 5; i++ ){
                        let groupName = `group${i}`;
                        fulldoseAllocation[groupName] = 0;
                        console.log(`Reset Primary Series for vaccine: ${indexList} - group[${groupName}]`);
                    }
                }
                return {...oneAvailability, allocation: [fulldoseAllocation, boosterAllocation]};
            });


            return newAvailability;
        }
    },
    {
        name: "Reset Booster", 
        code: "rps",
        distribute: (vaccineAvailability, indexList=[0,1,2]) => {
            console.log(`Reset Booster for vaccine: ${indexList}: vaccineAvailability: ${vaccineAvailability}`);
            let newAvailability = [...vaccineAvailability];

            newAvailability = newAvailability.map((oneAvailability, index) => {
                let fulldoseAllocation = {...oneAvailability.allocation[0]};
                let boosterAllocation = {...oneAvailability.allocation[1]};

                if (indexList.includes(index)){
                    for(let i = 1; i <= 5; i++ ){
                        let groupName = `group${i}`;
                        //boosterAllocation[groupName] = 0;

                        boosterAllocation["primaryMatching"].forEach((matching) => {
                            matching[groupName] = 0;
                        });
                        console.log(`Reset Booster for vaccine: ${indexList} - group[${groupName}]`);
                    }
                }
                return {...oneAvailability, allocation: [fulldoseAllocation, boosterAllocation]};
            });


            return newAvailability;
        }
    },
    // This one depends on having the primary-booster matching ready
    /*
    {
        name: "Equally distributed allocated proportion for primary series", 
        code: "edps",
        distribute: (vaccineAvailability, indexList=[0,1,2]) => {
            let newAvailability = [...vaccineAvailability.value];

            newAvailability = newAvailability.map((oneAvailability, index) => {
                let fulldoseAllocation = {...oneAvailability.allocation[0]};
                let boosterAllocation = {...oneAvailability.allocation[1]};

                if (indexList.includes(index)){
                    let totalAllowance = fulldoseAllocation.proportion;
                    let currentAllowance = totalAllowance;

                    for(let i = 1; i <= 5; i++ ){
                        let groupName = `group${i}`;
                        if( i <= 4){
                            fulldoseAllocation[groupName] = Math.floor(totalAllowance/5);
                            currentAllowance = currentAllowance - fulldoseAllocation[groupName];
                        }
                        else{
                            fulldoseAllocation[groupName] = currentAllowance;
                        }
                    }
                }
                return {...oneAvailability, allocation: [fulldoseAllocation, boosterAllocation]};
            });


            return newAvailability;
        }
    },
    {
        name: "Equally distributed allocated proportion for booster", 
        code: "edps",
        distribute: (vaccineAvailability, indexList=[0,1,2]) => {
            let newAvailability = [...vaccineAvailability.value];

            newAvailability = newAvailability.map((oneAvailability, index) => {
                let fulldoseAllocation = {...oneAvailability.allocation[0]};
                let boosterAllocation = {...oneAvailability.allocation[1]};

                if (indexList.includes(index)){
                    let totalAllowance = boosterAllocation.proportion;
                    let currentAllowance = totalAllowance;

                    for(let i = 1; i <= 5; i++ ){
                        let groupName = `group${i}`;
                        if( i < 3){
                            boosterAllocation[groupName] = Math.floor(totalAllowance/3);
                            currentAllowance = currentAllowance - boosterAllocation[groupName];
                        }
                        else if (i == 3){
                            boosterAllocation[groupName] = currentAllowance;
                        }
                        else{
                            boosterAllocation[groupName] = 0;
                        }
                    }
                }
                return {...oneAvailability, allocation: [fulldoseAllocation, boosterAllocation]};
            });


            return newAvailability;
        }
    },
    {
        name: "Equally distributed between primary series and booster", 
        code: "eg",
        distribute: (vaccineAvailability, indexList=[0,1,2]) => {
            let newAvailability = [...vaccineAvailability.value];

            newAvailability = newAvailability.map((oneAvailability, index) => {
                let fulldoseAllocation = {...oneAvailability.allocation[0]};
                let boosterAllocation = {...oneAvailability.allocation[1]};

                

                if (indexList.includes(index)){
                    fulldoseAllocation.proportion = 50;
                    boosterAllocation.proportion = 50;

                    let totalAllowance = 100;
                    for(let i = 1; i <= 5; i++ ){
                        let groupName = `group${i}`;
                        fulldoseAllocation[groupName] = Math.floor(fulldoseAllocation.proportion/5);
                        if( i < 3 ){
                            boosterAllocation[groupName] = Math.floor(boosterAllocation.proportion/3);
                        }
                        else if (i == 3){
                            boosterAllocation[groupName] = boosterAllocation.proportion - 2 * Math.floor(boosterAllocation.proportion/3);
                        }
                        else{
                            boosterAllocation[groupName] =  0;
                        }

                    }
                }
                
                return {...oneAvailability, allocation: [fulldoseAllocation, boosterAllocation]};
            });


            return newAvailability;
        }
    },
    {
        name: "Elderly only and split between primary series and booster", 
        code: "eo",
        distribute: (vaccineAvailability, indexList=[0,1,2]) => {
            let newAvailability = [...vaccineAvailability.value];

            newAvailability = newAvailability.map((oneAvailability, index) => {
                let fulldoseAllocation = {...oneAvailability.allocation[0]};
                let boosterAllocation = {...oneAvailability.allocation[1]};

                if (indexList.includes(index)){
                    fulldoseAllocation.proportion = 50;
                    boosterAllocation.proportion = 50;

                    let totalAllowance = 100;

                    for(let i = 1; i <= 5; i++ ){
                        let groupName = `group${i}`;
                        if( i == 5){
                            // this is correct
                            fulldoseAllocation[groupName] = fulldoseAllocation.proportion;

                            // this needs to be equally spread
                            boosterAllocation[groupName] = 0;

                        }
                        else if(i == 4){
                            fulldoseAllocation[groupName] = 0;
                            boosterAllocation[groupName] = 0;
                        }
                        else if( i == 3){
                            fulldoseAllocation[groupName] = 0;
                            boosterAllocation[groupName] = boosterAllocation.proportion - 2 * Math.floor(boosterAllocation.proportion/3);

                        }
                        else{
                            fulldoseAllocation[groupName] = 0;
                            boosterAllocation[groupName] = Math.floor(boosterAllocation.proportion/3);
                        }
                    }

                }

                return {...oneAvailability, allocation: [fulldoseAllocation, boosterAllocation]};
            });


            return newAvailability;
        }
    }
    */
]);



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
    <Dropdown v-model="selectedStrategy" @change="onSelectionChange" :options="tools" optionLabel=name :filter="true"
        placeholder="Toolbox" :showClear="false">
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
