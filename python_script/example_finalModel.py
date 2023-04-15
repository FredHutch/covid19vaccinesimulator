from .model_tool_functions import input_function
import sys
import os
import json
import numpy as np
# from matplotlib import pyplot as plt
from json import JSONEncoder

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def main(paramObj):
    output = input_function(paramObj)

    # dict_keys(['peakHospitalization', 'cumulativeNumberOfDeaths', 'infectionTimeSeries', 'symptomaticInfectionTimeSeries', 'hospitalizationTimeSeries', 'deathTimeSeries'])
    #print(output.keys())

    #plotting

    """
    allInfections = output['infectionTimeSeries']
    sympInfections = output['symptomaticInfectionTimeSeries']
    hosp = output['hospitalizationTimeSeries']
    deaths = output['deathTimeSeries']

    myoutputs = [allInfections, sympInfections, hosp, deaths]
    """

    return json.loads(json.dumps(output, cls=NumpyArrayEncoder, indent=4))


if __name__ == '__main__':
    # v2: using http input
    file_path = os.path.join(os.path.dirname(__file__), 'pinia-state_for_Laura_LMedits_noPrevVac.json')
    f = open(file_path)

    # v1: using json file
    # f = open('pinia-state_for_Laura_LMedits_noPrevVac.json')
    # f = open('pinia-state_for_Laura_LMedits2.json')
    myjson_file = json.load(f)


    # [Key Change]: export result in JSON format to be consumed by the backend, to be used by the frontend
    result = main(myjson_file)
    print(json.dumps(result, indent=4, sort_keys=True))
    sys.stdout.flush()


"""
print(myoutputs)
print(json.dumps(myoutputs, indent=4, sort_keys=True))
sys.stdout.flush()
"""

"""
tspan = range(len(allInfections[0]))
counter = 1
fig = plt.figure()
for out in myoutputs:

    plt.subplot(2,2,counter)
    for ivals in range(5):
        plt.plot(tspan, out[ivals])

    counter +=1
# fig.savefig('example_output_figure.pdf')
#epiCurves = [totalInf, totalSympInf, hosp, deaths] each element of this list is an array of size number_of_days * 5, where
# each column is a different age group.
# eg. totalSympInf = time series of the total symptomatic infections one column per age group


# [[peakHosp, totalDeaths], epiCurves] = input_function(myjson_file)
# results = [[peakHosp, totalDeaths], epiCurves]
# print(totalDeaths)
# [allInfections, symptomaticInfections, hosp, deaths] = epiCurves
#each of these arrays have n rows where n = number of days and 5 columns one per age group
# with the first column being group 0-19

# tspan = range(np.shape(allInfections)[0])
# plt.subplot(2,2,1)
# plt.plot(tspan, allInfections)
# plt.subplot(2,2,2)
# plt.plot(tspan, symptomaticInfections)
# plt.subplot(2,2,3)
# plt.plot(tspan, hosp)
# plt.subplot(2,2,4)
# plt.plot(tspan, deaths, 'o')

plt.show()
"""