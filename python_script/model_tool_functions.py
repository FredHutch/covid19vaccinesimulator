import numpy as np
from scipy.integrate import odeint
# from matplotlib import pyplot as plt
import sys
import os
import json
import pandas as pd
import pickle
from .myFunctions import * #runVaccination_model, set_time_vaccine_simulation, set_vaccine_rates, \
#different from model_tool_functions0.py in that I will adapt all the functions to match the front end json file
    #contact_matrix_weighted_by_social_distancing, find_beta_System1, calculateMetrics
# from saveLoadFunctions import saveResults
# from myFunctions import contact_matrix_weighted_by_social_distancing, find_beta_System1, set_time_vaccine_simulation
# from myFunctions import runVaccination_model, calculateMetricsAndEpidemicCurves
def computeVE_P(VE_SUS, VE_DIS):

    VE_SYMP = np.zeros(3)
    for ivals in range(3):
        if VE_SUS[ivals] == 1:
            VE_SYMP[ivals] == 1
        else:
            VE_SYMP[ivals] = 1 - ((1 - VE_DIS[ivals])/(1 - VE_SUS[ivals]))
    return VE_SYMP


def computeVE_P_1d(VE_SUS, VE_DIS):
    VE_SYMP = 1 - ((1 - VE_DIS)/(1 - VE_SUS))
    # print(VE_SYMP)
    return VE_SYMP

def computeVE_HOSP_cond(VE_HOSP, VE_SUS, VE_SYMP):

    VE_HOSP_cond = np.zeros(3)
    for ivals in range(3):
        VE_HOSP_cond[ivals] = 1 - ((1-VE_HOSP[ivals])/((1-VE_SUS[ivals])*(1-VE_SYMP[ivals])))
    return VE_HOSP_cond

def computeVE_HOSP_cond_1d(VE_HOSP, VE_SUS, VE_SYMP):
    VE_HOSP_cond = 1 - ((1-VE_HOSP)/((1-VE_SUS)*(1-VE_SYMP)))
    return VE_HOSP_cond

def computeVE_HOSP_cond2(VE_HOSP, VE_DIS):

    VE_HOSP_cond = np.zeros(3)
    for ivals in range(3):
        VE_HOSP_cond[ivals] = 1 - ((1-VE_HOSP[ivals])/(1-VE_DIS[ivals]))
    return VE_HOSP_cond

def computeVE_HOSP_cond2_1d(VE_HOSP, VE_DIS):

    VE_HOSP_cond = 1 - ((1-VE_HOSP)/(1-VE_DIS))
    return VE_HOSP_cond

def get_vaccine_params_from_json(vaccineAvailability):
    """
    this function extracts the info for vaccine availability given by the user and turn it into the variables needed 
    to run the model.
    :param vaccineAvailability: 
    :return: 
    - num_doses: a vector D of size 1 x 3 that gives the TOTAL number of available doses for each vaccine (d_i gives the total
    number of vaccines of type i
    - num_vaccines_available_primary: a vector D of size 1 x 3 that gives the number of doses available for primary vaccination
    for each vaccine type. d_i gives number of vaccines of type i to use as primary vaccinations.
    - num_vaccines_available_booster: a vector D of size 1 x 3 that gives the number of doses available for booster vaccination
    for each vaccine type. d_i gives number of vaccines of type i to use as boosters. 
    - num_vaccines_available_pt_of_view_vaccinated: this is a list with three elements, V1, V2 and V3, representing the 
    number of vaccines available for boosters for people vaccinated with vaccine 1 (V1), vaccine 2 (V2) and vaccine 3 (V3).
    Vi = vector of size 1 * 3. Vi_j and represents the number of vaccines of type j available for people who got originally
    vaccinated with type i. 
    distribution_matrix_primary_series: a matrix M of size 3 x 5 representing the distribution of vaccine as primary series among 
    age groups. Each row Mi  represents the distribution of vaccine type i among the 5 age groups. 
    distribution_list_boosters: a list of three matrices, M1, M2 and M3 where the matrix Mi is a matrix of size  
    3 x 5 representing the distribution of vaccine of type i among the previously vaccinated.
    Each row represents people vaccinated with the vaccine of type k, so that the entry Mi_kj represents the number of doses
    of vaccine i that people in group j who were previoulsy vaccinated with vaccine k will get. 
    distribution_list_boosters_pt_of_view_vaccinated: a list of three matrices, M1, M2 and M3 where the matrix Mi is a matrix of size  
    3 x 5 representing the number of doses that people who previously got vaccinated with vaccine of type i will get from each 
    vaccine in each age group. So, Mi_kj represents the number of boosters of type j for people who got vaccinated with vaccine i as
    a primary series in group k.
    """""
    prop_vaccines_available_primary = np.zeros(3)
    prop_vaccines_available_booster = np.zeros(3)
    num_doses = np.zeros(3)
    num_vaccines_available_primary = np.zeros(3)
    # num_vaccines_available_booster = np.zeros(3)
    vaccination_startDates_primary = []
    vaccination_startDates_booster = []
    vaccination_rates = np.zeros(3)
    vaccination_rates_primary = np.zeros((3,5))
    vaccination_rates_booster_list_pt_of_view_vaccinated = [np.zeros((3,5)), np.zeros((3,5)),np.zeros((3,5))]
    num_doses_per_day_primary = np.zeros(3)
    num_doses_per_day_booster_list_pt_of_view_vaccinated = np.zeros((3,3))

    prop_distribution_matrix_primary_series = np.zeros((3,5))
    distribution_matrix_primary_series = np.zeros((3,5))
    prop_distribution_list_boosters = [np.zeros((3, 5)), np.zeros((3, 5)), np.zeros((3, 5))]
    distribution_list_boosters = [np.zeros((3, 5)), np.zeros((3, 5)), np.zeros((3, 5))]
    distribution_V1, distribution_V2, distribution_V3 = np.zeros((3, 5)), np.zeros((3, 5)), np.zeros((3, 5))
    numBoostersAvailable_for_V1_B, numBoostersAvailable_for_V2_B, numBoostersAvailable_for_V3_B = np.zeros(3), np.zeros(3), np.zeros(3)

    vaccineNames = []
    # create the lists from the point of view of the primary series vaccinated individuals
    distribution_list_boosters_pt_of_view_vaccinated = [distribution_V1, distribution_V2, distribution_V3]
    num_vaccines_available_pt_of_view_vaccinated = [numBoostersAvailable_for_V1_B, numBoostersAvailable_for_V2_B,
                                                    numBoostersAvailable_for_V3_B]
    prop_distribution_list_boosters_pt_of_view_vaccinated = [np.zeros((3, 5)), np.zeros((3, 5)), np.zeros((3, 5))]
    for ivals in range(3):

        #loop through vaccineAvailability list and extract the total number of doses
        num_doses[ivals] = vaccineAvailability[ivals]['number']
        #vaccination_starts_primary = ####### falta la fecha donde vamos a empezar a vacunar vaccineAvailability[ivals]
        # loop through vaccineAvailability list and extract the proportion of doses for the primary and booster series
        prop_vaccines_available_primary[ivals] = (1/100) * vaccineAvailability[ivals]['allocation'][0]['proportion']
        prop_vaccines_available_booster[ivals] = (1/100) * vaccineAvailability[ivals]['allocation'][1]['proportion']

        # #convert proportions into raw numbers of vaccines:
        num_vaccines_available_primary = np.multiply(num_doses, prop_vaccines_available_primary)
        num_vaccines_available_booster = np.multiply(num_doses, prop_vaccines_available_booster)


        # read the names of vaccines to be used:
        vaccineNames.append(vaccineAvailability[ivals]['code'])
        vaccination_startDates_primary.append(pd.to_datetime(vaccineAvailability[ivals]['allocation'][0]['date']))
        vaccination_startDates_booster.append(pd.to_datetime(vaccineAvailability[ivals]['allocation'][1]['date']))
        vaccination_rates[ivals] = vaccineAvailability[ivals]['rate']
        vaccination_rates_primary[ivals] = prop_vaccines_available_primary[ivals] * vaccineAvailability[ivals]['rate']
        #fill the distribution matrix for the primary series:
        for jvals in range(5):
            tempString = 'group'+str(jvals+1)
            prop_distribution_matrix_primary_series[ivals, jvals] = (1/100) * vaccineAvailability[ivals]['allocation'][0][tempString]
            distribution_matrix_primary_series[ivals, jvals] = prop_distribution_matrix_primary_series[ivals, jvals] * num_doses[ivals]

        ### fill the distribution matrix from the boosters' point of view:
        tempProp = prop_distribution_list_boosters[ivals]
        temp = distribution_list_boosters[ivals]
        for kvals in range(3):
            for lvals in range(5):
                tempString2 = 'group' + str(lvals + 1)
                tempProp[kvals, lvals] = (1/100) * vaccineAvailability[ivals]['allocation'][1]['primaryMatching'][kvals][tempString2]
                temp[kvals, lvals] = num_doses[ivals] * tempProp[kvals, lvals]

    # transform the lists of available boosters from booster point of view to previously vaccinated point of view
    for ivals in range(3):
        num_temp = num_vaccines_available_pt_of_view_vaccinated[ivals]
        for jvals in range(3):
            num_temp[jvals] = np.sum(distribution_list_boosters[jvals][ivals,:])
    #transform the proportion of available booster to be divided between groups to the proportion of available booster for
    #each previously vaccinated group and each age group (previously vaccinated point of view)
    for ivals in range(3):
        temp = distribution_list_boosters_pt_of_view_vaccinated[ivals]
        tempProp = prop_distribution_list_boosters_pt_of_view_vaccinated[ivals]
        for jvals in range(3):
            temp[jvals,:] = distribution_list_boosters[jvals][ivals,:]
            tempProp[jvals, :] = prop_distribution_list_boosters[jvals][ivals, :]
    # print(num_vaccines_available_pt_of_view_vaccinated)

    #compute the vaccination rates for each previously vaccinated group and each age group
    for ivals in range(3):
        # print(ivals)
        vaccination_rates_primary[ivals, :] = vaccination_rates[ivals]*prop_distribution_matrix_primary_series[ivals,:]
        vaccination_rates_booster_list_pt_of_view_vaccinated[ivals][0, :] = vaccination_rates[0] * prop_distribution_list_boosters_pt_of_view_vaccinated[ivals][0,:]
        vaccination_rates_booster_list_pt_of_view_vaccinated[ivals][1, :] = vaccination_rates[1] * prop_distribution_list_boosters_pt_of_view_vaccinated[ivals][1, :]
        vaccination_rates_booster_list_pt_of_view_vaccinated[ivals][2, :] = vaccination_rates[2] * prop_distribution_list_boosters_pt_of_view_vaccinated[ivals][2, :]

    for ivals in range(3):
        num_doses_per_day_primary[ivals] = np.sum(vaccination_rates_primary[ivals, :])
        for kvals in range(3):
            num_doses_per_day_booster_list_pt_of_view_vaccinated[ivals, kvals] = np.sum(vaccination_rates_booster_list_pt_of_view_vaccinated[ivals][kvals,:])

    return [num_vaccines_available_primary,num_vaccines_available_pt_of_view_vaccinated,
            vaccination_startDates_primary, vaccination_startDates_booster,
            distribution_matrix_primary_series,  distribution_list_boosters_pt_of_view_vaccinated,
            vaccination_rates_primary, vaccination_rates_booster_list_pt_of_view_vaccinated,
            num_doses_per_day_primary, num_doses_per_day_booster_list_pt_of_view_vaccinated]


