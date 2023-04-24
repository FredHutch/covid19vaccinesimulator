<script setup>
import { ref } from "vue";
import PanelMenu from 'primevue/panelmenu';
import Button from "primevue/button";
import MyToolBar from "../components/MyToolBar.vue";

const expandedKeys = ref({});
const items = ref([
  {
    key: "0",
    label: "Location",
    to: "/region",
    //icon: "pi pi-fw pi-file",
    items: [
      {
        key: "0_0",
        label: "Region",
        to: "/region"
        //icon: "pi pi-fw pi-plus",
        /*
        items: [
          {
            key: "0_0_0",
            label: "Bookmark",
            icon: "pi pi-fw pi-bookmark",
          },
          {
            key: "0_0_1",
            label: "Video",
            icon: "pi pi-fw pi-video",
          },
        ],
        */
      },
      {
        key: "0_1",
        label: "Social distancing",
        to: '/social-distancing'
        //icon: "pi pi-fw pi-trash",
      }
    ],
  },
  {
    key: "1",
    label: "Infection",
    to: '/infection-status',
    //icon: "pi pi-fw pi-pencil",
    items: [
      {
        key: "1_0",
        label: "Infection prevalence",
        to: '/infection-status',
        //icon: "pi pi-fw pi-align-left",
      }
    ],
  },
  {
    key: "2",
    label: "Vaccine",
    to: '/vaccine-selection',
    //icon: "pi pi-fw pi-pencil",
    items: [
      {
        key: "2_0",
        label: "Options",
        to: '/vaccine-selection',
        //icon: "pi pi-fw pi-align-left",
      },
      /*
      {
        key: "2_1",
        label: "Vaccination overview",
        to: '/vaccine-check'
        //icon: "pi pi-fw pi-align-right",
      },
      */
      {
        key: "2_2",
        label: "Vaccination by age",
        to: '/vaccination-by-age',
        //icon: "pi pi-fw pi-align-center",
      },
      /*
      {
        key: "2_3",
        label: "Effectiveness Data Screening",
        to: '/vaccination-efficacy-precheck',
        //icon: "pi pi-fw pi-align-justify",
      },
      */
      {
        key: "2_3",
        label: "Vaccine effectiveness",
        to: '/vaccine-efficacy?vaccine=1',
        //icon: "pi pi-fw pi-align-justify",
      }

    ],
  },
  {
    key: "3",
    label: "Vaccine Planning",
    to: '/vaccine-availability',
    //icon: "pi pi-fw pi-user",
    items: [
      {
        key: "3_0",
        label: "Availability",
        to: '/vaccine-availability',
        //icon: "pi pi-fw pi-user-plus",
      },
      {
        key: "3_1",
        label: "Allocation Strategy",
        to: '/vaccine-strategy',
        //icon: "pi pi-fw pi-users",
      },
      {
        key: "3_2",
        label: "Period for simulation",
        to: '/vaccine-plan-period',
        //icon: "pi pi-fw pi-user-minus",
      },
      {
        key: "3_3",
        label: "Additional parameters",
        to: '/additional-parameters',
        //icon: "pi pi-fw pi-user-minus",
      },
    ],
  },
  {
    key: "4",
    label: "Outcome",
    to: '/result',
    //icon: "pi pi-fw pi-calendar",
    items: [
      {
        key: "4_0",
        label: "Result",
        to: '/result',
        //icon: "pi pi-fw pi-pencil",
        /*
        items: [
          {
            key: "3_0_0",
            label: "Save",
            icon: "pi pi-fw pi-calendar-plus",
          },
          {
            key: "3_0_0",
            label: "Delete",
            icon: "pi pi-fw pi-calendar-minus",
          },
        ],
        */
      },
      /*
      {
        key: "3_1",
        label: "Archieve",
        icon: "pi pi-fw pi-calendar-times",
        items: [
          {
            key: "3_1_0",
            label: "Remove",
            icon: "pi pi-fw pi-calendar-minus",
          },
        ],
      },
      */
    ],
  },
]);

const expandAll = () => {
  for (let node of items.value) { // was nodes
    //console.log(`expandAll: node ${JSON.stringify(node)}`);
    expandNode(node);
  }

  expandedKeys.value = { ...expandedKeys.value };
};
const collapseAll = () => {
  expandedKeys.value = {};
};
const expandNode = (node) => {
  if (node.items && node.items.length) {
  //if (node.children && node.children.length) {
    expandedKeys.value[node.key] = true;

    for (let child of node.items) {
    //for (let child of node.children) {
      expandNode(child);
    }
  }
};

expandAll();

//return { items, expandedKeys, expandAll, collapseAll, expandNode }
</script>

<template>
  <div>
    <!--
    <h5>Default</h5>
    -->
    <div class="mb-3" style="display: none;">
            <Button type="button" icon="pi pi-plus" label="Expand All" @click="expandAll" class="mr-2" />
            <Button type="button" icon="pi pi-minus" label="Collapse All" @click="collapseAll" />
            </div>
    <MyToolBar></MyToolBar>
    <PanelMenu :model="items" :expandedKeys="expandedKeys" >
      
      <template #item="{item}">
        <!--
        <a :href="item.to" class="p-menuitem-link">
          <span class="p-menuitem-text">{{item.label}}</span>
        </a>
        -->
        <router-link :to="item.to" class="p-menuitem-link"><span class="p-menuitem-text">{{item.label}}</span></router-link>
        <!--
        <router-link :to="item.to" custom v-slot="{href, route, navigate, isActive, isExactActive}">
            <a :href="href" @click="navigate" class="p-menuitem-link" :class="{'active-link': isActive, 'active-link-exact': isExactActive}">
              <span class="p-menuitem-text">{{item.label}}</span>
            </a>
        </router-link>
        -->
      </template>
      
    </PanelMenu>
    
  </div>
</template>

<style scoped lang="scss">
.p-panelmenu {
  width: 100%; //22rem;
}

::v-deep(.p-panelmenu-header) {
    .p-menuitem-text {
      font-size: 1.5em; //22rem;
    }
}


</style>
