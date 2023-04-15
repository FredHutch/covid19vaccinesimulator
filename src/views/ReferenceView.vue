<script setup>
import Fieldset from "primevue/fieldset";
import Button from "primevue/button";
import Divider from "primevue/divider";
import Footer from "../components/Footer.vue";
import Header from "../components/Header.vue";
import Image from "primevue/image";
import { teamInfoList } from "../content/team-info";
import { referenceInfoList } from "../content/reference-info";
</script>

<template>
  <div class="grid">
    <div class="col-2"></div>
    <div class="col">
      <div class="sticky top-0"><Header :displayStrategyIndex="false"></Header></div>
      <h1 class="text-6xl text-center">Publications and References</h1>
      <Divider class="fh-divider-primary"></Divider>
      <div >
        <div
          class="m-4"
          v-for="(item, index) in referenceInfoList"
          v-bind:key="index"
        >
          <div>
            {{ item.label }}
            <span
              >[<a
                :href="item.links[0].link"
                target="_blank"
                rel="noopener noreferrer"
                >link</a
              >]</span
            >
          </div>
        </div>
      </div>
      <Divider class="mt-6" />
      <Footer></Footer>
    </div>
    <div class="col-2"></div>
  </div>
</template>