# def get_fraction_vaccine_distribution_from_json(vaccineAvailability):
#     """
#     this function extracts the info for vaccine availability given by the user and turn it into the variables needed
#     to run the model in terms of fractions of vaccine available only
#     :param vaccineAvailability:
#     :return:
#     - num_doses: a vector D of size 1 x 3 that gives the TOTAL number of available doses for each vaccine (d_i gives the total
#     number of vaccines of type i
#     - num_vaccines_available_primary: a vector D of size 1 x 3 that gives the number of doses available for primary vaccination
#     for each vaccine type. d_i gives number of vaccines of type i to use as primary vaccinations.
#     - num_vaccines_available_booster: a vector D of size 1 x 3 that gives the number of doses available for booster vaccination
#     for each vaccine type. d_i gives number of vaccines of type i to use as boosters.
#     - num_vaccines_available_pt_of_view_vaccinated: this is a list with three elements, V1, V2 and V3, representing the
#     number of vaccines available for boosters for people vaccinated with vaccine 1 (V1), vaccine 2 (V2) and vaccine 3 (V3).
#     Vi = vector of size 1 * 3. Vi_j and represents the number of vaccines of type j available for people who got originally
#     vaccinated with type i.
#     distribution_matrix_primary_series: a matrix M of size 3 x 5 representing the distribution of vaccine as primary series among
#     age groups. Each row Mi  represents the distribution of vaccine type i among the 5 age groups.
#     distribution_list_boosters: a list of three matrices, M1, M2 and M3 where the matrix Mi is a matrix of size
#     3 x 5 representing the distribution of vaccine of type i among the previously vaccinated.
#     Each row represents people vaccinated with the vaccine of type k, so that the entry Mi_kj represents the number of doses
#     of vaccine i that people in group j who were previoulsy vaccinated with vaccine k will get.
#     distribution_list_boosters_pt_of_view_vaccinated: a list of three matrices, M1, M2 and M3 where the matrix Mi is a matrix of size
#     3 x 5 representing the number of doses that people who previously got vaccinated with vaccine of type i will get from each
#     vaccine in each age group. So, Mi_kj represents the number of boosters of type j for people who got vaccinated with vaccine i as
#     a primary series in group k.
#     """""
#     prop_vaccines_available_primary = np.zeros(3)
#     prop_vaccines_available_booster = np.zeros(3)
#     num_doses = np.zeros(3)
#     num_vaccines_available_primary = np.zeros(3)
#     num_vaccines_available_booster = np.zeros(3)
#     vaccination_startDates_primary = np.zeros(3)
#     vaccination_startDates_booster = np.zeros(3)
#     vaccination_rates = np.zeros(3)
#     prop_distribution_matrix_primary_series = np.zeros((3,5))
#
#     prop_distribution_list_boosters = [np.zeros((3, 5)), np.zeros((3, 5)), np.zeros((3, 5))]
#     distribution_list_boosters = [np.zeros((3, 5)), np.zeros((3, 5)), np.zeros((3, 5))]
#     prop_distribution_V1, prop_distribution_V2, prop_distribution_V3 = np.zeros((3, 5)), np.zeros((3, 5)), np.zeros((3, 5))
#     numBoostersAvailable_for_V1_B, numBoostersAvailable_for_V2_B, numBoostersAvailable_for_V3_B = np.zeros(3), np.zeros(3), np.zeros(3)
#
#     vaccineNames = []
#     # create the lists from the point of view of the primary series vaccinated individuals
#     prop_distribution_list_boosters_pt_of_view_vaccinated = [prop_distribution_V1, prop_distribution_V2, prop_distribution_V3]
#     # num_vaccines_available_pt_of_view_vaccinated = [numBoostersAvailable_for_V1_B, numBoostersAvailable_for_V2_B,
#     #                                                 numBoostersAvailable_for_V3_B]
#     for ivals in range(3):
#
#         #loop through vaccineAvailability list and extract the total number of doses
#         num_doses[ivals] = vaccineAvailability[ivals]['number']
#         #vaccination_starts_primary = ####### falta la fecha donde vamos a empezar a vacunar vaccineAvailability[ivals]
#         # loop through vaccineAvailability list and extract the proportion of doses for the primary and booster series
#         prop_vaccines_available_primary[ivals] = (1/100) * vaccineAvailability[ivals]['allocation'][0]['proportion']
#         prop_vaccines_available_booster[ivals] = (1/100) * vaccineAvailability[ivals]['allocation'][1]['proportion']
#
#         # #convert proportions into raw numbers of vaccines:
#         num_vaccines_available_primary = np.multiply(num_doses, prop_vaccines_available_primary)
#         num_vaccines_available_booster = np.multiply(num_doses, prop_vaccines_available_booster)
#
#         # read the names of vaccines to be used:
#         vaccineNames.append(vaccineAvailability[ivals]['code'])
#         vaccination_startDates_primary[ivals] = vaccineAvailability[ivals]['allocation'][0]['date']
#         vaccination_startDates_booster[ivals] = vaccineAvailability[ivals]['allocation'][1]['date']
#         vaccination_rates[ivals] = vaccineAvailability[ivals]['vaccination_rate']
#         #fill the distribution matrix for the primary series:
#         for jvals in range(5):
#             tempString = 'group'+str(jvals+1)
#             prop_distribution_matrix_primary_series[ivals, jvals] = (1/100) * vaccineAvailability[ivals]['allocation'][0][tempString]
#
#     #
#         ### fill the distribution matrix from the boosters' point of view:
#         tempProp = prop_distribution_list_boosters[ivals]
#         # temp = distribution_list_boosters[ivals]
#         for kvals in range(3):
#             for lvals in range(5):
#                 tempString2 = 'group' + str(lvals + 1)
#                 tempProp[kvals, lvals] = (1/100) * vaccineAvailability[ivals]['allocation'][1]['primaryMatching'][kvals][tempString2]
#                 # temp[kvals, lvals] = num_doses[ivals] * tempProp[kvals, lvals]
#
#
#     # for ivals in range(3):
#     #     num_temp = num_vaccines_available_pt_of_view_vaccinated[ivals]
#     #     for jvals in range(3):
#     #         num_temp[jvals] = np.sum(distribution_list_boosters[jvals][ivals,:])
#
#     for ivals in range(3):
#         temp = prop_distribution_list_boosters_pt_of_view_vaccinated[ivals]
#         for jvals in range(3):
#             temp[jvals,:] = prop_distribution_list_boosters[jvals][ivals,:]
#     # print(num_vaccines_available_pt_of_view_vaccinated)
#     # print('distribution_list_boosters', distribution_list_boosters)
#     # print('distribution_list_boosters_pt_of_view_vaccinated', distribution_list_boosters_pt_of_view_vaccinated)
#
#     return [vaccineNames, num_doses, vaccination_rates,
#             vaccination_startDates_primary, vaccination_startDates_booster,
#             prop_distribution_matrix_primary_series,  prop_distribution_list_boosters_pt_of_view_vaccinated]



def extract_previous_infections(region):
    df = pd.read_csv ('HungMatrajt/Data/IHME_estimates/cum_infections_Nov_2021.csv')
    temp = df.loc[df['V2'] == region]
    return (temp.iloc[0]['V8'])


