<script setup>
import { storeToRefs } from "pinia";
import { systemName } from "../content/variable";
import { useStrategiesStore } from "../stores/strategies";
import Toolbar from "primevue/toolbar";
import Button from "primevue/button";
import FileUpload from "primevue/fileupload";
import { DateTime } from "luxon";
import Dialog from 'primevue/dialog';

import { useToast } from "primevue/usetoast";
import { fileFormatVersion } from "../content/variable";

import GeneralUtility from "../lib/GeneralUtility.mjs";

const strategiesStore = useStrategiesStore();
const {
  strategyList,
  selectedStrategyIndex,
  addDuplicateOfCurrentStrategy,
  selectStrategy,
  duplicateStrategyByIndex,
} = storeToRefs(strategiesStore);

// :displayStrategyIndex="true"
const props = defineProps({
  displayStrategyIndex: {
    type: Boolean,
    default: true,
  },
});

/*
<i class="pi pi-bars p-toolbar-separator mr-2" ></i>
<SplitButton label="Save" icon="pi pi-check" :model="items" class="p-button-warning"></SplitButton>
*/
const toast = useToast();

const onExportClick = (index) => {
  console.log(`onExportClick: strategy ${index}`);

  let exportData = GeneralUtility.composeExportDataFromStrategyList(strategyList.value);


  const fileString = `data:text/json;chatset=utf-8,${encodeURIComponent(
    JSON.stringify(exportData, null, 2)
  )}`;

  // simulation only
  /*
const fileString = `data:text/json;chatset=utf-8,${encodeURIComponent(
  JSON.stringify(strategy.simulatedOutcome, null, 2)
)}`;
*/

  /*
const fileString = `data:text/json;chatset=utf-8,${encodeURIComponent(
  JSON.stringify(strategy.simulatedOutcome)
)}`;
*/

  console.log(`onExportClick: fileString: ${fileString}`);

  // approach 1 (does not actully download file)

  const link = document.createElement("a");

  //link.href = URL.createObjectURL(fileString);
  link.href = fileString;

  let filePrefix = "strategy_list";

  let timeString = DateTime.now().toISO();

  let regionNameList = GeneralUtility.extraRegionNameFromStrategyList(strategyList.value);

  let regionString = regionNameList.join("-");

  let fileName = `${filePrefix}_for_${regionString}_on_${timeString}.json`;

  link.setAttribute("download", fileName);

  //link.download =
  link.click();

  //window.open(link.href)

  URL.revokeObjectURL(link.href);
  toast.add({severity:'success', summary: 'Success', detail:'Strategies successfully exported!', life: 3000});


  // approach 2
  // actually, this doesn't work exactly well, the file is not formatted as json
  /*
const data = fileString; //JSON.stringify(this.arr)
const blob = new Blob([data], {type: 'text/plain'})
const e = document.createEvent('MouseEvents'),

a = document.createElement('a');

let filePrefix = "strategy";

let timeString = DateTime.now().toISO();

let regionName = strategy.regionParameters.region.name;


a.download = `${filePrefix}_${index+1}_for_${regionName}_${timeString}.json`;
a.href = window.URL.createObjectURL(blob);
a.dataset.downloadurl = ['text/json', a.download, a.href].join(':');
e.initEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
a.dispatchEvent(e);
a.click();
*/
};

const onFileChange = (event) => {
  console.log(`onFileChange: ${event}`);

  const files = document.getElementById('file-upload').files;

  if (files.length <= 0) {
    return false;
  }

  const fr = new FileReader();

  fr.onload = (e) => {
    const result = JSON.parse(e.target.result);
    const formatted = JSON.stringify(result, null, 2);
    console.log(`File content: ${formatted}`);

    // need to check the version number?
    let importedFileFormatVersionString = result.fileFormatVersion;

    let versionCompareResult = GeneralUtility.composeTwoVersionNumbers(importedFileFormatVersionString, fileFormatVersion);

    // Return greater than 0 if a is greater than b
    // < 0 : imported file format  is older than the current version


    // ignore simulationOutcome in the exported file
    let strategyList = result.strategyList.map((strategy) => {
      // delete tempStrategy.simulatedOutcome;

      let strategyCopy = JSON.parse(JSON.stringify(strategy));
      delete strategyCopy.simulatedOutcome;

      strategyCopy = GeneralUtility.convertStrategyFromJSON(JSON.stringify(strategyCopy));

      return strategyCopy;
    });
    strategiesStore.setStrategyList(strategyList);
    toast.add({severity:'success', summary: 'Success', detail:'Strategies successfully imported', life: 3000});
    //document.getElementById('result').innerHTML = formatted;
  }
  fr.readAsText(files.item(0));
};

/*
<label for="file-upload" class="custom-file-upload">
    Custom Upload
</label>
*/
</script>

<template>
  <Toolbar>
    <template #start>
      <Button
        label="Export"
        icon="pi pi-download"
        class="mr-2"
        @click="onExportClick"
      >
      </Button>

      <Button id="import" for="file-upload" label="" class="p-button-success" style="width: 100px; height: 39px;">
        <label for="file-upload" style="width: 100%; height: 100%;" class="flex align-items-center">
          <i class="pi pi-upload"></i>&nbsp;Import
          <input
            id="file-upload"
            type="file"
            style="opacity: 0; width: 10; height: 100%; background-color: transparent"
            @change="onFileChange"
          />
        </label>
      </Button>
    </template>
    <template #end> </template>
  </Toolbar>
</template>
