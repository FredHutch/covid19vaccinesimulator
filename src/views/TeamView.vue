<script setup>
import Fieldset from "primevue/fieldset";
import Button from "primevue/button";
import Divider from "primevue/divider";
import Footer from "../components/Footer.vue";
import Header from "../components/Header.vue";
import Image from "primevue/image";
import { teamInfoList } from "../content/team-info";
</script>

<template>
  <div class="grid">
    <div class="col-2"></div>
    <div class="col">
      <div class="sticky top-0"><Header :displayStrategyIndex="false"></Header></div>
      <h1 class="text-6xl text-center">Research Team</h1>
      <Divider class="fh-divider-primary"></Divider>
      <div class="flex flex-row justify-content-center">
        <div class="flex p-2" v-for="(member, index) in teamInfoList" v-bind:key="index">
          <div class="member-profile">
            <div>
              <Image :src="member.photoURL" :alt="member.label" imageStyle="object-fit: cover; width: 280px; height: 280px;" />
            </div>
            <div>
              <a
                :href="member.siteURL"
                target="_blank"
                rel="noopener noreferrer"
                ><div>{{ member.label }}</div></a
              >
              <p>{{ member.position }}</p>
              <p >{{ member.affiliation }}</p>
            </div>
          </div>
        </div>

        
      </div>
      <div class="mt-8">This work was funded by NSF RAPID grant 2210382. The content is solely the responsibility of the authors and does not necessarily represent the official views of the National Science foundation.</div>
      <Divider class="mt-6" />
      <Footer></Footer>

        
    </div>
    <div class="col-2"></div>
  </div>
</template>

<style scoped lang="scss">

.member-profile {
  width: 280px;
}
</style>
