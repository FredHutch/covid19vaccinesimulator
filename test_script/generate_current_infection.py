import pandas as pd
import csv
import json
from os import listdir
from os.path import isfile, join

def readRegionNameMap():
    file_name = "../data/region_name_code.pickle"
    object = pd.read_pickle(file_name)



    object["Taiwan"] = "TWN"

    print(object)


    with open('region_code_map.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["Name", "Code"])
        for regionName in sorted(object):
            spamwriter.writerow([regionName, object[regionName]])

    newObjectList = []
    for regionName in sorted(object):
        newObjectList.append({
            "name": regionName,
            "code": object[regionName]
        })


    with open('region_code_map.json', 'w') as f:
        json.dump(newObjectList, f)

def createRegionPopulationMap():
    regionInfoList = []
    regionCodePopulationMap = {}
    regionInfoMap = {}
    file_name = "../data/region_name_code.pickle"
    object = pd.read_pickle(file_name)

    for region_name in object.keys():
        region_code = object[region_name]

        regionCodePopulationMap[region_code] = {
            "name": region_name,
            "code": region_code
        }


    regionCodePopulationMap["CIV"] = {
        "name": "Cote d'Ivoire",
        "code": "CIV"
    }

    regionCodePopulationMap["AUS"] = {
        "name": "Australia",
        "code": "AUS"
    }
    regionCodePopulationMap["HTI"] = {
        "name": "Haiti",
        "code": "HTI"
    }
    regionCodePopulationMap["JPN"] = {
        "name": "Japan",
        "code": "JPN"
    }
    regionCodePopulationMap["LBN"] = {
        "name": "Lebanon",
        "code": "LBN"
    }
    regionCodePopulationMap["SOM"] = {
        "name": "Somalia",
        "code": "SOM"
    }
    regionCodePopulationMap["TWN"] = {
        "name": "Taiwan",
        "code": "TWN"
    }

    region_name_list = [regionCodePopulationMap[key]["name"] for key in regionCodePopulationMap]

    regionNameInfectionMap = {}

    name_not_found_list = []

    with open('../data/cum_infections_Nov_2021_clean.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # This skips the first row of the CSV file.
        next(spamreader)
        for row in spamreader:
            region_name = row[0]
            infection_percentage = float(row[1])

            if(region_name not in region_name_list):
                print(f"{region_name} not in our region list")
            else:
                regionNameInfectionMap[region_name] = infection_percentage


    """
    for region_code in regionCodePopulationMap:
        name = regionCodePopulationMap[region_code]["name"]
        code = region_code
        populationList = regionCodePopulationMap[region_code]["populationList"]
        regionInfoList.append({
            "name": name,
            "code": code,
            "populationList": populationList
        })
    regionInfoList = sorted(regionInfoList, key=lambda x: x["name"])
    print(regionInfoList)
    """

    with open('region_infection.json', 'w') as f:
        json.dump(regionNameInfectionMap, f)

createRegionPopulationMap()