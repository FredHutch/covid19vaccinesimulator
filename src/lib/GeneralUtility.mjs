import { DateTime, Interval } from "luxon";
import { Decimal } from "decimal.js";
import { fileFormatVersion } from "../content/variable";
import { systemName } from "../content/variable";


export default class GeneralUtility {

  static divideNumbersAsDecimal(numA, numB) {
    let result = new Decimal(numA);
    return result.div(new Decimal(numB)).toNumber();
  }
  static multiplyNumbersAsDecimal(numA, numB) {
    let result = new Decimal(numA);
    return result.mul(new Decimal(numB)).toNumber();
  }

  static sumNumbersAsDecimal(numberList) {
    let result = new Decimal(0);

    numberList.forEach((number) => {
      let newNumber = new Decimal(number);
      result = result.add(newNumber);
    });

    return result.toNumber();
  }

  static minusNumbersAsDecimal(numA, numB) {
    let result = new Decimal(numA);
    return result.minus(new Decimal(numB)).toNumber();
  }

  static compareNumbersAsDecimal(numA, numB) {
    let result = 0;
    
    let decA = new Decimal(numA);
    let decB = new Decimal (numB);

    if( decA.equals(decB)){
      result = 0;
    }
    else if( decA.lessThan(decB)){
      result = -1;
    }
    else{
      result = 1;
    }


    return result;
  }

  static convertListOfListToXSVString(resultMatrix, delimeter=",") {
    console.log(`convertListOfListToXSV: row: ${resultMatrix.length}`);

    if( resultMatrix.length > 0){
      console.log(`convertListOfListToXSV: row: ${resultMatrix.length}, column: ${resultMatrix[0].length}`);
    }

    let resultString = "";

    resultMatrix.forEach((row) =>{
      let rowString = row.join(delimeter);
      resultString += rowString + "\n";
    });

    return resultString;
  }

  static convertStrategyFromJSON(strategyJSON) {
    console.log(`convertStrategyFromJSON: ${strategyJSON}`);

    let result = JSON.parse(strategyJSON);

    console.log(`convertStrategyFromJSON: simulationInterval ${result["simulationInterval"]}`);
    // first, simulation Interval
    result["simulationInterval"][0] = DateTime.fromISO(result["simulationInterval"][0]).toJSDate();
    result["simulationInterval"][1] = DateTime.fromISO(result["simulationInterval"][1]).toJSDate();

    // second, vaccine date

    result["vaccineParameters"]["vaccineList"] = result["vaccineParameters"]["vaccineList"].map((vaccineInfo) => {
      let convertedVaccineInfo = {...vaccineInfo};
      convertedVaccineInfo.date  = DateTime.fromISO(convertedVaccineInfo.date).toJSDate();
      convertedVaccineInfo.allocation[0].date = DateTime.fromISO(convertedVaccineInfo.allocation[0].date).toJSDate();
      convertedVaccineInfo.allocation[1].date = DateTime.fromISO(convertedVaccineInfo.allocation[1].date).toJSDate();
      return convertedVaccineInfo;
    });

    return result;
  }

  static validateStrategy(strategy, index) {
    console.log(`validateStrategy: ${strategy}`);

    let messageList = [];

    if(strategy.regionParameters.region == "" || strategy.regionParameters.region.name.length == 0){
      // region name is empty
      let msg = `Strategy ${index + 1} is missing region information.`;
      messageList.push(msg);
    }


    return messageList;
  }

  static composeTwoVersionNumbers(versionAString, versionBString) {
    console.log(`composeTwoVersionNumbers: ${versionAString}, ${versionBString}`);

    let versionIntListA = versionAString.split(".").map((numString) => { return Number(numString)});
    let versionIntListB = versionBString.split(".").map((numString) => { return Number(numString)});

    /*
    Return greater than 0 if a is greater than b
    Return 0 if a equals b
    Return less than 0 if a is less than b
    */

    for(let i = 0 ;i < versionIntListA.length; i++){
      let intA = versionIntListA[i];
      let intB = versionIntListB[i];

      if(intA != intB){
        return intA - intB
      }
    }

    return 0;
  }

  static composeExportDataFromStrategyList(strategyList) {
    console.log(`composeExportDataFromStrategyList: ${strategyList.length}`);
    let exportData = {
      systemName: systemName,
      fileFormatVersion: fileFormatVersion,
      strategyList: strategyList.map((strategy) => {
        let strategyCopy = JSON.parse(JSON.stringify(strategy));
  
        // simply return everything for now, including simulated outcome if there is
        return strategyCopy;
  
      })
    };

    return exportData;
  }

