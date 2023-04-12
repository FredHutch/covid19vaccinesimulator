<script setup>
import Fieldset from "primevue/fieldset";
import Button from "primevue/button";
import Divider from "primevue/divider";
import Footer from "../components/Footer.vue";
import Header from "../components/Header.vue";
import Image from "primevue/image";
import { teamInfoList } from "../content/team-info";
import { systemName } from "../content/variable";

</script>

<template>
  <div class="grid">
    <div class="col-2"></div>
    <div class="col">
      <div class="sticky top-0"><Header :displayStrategyIndex="false"></Header></div>

      
      <h1 class="text-6xl text-center">Legal Disclaimer</h1>
      <Divider class="fh-divider-primary"></Divider>
      <h2>Licence and Disclaimers</h2>
        <p>This work was funded by NSF RAPID grant 2210382. The content is solely the responsibility of the authors and does not necessarily represent the official views of the National Science foundation.</p>
        <p>Any use of this software package is subject to the MIT open source Licence Agreement (the "Licence") accessible at <a href="https://opensource.org/licenses/MIT" target="_blank" rel="noopener noreferrer">https://opensource.org/licenses/MIT</a></p>

        <p>The outputs from the {{systemName}} do not constitute clinical or individual public health advice and must not be used for the purposes of providing such advice. The purpose of {{systemName}}  is to compare different vaccine allocations for up to three vaccine products with specific effectiveness, availability and vaccination rate. The output of {{systemName}}  is not meant to be considered as a forecast of the COVID-19 pandemic under any circumstance. Any reliance placed on the data generated using the {{systemName}} to inform any decision, policy, expenditure, action, inaction or public or private statement is strictly at the discretion and risk of the person or body using the tool and choosing to place such reliance on it. Fred Hutchinson Cancer Center and the authors of this tool accept no responsibility for the results or actions taken based on the information provided in this website.</p>
        <p>The {{systemName}} has been developed in an academic environment in response to the Covid-19 pandemic to help support decision-making Accordingly:</p>
        <ol>
            <li>neither Fred Hutchinson Cancer Center, University of Michigan, or the authors of this tool make any representation or give any warranty, or undertaking that: (i) the scenarios produced by the software tool (as defined in the Licence) will predict the epidemic trajectory in any given setting; (ii) the model parameters, having been estimated using best-evidence at the time of the design of this tool, will be consistent with those in particular regions or under particular scenarios; nor (iii) any decisions informed by scenarios produced by this tool represent the optimal use of vaccine products for any given circumstances.</li>
            <li>neither Fred Hutchinson Cancer Center, University of Michigan or the authors of this tool accept any responsibility for any product that may be designed, developed, manufactured, used, marketed, sold, or supplied or any decision made using the {{systemName}};</li>
            <li>the {{systemName}} tool is made available "as is" and without any warranties, representations, or undertakings whatsoever. As examples, but without limiting the scope of the preceding sentence, neither Fred Hutchinson Cancer Center, University of Michigan or the authors of this tool make any representation or give any warranty, or undertaking:
                <ol>
                    <li>as to the scope, efficacy, or usefulness of the {{systemName}};</li>
                    <li>that Fred Hutchinson Cancer Center and the authors of this tool own all necessary property, intellectual property, and other rights in the {{systemName}};</li>
                    <li>that the {{systemName}} is of satisfactory quality, is fit for any purpose, complies with any sample or description, is made available with reasonable care and skill, is safe and free from bugs, errors, viruses, and other harmful elements, or that its use will be uninterrupted;</li>
                </ol>
            </li>
            <li>The user of the {{systemName}} (to the extent permitted by the Licence) is accepting to use it at their sole risk and expense.</li>
            <li>Please note this tool may be discontinued or change at any time without notice.</li>
        </ol>
      <p>Neither Fred Hutchinson Cancer Center, University of Michigan, the authors of this tool or funding partners shall be liable for any loss suffered or for any other adverse or negative consequence arising directly or indirectly from your reliance on the outputs from this software or from any other use of this software.</p>
      <div class="flex flex-row justify-content-center">
      </div>
      
      <Divider class="fh-divider-primary"></Divider>
        <Footer></Footer>
    </div>
    <div class="col-2"></div>
  </div>
</template>
