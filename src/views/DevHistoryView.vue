<script setup>
import Fieldset from "primevue/fieldset";
import Button from "primevue/button";
import Divider from "primevue/divider";
import Footer from "../components/Footer.vue";
import Header from "../components/Header.vue";
import Image from "primevue/image";
import { devHistoryInfoList } from "../content/dev-history-info";
import Timeline from 'primevue/timeline';

import { systemName } from "../content/variable";
import { useHead } from "@unhead/vue";
useHead({
  title: `Development History | ${systemName}`,
  /*
  meta: [
    { name: 'description', content: 'Learn more about us.' },
  ],
  */
})

</script>

<template>
  <div class="grid">
    <div class="col-2"></div>
    <div class="col">
      <Header :displayStrategyIndex="false"></Header>
      <h1 class="text-6xl text-center">Development History</h1>
      <Divider class="fh-divider-primary"></Divider>
    <Timeline :value="devHistoryInfoList">
        <template #opposite="slotProps">
                    {{slotProps.item.date}}
                </template>
        <template #content="slotProps">
            {{slotProps.item.status}}
        </template>
    </Timeline>
    <Divider class="fh-divider-primary"></Divider>
        <Footer></Footer>
    </div>
    <div class="col-2"></div>
  </div>
</template>
