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

    


    my_path = "../data/population_data/"
    only_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]

    for file_name in only_files:
        if ".pickle" not in file_name:
            continue
    
        region_code = file_name.split("_")[3].split(".")[0]
        file_path = "../data/population_data/" + file_name
        region_pop_list = [ int(f) for f in pd.read_pickle(file_path).tolist()]
        #print("region:", region_code, ", pop:", region_pop_list)
        #print("type: ", type(region_pop_list), "type [0]: ", type(region_pop_list[0]))

        regionCodePopulationMap[region_code]["populationList"] = region_pop_list

    # regionCodePopulationMap["TWN"]["populationList"] = [1895914, 2038897, 10070315, 5237789, 3972100]
    


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

    with open('region_info_list.json', 'w') as f:
        json.dump(regionInfoList, f)
createRegionPopulationMap()