def computeInitialConditions(region_pop, current_frac_infections, frac_sym, hosp_rate,
                             previous_frac_boosted, previous_frac_infections,
                             previous_frac_primary_vaccinated):
    """
    Computes the initial conditions based on the number of current and previous infections, and the number of previously
    vaccinated with primary and booster doses
    :param currentInfections: vector of size 1 x 5 with the fraction of people in each age group who is currently infected
    :param previous_infections: vector of size 1 x 5 with the fraction of people in each age group who was previously infected
    :param previous_primary_vaccinated: matrix of size 3 X 5 with the fraction of people in each age group (column j )
    who was vaccianted with vaccine i (Mij = fraction of people vaccinated with primary series i in age group j)
    :param previous_boosted: matrix of size 3 X 5 with the fraction of people in each age group (column j )
    who was vaccianted with vaccine i (Mij = fraction of people vaccinated with primary series i in age group j)
    :param region_pop: population in each age group
    :return: the vector of initial coniditions y0 to run the model.
    """
    #compute numbers of previous infections, previous primary vaccinations, previous boosters and
    # current infections per age group:
    previous_infections = np.multiply(previous_frac_infections, region_pop)
    current_infections = np.multiply(current_frac_infections, region_pop)
    previous_primary_vaccinated = np.multiply(previous_frac_primary_vaccinated, region_pop)
    previous_boosted = np.multiply(previous_frac_boosted, region_pop)
    # print('previous_infections', previous_infections)
    # print('current_infections', current_infections)
    # print('previous_primary_vaccinated', previous_primary_vaccinated)
    # print('previous_boosted', previous_boosted)

    #initialize the vector of initial conditions:
    numGroups = len(region_pop)
    y0 = np.zeros((109, numGroups))
    temp = np.reshape(y0, (109, numGroups))

    # # system for unvaccinated
    #
    # S = temp[0, :]  # susceptibles
    # E = temp[1, :]  # Exposed
    # A = temp[2, :]  # Asymptomatic infected
    # P = temp[3, :]  # Pre-symptomatic infected
    # I = temp[4, :]  # Symptomatic infected
    # H = temp[5, :]  # Hospitalized
    # R = temp[6, :]  # Recovered symptomatic
    # RA = temp[7, :]  # Recovered Asymptomatic
    # RH = temp[8, :]  # recovered hospitalized
    # R_R = temp[9, :]  # Recovered symptomatic with partial immunity
    # RA_R = temp[10, :]  # Recovered Asymptomatic with partial immunity
    # RH_R = temp[11, :]  # recovered hospitalized with partial immunity
    #
    # S_P = temp[12, :]  # susceptible partially protected
    # E_P = temp[13, :]  # Exposed partially protected
    # A_P = temp[14, :]  # Asymptomatic infected partially protected
    # P_P = temp[15, :]  # Pre-symptomatic infected partially protected
    # I_P = temp[16, :]  # Symptomatic infected partially protected
    # H_P = temp[17, :]  # Hospitalizes symptomatic infected partially protected
    # R_P = temp[18, :]  # Recovered symptomatic partially protected
    # RA_P = temp[19, :]  # Recovered Asymptomatic partially protected
    # RH_P = temp[20, :]  # Recovered Hospitalized partially protected
    # R_RP = temp[21, :]  # Recovered symptomatic  with partial protection
    # RA_RP = temp[22, :]  # Recovered Asymptomatic  with partial protection
    # RH_RP = temp[23, :]  # Recovered Hospitalized  with partial protection
    #
    # S_PV = temp[24, :]  # susceptible vaccinated partially protected
    # E_PV = temp[25, :]  # Exposed vaccinated partially protected
    # A_PV = temp[26, :]  # Asymptomatic vaccinated infected partially protected
    # P_PV = temp[27, :]  # Pre-symptomatic vaccinated infected partially protected
    # I_PV = temp[28, :]  # Symptomatic infected vaccinated partially protected
    # H_PV = temp[29, :]  # Hospitalizes symptomatic infected vaccinated partially protected
    # R_PV = temp[30, :]  # Recovered symptomatic vaccinated partially protected
    # RA_PV = temp[31, :]  # Recovered Asymptomatic vaccinated partially protected
    # RH_PV = temp[32, :]  # Recovered Hospitalized vaccinated partially protected
    # R_RPV = temp[33, :]  # Recovered symptomatic vaccinated with partial protection
    # RA_RPV = temp[34, :]  # Recovered Asymptomatic vaccinated with partial protection
    # RH_RPV = temp[35, :]  # Recovered Hospitalized vaccinated with partial protection
    #
    # # system for vaccinated people
    #
    # S_V1 = temp[36, :]  # susceptible vaccinated with vaccine type #1
    # E_V1 = temp[37, :]  # Exposed vaccinated  with vaccine type #1
    # A_V1 = temp[38, :]  # Asymptomatic infected vaccinated  with vaccine type #1
    # P_V1 = temp[39, :]  # Pre-symptomatic infected vaccinated  with vaccine type #1
    # I_V1 = temp[40, :]  # Symptomatic infected vaccinated  with vaccine #2
    # H_V1 = temp[41, :]  # Hospitalizes symptomatic infected vaccinated  with vaccine type #1
    # R_V1 = temp[42, :]  # Recovered symptomatic vaccinated  with vaccine type #2
    # RA_V1 = temp[43, :]  # Recovered Asymptomatic vaccinated  with vaccine type #2
    # RH_V1 = temp[44, :]  # Recovered Hospitalized vaccinated  with vaccine type #2
    # R_RV1 = temp[45, :]  # Recovered symptomatic vaccinated with partial immunity with vaccine type #1
    # RA_RV1 = temp[46, :]  # Recovered Asymptomatic vaccinated with partial immunity  with vaccine type #1
    # RH_RV1 = temp[47, :]  # Recovered Hospitalized vaccinated with partial immunity  with vaccine type #1
    #
    # S_V2 = temp[48, :]  # susceptible vaccinated with vaccine type #2
    # E_V2 = temp[49, :]  # Exposed vaccinated  with vaccine type  #2
    # A_V2 = temp[50, :]  # Asymptomatic infected vaccinated  with vaccine type  #2
    # P_V2 = temp[51, :]  # Pre-symptomatic infected vaccinated  with vaccine type  #2
    # I_V2 = temp[52, :]  # Symptomatic infected vaccinated  with vaccine type  #2
    # H_V2 = temp[53, :]  # Hospitalizes symptomatic infected vaccinated  with vaccine type  #2
    # R_V2 = temp[54, :]  # Recovered symptomatic vaccinated  with vaccine type  #2
    # RA_V2 = temp[55, :]  # Recovered Asymptomatic vaccinated  with vaccine type  #2
    # RH_V2 = temp[56, :]  # Recovered Hospitalized vaccinated  with vaccine type #2
    # R_RV2 = temp[57, :]  # Recovered symptomatic vaccinated with partial immunity  with vaccine type  #2
    # RA_RV2 = temp[58, :]  # Recovered Asymptomatic vaccinated with partial immunity  with vaccine type #2
    # RH_RV2 = temp[59, :]  # Recovered Hospitalized vaccinated with partial immunity  with vaccine type  #2
    #
    # S_V3 = temp[60, :]  # susceptible vaccinated with vaccine type  #3
    # E_V3 = temp[61, :]  # Exposed vaccinated  with vaccine type #3
    # A_V3 = temp[62, :]  # Asymptomatic infected vaccinated  with vaccine type  #3
    # P_V3 = temp[63, :]  # Pre-symptomatic infected vaccinated  with vaccine type  #3
    # I_V3 = temp[64, :]  # Symptomatic infected vaccinated  with vaccine type #3
    # H_V3 = temp[65, :]  # Hospitalizes symptomatic infected vaccinated  with vaccine type  #3
    # R_V3 = temp[66, :]  # Recovered symptomatic vaccinated  with vaccine type #3
    # RA_V3 = temp[67, :]  # Recovered Asymptomatic vaccinated  with vaccine type #3
    # RH_V3 = temp[68, :]  # Recovered Hospitalized vaccinated  with vaccine type #3
    # R_RV3 = temp[69, :]  # Recovered symptomatic vaccinated with partial immunity  with vaccine type  #3
    # RA_RV3 = temp[70, :]  # Recovered Asymptomatic vaccinated with partial immunity  with vaccine type #3
    # RH_RV3 = temp[71, :]  # Recovered Hospitalized vaccinated with partial immunity  with vaccine type #3
    #
    # S_B1 = temp[72, :]  # susceptible vaccinated with vaccine booster type #1
    # E_B1 = temp[73, :]  # Exposed vaccinated  with vaccine booster type #1
    # A_B1 = temp[74, :]  # Asymptomatic infected vaccinated  with vaccine booster type #1
    # P_B1 = temp[75, :]  # Pre-symptomatic infected vaccinated  with vaccine booster type #1
    # I_B1 = temp[76, :]  # Symptomatic infected vaccinated  with vaccine booster type #2
    # H_B1 = temp[77, :]  # Hospitalizes symptomatic infected vaccinated  with vaccine booster type #1
    # R_B1 = temp[78, :]  # Recovered symptomatic vaccinated  with vaccine booster type #2
    # RA_B1 = temp[79, :]  # Recovered Asymptomatic vaccinated  with vaccine booster type #2
    # RH_B1 = temp[80, :]  # Recovered Hospitalized vaccinated  with vaccine booster type #2
    # R_RB1 = temp[81, :]  # Recovered symptomatic vaccinated with partial immunity with vaccine booster type #1
    # RA_RB1 = temp[82, :]  # Recovered Asymptomatic vaccinated with partial immunity  with vaccine booster type #1
    # RH_RB1 = temp[83, :]  # Recovered Hospitalized vaccinated with partial immunity  with vaccine booster type #1
    #
    # S_B2 = temp[84, :]  # susceptible vaccinated with vaccine booster type #2
    # E_B2 = temp[85, :]  # Exposed vaccinated  with vaccine booster type  #2
    # A_B2 = temp[86, :]  # Asymptomatic infected vaccinated  with vaccine booster type  #2
    # P_B2 = temp[87, :]  # Pre-symptomatic infected vaccinated  with vaccine booster type  #2
    # I_B2 = temp[88, :]  # Symptomatic infected vaccinated  with vaccine booster type  #2
    # H_B2 = temp[89, :]  # Hospitalizes symptomatic infected vaccinated  with vaccine booster type  #2
    # R_B2 = temp[90, :]  # Recovered symptomatic vaccinated  with vaccine booster type  #2
    # RA_B2 = temp[91, :]  # Recovered Asymptomatic vaccinated  with vaccine booster type  #2
    # RH_B2 = temp[92, :]  # Recovered Hospitalized vaccinated  with vaccine booster type #2
    # R_RB2 = temp[93, :]  # Recovered symptomatic vaccinated with partial immunity and with vaccine booster type  #2
    # RA_RB2 = temp[94, :]  # Recovered Asymptomatic vaccinated with partial immunity and with vaccine booster type #2
    # RH_RB2 = temp[95, :]  # Recovered Hospitalized vaccinated with partial immunity and with vaccine booster type  #2
    #
    # S_B3 = temp[96, :]  # susceptible vaccinated with vaccine booster type  #3
    # E_B3 = temp[97, :]  # Exposed vaccinated  with vaccine booster type #3
    # A_B3 = temp[98, :]  # Asymptomatic infected vaccinated  with vaccine booster type  #3
    # P_B3 = temp[99, :]  # Pre-symptomatic infected vaccinated  with vaccine booster type  #3
    # I_B3 = temp[100, :]  # Symptomatic infected vaccinated  with vaccine booster type #3
    # H_B3 = temp[101, :]  # Hospitalizes symptomatic infected vaccinated  with vaccine booster type  #3
    # R_B3 = temp[102, :]  # Recovered symptomatic vaccinated  with vaccine booster type #3
    # RA_B3 = temp[103, :]  # Recovered Asymptomatic vaccinated  with vaccine booster type #3
    # RH_B3 = temp[104, :]  # Recovered Hospitalized vaccinated  with vaccine booster type #3
    # R_RB3 = temp[105, :]  # Recovered symptomatic vaccinated with partial immunity  with vaccine booster type  #3
    # RA_RB3 = temp[106, :]  # Recovered Asymptomatic vaccinated with partial immunity  with vaccine booster type #3
    # RH_RB3 = temp[107, :]  # Recovered Hospitalized vaccinated with partial immunity  with vaccine booster type #3

    # #figure out which age groups have been previously vaccinated:
    bool_previous_primary_vaccinated = (previous_primary_vaccinated != 0)
    bool_previous_boosted = (previous_boosted != 0)
    for jvals in range(5):
        print('group', jvals)
        my_sus_vac_list = []

        #### Indices needed to allocate current infections in previously vaccinated individuals
        var_V1 = range(37,42)
        var_V2 = range(49,54)
        var_V3 = range(61,66)
        var_Vs = [var_V1, var_V2, var_V3]

        #### Indices needed to allocate current infections in previously boosted individuals
        var_B1 = range(73,78)
        var_B2 = range(85,90)
        var_B3 = range(97,102)
        var_Bs = [var_B1, var_B2, var_B3]

        #### Indices needed to allocate current infections in previously vaccinated waned individuals:
        var_waned = range(25,30)

        #### Indices needed to allocate  previously infected in vaccinated individuals
        recs_V1 = range(42,48)
        recs_V2 = range(54,60)
        recs_V3 = range(66,72)
        rec_V = [recs_V1, recs_V2, recs_V3]

        #### Indices needed to allocate  previously infected in boosted individuals:
        recs_B1 = range(78,84)
        recs_B2 = range(90,96)
        recs_B3 = range(102,108)
        rec_B = [recs_B1, recs_B2, recs_B3]

        #### Indices needed to allocate previously infected in waned vaccinated individuals:
        rec_partially_vac_indices = range(30,36)


        #### get the indices for the currently exposed
        currently_exposed_indices = [1, 13]
        currently_asymptomatic_indices = [2, 14]
        currently_presymptomatic_indices = [3, 15]
        currently_symptomatic_indices = [4, 16]
        currently_hosp_indices = [5, 17]

        #### get the indices for the previously infected and now recovered
        recovered_asymp_indices = [7, 10, 19, 22]
        recovered_symp_indices = [6, 9, 18, 21]
        recovered_hosp_indices = [8, 11, 20, 23]

        #### get indices of the susceptible vaccinated and vaccinated waned for each type of vaccine:
        sus_vac = [36, 48, 60]
        V1_indices_not_sus = [37,47]
        V2_indices_not_sus = [49,59]
        V3_indices_not_sus = [61, 71]
        V_indices_not_sus = [V1_indices_not_sus, V2_indices_not_sus, V3_indices_not_sus]

        boosted_sus = [72, 84, 96]
        B1_indices_not_sus = [73,83]
        B2_indices_not_sus = [85,95]
        B3_indices_not_sus = [97,107]
        B_indices_not_sus = [B1_indices_not_sus,B2_indices_not_sus,B3_indices_not_sus]



        ############ STEP 1: DISTRIBUTE CURRENT AND PAST INFECTIONS  #################################################
        # distribute current infections equally among all infected classes

        #if there is any previously vaccinated, we need to add the variables for the previously vaccinated waned
        # to the list of current infections and recovered infections
        if len(np.where(bool_previous_primary_vaccinated[:, jvals])[0])>0:
            #add to the index list the vaccinated waned indices for currently infected and previously infected
            currently_exposed_indices.append(var_waned[0])
            currently_asymptomatic_indices.append(var_waned[1])
            currently_presymptomatic_indices.append(var_waned[2])
            currently_symptomatic_indices.append(var_waned[3])
            currently_hosp_indices.append(var_waned[4])
            # print('after!!!!!!!!!!!!!!!!')

            recovered_symp_indices.extend([rec_partially_vac_indices[0], rec_partially_vac_indices[3]])
            recovered_asymp_indices.extend([rec_partially_vac_indices[1], rec_partially_vac_indices[4]])
            recovered_hosp_indices.extend([rec_partially_vac_indices[2], rec_partially_vac_indices[5]])


            # add to the susceptible vaccinated list the susceptible vaccinated waned
            my_sus_vac_list.append(24)

        for ivals in range(3):
            if bool_previous_primary_vaccinated[ivals, jvals] == True:
            # if jvals in previously_vaccinated_indices[ivals]:
                currently_exposed_indices.append(var_Vs[ivals][0])
                currently_asymptomatic_indices.append(var_Vs[ivals][1])
                currently_presymptomatic_indices.append(var_Vs[ivals][2])
                currently_symptomatic_indices.append(var_Vs[ivals][3])
                currently_hosp_indices.append(var_Vs[ivals][4])
                # print('after!!!!!!!!!!!!!!!!')
                # print('currently_exposed_indices', currently_exposed_indices)
                # print('currently_asymptomatic_indices', currently_asymptomatic_indices)
                # print('currently_presymptomatic_indices', currently_presymptomatic_indices)
                # print('currently_symptomatic_indices', currently_symptomatic_indices)
                # print('currently_hosp_indices', currently_hosp_indices)

                recovered_symp_indices.extend([rec_V[ivals][0], rec_V[ivals][3]])
                recovered_asymp_indices.extend([rec_V[ivals][1],rec_V[ivals][4]])
                recovered_hosp_indices.extend([rec_V[ivals][2], rec_V[ivals][5]])
                # print('recovered_symp_indices', recovered_symp_indices)
                # print('recovered_asymp_indices', recovered_asymp_indices)
                # print('recovered_hosp_indices', recovered_hosp_indices)

            # if jvals in previously_boosted_indices[ivals]:
            if bool_previous_boosted[ivals, jvals] == True:
                currently_exposed_indices.append(var_Bs[ivals][0])
                currently_asymptomatic_indices.append(var_Bs[ivals][1])
                currently_presymptomatic_indices.append(var_Bs[ivals][2])
                currently_symptomatic_indices.append(var_Bs[ivals][3])
                currently_hosp_indices.append(var_Bs[ivals][4])

                recovered_symp_indices.extend([rec_B[ivals][0], rec_B[ivals][3]])
                recovered_asymp_indices.extend([rec_B[ivals][1], rec_B[ivals][4]])
                recovered_hosp_indices.extend([rec_B[ivals][2], rec_B[ivals][5]])

                # print('recovered_symp_indices', recovered_symp_indices)
                # print('recovered_asymp_indices', recovered_asymp_indices)
                # print('recovered_hosp_indices', recovered_hosp_indices)

        #distribute the infections in all infection categories (exposed, asymp, presymp, symp, hosp):
        all_inf = current_infections[jvals]
        all_exp = 0.24 * all_inf #rationale: currently I assume 2 days for latent period + 1.5 presymptomatic + 5 symptomatic
                                 # so 2/8.5 = 0.2352 time spent in latent compartment
        all_asym = (1 - 0.24) * (1 - frac_sym[jvals]) * all_inf
        all_pre_symp = (1 - 0.24) * (frac_sym[jvals]) * 0.23 * all_inf
        all_symp = (1 - 0.24) * (frac_sym[jvals]) * (1 - 0.23) * (1 - hosp_rate[jvals]) * all_inf
        all_hosp = (1 - 0.24) * (frac_sym[jvals]) * (1 - 0.23) * hosp_rate[jvals] * all_inf
        # print('all inf', all_inf)
        # print(all_exp + all_symp + all_asym + all_hosp + all_pre_symp)
        # distribute the previously infected among all the infection categories (asymp, symp, hosp)
        all_rec = previous_infections[jvals]
        all_rec_asym = (1 - frac_sym[jvals]) * all_rec
        all_rec_sym = frac_sym[jvals] * (1 - hosp_rate[jvals]) * all_rec
        all_rec_hosp = frac_sym[jvals] * hosp_rate[jvals] * all_rec
        # print('all rec', all_rec)
        # print(all_rec_sym + all_rec_asym + all_rec_hosp)
        #distribute the current infections in all the immune status categories (all distributed equally):
        mynum = len(currently_exposed_indices)
        # print('currently_exposed_indices', currently_exposed_indices)
        # print(all_exp, all_asym, all_symp, all_hosp)
        for index in currently_exposed_indices:
            temp[index, jvals] += (1/mynum)*all_exp

        for index in currently_asymptomatic_indices:
            temp[index, jvals] += (1/mynum)* all_asym

        for index in currently_presymptomatic_indices:
            temp[index, jvals] += (1 / mynum) * all_pre_symp

        for index in currently_symptomatic_indices:
            temp[index, jvals] += (1 / mynum) * all_symp

        for index in currently_hosp_indices:
            temp[index, jvals] += (1 / mynum) * all_hosp

        # distribute the previous infections in all the immune status categories (all distributed equally):
        mynum2 = len(recovered_symp_indices)
        # print(recovered_symp_indices)
        # print(all_rec, all_rec_asym, all_rec_sym, all_rec_hosp)
        for index in recovered_symp_indices:
            temp[index, jvals] += (1/mynum2) * all_rec_sym
            # print([index, jvals], temp[index, jvals])
        for index in recovered_asymp_indices:
            temp[index, jvals] += (1 / mynum2) * all_rec_asym
            # print([index, jvals], temp[index, jvals])
        for index in recovered_hosp_indices:
            temp[index, jvals] += (1 / mynum2) * all_rec_hosp
            # print([index, jvals], temp[index, jvals])
        #step 2: put the previously primary vaccinated in their corresponding compartments split between waned and not
        #waned. We need to consider the people who were previously infected or who are currently infected that we already
        #put in the vaccinated categories.
        #compute how many vaccines were used in that group for the primary vaccinated

        for ivals in range(3):
            if previous_primary_vaccinated[ivals, jvals] != 0:
                #if people have been vaccinated with this vaccine in this age group, then sum all the people that we already
                #put in this age group with vaccine and
                total_vac_temp = previous_primary_vaccinated[ivals, jvals]
                print('total_vac_temp', total_vac_temp)
    #             #get the number of people already allocated vaccine
                lower_ind = V_indices_not_sus[ivals][0]
                upper_ind = V_indices_not_sus[ivals][1]
                partial_tot_vac = np.sum(temp[lower_ind:upper_ind,jvals])
                print('partial_tot_vac', partial_tot_vac)
                num_types_vaccines_used = len(np.nonzero(previous_primary_vaccinated[:, jvals]))
                # print(num_types_vaccines_used)
                partial_waned = (1/num_types_vaccines_used) * np.sum([temp[25:35, jvals]]) #partially vaccinated indices not susceptible:
                print('partial_waned', partial_waned)
    #             vacc_people_to_allocate = total_vac_temp - partial_tot_vac - partial_waned
    #             print('vacc_people_to_allocate', vacc_people_to_allocate)
    #             #allocate equally among susceptible waned and not waned
    #             temp[sus_vac[ivals], jvals] = 0.5 * vacc_people_to_allocate
    #             temp[24, jvals] = 0.5 * vacc_people_to_allocate
    #             # print(temp[sus_vac[ivals], jvals])
    #             # print(temp[24, jvals])
    #
    #         if previous_boosted[ivals, jvals] !=0:
    #             num_booster_vaccines_used = len(np.nonzero(previous_boosted[:, jvals]))
    #             #allocate individuals in the boosted susceptible class if they were boosted
    #             total_boosted_temp = previous_boosted[ivals, jvals]
    #             # print('total_boosted_temp', total_boosted_temp)
    #             lower_ind_B = B_indices_not_sus[ivals][0]
    #             upper_ind_B = B_indices_not_sus[ivals][1]
    #             partial_total_boosted = np.sum(temp[lower_ind_B:upper_ind_B,jvals])
    #             # print('partial_total_boosted', partial_total_boosted)
    #
    #             temp[boosted_sus[ivals], jvals] = total_boosted_temp - partial_total_boosted
    #             # print(temp[boosted_sus[ivals], jvals])
    #
    #
    #     #step 3: put everyone who was not previously infected or recovered or vaccinated or boosted in the susceptible class
    #     sus_people = region_pop[jvals] - np.sum(temp[:, jvals])
    #     temp[0, jvals] = sus_people
    # #check that everything is working as expected:
    # #check we are not losing people:
    # post_vac_matrix = np.zeros((3,5))
    # post_boosted_matrix = np.zeros((3,5))
    # # print('all',np.sum(temp))
    # # for jvals in range(5):
    # #     print('group', jvals)
    # #     total_waned = np.sum([temp[24:36, jvals]])
    # #     for ivals in range(3):
    # #         # print('vaccinated with ', ivals)
    # #         post_vac_matrix[ivals, jvals] = (np.sum(temp[(36 + ivals*12):(48 + ivals*12), jvals]))
    # #         # print('boosted')
    # #         post_boosted_matrix[ivals, jvals] = (np.sum(temp[(72 + ivals * 12):(84 + ivals * 12), jvals]))
    # # print('post_vac_matrix', post_vac_matrix)
    # # print('post_boosted_matrix', post_boosted_matrix)
    # myind = (np.where(temp < 0))
    # print(myind)
    # print(temp[myind])
    return temp.reshape((109 * numGroups))