  static extraRegionNameFromStrategyList(strategyList) {
    console.log(`extraRegionNameFromStrategyList: ${strategyList.length}`);

    let regionList = strategyList.map((strategy) => {
      return strategy.regionParameters.region.name;
    });

    return regionList;
  }

  static hasEnoughSimulationPeriod(aDate, bDate, dateDaysList) {
    console.log(`hasEnoughSimulationPeriod: ${aDate}, ${bDate}, ${JSON.stringify(dateDaysList)}`);

    let result = true;

    let expectedResult = GeneralUtility.calculateStartAndEndWithDateAndDaysList(dateDaysList);

    //let expectedPeriod = GeneralUtility.diffDateByUnits(expectedResult[0], expectedResult[1], "days");

    let expectedStart = DateTime.fromJSDate(expectedResult[0]);
    let expectedEnd = DateTime.fromJSDate(expectedResult[1]);


    // check if the interval is a super set of the interval formed by aDate and bDate
    // let expectedInterval = Interval.fromDateTimes(expectedStart, expectedEnd);

    let currentInterval = Interval.fromDateTimes(DateTime.fromJSDate(aDate).startOf("day"),DateTime.fromJSDate(bDate).endOf("day"));

    if(currentInterval.contains(expectedStart)){
      console.log(`hasEnoughSimulationPeriod: expected start date [${expectedStart}] is in the period: ${currentInterval}`);
    }
    else{
      console.log(`hasEnoughSimulationPeriod: expected start date [${expectedStart}] is not in the period: ${currentInterval}`);
      result = false;
    }

    if(currentInterval.contains(expectedEnd)){
      console.log(`hasEnoughSimulationPeriod: expected end date [${expectedEnd}] is in the period: ${currentInterval}`);
    }
    else{
      console.log(`hasEnoughSimulationPeriod: expected end date [${expectedEnd}] is not in the period: ${currentInterval}`);
      result = false;
    }

    console.log(`hasEnoughSimulationPeriod: ${result}`);

    return result;
  }

  static sortDateCompareFunction(aDate, bDate) {
    let aDateTime = DateTime.fromJSDate(aDate);
    let bDateTime = DateTime.fromJSDate(bDate);

    if (aDateTime < bDateTime) {
      return -1;
    } else if (aDateTime > bDateTime) {
      return 1;
    } else {
      return 0;
    }
  }

  static calculateStartAndEndWithDateAndDaysList(dateDatesList) {
    console.log(`calculateStartAndEndWithDateAndDaysList: ${JSON.stringify(dateDatesList)}`);

    let expectedStartDate = undefined;
    let expectedEndDate = undefined;

    if (dateDatesList.length == 0) {
      return [expectedStartDate, expectedEndDate];
    }

    // identify all the end date
    let myList = dateDatesList.map((dInfo) => {
      // calculate the end date
      return {
        ...dInfo,
        endDate: DateTime.fromJSDate(dInfo.startDate)
          .plus({ days: dInfo.days })
          .toJSDate(),
      };
    });

    // ok, now we have all the information

    // identify the earliest start dates
    let startDateList = myList.map((dInfo) => {
      return dInfo.startDate;
    });

    startDateList.sort(GeneralUtility.sortDateCompareFunction);

    // now, need to pick the earlist one
    expectedStartDate = startDateList[0];

    // identify the latest end dates
    let endDateList = myList.map((dInfo) => {
      return dInfo.endDate;
    });

    endDateList.sort(GeneralUtility.sortDateCompareFunction);

    // now, need to pick the earlist one
    expectedEndDate = endDateList[endDateList.length - 1];

    return [expectedStartDate, expectedEndDate];
  }

  static diffDateByUnits(date1, date2, unit="days") {
    let start = DateTime.fromISO(DateTime.fromJSDate(date1).toISODate());
    let end = DateTime.fromISO(DateTime.fromJSDate(date2).toISODate());

    let diffInDays = GeneralUtility.diffDateTime(start, end, unit);
    return diffInDays.toObject()[unit];
  }

  static diffDateTime(datetimeA, datetimeB, unit) {
    return datetimeB.diff(datetimeA, unit);
  }

  static isPositiveNumber(val) {
    let str = String(val);
    str = str.trim();
    if (!str) {
      return false;
    }
    str = str.replace(/^0+/, "") || "0";
    let n = new Decimal(Number(str));

    return n.toNumber() !== Infinity && n >= 0;

    //return n !== Infinity && String(n) === str && n >= 0;
  }

  static isPositiveInteger(val) {
    let str = String(val);
    str = str.trim();
    if (!str) {
      return false;
    }
    str = str.replace(/^0+/, "") || "0";
    var n = Math.floor(Number(str));
    return n !== Infinity && String(n) === str && n >= 0;
  }
}