def computeInitialConditions2(region_pop, current_frac_infections, frac_sym, hosp_rate,
                             previous_frac_boosted, previous_frac_infections,
                             previous_frac_primary_vaccinated, prop_waned):
    """
       Computes the initial conditions based on the number of current and previous infections, and the number of previously
    vaccinated with primary and booster doses
    :param region_pop: population in each age group
    :param current_frac_infections: vector of size 1 x 5 with the fraction of people in each age group who is currently infected
    :param frac_sym: vector of size 1 x 5 with fraction of symptomatics per group
    :param hosp_rate: vector of size 1 x 5 with hospitalization rates per group
    :param previous_frac_boosted: matrix of size 3 X 5 with the fraction of people in each age group (column j )
    who was boosted with vaccine i (Mij = fraction of people vaccinated with primary series i in age group j)
    :param previous_frac_infections: vector of size 1 x 5 with the fraction of people in each age group who was previously infected
    :param previous_frac_primary_vaccinated: matrix of size 3 X 5 with the fraction of people in each age group (column j )
    who was vaccianted with vaccine i (Mij = fraction of people vaccinated with primary series i in age group j)
    :param prop_waned: fraction of everything that will go to the waned classes
    :return: :return: the vector of initial coniditions y0 to run the model.
    """
    # print('previous_frac_boosted', previous_frac_boosted)
    # print('previous_frac_infections', previous_frac_infections)
    # print('previous_frac_primary_vaccinated', previous_frac_primary_vaccinated)
    # print('current_frac_infections', current_frac_infections)
    y0 = np.zeros((109, len(region_pop)))
    temp = np.reshape(y0, (109, len(region_pop)))
    #for each age group, compute the intersection of people who were
    # 1. previously infected and previously vaccinated and
    # 2. currently infected and previously vaccinated.
    inter_currently_inf_and_vaccinated = np.zeros((3,5))
    inter_previous_inf_and_vaccinated = np.zeros((3,5))
    inter_currently_inf_and_boosted = np.zeros((3,5))
    inter_previous_inf_and_boosted = np.zeros((3,5))


    #compute proportion of waned in each age group relative to the proportions of vaccine previously given:
    prop_waned_vac = np.zeros((3,5))
    vac_waned = np.zeros((3,5))
    vac_not_waned = np.zeros((3,5))
    for jvals in range(5):
        if np.any(previous_frac_primary_vaccinated[:, jvals]) !=0:
            for ivals in range(3):
                prop_waned_vac[ivals, jvals] = previous_frac_primary_vaccinated[ivals, jvals]/np.sum(previous_frac_primary_vaccinated[:, jvals])
    # print('prop_waned_vac', prop_waned_vac)

    for jvals in range(5):
        # print(jvals)
        # print('sus waned antes', temp[24, jvals])
        for ivals in range(3):
            if previous_frac_primary_vaccinated[ivals, jvals] != 0:
                # print('sus waned antes', temp[24, jvals])
                inter_currently_inf_and_vaccinated[ivals, jvals] = current_frac_infections[jvals] * previous_frac_primary_vaccinated[ivals, jvals] * region_pop[jvals]
                inter_previous_inf_and_vaccinated[ivals, jvals] = previous_frac_infections[jvals] * previous_frac_primary_vaccinated[ivals, jvals] * region_pop[jvals]
                # print('inter_currently_inf_and_vaccinated[ivals, jvals]',inter_currently_inf_and_vaccinated[ivals, jvals])
                # divide the vaccinated individuals between waned and not waned. The proportion of waned from each vaccine will
                # be proportional to the previously vaccinated
                vac_waned[ivals, jvals] = prop_waned #* prop_waned_vac[ivals, jvals]
                vac_not_waned[ivals, jvals] = (1 - vac_waned[ivals, jvals])
                # print('vac_waned', vac_waned[ivals, jvals])
                # print('vac_not_waned[ivals, jvals]', vac_not_waned[ivals, jvals])

                ##### Assign people to the vaccinated compartments
                ##### Currently infected
                #the 0.24 and 0.23 comes from the following logic:#rationale: currently I assume 2 days for latent period + 1.5 presymptomatic + 5 symptomatic
                # so 2/8.5 = 0.2352 time spent in latent compartment. Similar for the pre-symptomatic

                #assign people to the infected waned compartment
                temp[25, jvals] += 0.24 * vac_waned[ivals,jvals] * inter_currently_inf_and_vaccinated[ivals, jvals] # Exposed
                temp[26, jvals] += (1 - 0.24) * (1 - frac_sym[jvals]) * vac_waned[ivals,jvals] * inter_currently_inf_and_vaccinated[ivals, jvals] #asymptomatic
                temp[27, jvals] += (1 - 0.24) * frac_sym[jvals] * 0.23 * vac_waned[ivals,jvals] * inter_currently_inf_and_vaccinated[ivals, jvals] #presymptomatic
                temp[28, jvals] += (1 - 0.24) * (frac_sym[jvals]) * (1 - 0.23) * (1 - hosp_rate[jvals]) *  vac_waned[ivals,jvals] * inter_currently_inf_and_vaccinated[ivals, jvals]  #symptomatic not hosp
                temp[29, jvals] += (1 - 0.24) * (frac_sym[jvals]) * (1 - 0.23) * hosp_rate[jvals] *  vac_waned[ivals,jvals] * inter_currently_inf_and_vaccinated[ivals, jvals]  #symptomatic not hosp
                # print('waned', np.sum(temp[25:30, jvals]))
                # assign people to the recovered waned compartment:
                temp[30, jvals] += 0.5 * frac_sym[jvals] * (1 - hosp_rate[jvals]) * vac_waned[ivals,jvals] * inter_previous_inf_and_vaccinated[ivals, jvals]
                temp[31 , jvals] += 0.5 * (1 - frac_sym[jvals]) * vac_waned[ivals, jvals] * inter_previous_inf_and_vaccinated[ivals, jvals]
                temp[32 , jvals] += 0.5 * frac_sym[jvals] * hosp_rate[jvals] * vac_waned[ivals, jvals] * inter_previous_inf_and_vaccinated[ivals, jvals]
                temp[33 , jvals] += 0.5 * frac_sym[jvals] * (1 - hosp_rate[jvals]) * vac_waned[ivals, jvals] * inter_previous_inf_and_vaccinated[ivals, jvals]
                temp[34 , jvals] += 0.5 * (1 - frac_sym[jvals]) * vac_waned[ivals, jvals] * inter_previous_inf_and_vaccinated[ivals, jvals]
                temp[35 , jvals] += 0.5 * frac_sym[jvals] * hosp_rate[jvals] * vac_waned[ivals, jvals] * inter_previous_inf_and_vaccinated[ivals, jvals]
                # print('waned rec', np.sum(temp[30:36, jvals]))

                #assign people to the current infected in corresponding vaccine group
                temp[37 + 12*ivals, jvals] += 0.24 * vac_not_waned[ivals,jvals] * inter_currently_inf_and_vaccinated[ivals, jvals] # Exposed
                temp[38 + 12*ivals, jvals] += (1 - 0.24) * (1 - frac_sym[jvals]) * vac_not_waned[ivals,jvals] * inter_currently_inf_and_vaccinated[ivals, jvals] #asymptomatic
                temp[39 + 12*ivals, jvals] += (1 - 0.24) * frac_sym[jvals] * 0.23 * vac_not_waned[ivals,jvals] * inter_currently_inf_and_vaccinated[ivals, jvals] #presymptomatic
                temp[40 + 12*ivals, jvals] += (1 - 0.24) * (frac_sym[jvals]) * (1 - 0.23) * (1 - hosp_rate[jvals]) *  vac_not_waned[ivals,jvals] * inter_currently_inf_and_vaccinated[ivals, jvals]  #symptomatic not hosp
                temp[41 + 12*ivals, jvals] += (1 - 0.24) * (frac_sym[jvals]) * (1 - 0.23) * hosp_rate[jvals] *  vac_not_waned[ivals,jvals] * inter_currently_inf_and_vaccinated[ivals, jvals]  #symptomatic not hosp
                # print('infected vac', np.sum(temp[(37 + 12*ivals):(42 + 12*ivals), jvals]))
                #assign people ot the recovered in corresponding vaccine group (equally distributed among all recovered classes)
                temp[42 + 12*ivals, jvals] += 0.5 * frac_sym[jvals] * (1 - hosp_rate[jvals])  * vac_not_waned[ivals, jvals] * inter_previous_inf_and_vaccinated[ivals, jvals]
                temp[43 + 12*ivals, jvals] += 0.5 * (1 - frac_sym[jvals])  * vac_not_waned[ivals, jvals] * inter_previous_inf_and_vaccinated[ivals, jvals]
                temp[44 + 12*ivals, jvals] += 0.5 * frac_sym[jvals] * hosp_rate[jvals] * vac_not_waned[ivals, jvals] * inter_previous_inf_and_vaccinated[ivals, jvals]
                temp[45 + 12*ivals, jvals] += 0.5 * frac_sym[jvals] * (1 - hosp_rate[jvals]) * vac_not_waned[ivals, jvals] * inter_previous_inf_and_vaccinated[ivals, jvals]
                temp[46 + 12*ivals, jvals] += 0.5 * (1 - frac_sym[jvals]) * vac_not_waned[ivals, jvals] * inter_previous_inf_and_vaccinated[ivals, jvals]
                temp[47 + 12*ivals, jvals] += 0.5 * frac_sym[jvals] * hosp_rate[jvals] * vac_not_waned[ivals, jvals] * inter_previous_inf_and_vaccinated[ivals, jvals]

                # assign people to the susceptibles vaccinated and vaccinated waned (everyone who is not currently infected or recovered)
                temp_vac_left = previous_frac_primary_vaccinated[ivals, jvals] * region_pop[jvals] - \
                                inter_currently_inf_and_vaccinated[ivals, jvals] - inter_previous_inf_and_vaccinated[ivals, jvals]#temp_sum
                # print('temp_vac_left', temp_vac_left)
                temp_vac_left_waned = vac_waned[ivals,jvals] * temp_vac_left
                # print('temp_vac_left_waned',temp_vac_left_waned)
                temp[24, jvals] += temp_vac_left_waned
                # print('sus waned', temp[24, jvals])
                temp[36 + 12 * ivals, jvals] += temp_vac_left - temp_vac_left_waned
                # print('sus vac', temp[36 + 12 * ivals, jvals])
                # print('other waned', np.sum(temp[25:36, jvals]))

            if previous_frac_boosted[ivals, jvals] != 0:
                inter_currently_inf_and_boosted[ivals, jvals] = current_frac_infections[jvals] * previous_frac_boosted[ivals, jvals] * region_pop[jvals]
                inter_previous_inf_and_boosted[ivals, jvals] = previous_frac_infections[jvals] * previous_frac_boosted[ivals, jvals] * region_pop[jvals]
                # print('inter_currently_inf_and_vaccinated', inter_currently_inf_and_vaccinated[ivals, jvals])
                # print('inter_previous_inf_and_vaccinated', inter_previous_inf_and_vaccinated[ivals, jvals])

                #assign people to the current infected in corresponding booster group
                temp[73 + 12*ivals, jvals] += 0.24 * inter_currently_inf_and_boosted[ivals, jvals] # Exposed
                temp[74 + 12*ivals, jvals] += (1 - 0.24) * (1 - frac_sym[jvals]) * inter_currently_inf_and_boosted[ivals, jvals]#asymptomatic
                temp[75 + 12*ivals, jvals] += (1 - 0.24) * frac_sym[jvals] * 0.23 * inter_currently_inf_and_boosted[ivals, jvals]#presymptomatic
                temp[76 + 12*ivals, jvals] += (1 - 0.24) * (frac_sym[jvals]) * (1 - 0.23) * (1 - hosp_rate[jvals]) * inter_currently_inf_and_boosted[ivals, jvals]  #symptomatic not hosp
                temp[77 + 12*ivals, jvals] += (1 - 0.24) * (frac_sym[jvals]) * (1 - 0.23) * hosp_rate[jvals] *  inter_currently_inf_and_boosted[ivals, jvals] #symptomatic not hosp

                #assign people ot the recovered in corresponding boosted group
                temp[78 + 12*ivals, jvals] += 0.5 * frac_sym[jvals] * (1 - hosp_rate[jvals])  * inter_previous_inf_and_boosted[ivals, jvals]
                temp[79 + 12*ivals, jvals] += 0.5 * (1 - frac_sym[jvals])  * inter_previous_inf_and_boosted[ivals, jvals]
                temp[80 + 12*ivals, jvals] += 0.5 * frac_sym[jvals] * hosp_rate[jvals] * inter_previous_inf_and_boosted[ivals, jvals]
                temp[81 + 12*ivals, jvals] += 0.5 * frac_sym[jvals] * (1 - hosp_rate[jvals]) * inter_previous_inf_and_boosted[ivals, jvals]
                temp[82 + 12*ivals, jvals] += 0.5 * (1 - frac_sym[jvals]) * inter_previous_inf_and_boosted[ivals, jvals]
                temp[83 + 12*ivals, jvals] += 0.5 * frac_sym[jvals] * hosp_rate[jvals] * inter_previous_inf_and_boosted[ivals, jvals]

                # assign people to the susceptibles boosted (everyone who is not currently infected or recovered)
                temp_booster_left = previous_frac_boosted[ivals,jvals]*region_pop[jvals] - \
                                    (inter_currently_inf_and_boosted[ivals, jvals] + inter_previous_inf_and_boosted[ivals, jvals])
                temp[72 + 12*ivals, jvals] += temp_booster_left

        ####### assign people to the infected classes:
        ### compute number of current infections to be put in the naive and waned classes
        # print(current_frac_infections[jvals] * region_pop[jvals])
        # print(np.sum(inter_currently_inf_and_vaccinated[:, jvals]))
        # print(np.sum(inter_currently_inf_and_boosted[:, jvals]))
        temp_infected = current_frac_infections[jvals] * region_pop[jvals] - np.sum(inter_currently_inf_and_vaccinated[:, jvals]) -\
            np.sum(inter_currently_inf_and_boosted[:, jvals])
        # print('temp_infected', temp_infected)
        temp_infected_waned = prop_waned*temp_infected
        temp_infected_naive = temp_infected - temp_infected_waned
        # print('temp_infected_waned', temp_infected_waned)
        # print('temp_infected_naive', temp_infected_naive)

        #Currently Infected naive
        temp[1, jvals] += 0.24 *  temp_infected_naive # Exposed
        temp[2, jvals] += (1 - 0.24) * (1 - frac_sym[jvals]) * temp_infected_naive # asymptomatic
        temp[3, jvals] += (1 - 0.24) * frac_sym[jvals] * 0.23 * temp_infected_naive  # presymptomatic
        temp[4, jvals] += (1 - 0.24) * (frac_sym[jvals]) * (1 - 0.23) * (1 - hosp_rate[jvals]) * temp_infected_naive# symptomatic not hosp
        temp[5, jvals] += (1 - 0.24) * (frac_sym[jvals]) * (1 - 0.23) * hosp_rate[jvals]* temp_infected_naive
        # print('total_infected', np.sum(temp[1:6, jvals]))
        #currently infected waned
        temp[13, jvals] += 0.24 *  temp_infected_waned # Exposed
        temp[14, jvals] += (1 - 0.24) * (1 - frac_sym[jvals]) *  temp_infected_waned# asymptomatic
        temp[15, jvals] += (1 - 0.24) * frac_sym[jvals] * 0.23 *   temp_infected_waned# presymptomatic
        temp[16, jvals] += (1 - 0.24) * (frac_sym[jvals]) * (1 - 0.23) * (1 - hosp_rate[jvals]) * temp_infected_waned# symptomatic not hosp
        temp[17, jvals] += (1 - 0.24) * (frac_sym[jvals]) * (1 - 0.23) * hosp_rate[jvals]* temp_infected_waned
        # print('total waned', np.sum(temp[13:18, jvals]))
        ####### assign people to the recovered classes:
        ### compute number of previous infections to be put in the naive and waned classes
        temp_recovered = previous_frac_infections[jvals] * region_pop[jvals] - np.sum(inter_previous_inf_and_vaccinated[:, jvals]) -\
            np.sum(inter_previous_inf_and_boosted[:, jvals])
        temp_recovered_waned = prop_waned * temp_recovered
        temp_recovered_naive = temp_recovered - temp_recovered_waned

        ###Recovered naive
        temp[6, jvals] += 0.5 * frac_sym[jvals] * (1 - hosp_rate[jvals])  * temp_recovered_naive
        temp[7, jvals] += 0.5 * (1 - frac_sym[jvals])  * temp_recovered_naive
        temp[8, jvals] += 0.5 * frac_sym[jvals] * hosp_rate[jvals] * temp_recovered_naive
        temp[9, jvals] += 0.5 * frac_sym[jvals] * (1 - hosp_rate[jvals]) * temp_recovered_naive
        temp[10, jvals] += 0.5 * (1 - frac_sym[jvals]) * temp_recovered_naive
        temp[11, jvals] += 0.5 * frac_sym[jvals] * hosp_rate[jvals] * temp_recovered_naive

        ### Recovered waned
        temp[18, jvals] += 0.5 * frac_sym[jvals] * (1 - hosp_rate[jvals])  * temp_recovered_waned
        temp[19, jvals] += 0.5 * (1 - frac_sym[jvals])  * temp_recovered_waned
        temp[20, jvals] += 0.5 * frac_sym[jvals] * hosp_rate[jvals] * temp_recovered_waned
        temp[21, jvals] += 0.5 * frac_sym[jvals] * (1 - hosp_rate[jvals]) * temp_recovered_waned
        temp[22, jvals] += 0.5 * (1 - frac_sym[jvals]) * temp_recovered_waned
        temp[23, jvals] += 0.5 * frac_sym[jvals] * hosp_rate[jvals] * temp_recovered_waned

        # finally, assign everyone else to the susceptible class:
        all_other_classes = np.sum(temp[1:108, jvals])
        temp[0, jvals] = (1 - prop_waned) * (region_pop[jvals] - all_other_classes)
        temp[12,jvals] = prop_waned * (region_pop[jvals] - all_other_classes)


    # print(np.where(temp < -1e-3))
    return temp.reshape((109 * len(region_pop)))
    # print(vac_waned)
    # print(vac_not_waned)

def compute_proportion_in_each_age_group(popGroups):
    return np.divide(popGroups, np.sum(popGroups))

def getVEParams(vaccineAvailability):

    VE_SUS_primary, VE_DIS_primary, VE_H_primary, \
    VE_SUS_booster, VE_DIS_booster, VE_H_booster = np.zeros(3), np.zeros(3), np.zeros(3), \
                                                   np.zeros(3), np.zeros(3), np.zeros(3)
    # mean_duration_immunity_primary, mean_duration_immunity_booster = np.zeros(3), np.zeros(3),
    #extract the effectiveness:
    for ivals in range(3):
        temp = vaccineAvailability[ivals]["efficacyData"]

        VE_SUS_primary[ivals] = (1/100)*temp[0]['fulldose']
        VE_DIS_primary[ivals] = (1/100)*temp[1]['fulldose']
        VE_H_primary[ivals] = (1/100)*temp[2]['fulldose']

        VE_SUS_booster[ivals] = (1/100)*temp[0]['booster']
        VE_DIS_booster[ivals] = (1/100)*temp[1]['booster']
        VE_H_booster[ivals] = (1/100)*temp[2]['booster']
        # mean_duration_immunity_booster[ivals] = temp_booster['mean_duration_immunity_booster']

    return [VE_SUS_primary, VE_DIS_primary, VE_H_primary, VE_SUS_booster, VE_DIS_booster, VE_H_booster]

    # return [VE_SUS_partially_sus_vaccinated, VE_DIS_partially_sus_vaccinated, VE_H_partially_sus_vaccinated, \
    #         VE_SUS_primary, VE_DIS_primary, VE_H_primary, \
    #         # VE_SUS_booster, VE_DIS_booster, VE_H_booster]#, mean_duration_immunity_primary, mean_duration_immunity_booster]

def get_info_from_frontEnd(myjson_file):
    """
    extract the lists of all the information entered to the frontEnd to run the model
    :param myjson_file: json file with all the info collected by the frontEnd.
    :return:
    """
    startDate = myjson_file['simulationInterval'][0]
    endDate = myjson_file['simulationInterval'][1]
    startDate = pd.to_datetime(startDate)
    endDate = pd.to_datetime(endDate)


    region_name = myjson_file['regionParameters']['region']['name']
    region_code = myjson_file['regionParameters']['region']['code']
    region_pop = np.array(myjson_file['regionParameters']['region']['populationList'])

    R0 = myjson_file['regionParameters']["infectiousnessLevel"]
    #follow the same order it will be passed to model: "home", "work", "school", "others"
    social_distancing_multipliers = np.ones(4) - np.array([myjson_file['regionParameters']["socialDistancing"]["homeSCLevel"],
                                              myjson_file['regionParameters']["socialDistancing"]["workSCLevel"],
                                              myjson_file['regionParameters']["socialDistancing"]["schoolSCLevel"],
                                              myjson_file['regionParameters']["socialDistancing"]["otherSCLevel"]]
                                             )
    location_params = [region_name, region_code, region_pop, endDate, R0, social_distancing_multipliers, startDate]
    previous_frac_infections = (1/100) * np.array([myjson_file['regionParameters']["infectionStatus"][0]['group1'],
                                    myjson_file['regionParameters']["infectionStatus"][0]['group2'],
                                    myjson_file['regionParameters']["infectionStatus"][0]['group3'],
                                    myjson_file['regionParameters']["infectionStatus"][0]['group4'],
                                    myjson_file['regionParameters']["infectionStatus"][0]['group5']])

    current_frac_infections = (1/100) * np.array([myjson_file['regionParameters']["infectionStatus"][1]['group1'],
                                    myjson_file['regionParameters']["infectionStatus"][1]['group2'],
                                    myjson_file['regionParameters']["infectionStatus"][1]['group3'],
                                    myjson_file['regionParameters']["infectionStatus"][1]['group4'],
                                    myjson_file['regionParameters']["infectionStatus"][1]['group5']])

    previous_frac_primary_vaccinated = np.zeros((3,5))
    previous_frac_boosted = np.zeros((3,5))
    for ivals in range(3):
        previous_frac_primary_vaccinated[ivals,:] = (1/100) * np.array([myjson_file["vaccineParameters"]["vaccinationStatusByAgeGroup"]['group1'][ivals]['fulldose'],
                                                 myjson_file["vaccineParameters"]["vaccinationStatusByAgeGroup"]['group2'][ivals]['fulldose'],
                                                 myjson_file["vaccineParameters"]["vaccinationStatusByAgeGroup"]['group3'][ivals]['fulldose'],
                                                 myjson_file["vaccineParameters"]["vaccinationStatusByAgeGroup"]['group4'][ivals]['fulldose'],
                                                 myjson_file["vaccineParameters"]["vaccinationStatusByAgeGroup"]['group5'][ivals]['fulldose']])


        previous_frac_boosted[ivals,:] = (1/100) * np.array([myjson_file["vaccineParameters"]["vaccinationStatusByAgeGroup"]['group1'][ivals]['booster'],
                                                 myjson_file["vaccineParameters"]["vaccinationStatusByAgeGroup"]['group2'][ivals]['booster'],
                                                 myjson_file["vaccineParameters"]["vaccinationStatusByAgeGroup"]['group3'][ivals]['booster'],
                                                 myjson_file["vaccineParameters"]["vaccinationStatusByAgeGroup"]['group4'][ivals]['booster'],
                                                 myjson_file["vaccineParameters"]["vaccinationStatusByAgeGroup"]['group5'][ivals]['booster']])
    initial_conditions_params = [current_frac_infections, previous_frac_infections, previous_frac_primary_vaccinated,
                                 previous_frac_boosted]
    default_params_list = myjson_file["fixedParameters"]
    default_params = get_default_params(default_params_list)

    vaccineAvailability = myjson_file["vaccineParameters"]['vaccineList']
    vaccine_Params = get_vaccine_params_from_json(vaccineAvailability)
    # print(vaccine_Params)
    vaccine_effectiveness_params = getVEParams(vaccineAvailability)

    return [default_params, initial_conditions_params, location_params, vaccine_Params, vaccine_effectiveness_params]



def get_default_params(mydic):
    average_time_between_symptom_onset_and_hospitalization = mydic['averageTimeBetweenSymptomOnsetAndHospitalization']
    mean_duration_infectiousness_post_symptoms = mydic['meanDurationInfectiousnessPostSymptoms']
    mean_duration_hospitalization = mydic['meanDurationHospitalization']
    mean_duration_latent_period = mydic['meanDurationLatentPeriod']
    mean_duration_pre_symptomatic_period = mydic['meanDurationPreSymptomaticPeriod']
    mean_duration_nat_immunity_after_infection = mydic['meanDurationNatImmunityAfterInfection']
    mean_duration_nat_immunity_after_infection2 = mydic['meanDurationNatImmunityAfterInfection2']
    mean_duration_immunity_waned_vax_hybrid = mydic['meanDurationImmunityWanedVaxHybrid']
    mean_duration_primary_immunity = mydic['meanDurationPrimaryImmunity']
    mean_duration_hybrid_immunity = mydic['meanDurationHybridImmunity']
    mean_duration_booster_immunity = mydic['meanDurationBoosterImmunity']
    mean_duration_boosted_hybrid_immunity = mydic['meanDurationBoostedHybridImmunity']
    prop_symptomatic_infection = np.array(mydic['propSymptomaticInfection'])
    relative_infectiousness_asymptomatic_infection = np.array(mydic['relativeInfectiousnessAsymptomaticInfection'])
    relative_infectiousness_hospitalized_infection = np.array(mydic['relativeInfectiousnessHospitalizedInfection'])
    relative_infectiousness_pre_symptomatic_infection = np.array(mydic['relativeInfectiousnessPreSymptomaticInfection'])
    relative_susceptibility = np.array(mydic['relativeSusceptibility'])
    VE_SUS_partially_sus  = (1/100) * np.array(mydic['VESUSpartiallySus'])
    VE_DIS_partially_sus = (1/100) * np.array(mydic['VEDISpartiallySus'])
    VE_H_partially_sus = (1/100) * np.array(mydic['VEHpartiallySus'])
    VE_SUS_partially_sus_vaccinated = (1/100) * np.array(mydic["VESUSpartiallySusVaccinated"])
    VE_DIS_partially_sus_vaccinated = (1/100) * np.array(mydic["VEDISpartiallySusVaccinated"])
    VE_H_partially_sus_vaccinated = (1/100) * np.array(mydic["VEHpartiallySusVaccinated"])

    return [average_time_between_symptom_onset_and_hospitalization,mean_duration_infectiousness_post_symptoms,
            mean_duration_hospitalization,mean_duration_latent_period,mean_duration_pre_symptomatic_period,
            mean_duration_nat_immunity_after_infection,mean_duration_nat_immunity_after_infection2,
            mean_duration_immunity_waned_vax_hybrid,mean_duration_primary_immunity,mean_duration_hybrid_immunity,
            mean_duration_booster_immunity,mean_duration_boosted_hybrid_immunity,prop_symptomatic_infection,
            relative_infectiousness_asymptomatic_infection,relative_infectiousness_hospitalized_infection,
            relative_infectiousness_pre_symptomatic_infection,relative_susceptibility,
            VE_SUS_partially_sus, VE_DIS_partially_sus, VE_H_partially_sus,
            VE_SUS_partially_sus_vaccinated, VE_DIS_partially_sus_vaccinated, VE_H_partially_sus_vaccinated]

def input_function(myjson_file):
    default_params, initial_conditions_params, location_params, vaccine_Params, vaccine_effectiveness_params = get_info_from_frontEnd(myjson_file)

    ##################################    LOCATION PARAMETERS     ##########################################
    [region_name, region_code, region_pop, endDate, R0, social_distancing_multipliers, startDate] = location_params

    ################################## VACCINATION PARAMETERS     ###########################################
    [VE_SUS_primary, VE_DIS_primary, VE_H_primary, VE_SUS_booster, VE_DIS_booster, VE_H_booster] = vaccine_effectiveness_params

    [num_vaccines_available_primary, num_vaccines_available_pt_of_view_vaccinated,
     vaccination_startDates_primary, vaccination_startDates_booster,
     distribution_matrix_primary_series, distribution_list_boosters_pt_of_view_vaccinated,
     vaccination_rates_primary, vaccination_rates_booster_list_pt_of_view_vaccinated,
     num_doses_per_day_primary, num_doses_per_day_booster_list_pt_of_view_vaccinated] = vaccine_Params
    # num_doses_per_day = np.divide(num_doses, vaccination_rates)
    numBoostersAvailable_for_V1_B, numBoostersAvailable_for_V2_B, numBoostersAvailable_for_V3_B = num_vaccines_available_pt_of_view_vaccinated
    distributionPercentageMatrix_for_V1_B, distributionPercentageMatrix_for_V2_B, distributionPercentageMatrix_for_V3_B = distribution_list_boosters_pt_of_view_vaccinated


    #convert times into numbers
    tfinal = (endDate - startDate) / np.timedelta64(1, 'D')
    # print(tfinal)
    vaccination_start_days_primary = np.zeros(3)
    vaccination_start_days_booster = np.zeros(3)
    for ivals in range(3):
        vaccination_start_days_primary[ivals] = (vaccination_startDates_primary[ivals] - startDate) / np.timedelta64(1, 'D')
        vaccination_start_days_booster[ivals] = (vaccination_startDates_booster[ivals] - startDate) / np.timedelta64(1,
                                                                                                                     'D')

    # print(vaccination_start_days)
    # ######## load the data that we will need to run the model
    myURL = os.path.dirname(__file__) # ''#'HungMatrajt/'
    numAgeGroups = len(region_pop)

    #get the three letter region name to load matrices:
    # myregion = region_name[region]



    ############ compute the matrix under current social distancing interventions:

    matNew = contact_matrix_weighted_by_social_distancing(myURL, social_distancing_multipliers, region_code, numAgeGroups)

    ############ compute the matrix without any social distancing interventions (used later to comptue beta):
    matAll = contact_matrix_weighted_by_social_distancing(myURL,np.ones(4), region_code, numAgeGroups)

    ##################################    DEFAULT PARAMETERS     ##########################################
    [average_time_between_symptom_onset_and_hospitalization,
     mean_duration_infectiousness_post_symptoms,
     mean_duration_hospitalization,
     mean_duration_latent_period,
     mean_duration_pre_symptomatic_period,
     mean_duration_nat_immunity_after_infection,
     mean_duration_nat_immunity_after_infection2,
     mean_duration_immunity_waned_vax_hybrid,
     mean_duration_primary_immunity,
     mean_duration_hybrid_immunity,
     mean_duration_booster_immunity,
     mean_duration_boosted_hybrid_immunity,
     prop_symptomatic_infection,
     relative_infectiousness_asymptomatic_infection,
     relative_infectiousness_hospitalized_infection,
     relative_infectiousness_pre_symptomatic_infection,
     relative_susceptibility,
     VE_SUS_partially_sus, VE_DIS_partially_sus, VE_H_partially_sus,
     VE_SUS_partially_sus_vaccinated, VE_DIS_partially_sus_vaccinated, VE_H_partially_sus_vaccinated
     ] = default_params
    #set the default parameters here


    sigma_base = 1 / average_time_between_symptom_onset_and_hospitalization
    sigma = sigma_base * np.ones(numAgeGroups)
    #reduction in susceptibility by age
    red_sus = np.array(relative_susceptibility) #assumed all ages have equal susceptibility to infection

    #fraction of symptomatic infections stratified by age
    frac_sym = prop_symptomatic_infection
    oneMinusFracSym = np.ones(numAgeGroups) - frac_sym  #needed later to pass to the model

    #reduction of infectiousness:
    redA = relative_infectiousness_asymptomatic_infection  # reduction of infectiousness for asymptomatic infections
    redH = relative_infectiousness_hospitalized_infection  # reduction of infectiousness for hospitalized infections
    redP = relative_infectiousness_pre_symptomatic_infection  # reduction of infectiousness for pre-symp infections

    #transition rates:
    durI = mean_duration_infectiousness_post_symptoms  # duration of infectiousness after developing symptoms
    durP = mean_duration_pre_symptomatic_period  # duration of infectiousness before developing symptoms
    durA = durI + durP  # the duration of asymptomatic infections is equal to that of symptomatic infections
    gammaA = 1 / durA  # recovery rate for asymptomatic
    gammaI = 1 / durI  # recovery rate for symptomatic infections (not hospitalized)
    gammaP = 1 / durP  # transition rate fromm pre-symptomatic to symptomatic
    gammaE = 1 / mean_duration_latent_period  # transition rate from exposed to infectious
    gammaH = 1 / mean_duration_hospitalization #recovery rate for hospitalized (non ICU)

    #waning immunity for 1st infection:

    gammaR = 1 / mean_duration_nat_immunity_after_infection
    gammaRA = 1 / mean_duration_nat_immunity_after_infection
    gammaRH = 1 / mean_duration_nat_immunity_after_infection


    # waning time for unvaccinated people after second infection
    durRP = mean_duration_nat_immunity_after_infection2
    gammaRP = 1 / durRP
    gammaRAP = 1 / durRP
    gammaRHP = 1 / durRP

    #waning immunity for waned hybrid immunity (waned vaccinated + infected) (assumed to be equal for all vaccines)
    gammaRPV = 1/mean_duration_immunity_waned_vax_hybrid
    gammaRAPV = 1/mean_duration_immunity_waned_vax_hybrid
    gammaRHPV = 1/mean_duration_immunity_waned_vax_hybrid

    

    #waning immunity for hybrid immunity (vaccinated + infected) for each vaccine type
    dur_hybrid_immunity = np.array(mean_duration_hybrid_immunity) #assumed to be 8 months
    gammaRV = np.divide(1, dur_hybrid_immunity)
    gammaRAV = np.divide(1, dur_hybrid_immunity)
    gammaRHV = np.divide(1, dur_hybrid_immunity)

    # waning immunity for boosted + recovered for each vaccine type
    dur_boosted_hybrid_immunity = np.array(mean_duration_boosted_hybrid_immunity)
    gammaRB = np.divide(1, dur_boosted_hybrid_immunity)
    gammaRAB = np.divide(1, dur_boosted_hybrid_immunity)
    gammaRHB = np.divide(1, dur_boosted_hybrid_immunity)

    # waning for vaccine-induced immunity
    gammaSV = np.divide(1, mean_duration_primary_immunity)
    gammaSB = np.divide(1, mean_duration_booster_immunity)


    #load mortality data
    file_path = os.path.join(myURL, 'Data/mortality_rates/',  'mortality_rate_5' + '_' + region_code + '.pickle')
    f = open(file_path,'rb')

    # f = open(myURL + 'Data/mortality_rates/' + 'mortality_rate_5' + '_' + region_code + '.pickle','rb')
    
    death_rate = pickle.load(f)  # mortality rate per group

    f.close()


    # load hospitalized fraction per group
    file_path = os.path.join(myURL, 'Data/hospitalization_rates/', 'hosp_rate_5' + '_' + region_code + '.pickle')
    f = open(file_path,'rb')


    # f = open(myURL + 'Data/hospitalization_rates/' + 'hosp_rate_5' + '_' + region_code + '.pickle','rb')

    hosp_rate = pickle.load(f)
    f.close()
    # print('hosp rates', hosp_rate)
    oneMinusFracHosp = np.ones(numAgeGroups) - hosp_rate


    #### compute beta with all these parameters #########
    beta = find_beta_System1(matAll, frac_sym, gammaA, gammaE, gammaH, gammaI, gammaP,
                             hosp_rate, oneMinusFracHosp, sigma, redA, redH, redP, red_sus, R0, region_pop)
    # print(beta)
    ###############################    VACCINE EFFECTIVENESS PARAMETERS     ########################################
    #compute the VE_SYMP based on the VE_DIS:
    VE_SYMP_partially_sus = computeVE_P_1d(VE_SUS_partially_sus, VE_DIS_partially_sus)
    VE_SYMP_partially_sus_vaccinated = computeVE_P_1d(VE_SUS_partially_sus_vaccinated, VE_DIS_partially_sus_vaccinated)
    VE_SYMP_primary = computeVE_P(VE_SUS_primary, VE_DIS_primary)
    VE_SYMP_booster = computeVE_P(VE_SUS_booster, VE_DIS_booster)

    VE_HOSP_cond_partially_sus = computeVE_HOSP_cond2_1d(VE_H_partially_sus, VE_DIS_partially_sus)
    VE_HOSP_cond_partially_sus_vaccinated = computeVE_HOSP_cond2_1d(VE_H_partially_sus_vaccinated, VE_DIS_partially_sus_vaccinated)
    VE_HOSP_cond_primary = computeVE_HOSP_cond2(VE_H_primary, VE_DIS_primary)
    VE_HOSP_cond_booster = computeVE_HOSP_cond2(VE_H_booster, VE_DIS_primary)

    #define all the 1 - VE for ODE input:
    ##VE_SUS
    oneMinus_VESUS_partially_sus = 1 - VE_SUS_partially_sus
    oneMinus_VESUS_partially_sus_vaccinated = 1 - VE_SUS_partially_sus_vaccinated
    oneMinus_VESUS_primary = 1 - VE_SUS_primary
    oneMinus_VESUS_booster = 1 - VE_SUS_booster

    ##VE_SYMP
    oneMinus_VESYMP_partially_sus = frac_sym * (1 - VE_SYMP_partially_sus)
    oneMinus_VESYMP_partially_sus_vaccinated = frac_sym * (1 - VE_SYMP_partially_sus_vaccinated)
    oneMinus_VESYMP_primary = np.array([frac_sym * (1 - VE_SYMP_primary[0]), frac_sym * (1 - VE_SYMP_primary[1]),
                                        frac_sym * (1 - VE_SYMP_primary[2])])
    oneMinus_VESYMP_booster = np.array([frac_sym * (1 - VE_SYMP_booster[0]), frac_sym * (1 - VE_SYMP_booster[1]),
                                        frac_sym * (1 - VE_SYMP_booster[2])])

    #define the 1 - oneMinus
    oneMinus_oneMinus_VESYMP_partially_sus = 1 - oneMinus_VESYMP_partially_sus
    oneMinus_oneMinus_VESYMP_partially_sus_vaccinated = 1 - oneMinus_VESYMP_partially_sus_vaccinated
    oneMinus_oneMinus_VESYMP_primary = 1 - oneMinus_VESYMP_primary
    oneMinus_oneMinus_VESYMP_booster = 1 - oneMinus_VESYMP_booster

    ##VE_HOSP_COND:
    oneMinus_VE_HOSP_cond_partially_sus = hosp_rate * (1 - VE_HOSP_cond_partially_sus)
    oneMinus_VE_HOSP_cond_partially_sus_vaccinated = hosp_rate * (1 - VE_HOSP_cond_partially_sus_vaccinated)
    oneMinus_VE_HOSP_cond_primary = np.array([hosp_rate * (1 - VE_HOSP_cond_primary[0]),
                                              hosp_rate * (1 - VE_HOSP_cond_primary[1]),
                                              hosp_rate * (1 - VE_HOSP_cond_primary[2])])
    oneMinus_VE_HOSP_cond_booster = np.array([hosp_rate * (1 - VE_HOSP_cond_booster[0]),
                                              hosp_rate * (1 - VE_HOSP_cond_booster[1]),
                                              hosp_rate * (1 - VE_HOSP_cond_booster[2])])


    #define the 1 - oneMinus
    oneMinus_oneMinus_VE_HOSP_cond_partially_sus = 1 - oneMinus_VE_HOSP_cond_partially_sus
    oneMinus_oneMinus_VE_HOSP_cond_partially_sus_vaccinated = 1 - oneMinus_VE_HOSP_cond_partially_sus_vaccinated
    oneMinus_oneMinus_VE_HOSP_cond_primary = 1 - oneMinus_VE_HOSP_cond_primary
    oneMinus_oneMinus_VE_HOSP_cond_booster = 1 - oneMinus_VE_HOSP_cond_booster

    current_frac_infections, previous_frac_infections, previous_frac_primary_vaccinated,\
    previous_frac_boosted = initial_conditions_params
    init_cond = computeInitialConditions2(region_pop, current_frac_infections, frac_sym, hosp_rate,
                             previous_frac_boosted, previous_frac_infections,
                             previous_frac_primary_vaccinated, prop_waned=0)
    myind = np.where(init_cond < 0)
    init_cond[myind] = 0

    # # ###### PRIMARY VACCINATION SETTINGS:
    # # # #compute the time partition with primary vaccines to run the model
    tEnd_primary = set_time_vaccine_simulation(vaccination_start_days_primary, tfinal, num_vaccines_available_primary,
                                        num_doses_per_day_primary)


    # # # ####### BOOSTER SETTINGS:
    numVaccinesPerGroupPerDayV1_B = num_doses_per_day_booster_list_pt_of_view_vaccinated[0]
    numVaccinesPerGroupPerDayV2_B = num_doses_per_day_booster_list_pt_of_view_vaccinated[1]
    numVaccinesPerGroupPerDayV3_B = num_doses_per_day_booster_list_pt_of_view_vaccinated[2]



    tEndV1_B = set_time_vaccine_simulation(vaccination_start_days_booster, tfinal, numBoostersAvailable_for_V1_B, numVaccinesPerGroupPerDayV1_B)
    tEndV2_B = set_time_vaccine_simulation(vaccination_start_days_booster, tfinal, numBoostersAvailable_for_V2_B, numVaccinesPerGroupPerDayV2_B)
    tEndV3_B = set_time_vaccine_simulation(vaccination_start_days_booster, tfinal, numBoostersAvailable_for_V3_B, numVaccinesPerGroupPerDayV3_B)

    paramsRunModel = [beta, matNew, death_rate, frac_sym, gammaA, gammaE, gammaH, gammaI, gammaP, gammaR,
                      gammaRA, gammaRH, gammaRP, gammaRAP, gammaRHP, gammaRPV, gammaRAPV, gammaRHPV, gammaRV, gammaRAV,
                      gammaRHV, gammaRB, gammaRAB, gammaRHB,gammaSV, gammaSB, hosp_rate, numAgeGroups, oneMinusFracSym, oneMinusFracHosp,
                      redA, redH, redP, red_sus, sigma, region_pop, #36
                  oneMinus_VESUS_partially_sus,
                  oneMinus_VESYMP_partially_sus, oneMinus_oneMinus_VESYMP_partially_sus,
                  oneMinus_VE_HOSP_cond_partially_sus, oneMinus_oneMinus_VE_HOSP_cond_partially_sus, #41
                  oneMinus_VESUS_partially_sus_vaccinated,
                  oneMinus_VESYMP_partially_sus_vaccinated,oneMinus_oneMinus_VESYMP_partially_sus_vaccinated,
                  oneMinus_VE_HOSP_cond_partially_sus_vaccinated, oneMinus_oneMinus_VE_HOSP_cond_partially_sus_vaccinated,
                  oneMinus_VESUS_primary,
                  oneMinus_VESYMP_primary, oneMinus_oneMinus_VESYMP_primary,
                  oneMinus_VE_HOSP_cond_primary, oneMinus_oneMinus_VE_HOSP_cond_primary, #51
                  oneMinus_VESUS_booster,
                  oneMinus_VESYMP_booster, oneMinus_oneMinus_VESYMP_booster,
                  oneMinus_VE_HOSP_cond_booster,oneMinus_oneMinus_VE_HOSP_cond_booster, #56
                  tEnd_primary, tEndV1_B, tEndV2_B, tEndV3_B]


    result, tspan = runVaccination_model(init_cond, paramsRunModel,
                                         vaccination_start_days_primary,
                                         vaccination_start_days_booster[0]*np.ones(3), vaccination_start_days_booster[1]*np.ones(3), vaccination_start_days_booster[2]*np.ones(3),
                                         tEnd_primary, tEndV1_B, tEndV2_B, tEndV3_B, tfinal,
                                         vaccination_rates_primary,
                                         vaccination_rates_booster_list_pt_of_view_vaccinated[0],
                                         vaccination_rates_booster_list_pt_of_view_vaccinated[1],
                                         vaccination_rates_booster_list_pt_of_view_vaccinated[2])

    # print(tspan[::2])
    # # print(np.shape(result))
    # QOI = calculateMetrics(death_rate, numAgeGroups, result)
    [[peakHosp, cumDeaths], epiCurves] = calculateMetricsAndEpidemicCurves(death_rate, numAgeGroups, result)
    [totalInf, totalSympInf, hosp, deaths] = (epiCurves)
    # myResMat = np.concatenate((totalInf, totalSympInf, hosp, deaths), axis=1)
    myresultsList =  [['Day',
                          'InfectionsG1', 'InfectionsG2', 'InfectionsG3', 'InfectionsG4', 'InfectionsG5',
                          'Symptomatic_infectionsG1', 'Symptomatic_infectionsG2', 'Symptomatic_infectionsG3', 'Symptomatic_infectionsG4', 'Symptomatic_infectionsG5',
                          'HospitalizationsG1', 'HospitalizationsG2', 'HospitalizationsG3', 'HospitalizationsG4', 'HospitalizationsG5',
                          'DeathsG1', 'DeathsG2', 'DeathsG3', 'DeathsG4', 'DeathsG5']]
    for tvals in range(len(totalInf[:,0])):
        temp = [tvals, totalInf[tvals, 0], totalInf[tvals, 1], totalInf[tvals, 2], totalInf[tvals, 3], totalInf[tvals, 4],
                totalSympInf[tvals, 0], totalSympInf[tvals, 1], totalSympInf[tvals, 2],
                totalSympInf[tvals, 3], totalSympInf[tvals, 4],
                hosp[tvals, 0], hosp[tvals, 1], hosp[tvals, 2], hosp[tvals, 3], hosp[tvals, 4],
                deaths[tvals, 0], deaths[tvals, 1], deaths[tvals, 2], deaths[tvals, 3], deaths[tvals, 4]]
        myresultsList.append(temp)

    output = {
        'peakHospitalization': np.round(peakHosp),
        'cumulativeNumberOfDeaths': np.round(cumDeaths),
        'infectionTimeSeries': [totalInf[:, 0], totalInf[:, 1], totalInf[:, 2], totalInf[:, 3], totalInf[:, 4]],
        'symptomaticInfectionTimeSeries': [totalSympInf[:, 0], totalSympInf[:, 1], totalSympInf[:, 2],
                                             totalSympInf[:, 3], totalSympInf[:, 4]],
        'hospitalizationTimeSeries': [hosp[:, 0], hosp[:, 1], hosp[:, 2], hosp[:, 3], hosp[:, 4]],
        'deathTimeSeries': [deaths[:, 0], deaths[:, 1], deaths[:, 2], deaths[:, 3], deaths[:, 4]],
        'resultMatrix': myresultsList
    }



    # print("metrics:", QOI)
    #epiCurves  = totalInf, totalSympInf, hosp, deaths
    return output



