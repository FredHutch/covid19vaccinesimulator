# Author: Imelda Trejo
# Some functions were adpted from Laura Matrajt work:
# https://github.com/lulelita/vaccine_optimization/blob/master/coronavirusMainFunctionsP.py
# Day created: April 21, 2022
# Last updated day: July 27th, 2022


import numpy as np
import os
import sys
from scipy.integrate import odeint
import pickle
# from inputs import region_name


def calculateMetricsAndEpidemicCurves(deathRate, numAgeGroups, timeSeries):
    '''Takes a time series from coronavirusODE_withVaccines (109 classes * 5 age groups)
    and computes metrics of disease burden.
    :param deathRate: 1x5 vector. The element (U)i is the mortality rate of group i
    :param numAgeGroups: total age group 5.
    :param timeSeries: 1x540 vector
    :return: number metrics of disease burden (total infections, symp infections, hospitalizations, and deaths)
    '''

    # reshape the cumulative time series into the 109 classes that are subdivided in 9 sub-classes
    # out = (timeSeries[:, ]).reshape(109, numAgeGroups)
    q = [2, 4, 5]  # index for asymtomatic, symptomatic, and hospitalized classes

    mysize = np.shape(timeSeries)[0]
    allInfections, symptomaticInfections, hosp, deaths = np.zeros((mysize, 5)), np.zeros((mysize, 5)), np.zeros((mysize, 5)), np.zeros((mysize, 5))

    # for jvals in range(5):
    for t in range(mysize):
        temp = timeSeries[t, :].reshape((109,5))
        for kvals in range(9):
            symptomaticInfections[t, :] += temp[4 + 12*kvals, :] + temp[5 + 12*kvals, :]
            allInfections[t, :] += symptomaticInfections[t, :] + np.sum(temp[2 + 12*kvals, :])
            hosp[t, :] += temp[5 + 12*kvals, :]
            deaths[t, :] = temp[-1, :]


    totalDeaths = np.sum(deaths[-1, :])
    peakHosp = np.max(hosp)
    epiCurves = [np.round(allInfections[::2, :]), np.round(symptomaticInfections[::2, :]),
                                                           np.round(hosp[::2, :]), np.round(deaths[::2, :])]

    return [[np.round(peakHosp), np.round(totalDeaths)], epiCurves]

def find_beta_System1(C, frac_sym, gammaA, gammaE, gammaH, gammaI, gammaP, hosp_rate,
                      one_minus_hosp_rate, sigma, redA, redH, redP, red_sus,  R0, totalPop):
    '''
    Compute the value of beta for the model coronavirusODE_withVaccines using
    the 1st system of eqs (60 eqs) and applying Van den Drieshhche method.
    :param C: contact matrix 5x5 from Prem Kiesha, using all location
    :param frac_sym: 1x5 vector
    :param gammaA, gammaE, gammaH, gammaI, gammaP:
    :param hosp_rate: 1x5 vector
    :param one_minus_hosp_rate: 1x5 vector
    :param sigma: mean time in days from sypmtom onset to hospipatizazion
    :param redA,redP, redH: a fraction number. Relative infectiousness of asymptomatics, pre-symptomatic, and hospitalized infections
    :param red_sus: 1x5 vector, reduction of susceptibility parameter
    :param R0: a positive number
    :param totalPop: 1x5 vector with the total population of each group
    :return: a real number beta, the disease transmission
    '''
    [n1, n2] = np.shape(C)

    # create F
    N = np.sum(totalPop)
    Z = np.zeros((n1, n1))
    C1 = np.zeros((n1, n1))
    for ivals in range(n1):
        for jvals in range(n1):
            C1[ivals, jvals] = red_sus[ivals] * C[ivals, jvals] * totalPop[ivals]/totalPop[jvals]


    #create F by concatenating different matrices:
    F1 = np.concatenate((Z, redA*C1, redP*C1, C1, redH*C1), 1)
    F2 = np.zeros((4*n1, 5*n1))

    F = np.concatenate((F1, F2), 0)

    #create V
    VgammaE = np.diag(gammaE * np.ones(n1))
    VgammaA = np.diag(gammaA * np.ones(n1))
    VgammaP = np.diag(gammaP * np.ones(n1))
    VgammaI = np.diag(gammaI*one_minus_hosp_rate+sigma*hosp_rate)
    #print("infection sub matrix",VgammaI)
    VgammaH = np.diag(gammaH * np.ones(n1))

    Vsub1 = np.diag(-(np.ones(n1)-frac_sym) * gammaE)
    Vsub2 = np.diag(-(frac_sym) * gammaE)

    Vsub3 = np.diag(- gammaP * np.ones(n1))
    Vsub4 = np.diag(- sigma * np.ones(n1))
    # print(V)

    V1 = np.concatenate((VgammaE, Z, Z, Z, Z), 1)
    V2 = np.concatenate((Vsub1, VgammaA, Z, Z, Z), 1)
    V3 = np.concatenate((Vsub2, Z, VgammaP, Z, Z), 1)
    V4 = np.concatenate((Z, Z, Vsub3, VgammaI, Z), 1)
    V5 = np.concatenate((Z, Z, Z,Vsub4, VgammaH), 1)

    V = np.concatenate((V1, V2, V3, V4, V5), 0)
    #print(np.linalg.inv(V))

    myProd = np.dot(F, np.linalg.inv(V))
    #print(myProd)
    myEig = np.linalg.eig(myProd)
    #print(myEig)
    largestEig = np.max(myEig[0])
    if largestEig.imag == 0.0:

        beta = R0 / largestEig.real
        #print('beta', beta)
        return beta
    else:
        print(largestEig)
        raise Exception('largest eigenvalue is not real')


def contact_matrix_weighted_by_social_distancing(myURL,d,myregion,numGroups):
    '''Compute the contact matrix weighted by the social distancing parameter d.
    :param myURL: path to read the contact matrices data
    :param d: vector of 1x4. The element d_i is the social distancing percentage parameter at location[i]
    :param region: name of the region
    :param numGroups:  numbers of group as definded in the contact matrix
    :return: NewMat a matrix of dimension numGroups times numGroups
    '''
    location = np.array(["home", "work", "school", "others"])
    NewMat=np.zeros((numGroups,numGroups))
    no_reduction_social_distancing=np.ones(len(location))

    if np.array_equal(no_reduction_social_distancing,d)==True:
        file_path = os.path.join(myURL, 'Data/contact_matrices_data/', 'contact_grp5_' + 'all_' + myregion + '.pickle')
        f = open(file_path,'rb')
        # f = open(myURL + 'Data/contact_matrices_data/' + 'contact_grp5_' + 'all_' + myregion + '.pickle','rb')
        NewMat = pickle.load(f)
        f.close()
        #print("no social distancing")
    else:
        for i in range(len(location)):
            file_path = os.path.join(myURL, 'Data/contact_matrices_data/', 'contact_grp5_' + location[i] + '_' + myregion + '.pickle')
            f = open(file_path,'rb')

            # f = open(myURL + 'Data/contact_matrices_data/' + 'contact_grp5_' + location[i] + '_' + myregion + '.pickle', 'rb')
            MyMat = pickle.load(f)
            f.close()
            NewMat=NewMat+d[i]*MyMat
    return NewMat


def theta(t, t1, S, num_vaccines):
    '''
    Compute the instantaneous vaccination rate of model coronavirusODE_withVaccines.
    It is a discontinuous function to the left of t1.
    :param t: intantaneous time
    :param t1: end of vaccination
    :param S: 1x5 vector. State variable at time t stratified by age.
    :param num_vaccines: number of vaccines available per day
    :return: 1x5 vector with the vaccination rate
    '''
    ToVaccinatePerDay = np.zeros(len(S))
    for i in range(len(S)):
        if ((t<=t1) & (S[i] > 0)):
            #print(t)
            ToVaccinatePerDay[i] = np.minimum(num_vaccines[i], S[i])
    return ToVaccinatePerDay


def set_time_vaccine_simulation(tStart, t_final, numVaccinesAvailable, numDosesPerDay):
    '''
    Compute the number of days to vaccinate people with a vaccine type 1, 2, and 3.
    :param tStart: 1x3 vector st:  (st)j time to start vaccination with vaccine type j
    :param t_final: positve integer number. Horizon time.
    :param numVaccinesAvailable: 1x3 vector:  (x)j number of vaccines available of vaccine type j.
    :param numDosesPerDay: vector of 1x3: (r)j number of vaccines type j to be administered per day
    :return:
    '''
    numV = len(tStart)  # number of vaccine types: V1, V2, V3, ..
    numDaysToUseVaccine = np.zeros(numV)
    tEnd = np.zeros(numV)  # final time to use vaccine

    # compute the ending time for each vaccine type
    for j in range(numV):

        if numDosesPerDay[j] == 0:
            numDaysToUseVaccine[j] = 0
        else:
            numDaysToUseVaccine[j] = numVaccinesAvailable[j] / numDosesPerDay[j]

        if numDaysToUseVaccine[j] < 0:
            print('problem: number of days to use vaccine is negative')
            sys.exit()

    # set  vaccination ending day
    for j in range(numV):
        if tStart[j] < 0:
            print('problem: starting time of vaccination is negative')
            sys.exit()
        if numDaysToUseVaccine[j] > 0:
            tEnd[j] = tStart[j] + numDaysToUseVaccine[j]  # day end of vaccination

    # Verify that the time horizon is enough to implement the model
    tEndVmax = max(tEnd)

    if t_final <= tEndVmax:
        print('problem: increase the time horizon, at least' +  str(tEndVmax + 1) + 'days are needed to simulate the ' +
                'vaccination campaign at that rate')
        # sys.exit()

    return tEnd


def findVaccinationRateForEachElegibleClasses(FracTovaccinateFulldose, numVaccinesPerDayPerGroupPerType):
    '''
    Compute the vaccination rate for each eligible class with a given vaccine type.
    The vaccine can be booster or primary series of type 1, 2, or 3, it is encapsulated in numVaccinesPerDayPerGroupPerType.
    :param FracTovaccinateFulldose: List of 14 vectors, U, of size 1x5. (U)i fraction of people from class U and group i
    to vaccinate with primary series.
    :param numVaccinesPerDayPerGroupPerType: vector of 1x5, U. (U)i is the vaccination rate for people from group i
    with primary series vaccine of a given vaccine type 1,2, or 3.
    :return:
    '''
    dim=np.shape(FracTovaccinateFulldose)
    numElegibleClasses, numGroups = dim[0],dim[1]  #total of eligible classes and total of groups
    #print(numElegibleClasses,numGroups)
    #print(numVaccinesPerDayPerGroupPerType)
    vaccinationRate = np.zeros((numElegibleClasses, numGroups))
    for k in range(numElegibleClasses):
        vaccinationRate[k] = np.multiply(FracTovaccinateFulldose[k], numVaccinesPerDayPerGroupPerType)
    #print(np.sum(vaccinationRate[:,1]))
    return vaccinationRate


def findFractionSeekersFullDose(y, numAgeGroups):
    """ The function computes the relative fraction of all model-eligible classes to be vaccinated
     with full dose per group. Eligible classes: susceptible, exposed, asymptomatic infected,
     pre-symptomatic infected, and all recovered classes for each unvaccinated-group with full dose.
     The corresponding fractions of vaccines for exposed, asymptomatic infected, and pre-symptomatic
     infected classes are set zeros. As for those classes the vaccines did not have any effect on them.
    This is valid ONLY for coronavirusODE_withVaccines equations assuming NO ONE has been vaccinated before.
    :param numAgeGroups: number of age groups
    :param y: the state vector at the beginning of each vaccination campaign, it has 109*numAgeGroups elements.
    :return: A list of 14 elements. Each element is a vector U of 1x5. The element (u)i is the fraction
    of people to vaccinate with primary series for the class U and group i.
    """
    temp = np.reshape(y, (109, numAgeGroups))
    relativeTotal = (temp[0, :] +  # susceptibles
                     temp[1, :] +  # exposed
                     temp[2, :] +  # asymptomatic infected
                     temp[3, :] +  # pre-symptomatic infected
                     temp[6, :] +  # removed symptomatic with half-waning-immunity time (Rec1)
                     temp[7, :] +  # removed asymptomatic with half-waning-immunity time
                     temp[8, :] +  # removed hospitalized with half-waning-immunity time
                     temp[9, :] +  # removed symptomatic within the last stage of their waning immunity
                     temp[10, :] +  # removed asymptomatic within the last stage of their waning immunity
                     temp[11, :] +  # removed hospitalized within the last stage of their waning immunity
                     temp[12, :] +  # susceptible partially protected
                     temp[13, :] +  # exposed partially protected
                     temp[14, :] +  # asymptomatic infected partially protected
                     temp[15, :] +  # pre-symptomatic infected partially protected
                     temp[18, :] +  # removed symptomatic partially protected with half-waning-immunity time
                     temp[19, :] +  # removed asymptomatic partially protected with half-waning-immunity time
                     temp[20, :] +  # removed hospitalized partially protected with half-waning-immunity time
                     temp[21,
                     :] +  # removed symptomatic partially protected withing the last stage of their waning immunity
                     temp[22,
                     :] +  # removed symptomatic partially protected within the last stage of their waning immunity
                     temp[23, :]
                     # removed hospitalized partially protected within the last stage of their waning immunity
                     )

    fractionSus = np.divide(temp[0, :], relativeTotal, out=np.zeros_like(temp[0, :]), where=relativeTotal != 0)
    fractionRec = np.divide(temp[6, :], relativeTotal, out=np.zeros_like(temp[6, :]), where=relativeTotal != 0)
    fractionRecAsym = np.divide(temp[7, :], relativeTotal, out=np.zeros_like(temp[7, :]), where=relativeTotal != 0)
    fractionRecHosp = np.divide(temp[8, :], relativeTotal, out=np.zeros_like(temp[8, :]), where=relativeTotal != 0)
    fractionRec2 = np.divide(temp[9, :], relativeTotal, out=np.zeros_like(temp[9, :]), where=relativeTotal != 0)
    fractionRecAsym2 = np.divide(temp[10, :], relativeTotal, out=np.zeros_like(temp[10, :]), where=relativeTotal != 0)
    fractionRecHosp2 = np.divide(temp[11, :], relativeTotal, out=np.zeros_like(temp[11, :]), where=relativeTotal != 0)

    # for partially protected classes
    fractionSusP = np.divide(temp[12, :], relativeTotal, out=np.zeros_like(temp[12, :]), where=relativeTotal != 0)
    fractionRecP = np.divide(temp[18, :], relativeTotal, out=np.zeros_like(temp[18, :]), where=relativeTotal != 0)
    fractionRecAsymP = np.divide(temp[19, :], relativeTotal, out=np.zeros_like(temp[19, :]), where=relativeTotal != 0)
    fractionRecHospP = np.divide(temp[20, :], relativeTotal, out=np.zeros_like(temp[20, :]), where=relativeTotal != 0)
    fractionRec2P = np.divide(temp[21, :], relativeTotal, out=np.zeros_like(temp[21, :]), where=relativeTotal != 0)
    fractionRecAsym2P = np.divide(temp[22, :], relativeTotal, out=np.zeros_like(temp[22, :]), where=relativeTotal != 0)
    fractionRecHosp2P = np.divide(temp[23, :], relativeTotal, out=np.zeros_like(temp[23, :]), where=relativeTotal != 0)

    FracToVaccinateWithFullDose = [fractionSus, fractionRec, fractionRecAsym, fractionRecHosp,
                                   fractionRec2, fractionRecAsym2, fractionRecHosp2,
                                   fractionSusP, fractionRecP, fractionRecAsymP, fractionRecHospP,
                                   fractionRec2P, fractionRecAsym2P, fractionRecHosp2P]
    return FracToVaccinateWithFullDose


def findFractionSeekersBoosters(y, numAgeGroups, VType):
    """compute the relative fraction of  all model-eligible classes to be vaccinated with booster
    during each vaccination campaign with vaccines type 1, vaccines type 2, and vaccines type 3.
    The relative fraction is done among vaccinated susceptible, vaccinated exposed, vaccinated asymptomatic infected,
    vaccinated pre-symptomatic infected, and vaccinated recovered classes with full dose of type k, k=1,2,3,
    and for each age group and their corresponding partially protected-unvaccinated classes with boosters.
    This is valid ONLY for coronavirusODE_withVaccines equations assuming NO ONE has been vaccinated before.
    The corresponding fractions of vaccines for exposed, asymtomatic infected, and pre-symptomatic infected
    classes are set zeros. As for those classes the vaccines did not have any  effect on them.
    :param numAgeGroups: number of age groups
    :param y: the state vector at the time of vaccination, it has 109*numAgeGroups elements.
    :param VType: it refers to the booster vaccination campaign for vaccinated people with full dose type 1,2, or 3
    :return: the fraction of eligible classes in each age group """

    temp = np.reshape(y, (109, numAgeGroups))
    if VType == 1:
        k = 3
    if VType == 2:
        k = 4
    if VType == 3:
        k = 5

    relativeTotal = (temp[24, :] +  # susceptible vaccinated with partial protection
                     temp[25, :] +  # exposed vaccinated with partial protection
                     temp[26, :] +  # asymptomatic infected vaccinated with partial protection
                     temp[27, :] +  # pre-symptomatic infected vaccinated with partial protection
                     temp[30, :] +  # removed symptomatic vaccinated partially protected within half-waning-immunity time (RecPV)
                     temp[31, :] +  # removed asymptomatic vaccinated partially protected within half-waning-immunity time
                     temp[32, :] +  # removed hospitalized vaccinated partially protected within half-waning-immunity time
                     temp[33,
                     :] +  # removed symptomatic vaccinated partially protected within the last stage of their waning immunity
                     temp[34,
                     :] +  # removed asymptomatic vaccinated partially protected within the last stage of their waning immunity
                     temp[35,
                     :] +  # removed hospitalized  partially protected within the last stage of their waning immunity
                     temp[(12*k), :] +  # susceptible vaccinated with vaccine # VType
                     temp[(12*k+1), :] +  # exposed vaccinated with vaccine # VType
                     temp[(12*k+2), :] +  # asymptomatic infected vaccinated with vaccine # VType
                     temp[(12*k+3), :] +  # pre-symptomatic infected vaccinated with vaccine # VType
                     temp[(12*k+6),
                     :] +  # removed symptomatic vaccinated with type #1  and within half-waning-immunity time
                     temp[(12*k+7), :] +  # removed asymptomatic vaccinated with vaccine #VType within half-waning-immunity time
                     temp[(12*k+8), :] +  # removed hospitalized vaccinated with vaccine #VType within half-waning-immunity time
                     temp[(12*k+9),
                     :] +  # removed symptomatic with vaccine #VType withing the last stage of their waning immunity
                     temp[(12*k+10),
                     :] +  # removed asymptomatic with vaccine #VType within the last stage of their waning immunity
                     temp[(12*k+11), :]  # removed hospitalized with vaccine #VType within the last stage of their waning immunity
                     )

    # for partially protected classes
    fractionSusPV = np.divide(temp[24, :], relativeTotal, out=np.zeros_like(temp[24, :]), where=relativeTotal != 0)
    # fractionExpoPV = np.zeros(numAgeGroups)
    # fractionAsymPV = np.zeros(numAgeGroups)
    # fractionPreSympPV = np.zeros(numAgeGroups)
    fractionRecPV = np.divide(temp[30, :], relativeTotal, out=np.zeros_like(temp[30, :]), where=relativeTotal != 0)
    fractionRecAsymPV = np.divide(temp[31, :], relativeTotal, out=np.zeros_like(temp[31, :]), where=relativeTotal != 0)
    fractionRecHospPV = np.divide(temp[32, :], relativeTotal, out=np.zeros_like(temp[32, :]), where=relativeTotal != 0)
    fractionRec2PV = np.divide(temp[33, :], relativeTotal, out=np.zeros_like(temp[33, :]), where=relativeTotal != 0)
    fractionRecAsym2PV = np.divide(temp[34, :], relativeTotal, out=np.zeros_like(temp[34, :]), where=relativeTotal != 0)
    fractionRecHosp2PV = np.divide(temp[35, :], relativeTotal, out=np.zeros_like(temp[35, :]), where=relativeTotal != 0)

    # for vaccinated clasess with full dose
    fractionSusV = np.divide(temp[(12*k), :], relativeTotal, out=np.zeros_like(temp[(12*k), :]), where=relativeTotal != 0)
    # fractionExpoV = np.zeros(numAgeGroups)
    # fractionAsymV = np.zeros(numAgeGroups)
    # fractionPreSympV = np.zeros(numAgeGroups)
    fractionRecV = np.divide(temp[(12*k+6), :], relativeTotal, out=np.zeros_like(temp[(12*k+6), :]), where=relativeTotal != 0)
    fractionRecAsymV = np.divide(temp[(12*k+7), :], relativeTotal, out=np.zeros_like(temp[(12*k+7), :]), where=relativeTotal != 0)
    fractionRecHospV = np.divide(temp[(12*k+8), :], relativeTotal, out=np.zeros_like(temp[(12*k+8), :]), where=relativeTotal != 0)
    fractionRec2V = np.divide(temp[(12*k+9), :], relativeTotal, out=np.zeros_like(temp[(12*k+9), :]), where=relativeTotal != 0)
    fractionRecAsym2V = np.divide(temp[(12*k+10), :], relativeTotal, out=np.zeros_like(temp[(12*k+10), :]), where=relativeTotal != 0)
    fractionRecHosp2V = np.divide(temp[(12*k+11), :], relativeTotal, out=np.zeros_like(temp[(12*k+11), :]), where=relativeTotal != 0)

    ToVaccinateWithBooster = [fractionSusPV, fractionRecPV, fractionRecAsymPV, fractionRecHospPV,fractionRec2PV,
                              fractionRecAsym2PV, fractionRecHosp2PV,
                              fractionSusV, fractionRecV, fractionRecAsymV, fractionRecHospV,
                              fractionRec2V, fractionRecAsym2V, fractionRecHosp2V]

    return ToVaccinateWithBooster

def vaccine_rate_all_eligible_classes(y0,t0, tStartV,tStartV1_B, tStartV2_B, tStartV3_B, numVaccinesPerGroupPerDay_V,
                        numVaccinesPerGroupPerDayV1_B,numVaccinesPerGroupPerDayV2_B, numVaccinesPerGroupPerDayV3_B):
    '''
    Sets the rate to vaccinate all eligible state variable, 14 variables, at the beginning of each vaccination campaign.
    :param y0: 1x540 vector. Initial condition for coronavirusODE_withVaccines
    :param tStarV: (tS)j time to start vaccination with “primary series vaccine type j”.
    :param tStartVk_B: (tS)j time to start vaccination with “booster type j” for only those who have been vaccinated
    with “primary series vaccine type k”, k,j=1,2,3.
    :param numVaccinesPerGroupPerDay_V: (a)ji number of “primary series vaccine type j” per day allocated for group i.
    :param numVaccinesPerGroupPerDayVk_B: (a)ji number of “booster type j” per day allocated
    for group i that has been vaccinated with “primary series vaccine type k”, i=1,…,5 and k,j=1,2,3.
    :return: 4 matrices: A1, A2, A3, A4. Each matrix A has size 42x5 and contains the rates for the 14 classes grouped by 5
    age-group to vaccinate with each vaccine type 1, 2, and 3.: (A1)ji rate to vaccinate group i with primary series of
    vaccine type 1, 0<=j<=14, (A1)ji rate to vaccinate group i with primary series of vaccine type 2, 14<=j<=28,
     (A1)ji rate to vaccinate group i with primary series of vaccine type 3, 28<=j<=42. (A2)ji rate to vaccinate
     group i with booster type 1 for those vaccinated with primary series with vaccine type 1, 0<=j<=14.
    (A2)ji rate to vaccinate group i with booster type 2 for those vaccinated with vaccine type 1, 14<=j<=28.
     (A2)ji rate to vaccinate group i with booster type 3 for those vaccinated with primary series with vaccine type 1,
     28<=j<=42. And so on to complete keeping the 9-booster-swapping vaccines.
    '''

    initCond = np.copy(y0)
    dim = np.shape(numVaccinesPerGroupPerDay_V)
    numVtypes, numAgeGroups = dim[0], dim[1]

    vaccinationRateV = [np.zeros((14, numAgeGroups)),np.zeros((14, numAgeGroups)),np.zeros((14, numAgeGroups))]
    # booster vaccine rates for vaccinated with V1 and partially protected-vaccinated
    vaccinationRateBoosters_for_V1W = [np.zeros((14, numAgeGroups)),np.zeros((14, numAgeGroups)),np.zeros((14, numAgeGroups))]
    # booster vaccine rates for vaccinated with V1 and partially protected-vaccinated
    vaccinationRateBoosters_for_V2W = [np.zeros((14, numAgeGroups)),np.zeros((14, numAgeGroups)),np.zeros((14, numAgeGroups))]
    # booster vaccine rates for vaccinated with V1 and partially protected-vaccinated
    vaccinationRateBoosters_for_V3W = [np.zeros((14, numAgeGroups)),np.zeros((14, numAgeGroups)),np.zeros((14, numAgeGroups))]


    for j in range(numVtypes):
        # set number of vaccines for people how are seeking "primary series vaccine"
        if t0 == tStartV[j]:
            #print('initiate vaccination with primary vaccine type', j+1)
            FracEligibleClasses = findFractionSeekersFullDose(initCond, numAgeGroups)
            vaccinationRateV[j] = findVaccinationRateForEachElegibleClasses(FracEligibleClasses,
                                                                                 numVaccinesPerGroupPerDay_V[j])
            #print(vaccinationRateFullDose)

        # set number of vaccines for people how are seeking boosters and have been vaccinated with primary of type 1
        if t0 == tStartV1_B[j]:
            #print('initiate vaccination with booster type', j+1,
            #      'for vaccinated with V1 and partially protected-vaccinated classes')
            FracEligibleClasses = findFractionSeekersBoosters(initCond, numAgeGroups, 1)
            vaccinationRateBoosters_for_V1W[j] = findVaccinationRateForEachElegibleClasses(FracEligibleClasses,
                                                      numVaccinesPerGroupPerDayV1_B[j])
            # print(vaccinationRateBoosters_for_V1W[j])

        # set number of vaccines for people how are seeking boosters and have been vaccinated with primary of type 2
        if t0 == tStartV2_B[j]:
            #print('initiate vaccination with booster type', j+1,
            #      'for vaccinated with V2 and partially protected-vaccinated classes')
            FracEligibleClasses = findFractionSeekersBoosters(initCond, numAgeGroups, 2)
            vaccinationRateBoosters_for_V2W[j] = \
            findVaccinationRateForEachElegibleClasses(FracEligibleClasses,numVaccinesPerGroupPerDayV2_B[j])
            # print(vaccinationRateBoosters_for_V2W[j])

        # set number of vaccines for people how are seeking boosters and have been vaccinated with primary of type 3
        if t0 == tStartV3_B[j]:
            #print('initiate vaccination with booster type', j+1,
            #      'for vaccinated with V3 and partially protected-vaccinated classes')
            FracEligibleClasses = findFractionSeekersBoosters(initCond, numAgeGroups, 3)
            vaccinationRateBoosters_for_V3W[j] = \
            findVaccinationRateForEachElegibleClasses(FracEligibleClasses,
                                                      numVaccinesPerGroupPerDayV3_B[j])
            # print("rate for Bj from V3", vaccinationRateBoosters_for_V3W[j])

    return vaccinationRateV, vaccinationRateBoosters_for_V1W, vaccinationRateBoosters_for_V2W, vaccinationRateBoosters_for_V3W

def runVaccination_model(y0, params, tStartV, tStartV1_B, tStartV2_B, tStartV3_B, tEndV, tEndV1_B, tEndV2_B, tEndV3_B,
                         t_final, numVaccinesPerGroupPerDay_V, numVaccinesPerGroupPerDayV1_B,
                         numVaccinesPerGroupPerDayV2_B, numVaccinesPerGroupPerDayV3_B):
    '''At the beginning of each vaccination campaign, it computes and fixes the rate to vaccinate people from
    each eligible state variable, 14 variables. Then uses all these computed rates to complement
    the paramsRunModel and be able to run the model coronavirusODE_withVaccines.
    :param y0: 1x540 vector. Initial condition for coronavirusODE_withVaccines
    :param params: list of 59 elements.
    :param tStartV: (tS)j time to start vaccination with “primary series vaccine type j”.
    :param tStartVk_B: (tS)j time to start vaccination with “booster type j” for those who have been vaccinated
    with “primary series vaccine type k”, k,j=1,2,3.
    :param t_final: time horizon in days
    :param numVaccinesPerGroupPerDay_V: (a)ji number of “primary series vaccine type j” per day allocated for group i.
    :param numVaccinesPerGroupPerDayVk_B: (a)ji number of “booster type j” per day allocated
    for group i that has been vaccinated with “primary series vaccine type k”, i=1,…,5 and k,j=1,2,3.
    :return:
    '''
    initCond = np.copy(y0)
    numEqs = len(y0)
    dim = np.shape(numVaccinesPerGroupPerDay_V)
    numVtypes, numAgeGroups = dim[0], dim[1]
    vaccinationRateZeros = np.zeros((14, numAgeGroups))

    #set up the time partition for allocating vacccines at the beginning of each campaign.
    all_times = np.concatenate((tStartV, tStartV1_B, tStartV2_B, tStartV3_B))
    # number of current vaccine types
    end_ordered_times = np.unique(np.concatenate((tEndV, tEndV1_B, tEndV2_B, tEndV3_B)))
    CurrentNumVaccinesTypes = np.count_nonzero(end_ordered_times)

    if CurrentNumVaccinesTypes == 0:
        paramsODE = [*params,*[vaccinationRateZeros, vaccinationRateZeros, vaccinationRateZeros,
                      vaccinationRateZeros, vaccinationRateZeros, vaccinationRateZeros, vaccinationRateZeros,
                               vaccinationRateZeros,vaccinationRateZeros, vaccinationRateZeros, vaccinationRateZeros,
                      vaccinationRateZeros]]

        mytspan = np.linspace(0, t_final, int(t_final) * 2)
        out = odeint(coronavirusODE_withVaccines_withDeaths, initCond, mytspan, args=(paramsODE,))
        print('Current outbreak without vaccine allocations')

    else:

        # During vaccination campaign
        my_times = np.concatenate(([0], all_times, [t_final]))
        ordered_times = np.unique(my_times) #sorted unique
        chunks = len(ordered_times)
        out = [y0]
        mytspan = np.array([0])
        # print('partition time to allocate vaccines', ordered_times)
        #print(chunks)


        for ivals in range(chunks - 1):
            myStart = ordered_times[ivals]
            myEnd = ordered_times[ivals + 1]
            #print(myStart, myEnd)

            # compute the number of vaccines to be distributed among all eligible classes for each vaccine types: V1, V2,V3.
            rate_V, rate_V1B, rate_V2B, rate_V3B = vaccine_rate_all_eligible_classes(initCond, myStart,
                tStartV, tStartV1_B, tStartV2_B, tStartV3_B, numVaccinesPerGroupPerDay_V, numVaccinesPerGroupPerDayV1_B,
                numVaccinesPerGroupPerDayV2_B, numVaccinesPerGroupPerDayV3_B)

            paramsODE = [*params,*[rate_V[0], rate_V[1], rate_V[2], rate_V1B[0],rate_V1B[1],rate_V1B[2],
                         rate_V2B[0],rate_V2B[1],rate_V3B[2],rate_V3B[0],rate_V3B[1],rate_V3B[2]]]

            # create tspan and run the model when the tspan is not an empty set
            tspan_temp = np.linspace(myStart, myEnd, int(np.ceil(myEnd - myStart)) * 2)
            if len(tspan_temp) > 0:
                # run the ODE
                out_temp, info = odeint(coronavirusODE_withVaccines_withDeaths, initCond, tspan_temp, args=(paramsODE,),
                                        rtol=1e-7,atol=1e-9, full_output=True)
                if info['message'] != 'Integration successful.':
                    print('problems with integration')

                # prepare the initial conditions and parameters for the next chunk
                initCond = out_temp[-1, :].reshape(numEqs)
                out_temp = out_temp[1:]
                mytspan = np.concatenate((mytspan, tspan_temp[1:]))
                out = np.concatenate((out, out_temp), axis=0)

    return out, mytspan



def coronavirusODE_withVaccines_withDeaths(y, t, params):
    """
    Different from coronavirusODE_withVaccines because deaths will be splitted and have their own equations
    coronavirus equations with asymptomatic, pre-symptomatic infected, infected symptomatic hospitalized, infected
    symptomatic not-hospitalized individuals, and its vaccinated corresponding classes.
    Infected individuals in the hospital are assumed not to infect anyone
    USING A MATRIX OF CONTACTS THAT IS Quasi-SYMMETRIC
    The vaccination distribution strategy is defined in 12 vaccination rates.
    :param y: vector of the current state of the system
    :param t: time
    :param params: all the params to run the ODE, defined below

    beta: rate of infection given contact
    C: contact matrix across age groups

    gammaA, gammaE, gammaH, gammaI, gammaP, gammaR, gmmaRA, gammaRH : transition rates out of the asymptomatic, exposed,
    infectious symptomatic hospitalized, infectious symptomatic non-hospitalized, infectious pre-symptomatic,  waining
    rates for recovered symptomatic, asymptomatic and hospitalized classes.


    hospFrac: rates of hospitalization in each age group
    numGroups: number of groups in the simulation
    redA, redH, redP: reduction in the infectiousness for asymptomatic, pre-symptomatic and hospitalized individuals

    totalPop: a vector of size 1x5 with the population in each of the age groups.
    sigma: rate from the transition from infectiousness to hospital

    ###---VE: vaccine efficacy (example):
    1-VESUS1 :  reduction the fraction of susceptibility because the 1st vaccine full dose,
    1-VESYMP1:  reduction fraction of pre-symptomatic individuals because of vaccine 1
    1-VEH1: reduction fraction of hospitalized individuals because of vaccine 1

    theta: function to set the vaccination rate per day per state variable.
    vaccinationRates: 14x5 vector. Vaccination rate per group per vaccines for all elegible clasess.

    :return: the ODE solution. Array with 5 * 109 columns that corresponds to the total number of state variables.
    """


    [beta, C, deathRate, frac_sym, gammaA, gammaE, gammaH, gammaI, gammaP, gammaR, gammaRA, gammaRH, gammaRP, gammaRAP, gammaRHP,
     gammaRPV, gammaRAPV, gammaRHPV,
     gammaRV, gammaRAV, gammaRHV, gammaRB, gammaRAB, gammaRHB, gammaSV, gammaSB, hosp_frac, numGroups,
     one_minus_frac_sym, one_minus_hosp_frac, redA, redH, redP, red_sus, sigma, popGroups,
     one_minus_VESUSP, one_minus_frac_VESYMPP, one_minus_one_minus_frac_VESYMPP,
     one_minus_frac_VEHP, one_minus_one_minus_frac_VEHP, one_minus_VESUSPV, one_minus_frac_VESYMPPV,
     one_minus_one_minus_frac_VESYMPPV,
     one_minus_frac_VEHPV, one_minus_one_minus_frac_VEHPV, one_minus_VESUSV,
     one_minus_frac_VESYMPV, one_minus_one_minus_frac_VESYMPV, one_minus_frac_VEHV, one_minus_one_minus_frac_VEHV,
     one_minus_VESUSB, one_minus_frac_VESYMPB, one_minus_one_minus_frac_VESYMPB,
     one_minus_frac_VEHB, one_minus_one_minus_frac_VEHB, tStartV, tStartV1B, tStartV2B, tStartV3B,
     vaccinationRateFullDoseType1, vaccinationRateFullDoseType2, vaccinationRateFullDoseType3,
     vaccinationRateBoostersType1_for_V1PV, vaccinationRateBoostersType2_for_V1PV,
     vaccinationRateBoostersType3_for_V1PV,
     vaccinationRateBoostersType1_for_V2PV, vaccinationRateBoostersType2_for_V2PV,
     vaccinationRateBoostersType3_for_V2PV,
     vaccinationRateBoostersType1_for_V3PV, vaccinationRateBoostersType2_for_V3PV,
     vaccinationRateBoostersType3_for_V3PV
     ] = params




    temp = np.reshape(y, (109, numGroups))

    # system for unvaccinated

    S = temp[0, :]  # susceptibles
    E = temp[1, :]  # Exposed
    A = temp[2, :]  # Asymptomatic infected
    P = temp[3, :]  # Pre-symptomatic infected
    I = temp[4, :]  # Symptomatic infected
    H = temp[5, :]  # Hospitalized
    R = temp[6, :]  # Recovered symptomatic
    RA = temp[7, :]  # Recovered Asymptomatic
    RH = temp[8, :]  # recovered hospitalized
    R_R = temp[9, :]  # Recovered symptomatic with partial immunity
    RA_R = temp[10, :]  # Recovered Asymptomatic with partial immunity
    RH_R = temp[11, :]  # recovered hospitalized with partial immunity

    S_P = temp[12, :]  # susceptible partially protected
    E_P = temp[13, :]  # Exposed partially protected
    A_P = temp[14, :]  # Asymptomatic infected partially protected
    P_P = temp[15, :]  # Pre-symptomatic infected partially protected
    I_P = temp[16, :]  # Symptomatic infected partially protected
    H_P = temp[17, :]  # Hospitalizes symptomatic infected partially protected
    R_P = temp[18, :]  # Recovered symptomatic partially protected
    RA_P = temp[19, :]  # Recovered Asymptomatic partially protected
    RH_P = temp[20, :]  # Recovered Hospitalized partially protected
    R_RP = temp[21, :]  # Recovered symptomatic vaccinated with partial protection
    RA_RP = temp[22, :]  # Recovered Asymptomatic vaccinated with partial protection
    RH_RP = temp[23, :]  # Recovered Hospitalized vaccinated with partial protection

    S_PV = temp[24, :]  # susceptible partially protected
    E_PV = temp[25, :]  # Exposed partially protected
    A_PV = temp[26, :]  # Asymptomatic infected partially protected
    P_PV = temp[27, :]  # Pre-symptomatic infected partially protected
    I_PV = temp[28, :]  # Symptomatic infected partially protected
    H_PV = temp[29, :]  # Hospitalizes symptomatic infected partially protected
    R_PV = temp[30, :]  # Recovered symptomatic partially protected
    RA_PV = temp[31, :]  # Recovered Asymptomatic partially protected
    RH_PV = temp[32, :]  # Recovered Hospitalized partially protected
    R_RPV = temp[33, :]  # Recovered symptomatic vaccinated with partial protection
    RA_RPV = temp[34, :]  # Recovered Asymptomatic vaccinated with partial protection
    RH_RPV = temp[35, :]  # Recovered Hospitalized vaccinated with partial protection

    # system for vaccinated people

    S_V1 = temp[36, :]  # susceptible vaccinated with vaccine type #1
    E_V1 = temp[37, :]  # Exposed vaccinated  with vaccine type #1
    A_V1 = temp[38, :]  # Asymptomatic infected vaccinated  with vaccine type #1
    P_V1 = temp[39, :]  # Pre-symptomatic infected vaccinated  with vaccine type #1
    I_V1 = temp[40, :]  # Symptomatic infected vaccinated  with vaccine #2
    H_V1 = temp[41, :]  # Hospitalizes symptomatic infected vaccinated  with vaccine type #1
    R_V1 = temp[42, :]  # Recovered symptomatic vaccinated  with vaccine type #2
    RA_V1 = temp[43, :]  # Recovered Asymptomatic vaccinated  with vaccine type #2
    RH_V1 = temp[44, :]  # Recovered Hospitalized vaccinated  with vaccine type #2
    R_RV1 = temp[45, :]  # Recovered symptomatic vaccinated with partial immunity with vaccine type #1
    RA_RV1 = temp[46, :]  # Recovered Asymptomatic vaccinated with partial immunity  with vaccine type #1
    RH_RV1 = temp[47, :]  # Recovered Hospitalized vaccinated with partial immunity  with vaccine type #1

    S_V2 = temp[48, :]  # susceptible vaccinated with vaccine type #2
    E_V2 = temp[49, :]  # Exposed vaccinated  with vaccine type  #2
    A_V2 = temp[50, :]  # Asymptomatic infected vaccinated  with vaccine type  #2
    P_V2 = temp[51, :]  # Pre-symptomatic infected vaccinated  with vaccine type  #2
    I_V2 = temp[52, :]  # Symptomatic infected vaccinated  with vaccine type  #2
    H_V2 = temp[53, :]  # Hospitalizes symptomatic infected vaccinated  with vaccine type  #2
    R_V2 = temp[54, :]  # Recovered symptomatic vaccinated  with vaccine type  #2
    RA_V2 = temp[55, :]  # Recovered Asymptomatic vaccinated  with vaccine type  #2
    RH_V2 = temp[56, :]  # Recovered Hospitalized vaccinated  with vaccine type #2
    R_RV2 = temp[57, :]  # Recovered symptomatic vaccinated with partial immunity  with vaccine type  #2
    RA_RV2 = temp[58, :]  # Recovered Asymptomatic vaccinated with partial immunity  with vaccine type #2
    RH_RV2 = temp[59, :]  # Recovered Hospitalized vaccinated with partial immunity  with vaccine type  #2

    S_V3 = temp[60, :]  # susceptible vaccinated with vaccine type  #3
    E_V3 = temp[61, :]  # Exposed vaccinated  with vaccine type #3
    A_V3 = temp[62, :]  # Asymptomatic infected vaccinated  with vaccine type  #3
    P_V3 = temp[63, :]  # Pre-symptomatic infected vaccinated  with vaccine type  #3
    I_V3 = temp[64, :]  # Symptomatic infected vaccinated  with vaccine type #3
    H_V3 = temp[65, :]  # Hospitalizes symptomatic infected vaccinated  with vaccine type  #3
    R_V3 = temp[66, :]  # Recovered symptomatic vaccinated  with vaccine type #3
    RA_V3 = temp[67, :]  # Recovered Asymptomatic vaccinated  with vaccine type #3
    RH_V3 = temp[68, :]  # Recovered Hospitalized vaccinated  with vaccine type #3
    R_RV3 = temp[69, :]  # Recovered symptomatic vaccinated with partial immunity  with vaccine type  #3
    RA_RV3 = temp[70, :]  # Recovered Asymptomatic vaccinated with partial immunity  with vaccine type #3
    RH_RV3 = temp[71, :]  # Recovered Hospitalized vaccinated with partial immunity  with vaccine type #3

    S_B1 = temp[72, :]  # susceptible vaccinated with vaccine booster type #1
    E_B1 = temp[73, :]  # Exposed vaccinated  with vaccine booster type #1
    A_B1 = temp[74, :]  # Asymptomatic infected vaccinated  with vaccine booster type #1
    P_B1 = temp[75, :]  # Pre-symptomatic infected vaccinated  with vaccine booster type #1
    I_B1 = temp[76, :]  # Symptomatic infected vaccinated  with vaccine booster type #2
    H_B1 = temp[77, :]  # Hospitalizes symptomatic infected vaccinated  with vaccine booster type #1
    R_B1 = temp[78, :]  # Recovered symptomatic vaccinated  with vaccine booster type #2
    RA_B1 = temp[79, :]  # Recovered Asymptomatic vaccinated  with vaccine booster type #2
    RH_B1 = temp[80, :]  # Recovered Hospitalized vaccinated  with vaccine booster type #2
    R_RB1 = temp[81, :]  # Recovered symptomatic vaccinated with partial immunity with vaccine booster type #1
    RA_RB1 = temp[82, :]  # Recovered Asymptomatic vaccinated with partial immunity  with vaccine booster type #1
    RH_RB1 = temp[83, :]  # Recovered Hospitalized vaccinated with partial immunity  with vaccine booster type #1

    S_B2 = temp[84, :]  # susceptible vaccinated with vaccine booster type #2
    E_B2 = temp[85, :]  # Exposed vaccinated  with vaccine booster type  #2
    A_B2 = temp[86, :]  # Asymptomatic infected vaccinated  with vaccine booster type  #2
    P_B2 = temp[87, :]  # Pre-symptomatic infected vaccinated  with vaccine booster type  #2
    I_B2 = temp[88, :]  # Symptomatic infected vaccinated  with vaccine booster type  #2
    H_B2 = temp[89, :]  # Hospitalizes symptomatic infected vaccinated  with vaccine booster type  #2
    R_B2 = temp[90, :]  # Recovered symptomatic vaccinated  with vaccine booster type  #2
    RA_B2 = temp[91, :]  # Recovered Asymptomatic vaccinated  with vaccine booster type  #2
    RH_B2 = temp[92, :]  # Recovered Hospitalized vaccinated  with vaccine booster type #2
    R_RB2 = temp[93, :]  # Recovered symptomatic vaccinated with partial immunity and with vaccine booster type  #2
    RA_RB2 = temp[94, :]  # Recovered Asymptomatic vaccinated with partial immunity and with vaccine booster type #2
    RH_RB2 = temp[95, :]  # Recovered Hospitalized vaccinated with partial immunity and with vaccine booster type  #2

    S_B3 = temp[96, :]  # susceptible vaccinated with vaccine booster type  #3
    E_B3 = temp[97, :]  # Exposed vaccinated  with vaccine booster type #3
    A_B3 = temp[98, :]  # Asymptomatic infected vaccinated  with vaccine booster type  #3
    P_B3 = temp[99, :]  # Pre-symptomatic infected vaccinated  with vaccine booster type  #3
    I_B3 = temp[100, :]  # Symptomatic infected vaccinated  with vaccine booster type #3
    H_B3 = temp[101, :]  # Hospitalizes symptomatic infected vaccinated  with vaccine booster type  #3
    R_B3 = temp[102, :]  # Recovered symptomatic vaccinated  with vaccine booster type #3
    RA_B3 = temp[103, :]  # Recovered Asymptomatic vaccinated  with vaccine booster type #3
    RH_B3 = temp[104, :]  # Recovered Hospitalized vaccinated  with vaccine booster type #3
    R_RB3 = temp[105, :]  # Recovered symptomatic vaccinated with partial immunity  with vaccine booster type  #3
    RA_RB3 = temp[106, :]  # Recovered Asymptomatic vaccinated with partial immunity  with vaccine booster type #3
    RH_RB3 = temp[107, :]  # Recovered Hospitalized vaccinated with partial immunity  with vaccine booster type #3
    Deaths = temp[108, :]  #Deaths


    # totalInf = temp[22, :]   #total cummulative infections

    Cnew = np.multiply(C, red_sus[:, np.newaxis])  # mC element-wise
    mylambda = np.dot(Cnew, beta * np.divide((redA * (A + A_P + A_PV + A_V1 + A_V2 + A_V3 + A_B1 + A_B2 + A_B3)
                                              + redP * (P + P_P + P_PV + P_V1 + P_V2 + P_V3 + P_B1 + P_B2 + P_B3)
                                              + redH * (H + H_P + H_PV + H_V1 + H_V2 + H_V3 + H_B1 + H_B2 + H_B3)
                                              + (I + I_P + I_PV + I_V1 + I_V2 + I_V3 + I_B1 + I_B2 + I_B3)),
                                             popGroups))  # force of infection

    # Vaccination rate for unvaccinated peoples with full dose (vaccine type 1,2,3)

    frac_susS_vaccinatedV1 = theta(t, tStartV[0], S, vaccinationRateFullDoseType1[0])
    frac_susS_vaccinatedV2 = theta(t, tStartV[1], S - frac_susS_vaccinatedV1, vaccinationRateFullDoseType2[0])
    frac_susS_vaccinatedV3 = theta(t, tStartV[2], S - frac_susS_vaccinatedV1 - frac_susS_vaccinatedV2,
                                   vaccinationRateFullDoseType3[0])

    frac_recR_vaccinatedV1 = theta(t, tStartV[0], R, vaccinationRateFullDoseType1[1])
    frac_recR_vaccinatedV2 = theta(t, tStartV[1], R - frac_recR_vaccinatedV1, vaccinationRateFullDoseType2[1])
    frac_recR_vaccinatedV3 = theta(t, tStartV[2], R - frac_recR_vaccinatedV1 - frac_recR_vaccinatedV2,
                                   vaccinationRateFullDoseType3[1])
    #print(frac_recR_vaccinatedV1,frac_recR_vaccinatedV2,frac_recR_vaccinatedV3)

    frac_recRA_vaccinatedV1 = theta(t, tStartV[0], RA, vaccinationRateFullDoseType1[2])
    frac_recRA_vaccinatedV2 = theta(t, tStartV[1], RA - frac_recRA_vaccinatedV1, vaccinationRateFullDoseType2[2])
    frac_recRA_vaccinatedV3 = theta(t, tStartV[2], RA - frac_recRA_vaccinatedV1 - frac_recRA_vaccinatedV2,
                                    vaccinationRateFullDoseType3[2])

    frac_recRH_vaccinatedV1 = theta(t, tStartV[0], RH, vaccinationRateFullDoseType1[3])
    frac_recRH_vaccinatedV2 = theta(t, tStartV[1], RH - frac_recRH_vaccinatedV1, vaccinationRateFullDoseType2[3])
    frac_recRH_vaccinatedV3 = theta(t, tStartV[2], RH - frac_recRH_vaccinatedV1 - frac_recRH_vaccinatedV2,
                                    vaccinationRateFullDoseType3[3])

    frac_recRR_vaccinatedV1 = theta(t, tStartV[0], R_R, vaccinationRateFullDoseType1[4])
    frac_recRR_vaccinatedV2 = theta(t, tStartV[1], R_R - frac_recRR_vaccinatedV1, vaccinationRateFullDoseType2[4])
    frac_recRR_vaccinatedV3 = theta(t, tStartV[2], R_R - frac_recRR_vaccinatedV1 - frac_recRR_vaccinatedV2,
                                    vaccinationRateFullDoseType3[4])

    frac_recRAR_vaccinatedV1 = theta(t, tStartV[0], RA_R, vaccinationRateFullDoseType1[5])
    frac_recRAR_vaccinatedV2 = theta(t, tStartV[1], RA_R - frac_recRAR_vaccinatedV1, vaccinationRateFullDoseType2[5])
    frac_recRAR_vaccinatedV3 = theta(t, tStartV[2], RA_R - frac_recRAR_vaccinatedV1 - frac_recRAR_vaccinatedV2,
                                     vaccinationRateFullDoseType3[5])

    frac_recRHR_vaccinatedV1 = theta(t, tStartV[0], RH_R, vaccinationRateFullDoseType1[6])
    frac_recRHR_vaccinatedV2 = theta(t, tStartV[1], RH_R - frac_recRHR_vaccinatedV1, vaccinationRateFullDoseType2[6])
    frac_recRHR_vaccinatedV3 = theta(t, tStartV[2], RH_R - frac_recRHR_vaccinatedV1 - frac_recRHR_vaccinatedV2,
                                     vaccinationRateFullDoseType3[6])

    # Vaccination rate for partially protected peoples to vaccine with full dose (vaccine type 1,2,3)

    frac_susSP_vaccinatedV1 = theta(t, tStartV[0], S_P, vaccinationRateFullDoseType1[7])
    frac_susSP_vaccinatedV2 = theta(t, tStartV[1], S_P - frac_susSP_vaccinatedV1, vaccinationRateFullDoseType2[7])
    frac_susSP_vaccinatedV3 = theta(t, tStartV[2], S_P - frac_susSP_vaccinatedV1 - frac_susSP_vaccinatedV2,
                                    vaccinationRateFullDoseType3[7])

    frac_recRP_vaccinatedV1 = theta(t, tStartV[0], R_P, vaccinationRateFullDoseType1[8])
    frac_recRP_vaccinatedV2 = theta(t, tStartV[1], R_P - frac_recRP_vaccinatedV1, vaccinationRateFullDoseType2[8])
    frac_recRP_vaccinatedV3 = theta(t, tStartV[2], R_P - frac_recRP_vaccinatedV1 - frac_recRP_vaccinatedV2,
                                    vaccinationRateFullDoseType3[8])

    frac_recRAP_vaccinatedV1 = theta(t, tStartV[0], RA_P, vaccinationRateFullDoseType1[9])
    frac_recRAP_vaccinatedV2 = theta(t, tStartV[1], RA_P - frac_recRAP_vaccinatedV1, vaccinationRateFullDoseType2[9])
    frac_recRAP_vaccinatedV3 = theta(t, tStartV[2], RA_P - frac_recRAP_vaccinatedV1 - frac_recRAP_vaccinatedV2,
                                     vaccinationRateFullDoseType3[9])

    frac_recRHP_vaccinatedV1 = theta(t, tStartV[0], RH_P, vaccinationRateFullDoseType1[10])
    frac_recRHP_vaccinatedV2 = theta(t, tStartV[1], RH_P - frac_recRHP_vaccinatedV1, vaccinationRateFullDoseType2[10])
    frac_recRHP_vaccinatedV3 = theta(t, tStartV[2], RH_P - frac_recRHP_vaccinatedV1 - frac_recRHP_vaccinatedV2,
                                     vaccinationRateFullDoseType3[10])

    frac_recRRP_vaccinatedV1 = theta(t, tStartV[0], R_RP, vaccinationRateFullDoseType1[11])
    frac_recRRP_vaccinatedV2 = theta(t, tStartV[1], R_RP - frac_recRRP_vaccinatedV1, vaccinationRateFullDoseType2[11])
    frac_recRRP_vaccinatedV3 = theta(t, tStartV[2], R_RP - frac_recRRP_vaccinatedV1 - frac_recRRP_vaccinatedV2,
                                     vaccinationRateFullDoseType3[11])

    frac_recRARP_vaccinatedV1 = theta(t, tStartV[0], RA_RP, vaccinationRateFullDoseType1[12])
    frac_recRARP_vaccinatedV2 = theta(t, tStartV[1], RA_RP - frac_recRARP_vaccinatedV1,
                                      vaccinationRateFullDoseType2[12])
    frac_recRARP_vaccinatedV3 = theta(t, tStartV[2], RA_RP - frac_recRARP_vaccinatedV1 - frac_recRARP_vaccinatedV2,
                                      vaccinationRateFullDoseType3[12])

    frac_recRHRP_vaccinatedV1 = theta(t, tStartV[0], RH_RP, vaccinationRateFullDoseType1[13])
    frac_recRHRP_vaccinatedV2 = theta(t, tStartV[1], RH_RP - frac_recRHRP_vaccinatedV1,
                                      vaccinationRateFullDoseType2[13])
    frac_recRHRP_vaccinatedV3 = theta(t, tStartV[2], RH_RP - frac_recRHRP_vaccinatedV1 - frac_recRHRP_vaccinatedV2,
                                      vaccinationRateFullDoseType3[13])

    # Vaccination rate per day per group with booster type 1,2,3 AS A RESULTS OF
    # vaccination with booster-campaign for VACCINATED WITH full dose
    #V1VP has the total vaccines to ditribute for both wane-vaccinated and already vaccinated with primary
    # S_PV

    numVaccinatedSPV = S_PV
    frac_susSPV_vaccinatedB1_fromV1Campaign = theta(t, tStartV1B[0], numVaccinatedSPV,
                                                    vaccinationRateBoostersType1_for_V1PV[0])

    numVaccinatedSPV -= frac_susSPV_vaccinatedB1_fromV1Campaign
    frac_susSPV_vaccinatedB2_fromV1Campaign = theta(t, tStartV1B[1], numVaccinatedSPV,
                                                    vaccinationRateBoostersType2_for_V1PV[0])

    numVaccinatedSPV -= frac_susSPV_vaccinatedB2_fromV1Campaign
    frac_susSPV_vaccinatedB3_fromV1Campaign = theta(t, tStartV1B[2], numVaccinatedSPV,
                                                    vaccinationRateBoostersType3_for_V1PV[0])

    numVaccinatedSPV -= frac_susSPV_vaccinatedB3_fromV1Campaign
    frac_susSPV_vaccinatedB1_fromV2Campaign = theta(t, tStartV2B[0], numVaccinatedSPV,
                                                    vaccinationRateBoostersType1_for_V2PV[0])

    numVaccinatedSPV -= frac_susSPV_vaccinatedB1_fromV2Campaign
    frac_susSPV_vaccinatedB2_fromV2Campaign = theta(t, tStartV2B[1], numVaccinatedSPV,
                                                    vaccinationRateBoostersType2_for_V2PV[0])
    #print(frac_susSPV_vaccinatedB2_fromV2Campaign)

    numVaccinatedSPV -= frac_susSPV_vaccinatedB2_fromV2Campaign
    frac_susSPV_vaccinatedB3_fromV2Campaign = theta(t, tStartV2B[2], numVaccinatedSPV,
                                                    vaccinationRateBoostersType3_for_V2PV[0])

    numVaccinatedSPV -= frac_susSPV_vaccinatedB3_fromV2Campaign
    frac_susSPV_vaccinatedB1_fromV3Campaign = theta(t, tStartV3B[0], numVaccinatedSPV,
                                                    vaccinationRateBoostersType1_for_V3PV[0])

    numVaccinatedSPV -= frac_susSPV_vaccinatedB1_fromV3Campaign
    frac_susSPV_vaccinatedB2_fromV3Campaign = theta(t, tStartV3B[1], numVaccinatedSPV,
                                                    vaccinationRateBoostersType2_for_V3PV[0])

    numVaccinatedSPV -= frac_susSPV_vaccinatedB2_fromV3Campaign
    frac_susSPV_vaccinatedB3_fromV3Campaign = theta(t, tStartV3B[2], numVaccinatedSPV,
                                                    vaccinationRateBoostersType3_for_V3PV[0])

    # RecR_PV

    numVaccinatedRPV = R_PV
    frac_recRPV_vaccinatedB1_fromV1Campaign = theta(t, tStartV1B[0], numVaccinatedRPV,
                                                    vaccinationRateBoostersType1_for_V1PV[1])

    numVaccinatedRPV -= frac_recRPV_vaccinatedB1_fromV1Campaign
    frac_recRPV_vaccinatedB2_fromV1Campaign = theta(t, tStartV1B[1], numVaccinatedRPV,
                                                    vaccinationRateBoostersType2_for_V1PV[1])

    numVaccinatedRPV -= frac_recRPV_vaccinatedB2_fromV1Campaign
    frac_recRPV_vaccinatedB3_fromV1Campaign = theta(t, tStartV1B[2], numVaccinatedRPV,
                                                    vaccinationRateBoostersType3_for_V1PV[1])

    numVaccinatedRPV -= frac_recRPV_vaccinatedB3_fromV1Campaign
    frac_recRPV_vaccinatedB1_fromV2Campaign = theta(t, tStartV2B[0], numVaccinatedRPV,
                                                    vaccinationRateBoostersType1_for_V2PV[1])

    numVaccinatedRPV -= frac_recRPV_vaccinatedB1_fromV2Campaign
    frac_recRPV_vaccinatedB2_fromV2Campaign = theta(t, tStartV2B[1], numVaccinatedRPV,
                                                    vaccinationRateBoostersType2_for_V2PV[1])

    numVaccinatedRPV -= frac_recRPV_vaccinatedB2_fromV2Campaign
    frac_recRPV_vaccinatedB3_fromV2Campaign = theta(t, tStartV2B[2], numVaccinatedRPV,
                                                    vaccinationRateBoostersType3_for_V2PV[1])

    numVaccinatedRPV -= frac_recRPV_vaccinatedB3_fromV2Campaign
    frac_recRPV_vaccinatedB1_fromV3Campaign = theta(t, tStartV3B[0], numVaccinatedRPV,
                                                    vaccinationRateBoostersType1_for_V3PV[1])

    numVaccinatedRPV -= frac_recRPV_vaccinatedB1_fromV3Campaign
    frac_recRPV_vaccinatedB2_fromV3Campaign = theta(t, tStartV3B[1], numVaccinatedRPV,
                                                    vaccinationRateBoostersType2_for_V3PV[1])

    numVaccinatedRPV -= frac_recRPV_vaccinatedB2_fromV3Campaign
    frac_recRPV_vaccinatedB3_fromV3Campaign = theta(t, tStartV3B[2], numVaccinatedRPV,
                                                    vaccinationRateBoostersType3_for_V3PV[1])

    # RecRA_PV

    numVaccinatedRAPV = RA_PV
    frac_recRAPV_vaccinatedB1_fromV1Campaign = theta(t, tStartV1B[0], numVaccinatedRAPV,
                                                     vaccinationRateBoostersType1_for_V1PV[2])

    numVaccinatedRAPV -= frac_recRAPV_vaccinatedB1_fromV1Campaign
    frac_recRAPV_vaccinatedB2_fromV1Campaign = theta(t, tStartV1B[1], numVaccinatedRAPV,
                                                     vaccinationRateBoostersType2_for_V1PV[2])

    numVaccinatedRAPV -= frac_recRAPV_vaccinatedB2_fromV1Campaign
    frac_recRAPV_vaccinatedB3_fromV1Campaign = theta(t, tStartV1B[2], numVaccinatedRAPV,
                                                     vaccinationRateBoostersType3_for_V1PV[2])

    numVaccinatedRAPV -= frac_recRAPV_vaccinatedB3_fromV1Campaign
    frac_recRAPV_vaccinatedB1_fromV2Campaign = theta(t, tStartV2B[0], numVaccinatedRAPV,
                                                     vaccinationRateBoostersType1_for_V2PV[2])

    numVaccinatedRAPV -= frac_recRAPV_vaccinatedB1_fromV2Campaign
    frac_recRAPV_vaccinatedB2_fromV2Campaign = theta(t, tStartV2B[1], numVaccinatedRAPV,
                                                     vaccinationRateBoostersType2_for_V2PV[2])

    numVaccinatedRAPV -= frac_recRAPV_vaccinatedB2_fromV2Campaign
    frac_recRAPV_vaccinatedB3_fromV2Campaign = theta(t, tStartV2B[2], numVaccinatedRAPV,
                                                      vaccinationRateBoostersType3_for_V2PV[2])

    numVaccinatedRAPV -= frac_recRAPV_vaccinatedB3_fromV2Campaign
    frac_recRAPV_vaccinatedB1_fromV3Campaign = theta(t, tStartV3B[0], numVaccinatedRAPV,
                                                     vaccinationRateBoostersType1_for_V3PV[2])

    numVaccinatedRAPV -= frac_recRAPV_vaccinatedB1_fromV3Campaign
    frac_recRAPV_vaccinatedB2_fromV3Campaign = theta(t, tStartV3B[1], numVaccinatedRAPV,
                                                     vaccinationRateBoostersType2_for_V3PV[2])

    numVaccinatedRAPV -= frac_recRAPV_vaccinatedB2_fromV3Campaign
    frac_recRAPV_vaccinatedB3_fromV3Campaign = theta(t, tStartV3B[2], numVaccinatedRAPV,
                                                     vaccinationRateBoostersType3_for_V3PV[2])

    # RecRH_PV

    numVaccinatedRHPV = RH_PV
    frac_recRHPV_vaccinatedB1_fromV1Campaign = theta(t, tStartV1B[0], numVaccinatedRHPV,
                                                     vaccinationRateBoostersType1_for_V1PV[3])

    numVaccinatedRHPV -= frac_recRHPV_vaccinatedB1_fromV1Campaign
    frac_recRHPV_vaccinatedB2_fromV1Campaign = theta(t, tStartV1B[1], numVaccinatedRHPV,
                                                     vaccinationRateBoostersType2_for_V1PV[3])

    numVaccinatedRHPV -= frac_recRHPV_vaccinatedB2_fromV1Campaign
    frac_recRHPV_vaccinatedB3_fromV1Campaign = theta(t, tStartV1B[2], numVaccinatedRHPV,
                                                     vaccinationRateBoostersType3_for_V1PV[3])

    numVaccinatedRHPV -= frac_recRHPV_vaccinatedB3_fromV1Campaign
    frac_recRHPV_vaccinatedB1_fromV2Campaign = theta(t, tStartV2B[0], numVaccinatedRHPV,
                                                     vaccinationRateBoostersType1_for_V2PV[3])

    numVaccinatedRHPV -= frac_recRHPV_vaccinatedB1_fromV2Campaign
    frac_recRHPV_vaccinatedB2_fromV2Campaign = theta(t, tStartV2B[1], numVaccinatedRHPV,
                                                     vaccinationRateBoostersType2_for_V2PV[3])

    numVaccinatedRHPV -= frac_recRHPV_vaccinatedB2_fromV2Campaign
    frac_recRHPV_vaccinatedB3_fromV2Campaign = theta(t, tStartV2B[2], numVaccinatedRHPV,
                                                     vaccinationRateBoostersType3_for_V2PV[3])

    numVaccinatedRHPV -= frac_recRHPV_vaccinatedB3_fromV2Campaign
    frac_recRHPV_vaccinatedB1_fromV3Campaign = theta(t, tStartV3B[0], numVaccinatedRHPV,
                                                     vaccinationRateBoostersType1_for_V3PV[3])

    numVaccinatedRHPV -= frac_recRHPV_vaccinatedB1_fromV3Campaign
    frac_recRHPV_vaccinatedB2_fromV3Campaign = theta(t, tStartV3B[1], numVaccinatedRHPV,
                                                     vaccinationRateBoostersType2_for_V3PV[3])

    numVaccinatedRHPV -= frac_recRHPV_vaccinatedB2_fromV3Campaign
    frac_recRHPV_vaccinatedB3_fromV3Campaign = theta(t, tStartV3B[2], numVaccinatedRHPV,
                                                     vaccinationRateBoostersType3_for_V3PV[3])

    # RecR_RPV

    numVaccinatedRRPV = R_RPV
    frac_recRRPV_vaccinatedB1_fromV1Campaign = theta(t, tStartV1B[0], numVaccinatedRRPV,
                                                     vaccinationRateBoostersType1_for_V1PV[4])

    numVaccinatedRRPV -= frac_recRRPV_vaccinatedB1_fromV1Campaign
    frac_recRRPV_vaccinatedB2_fromV1Campaign = theta(t, tStartV1B[1], numVaccinatedRRPV,
                                                     vaccinationRateBoostersType2_for_V1PV[4])

    numVaccinatedRRPV -= frac_recRRPV_vaccinatedB2_fromV1Campaign
    frac_recRRPV_vaccinatedB3_fromV1Campaign = theta(t, tStartV1B[2], numVaccinatedRRPV,
                                                     vaccinationRateBoostersType3_for_V1PV[4])

    numVaccinatedRRPV -= frac_recRRPV_vaccinatedB3_fromV1Campaign
    frac_recRRPV_vaccinatedB1_fromV2Campaign = theta(t, tStartV2B[0], numVaccinatedRRPV,
                                                     vaccinationRateBoostersType1_for_V2PV[4])

    numVaccinatedRRPV -= frac_recRRPV_vaccinatedB1_fromV2Campaign
    frac_recRRPV_vaccinatedB2_fromV2Campaign = theta(t, tStartV2B[1], numVaccinatedRRPV,
                                                     vaccinationRateBoostersType2_for_V2PV[4])

    numVaccinatedRRPV -= frac_recRRPV_vaccinatedB2_fromV2Campaign
    frac_recRRPV_vaccinatedB3_fromV2Campaign = theta(t, tStartV2B[2], numVaccinatedRRPV,
                                                     vaccinationRateBoostersType3_for_V2PV[4])

    numVaccinatedRRPV -= frac_recRRPV_vaccinatedB3_fromV2Campaign
    frac_recRRPV_vaccinatedB1_fromV3Campaign = theta(t, tStartV3B[0], numVaccinatedRRPV,
                                                     vaccinationRateBoostersType1_for_V3PV[4])

    numVaccinatedRRPV -= frac_recRRPV_vaccinatedB1_fromV3Campaign
    frac_recRRPV_vaccinatedB2_fromV3Campaign = theta(t, tStartV3B[1], numVaccinatedRRPV,
                                                     vaccinationRateBoostersType2_for_V3PV[4])

    numVaccinatedRRPV -= frac_recRRPV_vaccinatedB2_fromV3Campaign
    frac_recRRPV_vaccinatedB3_fromV3Campaign = theta(t, tStartV3B[2], numVaccinatedRRPV,
                                                     vaccinationRateBoostersType3_for_V3PV[4])

    # RecRA_RPV

    numVaccinatedRARPV = RA_RPV
    frac_recRARPV_vaccinatedB1_fromV1Campaign = theta(t, tStartV1B[0], numVaccinatedRARPV,
                                                      vaccinationRateBoostersType1_for_V1PV[5])

    numVaccinatedRARPV -= frac_recRARPV_vaccinatedB1_fromV1Campaign
    frac_recRARPV_vaccinatedB2_fromV1Campaign = theta(t, tStartV1B[1], numVaccinatedRARPV,
                                                      vaccinationRateBoostersType2_for_V1PV[5])

    numVaccinatedRARPV -= frac_recRARPV_vaccinatedB2_fromV1Campaign
    frac_recRARPV_vaccinatedB3_fromV1Campaign = theta(t, tStartV1B[2], numVaccinatedRARPV,
                                                      vaccinationRateBoostersType3_for_V1PV[5])

    numVaccinatedRARPV -= frac_recRARPV_vaccinatedB3_fromV1Campaign
    frac_recRARPV_vaccinatedB1_fromV2Campaign = theta(t, tStartV2B[0], numVaccinatedRARPV,
                                                      vaccinationRateBoostersType1_for_V2PV[5])

    numVaccinatedRARPV -= frac_recRARPV_vaccinatedB1_fromV2Campaign
    frac_recRARPV_vaccinatedB2_fromV2Campaign = theta(t, tStartV2B[1], numVaccinatedRARPV,
                                                      vaccinationRateBoostersType2_for_V2PV[5])

    numVaccinatedRARPV -= frac_recRARPV_vaccinatedB2_fromV2Campaign
    frac_recRARPV_vaccinatedB3_fromV2Campaign = theta(t, tStartV2B[2], numVaccinatedRARPV,
                                                      vaccinationRateBoostersType3_for_V2PV[5])

    numVaccinatedRARPV -= frac_recRARPV_vaccinatedB3_fromV2Campaign
    frac_recRARPV_vaccinatedB1_fromV3Campaign = theta(t, tStartV3B[0], numVaccinatedRARPV,
                                                      vaccinationRateBoostersType1_for_V3PV[5])

    numVaccinatedRARPV -= frac_recRARPV_vaccinatedB1_fromV3Campaign
    frac_recRARPV_vaccinatedB2_fromV3Campaign = theta(t, tStartV3B[1], numVaccinatedRARPV,
                                                      vaccinationRateBoostersType2_for_V3PV[5])

    numVaccinatedRARPV -= frac_recRARPV_vaccinatedB2_fromV3Campaign
    frac_recRARPV_vaccinatedB3_fromV3Campaign = theta(t, tStartV3B[2], numVaccinatedRARPV,
                                                      vaccinationRateBoostersType3_for_V3PV[5])

    # RecRH_RPV

    numVaccinatedRHRPV = RH_RPV
    frac_recRHRPV_vaccinatedB1_fromV1Campaign = theta(t, tStartV1B[0], numVaccinatedRHRPV,
                                                      vaccinationRateBoostersType1_for_V1PV[6])

    numVaccinatedRHRPV -= frac_recRPV_vaccinatedB1_fromV1Campaign
    frac_recRHRPV_vaccinatedB2_fromV1Campaign = theta(t, tStartV1B[1], numVaccinatedRHRPV,
                                                      vaccinationRateBoostersType2_for_V1PV[6])

    numVaccinatedRHRPV -= frac_recRHRPV_vaccinatedB2_fromV1Campaign
    frac_recRHRPV_vaccinatedB3_fromV1Campaign = theta(t, tStartV1B[2], numVaccinatedRHRPV,
                                                      vaccinationRateBoostersType3_for_V1PV[6])

    numVaccinatedRHRPV -= frac_recRHRPV_vaccinatedB3_fromV1Campaign
    frac_recRHRPV_vaccinatedB1_fromV2Campaign = theta(t, tStartV2B[0], numVaccinatedRHRPV,
                                                      vaccinationRateBoostersType1_for_V2PV[6])

    numVaccinatedRHRPV -= frac_recRHRPV_vaccinatedB1_fromV2Campaign
    frac_recRHRPV_vaccinatedB2_fromV2Campaign = theta(t, tStartV2B[1], numVaccinatedRHRPV,
                                                      vaccinationRateBoostersType2_for_V2PV[6])

    numVaccinatedRHRPV -= frac_recRHRPV_vaccinatedB2_fromV2Campaign
    frac_recRHRPV_vaccinatedB3_fromV2Campaign = theta(t, tStartV2B[2], numVaccinatedRHRPV,
                                                      vaccinationRateBoostersType3_for_V2PV[6])

    numVaccinatedRHRPV -= frac_recRHRPV_vaccinatedB3_fromV2Campaign
    frac_recRHRPV_vaccinatedB1_fromV3Campaign = theta(t, tStartV3B[0], numVaccinatedRHRPV,
                                                      vaccinationRateBoostersType1_for_V3PV[6])

    numVaccinatedRHRPV -= frac_recRHRPV_vaccinatedB1_fromV3Campaign
    frac_recRHRPV_vaccinatedB2_fromV3Campaign = theta(t, tStartV3B[1], numVaccinatedRHRPV,
                                                      vaccinationRateBoostersType2_for_V3PV[6])

    numVaccinatedRHRPV -= frac_recRHRPV_vaccinatedB2_fromV3Campaign
    frac_recRHRPV_vaccinatedB3_fromV3Campaign = theta(t, tStartV3B[2], numVaccinatedRHRPV,
                                                      vaccinationRateBoostersType3_for_V3PV[6])

    # Vaccination rate per day per group with booster type 1,2,3 for vaccinated with V1

    # S_V1

    frac_susSV1_vaccinatedB1 = theta(t, tStartV1B[0], S_V1, vaccinationRateBoostersType1_for_V1PV[7])
    frac_susSV1_vaccinatedB2 = theta(t, tStartV1B[1], S_V1 - frac_susSV1_vaccinatedB1,
                                     vaccinationRateBoostersType2_for_V1PV[7])
    frac_susSV1_vaccinatedB3 = theta(t, tStartV1B[2], S_V1 - frac_susSV1_vaccinatedB1 - frac_susSV1_vaccinatedB2,
                                     vaccinationRateBoostersType3_for_V1PV[7])
    #print(frac_susSV1_vaccinatedB1,frac_susSV1_vaccinatedB2,frac_susSV1_vaccinatedB3)

    # R_V1

    frac_recRV1_vaccinatedB1 = theta(t, tStartV1B[0], R_V1, vaccinationRateBoostersType1_for_V1PV[8])
    frac_recRV1_vaccinatedB2 = theta(t, tStartV1B[1], R_V1 - frac_recRV1_vaccinatedB1,
                                     vaccinationRateBoostersType2_for_V1PV[8])
    frac_recRV1_vaccinatedB3 = theta(t, tStartV1B[2], R_V1 - frac_recRV1_vaccinatedB1 - frac_recRV1_vaccinatedB2,
                                     vaccinationRateBoostersType3_for_V1PV[8])

    # RA_V1

    frac_recRAV1_vaccinatedB1 = theta(t, tStartV1B[0], RA_V1, vaccinationRateBoostersType1_for_V1PV[9])
    frac_recRAV1_vaccinatedB2 = theta(t, tStartV1B[1], RA_V1 - frac_recRAV1_vaccinatedB1,
                                      vaccinationRateBoostersType2_for_V1PV[9])
    frac_recRAV1_vaccinatedB3 = theta(t, tStartV1B[2], RA_V1 - frac_recRAV1_vaccinatedB1 - frac_recRAV1_vaccinatedB2,
                                      vaccinationRateBoostersType3_for_V1PV[9])
    # RH_V1

    frac_recRHV1_vaccinatedB1 = theta(t, tStartV1B[0], RH_V1, vaccinationRateBoostersType1_for_V1PV[10])
    frac_recRHV1_vaccinatedB2 = theta(t, tStartV1B[1], RA_V1 - frac_recRHV1_vaccinatedB1,
                                      vaccinationRateBoostersType2_for_V1PV[10])
    frac_recRHV1_vaccinatedB3 = theta(t, tStartV1B[2], RA_V1 - frac_recRHV1_vaccinatedB1 - frac_recRHV1_vaccinatedB2,
                                      vaccinationRateBoostersType3_for_V1PV[10])

    # R_RV1

    frac_recRRV1_vaccinatedB1 = theta(t, tStartV1B[0], R_RV1, vaccinationRateBoostersType1_for_V1PV[11])
    frac_recRRV1_vaccinatedB2 = theta(t, tStartV1B[1], R_RV1 - frac_recRRV1_vaccinatedB1,
                                      vaccinationRateBoostersType2_for_V1PV[11])
    frac_recRRV1_vaccinatedB3 = theta(t, tStartV1B[2], R_RV1 - frac_recRRV1_vaccinatedB1 - frac_recRRV1_vaccinatedB2,
                                      vaccinationRateBoostersType3_for_V1PV[11])

    # RA_RV1

    frac_recRARV1_vaccinatedB1 = theta(t, tStartV1B[0], RA_RV1, vaccinationRateBoostersType1_for_V1PV[12])
    frac_recRARV1_vaccinatedB2 = theta(t, tStartV1B[1], RA_RV1 - frac_recRARV1_vaccinatedB1,
                                       vaccinationRateBoostersType2_for_V1PV[12])
    frac_recRARV1_vaccinatedB3 = theta(t, tStartV1B[2],
                                       RA_RV1 - frac_recRARV1_vaccinatedB1 - frac_recRARV1_vaccinatedB2,
                                       vaccinationRateBoostersType3_for_V1PV[12])
    # RH_RV1

    frac_recRHRV1_vaccinatedB1 = theta(t, tStartV1B[0], RH_RV1, vaccinationRateBoostersType1_for_V1PV[13])
    frac_recRHRV1_vaccinatedB2 = theta(t, tStartV1B[1], RH_RV1 - frac_recRHRV1_vaccinatedB1,
                                       vaccinationRateBoostersType2_for_V1PV[13])
    frac_recRHRV1_vaccinatedB3 = theta(t, tStartV1B[2],
                                       RH_RV1 - frac_recRHRV1_vaccinatedB1 - frac_recRHRV1_vaccinatedB2,
                                       vaccinationRateBoostersType3_for_V1PV[13])

    # Vaccination rate per day per group with booster type 1,2,3 for vaccinated with V2

    # S_V2

    frac_susSV2_vaccinatedB1 = theta(t, tStartV2B[0], S_V2, vaccinationRateBoostersType1_for_V2PV[7])
    frac_susSV2_vaccinatedB2 = theta(t, tStartV2B[1], S_V2 - frac_susSV2_vaccinatedB1,
                                     vaccinationRateBoostersType2_for_V2PV[7])
    frac_susSV2_vaccinatedB3 = theta(t, tStartV2B[2], S_V2 - frac_susSV2_vaccinatedB1 - frac_susSV2_vaccinatedB2,
                                     vaccinationRateBoostersType3_for_V2PV[7])
    # R_V2

    frac_recRV2_vaccinatedB1 = theta(t, tStartV2B[0], R_V2, vaccinationRateBoostersType1_for_V2PV[8])
    frac_recRV2_vaccinatedB2 = theta(t, tStartV2B[1], R_V2 - frac_recRV2_vaccinatedB1,
                                     vaccinationRateBoostersType2_for_V2PV[8])
    frac_recRV2_vaccinatedB3 = theta(t, tStartV2B[2], R_V2 - frac_recRV2_vaccinatedB1 - frac_recRV2_vaccinatedB2,
                                     vaccinationRateBoostersType3_for_V2PV[8])

    # RA_V2

    frac_recRAV2_vaccinatedB1 = theta(t, tStartV2B[0], RA_V2, vaccinationRateBoostersType1_for_V2PV[9])
    frac_recRAV2_vaccinatedB2 = theta(t, tStartV2B[1], RA_V2 - frac_recRAV2_vaccinatedB1,
                                      vaccinationRateBoostersType2_for_V2PV[9])
    frac_recRAV2_vaccinatedB3 = theta(t, tStartV2B[2], RA_V2 - frac_recRAV2_vaccinatedB1 - frac_recRAV2_vaccinatedB2,
                                      vaccinationRateBoostersType3_for_V2PV[9])
    # RH_V2

    frac_recRHV2_vaccinatedB1 = theta(t, tStartV2B[0], RH_V2, vaccinationRateBoostersType1_for_V2PV[10])
    frac_recRHV2_vaccinatedB2 = theta(t, tStartV2B[1], RH_V2 - frac_recRHV2_vaccinatedB1,
                                      vaccinationRateBoostersType2_for_V2PV[10])
    frac_recRHV2_vaccinatedB3 = theta(t, tStartV2B[2], RH_V2 - frac_recRHV2_vaccinatedB1 - frac_recRHV2_vaccinatedB2,
                                      vaccinationRateBoostersType3_for_V2PV[10])

    # R_RV2

    frac_recRRV2_vaccinatedB1 = theta(t, tStartV2B[0], R_RV2, vaccinationRateBoostersType1_for_V2PV[11])
    frac_recRRV2_vaccinatedB2 = theta(t, tStartV2B[1], R_RV2 - frac_recRRV2_vaccinatedB1,
                                      vaccinationRateBoostersType2_for_V2PV[11])
    frac_recRRV2_vaccinatedB3 = theta(t, tStartV2B[2], R_RV2 - frac_recRRV2_vaccinatedB1 - frac_recRRV2_vaccinatedB2,
                                      vaccinationRateBoostersType3_for_V2PV[11])

    # RA_RV2

    frac_recRARV2_vaccinatedB1 = theta(t, tStartV2B[0], RA_RV2, vaccinationRateBoostersType1_for_V2PV[12])
    frac_recRARV2_vaccinatedB2 = theta(t, tStartV2B[1], RA_RV2 - frac_recRARV2_vaccinatedB1,
                                       vaccinationRateBoostersType2_for_V2PV[12])
    frac_recRARV2_vaccinatedB3 = theta(t, tStartV2B[2],
                                       RA_RV2 - frac_recRARV2_vaccinatedB1 - frac_recRARV2_vaccinatedB2,
                                       vaccinationRateBoostersType3_for_V2PV[12])
    # RH_RV2

    frac_recRHRV2_vaccinatedB1 = theta(t, tStartV2B[0], RH_RV2, vaccinationRateBoostersType1_for_V2PV[13])
    frac_recRHRV2_vaccinatedB2 = theta(t, tStartV2B[1], RH_RV2 - frac_recRHRV2_vaccinatedB1,
                                       vaccinationRateBoostersType2_for_V2PV[13])
    frac_recRHRV2_vaccinatedB3 = theta(t, tStartV2B[2],
                                       RH_RV2 - frac_recRHRV2_vaccinatedB1 - frac_recRHRV2_vaccinatedB2,
                                       vaccinationRateBoostersType3_for_V2PV[13])

    # Vaccination rate per day per group with vaccine booster type 1,2,3 for vaccinated with V3

    # S_V3

    frac_susSV3_vaccinatedB1 = theta(t, tStartV3B[0], S_V3, vaccinationRateBoostersType1_for_V3PV[7])
    frac_susSV3_vaccinatedB2 = theta(t, tStartV3B[1], S_V3 - frac_susSV3_vaccinatedB1,
                                     vaccinationRateBoostersType2_for_V3PV[7])
    frac_susSV3_vaccinatedB3 = theta(t, tStartV3B[2], S_V3 - frac_susSV3_vaccinatedB1 - frac_susSV3_vaccinatedB2,
                                     vaccinationRateBoostersType3_for_V3PV[7])

    # R_V3

    frac_recRV3_vaccinatedB1 = theta(t, tStartV3B[0], R_V3, vaccinationRateBoostersType1_for_V3PV[8])
    frac_recRV3_vaccinatedB2 = theta(t, tStartV3B[1], R_V3 - frac_recRV3_vaccinatedB1,
                                     vaccinationRateBoostersType2_for_V3PV[8])
    frac_recRV3_vaccinatedB3 = theta(t, tStartV3B[2], R_V3 - frac_recRV3_vaccinatedB1 - frac_recRV3_vaccinatedB2,
                                     vaccinationRateBoostersType3_for_V3PV[8])

    # RA_V3

    frac_recRAV3_vaccinatedB1 = theta(t, tStartV3B[0], RA_V3, vaccinationRateBoostersType1_for_V3PV[9])
    frac_recRAV3_vaccinatedB2 = theta(t, tStartV3B[1], RA_V3 - frac_recRAV3_vaccinatedB1,
                                      vaccinationRateBoostersType2_for_V3PV[9])
    frac_recRAV3_vaccinatedB3 = theta(t, tStartV3B[2], RA_V3 - frac_recRAV3_vaccinatedB1 - frac_recRAV3_vaccinatedB2,
                                      vaccinationRateBoostersType3_for_V3PV[9])
    # RH_V3

    frac_recRHV3_vaccinatedB1 = theta(t, tStartV3B[0], RH_V3, vaccinationRateBoostersType1_for_V3PV[10])
    frac_recRHV3_vaccinatedB2 = theta(t, tStartV3B[1], RH_V3 - frac_recRHV3_vaccinatedB1,
                                      vaccinationRateBoostersType2_for_V3PV[10])
    frac_recRHV3_vaccinatedB3 = theta(t, tStartV3B[2], RH_V3 - frac_recRHV3_vaccinatedB1 - frac_recRHV3_vaccinatedB2,
                                      vaccinationRateBoostersType3_for_V3PV[10])

    # R_RV3

    frac_recRRV3_vaccinatedB1 = theta(t, tStartV3B[0], R_RV3, vaccinationRateBoostersType1_for_V3PV[11])
    frac_recRRV3_vaccinatedB2 = theta(t, tStartV3B[1], R_RV3 - frac_recRRV3_vaccinatedB1,
                                      vaccinationRateBoostersType2_for_V3PV[11])
    frac_recRRV3_vaccinatedB3 = theta(t, tStartV3B[2], R_RV3 - frac_recRRV3_vaccinatedB1 - frac_recRRV3_vaccinatedB2,
                                      vaccinationRateBoostersType3_for_V3PV[11])

    # RA_RV3

    frac_recRARV3_vaccinatedB1 = theta(t, tStartV3B[0], RA_RV3, vaccinationRateBoostersType1_for_V3PV[12])
    frac_recRARV3_vaccinatedB2 = theta(t, tStartV3B[1], RA_RV3 - frac_recRARV3_vaccinatedB1,
                                       vaccinationRateBoostersType2_for_V3PV[12])
    frac_recRARV3_vaccinatedB3 = theta(t, tStartV3B[2], R_RV3 - frac_recRARV3_vaccinatedB1 - frac_recRARV3_vaccinatedB2,
                                       vaccinationRateBoostersType3_for_V3PV[12])

    # RH_RV3

    frac_recRHRV3_vaccinatedB1 = theta(t, tStartV3B[0], RH_RV3, vaccinationRateBoostersType1_for_V3PV[13])
    frac_recRHRV3_vaccinatedB2 = theta(t, tStartV3B[1], RH_RV3 - frac_recRHRV3_vaccinatedB1,
                                       vaccinationRateBoostersType2_for_V3PV[13])
    frac_recRHRV3_vaccinatedB3 = theta(t, tStartV3B[2], RH_V3 - frac_recRHRV3_vaccinatedB1 - frac_recRHRV3_vaccinatedB2,
                                       vaccinationRateBoostersType3_for_V3PV[13])

    #ODE eqs

    dS = - np.multiply(mylambda, S) - frac_susS_vaccinatedV1 - frac_susS_vaccinatedV2 - frac_susS_vaccinatedV3
    #print(dS)
    dE = np.multiply(mylambda, S) - gammaE * E

    dA = gammaE * np.multiply(E, one_minus_frac_sym) - gammaA * A

    dP = gammaE * np.multiply(E, frac_sym) - gammaP * P

    dI = gammaP * P - gammaI * np.multiply(I, one_minus_hosp_frac) - sigma * np.multiply(I, hosp_frac)

    dH = sigma * np.multiply(I, hosp_frac) - gammaH * H - deathRate * H

    dR = gammaI * np.multiply(I, one_minus_hosp_frac) - 2 * gammaR * R \
         - frac_recR_vaccinatedV1 - frac_recR_vaccinatedV2 - frac_recR_vaccinatedV3

    dRA = gammaA * A - 2 * gammaRA * RA \
          - frac_recRA_vaccinatedV1 - frac_recRA_vaccinatedV2 - frac_recRA_vaccinatedV3

    dRH = gammaH * H - 2 * gammaRH * RH \
          - frac_recRH_vaccinatedV1 - frac_recRH_vaccinatedV2 - frac_recRH_vaccinatedV3

    dR_R = 2 * gammaR * R - 2 * gammaR * R_R - frac_recRR_vaccinatedV1 \
           - frac_recRR_vaccinatedV2 - frac_recRR_vaccinatedV3

    dRA_R = 2 * gammaRA * RA - 2 * gammaRA * RA_R \
            - frac_recRAR_vaccinatedV1 - frac_recRAR_vaccinatedV2 - frac_recRAR_vaccinatedV3

    dRH_R = 2 * gammaRH * RH - 2 * gammaRH * RH_R \
            - frac_recRHR_vaccinatedV1 - frac_recRHR_vaccinatedV2 - frac_recRHR_vaccinatedV3

    # un-vaccinated & partially protected eqs

    dS_P = 2 * gammaR * R_R + 2 * gammaRA * RA_R + 2 * gammaRH * RH_R + 2 * gammaRP * R_RP + 2 * gammaRAP * RA_RP \
           + 2 * gammaRHP * RH_RP - one_minus_VESUSP * np.multiply(mylambda,S_P) \
           - frac_susSP_vaccinatedV1 - frac_susSP_vaccinatedV2 - frac_susSP_vaccinatedV3

    dE_P = one_minus_VESUSP * np.multiply(mylambda, S_P) - gammaE * E_P

    dA_P = gammaE * np.multiply(E_P, one_minus_one_minus_frac_VESYMPP) - gammaA * A_P

    dP_P = gammaE * np.multiply(E_P, one_minus_frac_VESYMPP) - gammaP * P_P

    dI_P = gammaP * P_P - gammaI * np.multiply(I_P, one_minus_one_minus_frac_VEHP) \
           - sigma * np.multiply(I_P,one_minus_frac_VEHP)

    dH_P = sigma * np.multiply(I_P, one_minus_frac_VEHP) - gammaH * H_P - deathRate * H_P

    dR_P = gammaI * np.multiply(I_P, one_minus_one_minus_frac_VEHP) - 2 * gammaRP * R_P \
           - frac_recRP_vaccinatedV1 - frac_recRP_vaccinatedV2 - frac_recRP_vaccinatedV3

    dRA_P = gammaA * A_P - 2 * gammaRAP * RA_P \
            - frac_recRAP_vaccinatedV1 - frac_recRAP_vaccinatedV2 - frac_recRAP_vaccinatedV3

    dRH_P = gammaH * H_P - 2 * gammaRHP * RH_P \
            - frac_recRHP_vaccinatedV1 - frac_recRHP_vaccinatedV2 - frac_recRHP_vaccinatedV3

    dR_RP = 2 * gammaRP * R_P - 2 * gammaRP * R_RP \
            - frac_recRRP_vaccinatedV1 - frac_recRRP_vaccinatedV2 - frac_recRRP_vaccinatedV3

    dRA_RP = 2 * gammaRAP * RA_P - 2 * gammaRAP * RA_RP \
             - frac_recRARP_vaccinatedV1 - frac_recRARP_vaccinatedV2 - frac_recRARP_vaccinatedV3

    dRH_RP = 2 * gammaRHP * RH_P - 2 * gammaRHP * RH_RP \
             - frac_recRHRP_vaccinatedV1 - frac_recRHRP_vaccinatedV2 - frac_recRHRP_vaccinatedV3

    # vaccinated & partially protected eqs

    dS_PV = 2 * gammaRPV * R_RPV + 2 * gammaRAPV * RA_RPV + 2 * gammaRHPV * RH_RPV + \
            gammaSV[0] * S_V1 + gammaSV[1] * S_V2 + gammaSV[2] * S_V3 - one_minus_VESUSPV * np.multiply(mylambda, S_PV) \
            - frac_susSPV_vaccinatedB1_fromV1Campaign - frac_susSPV_vaccinatedB2_fromV1Campaign - frac_susSPV_vaccinatedB3_fromV1Campaign \
            - frac_susSPV_vaccinatedB1_fromV2Campaign - frac_susSPV_vaccinatedB2_fromV2Campaign - frac_susSPV_vaccinatedB3_fromV2Campaign \
            - frac_susSPV_vaccinatedB1_fromV3Campaign - frac_susSPV_vaccinatedB2_fromV3Campaign - frac_susSPV_vaccinatedB3_fromV3Campaign

    dE_PV = one_minus_VESUSPV * np.multiply(mylambda, S_PV) - gammaE * E_PV

    dA_PV = gammaE * np.multiply(E_PV, one_minus_one_minus_frac_VESYMPPV) - gammaA * A_PV

    dP_PV = gammaE * np.multiply(E_PV, one_minus_frac_VESYMPPV) - gammaP * P_PV

    dI_PV = gammaP * P_PV - gammaI * np.multiply(I_PV, one_minus_one_minus_frac_VEHPV)\
            - sigma * np.multiply(I_PV,one_minus_frac_VEHPV)

    dH_PV = sigma * np.multiply(I_PV, one_minus_frac_VEHPV) - gammaH * H_PV - deathRate * H_PV

    dR_PV = gammaI * np.multiply(I_PV, one_minus_one_minus_frac_VEHPV) - 2 * gammaRPV * R_PV \
            - frac_recRPV_vaccinatedB1_fromV1Campaign - frac_recRPV_vaccinatedB2_fromV1Campaign - frac_recRPV_vaccinatedB3_fromV1Campaign \
            - frac_recRPV_vaccinatedB1_fromV2Campaign - frac_recRPV_vaccinatedB2_fromV2Campaign - frac_recRPV_vaccinatedB3_fromV2Campaign \
            - frac_recRPV_vaccinatedB1_fromV3Campaign - frac_recRPV_vaccinatedB2_fromV3Campaign - frac_recRPV_vaccinatedB3_fromV3Campaign

    dRA_PV = gammaA * A_PV - 2 * gammaRAPV * RA_PV \
             - frac_recRAPV_vaccinatedB1_fromV1Campaign - frac_recRAPV_vaccinatedB2_fromV1Campaign - frac_recRAPV_vaccinatedB3_fromV1Campaign \
             - frac_recRAPV_vaccinatedB1_fromV2Campaign - frac_recRAPV_vaccinatedB2_fromV2Campaign - frac_recRAPV_vaccinatedB3_fromV2Campaign \
             - frac_recRAPV_vaccinatedB1_fromV3Campaign - frac_recRAPV_vaccinatedB2_fromV3Campaign - frac_recRAPV_vaccinatedB3_fromV3Campaign

    dRH_PV = gammaH * H_PV - 2 * gammaRHPV * RH_PV \
             - frac_recRHPV_vaccinatedB1_fromV1Campaign - frac_recRHPV_vaccinatedB2_fromV1Campaign - frac_recRHPV_vaccinatedB3_fromV1Campaign \
             - frac_recRHPV_vaccinatedB1_fromV2Campaign - frac_recRHPV_vaccinatedB2_fromV2Campaign - frac_recRHPV_vaccinatedB3_fromV2Campaign \
             - frac_recRHPV_vaccinatedB1_fromV3Campaign - frac_recRHPV_vaccinatedB2_fromV3Campaign - frac_recRHPV_vaccinatedB3_fromV3Campaign

    dR_RPV = 2 * gammaRPV * R_PV - 2 * gammaRPV * R_RPV \
             - frac_recRRPV_vaccinatedB1_fromV1Campaign - frac_recRRPV_vaccinatedB2_fromV1Campaign - frac_recRRPV_vaccinatedB3_fromV1Campaign \
             - frac_recRRPV_vaccinatedB1_fromV2Campaign - frac_recRRPV_vaccinatedB2_fromV2Campaign - frac_recRRPV_vaccinatedB3_fromV2Campaign \
             - frac_recRRPV_vaccinatedB1_fromV3Campaign - frac_recRRPV_vaccinatedB2_fromV3Campaign - frac_recRRPV_vaccinatedB3_fromV3Campaign

    dRA_RPV = 2 * gammaRAPV * RA_PV - 2 * gammaRAPV * RA_RPV \
              - frac_recRARPV_vaccinatedB1_fromV1Campaign - frac_recRARPV_vaccinatedB2_fromV1Campaign - frac_recRARPV_vaccinatedB3_fromV1Campaign \
              - frac_recRARPV_vaccinatedB1_fromV2Campaign - frac_recRARPV_vaccinatedB2_fromV2Campaign - frac_recRARPV_vaccinatedB3_fromV2Campaign \
              - frac_recRARPV_vaccinatedB1_fromV3Campaign - frac_recRARPV_vaccinatedB2_fromV3Campaign - frac_recRARPV_vaccinatedB3_fromV3Campaign

    dRH_RPV = 2 * gammaRHPV * RH_PV - 2 * gammaRHPV * RH_RPV \
              - frac_recRHRPV_vaccinatedB1_fromV1Campaign - frac_recRHRPV_vaccinatedB2_fromV1Campaign - frac_recRHRPV_vaccinatedB3_fromV1Campaign \
              - frac_recRHRPV_vaccinatedB1_fromV2Campaign - frac_recRHRPV_vaccinatedB2_fromV2Campaign - frac_recRHRPV_vaccinatedB3_fromV2Campaign \
              - frac_recRHRPV_vaccinatedB1_fromV3Campaign - frac_recRHRPV_vaccinatedB2_fromV3Campaign - frac_recRHRPV_vaccinatedB3_fromV3Campaign

    # vaccinated eqs with vaccine 1

    dS_V1 = frac_susS_vaccinatedV1 + frac_susSP_vaccinatedV1 + gammaSB[0] * S_B1 \
            - frac_susSV1_vaccinatedB1 - frac_susSV1_vaccinatedB2 - frac_susSV1_vaccinatedB3 \
            - one_minus_VESUSV[0] * np.multiply(mylambda, S_V1) - gammaSV[0] * S_V1

    dE_V1 = one_minus_VESUSV[0] * np.multiply(mylambda, S_V1) - gammaE * E_V1

    dA_V1 = gammaE * np.multiply(E_V1, one_minus_one_minus_frac_VESYMPV[0]) - gammaA * A_V1

    dP_V1 = gammaE * np.multiply(E_V1, one_minus_frac_VESYMPV[0]) - gammaP * P_V1

    dI_V1 = gammaP * P_V1 - gammaI * np.multiply(I_V1, one_minus_one_minus_frac_VEHV[0]) \
            - sigma * np.multiply(I_V1, one_minus_frac_VEHV[0])

    dH_V1 = sigma * np.multiply(I_V1, one_minus_frac_VEHV[0]) - gammaH * H_V1 - deathRate * H_V1

    dR_V1 = gammaI * np.multiply(I_V1, one_minus_one_minus_frac_VEHV[0]) - 2 * gammaRV[0] * R_V1 \
            - frac_recRV1_vaccinatedB1 - frac_recRV1_vaccinatedB2 - frac_recRV1_vaccinatedB3 \
            + frac_recR_vaccinatedV1

    dRA_V1 = gammaA * A_V1 - 2 * gammaRAV[0] * RA_V1 \
             - frac_recRAV1_vaccinatedB1 - frac_recRAV1_vaccinatedB2 - frac_recRAV1_vaccinatedB3\
             +frac_recRA_vaccinatedV1

    dRH_V1 = gammaH * H_V1 - 2 * gammaRHV[0] * RH_V1 \
             - frac_recRHV1_vaccinatedB1 - frac_recRHV1_vaccinatedB2 - frac_recRHV1_vaccinatedB3\
             +frac_recRH_vaccinatedV1

    dR_RV1 = 2 * gammaRV[0] * R_V1 - 2 * gammaRV[0] * R_RV1 \
             - frac_recRRV1_vaccinatedB1 - frac_recRRV1_vaccinatedB2 - frac_recRRV1_vaccinatedB3\
             +frac_recRR_vaccinatedV1

    dRA_RV1 = 2 * gammaRAV[0] * RA_V1 - 2 * gammaRAV[0] * RA_RV1 \
              - frac_recRARV1_vaccinatedB1 - frac_recRARV1_vaccinatedB2 - frac_recRARV1_vaccinatedB3\
              +frac_recRAR_vaccinatedV1

    dRH_RV1 = 2 * gammaRHV[0] * RH_V1 - 2 * gammaRHV[0] * RH_RV1 \
              - frac_recRHRV1_vaccinatedB1 - frac_recRHRV1_vaccinatedB2 - frac_recRHRV1_vaccinatedB3\
              +frac_recRHR_vaccinatedV1

    # vaccinated eqs with vaccine 2

    dS_V2 = frac_susS_vaccinatedV2 + frac_susSP_vaccinatedV2 + gammaSB[1] * S_B2 \
            - frac_susSV2_vaccinatedB1 - frac_susSV2_vaccinatedB2 - frac_susSV2_vaccinatedB3 \
            - one_minus_VESUSV[1] * np.multiply(mylambda, S_V2) - gammaSV[1] * S_V2

    dE_V2 = one_minus_VESUSV[1] * np.multiply(mylambda, S_V2) - gammaE * E_V2

    dA_V2 = gammaE * np.multiply(E_V2, one_minus_one_minus_frac_VESYMPV[1]) - gammaA * A_V2

    dP_V2 = gammaE * np.multiply(E_V2, one_minus_frac_VESYMPV[1]) - gammaP * P_V2

    dI_V2 = gammaP * P_V2 - gammaI * np.multiply(I_V2, one_minus_one_minus_frac_VEHV[1]) \
            - sigma * np.multiply(I_V2,one_minus_frac_VEHV[1])

    dH_V2 = sigma * np.multiply(I_V2, one_minus_frac_VEHV[1]) - gammaH * H_V2 - deathRate * H_V2

    dR_V2 = gammaI * np.multiply(I_V2, one_minus_one_minus_frac_VEHV[1]) - 2 * gammaRV[1] * R_V2 \
            - frac_recRV2_vaccinatedB1 - frac_recRV2_vaccinatedB2 - frac_recRV2_vaccinatedB3\
            +frac_recR_vaccinatedV2

    dRA_V2 = gammaA * A_V2 - 2 * gammaRAV[1] * RA_V2 \
             - frac_recRAV2_vaccinatedB1 - frac_recRAV2_vaccinatedB2 - frac_recRAV2_vaccinatedB3\
             +frac_recRA_vaccinatedV2

    dRH_V2 = gammaH * H_V2 - 2 * gammaRHV[1] * RH_V2 \
             - frac_recRHV2_vaccinatedB1 - frac_recRHV2_vaccinatedB2 - frac_recRHV2_vaccinatedB3\
             +frac_recRH_vaccinatedV2

    dR_RV2 = 2 * gammaRV[1] * R_V2 - 2 * gammaRV[1] * R_RV2 \
             - frac_recRRV2_vaccinatedB1 - frac_recRRV2_vaccinatedB2 - frac_recRRV2_vaccinatedB3\
             +frac_recRR_vaccinatedV2

    dRA_RV2 = 2 * gammaRAV[1] * RA_V2 - 2 * gammaRAV[1] * RA_RV2 \
              - frac_recRARV2_vaccinatedB1 - frac_recRARV2_vaccinatedB2 - frac_recRARV2_vaccinatedB3\
              +frac_recRAR_vaccinatedV2

    dRH_RV2 = 2 * gammaRHV[1] * RH_V2 - 2 * gammaRHV[1] * RH_RV2 \
              - frac_recRHRV2_vaccinatedB1 - frac_recRHRV2_vaccinatedB2 - frac_recRHRV2_vaccinatedB3\
              +frac_recRHR_vaccinatedV2

    # vaccinated eqs with vaccine 3

    dS_V3 = frac_susS_vaccinatedV3 + frac_susSP_vaccinatedV3 + gammaSB[2] * S_B3 \
            - frac_susSV3_vaccinatedB1 - frac_susSV3_vaccinatedB2 - frac_susSV3_vaccinatedB3 \
            - one_minus_VESUSV[2] * np.multiply(mylambda, S_V3) - gammaSV[2] * S_V3

    dE_V3 = one_minus_VESUSV[2] * np.multiply(mylambda, S_V3) - gammaE * E_V3

    dA_V3 = gammaE * np.multiply(E_V3, one_minus_one_minus_frac_VESYMPV[2]) - gammaA * A_V3

    dP_V3 = gammaE * np.multiply(E_V3, one_minus_frac_VESYMPV[2]) - gammaP * P_V3

    dI_V3 = gammaP * P_V3 - gammaI * np.multiply(I_V3, one_minus_one_minus_frac_VEHV[2]) \
            - sigma * np.multiply(I_V3,one_minus_frac_VEHV[2])

    dH_V3 = sigma * np.multiply(I_V3, one_minus_frac_VEHV[2]) - gammaH * H_V3 - deathRate * H_V3

    dR_V3 = gammaI * np.multiply(I_V3, one_minus_one_minus_frac_VEHV[2]) - 2 * gammaRV[2] * R_V3 \
            - frac_recRV3_vaccinatedB1 - frac_recRV3_vaccinatedB2 - frac_recRV3_vaccinatedB3\
            +frac_recR_vaccinatedV3

    dRA_V3 = gammaA * A_V3 - 2 * gammaRAV[2] * RA_V3 \
             - frac_recRAV3_vaccinatedB1 - frac_recRAV3_vaccinatedB2 - frac_recRAV3_vaccinatedB3\
             +frac_recRA_vaccinatedV3

    dRH_V3 = gammaH * H_V3 - 2 * gammaRHV[2] * RH_V3 \
             - frac_recRHV3_vaccinatedB1 - frac_recRHV3_vaccinatedB2 - frac_recRHV3_vaccinatedB3\
             +frac_recRH_vaccinatedV3

    dR_RV3 = 2 * gammaRV[2] * R_V3 - 2 * gammaRV[2] * R_RV3 \
             - frac_recRRV3_vaccinatedB1 - frac_recRRV3_vaccinatedB2 - frac_recRRV3_vaccinatedB3\
             +frac_recRR_vaccinatedV3

    dRA_RV3 = 2 * gammaRAV[2] * RA_V3 - 2 * gammaRAV[2] * RA_RV3 \
              - frac_recRARV3_vaccinatedB1 - frac_recRARV3_vaccinatedB2 - frac_recRARV3_vaccinatedB3\
              +frac_recRAR_vaccinatedV3

    dRH_RV3 = 2 * gammaRHV[2] * RH_V3 - 2 * gammaRHV[2] * RH_RV3 \
              - frac_recRHRV3_vaccinatedB1 - frac_recRHRV3_vaccinatedB2 - frac_recRHRV3_vaccinatedB3\
              +frac_recRHR_vaccinatedV3

    # vaccinated eqs with booster 1

    dS_B1 = frac_susSV1_vaccinatedB1 + frac_susSV2_vaccinatedB1 + frac_susSV3_vaccinatedB1 \
            + frac_susSPV_vaccinatedB1_fromV1Campaign \
            + frac_susSPV_vaccinatedB1_fromV2Campaign + frac_susSPV_vaccinatedB1_fromV3Campaign \
            + 2 * gammaRAV[0] * RA_RV1 + 2 * gammaRV[0] * R_RV1 + 2 * gammaRHV[0] * RH_RV1 \
            + 2 * gammaRAB[0] * RA_RB1 + 2 * gammaRB[0] * R_RB1 + 2 * gammaRHB[0] * RH_RB1 \
            - one_minus_VESUSB[0] * np.multiply(mylambda, S_B1) - gammaSB[0] * S_B1

    dE_B1 = one_minus_VESUSB[0] * np.multiply(mylambda, S_B1) - gammaE * E_B1

    dA_B1 = gammaE * np.multiply(E_B1, one_minus_one_minus_frac_VESYMPB[0]) - gammaA * A_B1

    dP_B1 = gammaE * np.multiply(E_B1, one_minus_frac_VESYMPB[0]) - gammaP * P_B1

    dI_B1 = gammaP * P_B1 - gammaI * np.multiply(I_B1, one_minus_one_minus_frac_VEHB[0]) \
            - sigma * np.multiply(I_B1,one_minus_frac_VEHB[0])

    dH_B1 = sigma * np.multiply(I_B1, one_minus_frac_VEHB[0]) - gammaH * H_B1 - deathRate * H_B1

    dR_B1 = gammaI * np.multiply(I_B1, one_minus_one_minus_frac_VEHB[0]) - 2 * gammaRB[0] * R_B1 \
            + frac_recRP_vaccinatedV1 + frac_recRV1_vaccinatedB1 + frac_recRV2_vaccinatedB1 + frac_recRV3_vaccinatedB1 \
            + frac_recRPV_vaccinatedB1_fromV1Campaign + frac_recRPV_vaccinatedB1_fromV2Campaign + frac_recRPV_vaccinatedB1_fromV3Campaign

    dRA_B1 = gammaA * A_B1 - 2 * gammaRAB[0] * RA_B1 \
             + frac_recRAP_vaccinatedV1 + frac_recRAV1_vaccinatedB1 + frac_recRAV2_vaccinatedB1 + frac_recRAV3_vaccinatedB1 \
             + frac_recRAPV_vaccinatedB1_fromV1Campaign + frac_recRAPV_vaccinatedB1_fromV2Campaign + frac_recRAPV_vaccinatedB1_fromV3Campaign

    dRH_B1 = gammaH * H_B1 - 2 * gammaRHB[0] * RH_B1 \
             + frac_recRHP_vaccinatedV1 + frac_recRHV1_vaccinatedB1 + frac_recRHV2_vaccinatedB1 + frac_recRHV3_vaccinatedB1 \
             + frac_recRHPV_vaccinatedB1_fromV1Campaign + frac_recRHPV_vaccinatedB1_fromV2Campaign + frac_recRHPV_vaccinatedB1_fromV3Campaign

    dR_RB1 = 2 * gammaRB[0] * R_B1 - 2 * gammaRB[0] * R_RB1 \
             + frac_recRRP_vaccinatedV1 + frac_recRRV1_vaccinatedB1 + frac_recRRV2_vaccinatedB1 + frac_recRRV3_vaccinatedB1 \
             + frac_recRRPV_vaccinatedB1_fromV1Campaign + frac_recRRPV_vaccinatedB1_fromV2Campaign + frac_recRRPV_vaccinatedB1_fromV3Campaign

    dRA_RB1 = 2 * gammaRAB[0] * RA_B1 - 2 * gammaRAB[0] * RA_RB1 \
              + frac_recRARP_vaccinatedV1 + frac_recRARV1_vaccinatedB1 + frac_recRARV2_vaccinatedB1 + frac_recRARV3_vaccinatedB1 \
              + frac_recRARPV_vaccinatedB1_fromV1Campaign + frac_recRARPV_vaccinatedB1_fromV2Campaign + frac_recRARPV_vaccinatedB1_fromV3Campaign

    dRH_RB1 = 2 * gammaRHB[0] * RH_B1 - 2 * gammaRHB[0] * RH_RB1 \
              + frac_recRHRP_vaccinatedV1 + frac_recRHRV1_vaccinatedB1 + frac_recRHRV2_vaccinatedB1 + frac_recRHRV3_vaccinatedB1 \
              + frac_recRHRPV_vaccinatedB1_fromV1Campaign + frac_recRHRPV_vaccinatedB1_fromV2Campaign + frac_recRHRPV_vaccinatedB1_fromV3Campaign

    # vaccinated eqs with booster 2

    dS_B2 = frac_susSV1_vaccinatedB2 + frac_susSV2_vaccinatedB2 + frac_susSV3_vaccinatedB2 \
            + frac_susSPV_vaccinatedB2_fromV1Campaign + frac_susSPV_vaccinatedB2_fromV2Campaign + frac_susSPV_vaccinatedB2_fromV3Campaign \
            + 2 * gammaRAV[1] * RA_RV2 + 2 * gammaRV[1] * R_RV2 + 2 * gammaRHV[1] * RH_RV2 \
            + 2 * gammaRAB[1] * RA_RB2 + 2 * gammaRB[1] * R_RB2 + 2 * gammaRHB[1] * RH_RB2 \
            - one_minus_VESUSB[1] * np.multiply(mylambda, S_B2) - gammaSB[1] * S_B2

    dE_B2 = one_minus_VESUSB[1] * np.multiply(mylambda, S_B2) - gammaE * E_B2

    dA_B2 = gammaE * np.multiply(E_B2, one_minus_one_minus_frac_VESYMPB[1]) - gammaA * A_B2

    dP_B2 = gammaE * np.multiply(E_B2, one_minus_frac_VESYMPB[1]) - gammaP * P_B2

    dI_B2 = gammaP * P_B2 - gammaI * np.multiply(I_B2, one_minus_one_minus_frac_VEHB[1])\
            - sigma * np.multiply(I_B2, one_minus_frac_VEHB[1])

    dH_B2 = sigma * np.multiply(I_B2, one_minus_frac_VEHB[1]) - gammaH * H_B2 - deathRate * H_B2

    dR_B2 = gammaI * np.multiply(I_B2, one_minus_one_minus_frac_VEHB[1]) - 2 * gammaRB[1] * R_B2 \
            + frac_recRP_vaccinatedV2 + frac_recRV1_vaccinatedB2 + frac_recRV2_vaccinatedB2 + frac_recRV3_vaccinatedB2 \
            + frac_recRPV_vaccinatedB2_fromV1Campaign + frac_recRPV_vaccinatedB2_fromV2Campaign + frac_recRPV_vaccinatedB2_fromV3Campaign

    dRA_B2 = gammaA * A_B2 - 2 * gammaRAB[1] * RA_B2 \
             + frac_recRAP_vaccinatedV2 + frac_recRAV1_vaccinatedB2 + frac_recRAV2_vaccinatedB2 + frac_recRAV3_vaccinatedB2 \
             + frac_recRAPV_vaccinatedB2_fromV1Campaign + frac_recRAPV_vaccinatedB2_fromV2Campaign + frac_recRAPV_vaccinatedB2_fromV3Campaign

    dRH_B2 = gammaH * H_B2 - 2 * gammaRHB[1] * RH_B2 \
             + frac_recRHP_vaccinatedV2 + frac_recRHV1_vaccinatedB2 + frac_recRHV2_vaccinatedB2 + frac_recRHV3_vaccinatedB2 \
             + frac_recRHPV_vaccinatedB2_fromV1Campaign + frac_recRHPV_vaccinatedB2_fromV2Campaign + frac_recRHPV_vaccinatedB2_fromV3Campaign

    dR_RB2 = 2 * gammaRB[1] * R_B2 - 2 * gammaRB[1] * R_RB2 \
             + frac_recRRP_vaccinatedV2 + frac_recRRV1_vaccinatedB2 + frac_recRRV2_vaccinatedB2 + frac_recRRV3_vaccinatedB2 \
             + frac_recRRPV_vaccinatedB2_fromV1Campaign + frac_recRRPV_vaccinatedB2_fromV2Campaign + frac_recRRPV_vaccinatedB2_fromV3Campaign

    dRA_RB2 = 2 * gammaRAB[1] * RA_B2 - 2 * gammaRAB[1] * RA_RB2 \
              + frac_recRARP_vaccinatedV2 + frac_recRARV1_vaccinatedB2 + frac_recRARV2_vaccinatedB2 + frac_recRARV3_vaccinatedB2 \
              + frac_recRARPV_vaccinatedB2_fromV1Campaign + frac_recRARPV_vaccinatedB2_fromV2Campaign + frac_recRARPV_vaccinatedB2_fromV3Campaign

    dRH_RB2 = 2 * gammaRHB[1] * RH_B2 - 2 * gammaRHB[1] * RH_RB2 \
              + frac_recRHRP_vaccinatedV2 + frac_recRHRV1_vaccinatedB2 + frac_recRHRV2_vaccinatedB2 + frac_recRHRV3_vaccinatedB2 \
              + frac_recRHRPV_vaccinatedB2_fromV1Campaign + frac_recRHRPV_vaccinatedB2_fromV2Campaign + frac_recRHRPV_vaccinatedB2_fromV3Campaign

    # vaccinated eqs with booster 3

    dS_B3 = frac_susSV1_vaccinatedB3 + frac_susSV2_vaccinatedB3 + frac_susSV3_vaccinatedB3 \
            + frac_susSPV_vaccinatedB3_fromV1Campaign + frac_susSPV_vaccinatedB3_fromV2Campaign + frac_susSPV_vaccinatedB3_fromV3Campaign \
            + 2 * gammaRAV[2] * RA_RV3 + 2 * gammaRV[2] * R_RV3 + 2 * gammaRHV[2] * RH_RV3 \
            + 2 * gammaRAB[2] * RA_RB3 + 2 * gammaRB[2] * R_RB3 + 2 * gammaRHB[2] * RH_RB3 \
            - one_minus_VESUSB[2] * np.multiply(mylambda, S_B3) - gammaSB[2] * S_B3

    dE_B3 = one_minus_VESUSB[2] * np.multiply(mylambda, S_B3) - gammaE * E_B3

    dA_B3 = gammaE * np.multiply(E_B3, one_minus_one_minus_frac_VESYMPB[2]) - gammaA * A_B3

    dP_B3 = gammaE * np.multiply(E_B3, one_minus_frac_VESYMPB[2]) - gammaP * P_B3

    dI_B3 = gammaP * P_B3 - gammaI * np.multiply(I_B3, one_minus_one_minus_frac_VEHB[2]) \
            - sigma * np.multiply(I_B3,one_minus_frac_VEHB[2])

    dH_B3 = sigma * np.multiply(I_B3, one_minus_frac_VEHB[2]) - gammaH * H_B3 - deathRate * H_B3

    dR_B3 = gammaI * np.multiply(I_B3, one_minus_one_minus_frac_VEHB[2]) - 2 * gammaRB[2] * R_B3 \
            + frac_recRP_vaccinatedV3 + frac_recRV1_vaccinatedB3 + frac_recRV2_vaccinatedB3 + frac_recRV3_vaccinatedB3 \
            + frac_recRPV_vaccinatedB3_fromV1Campaign + frac_recRPV_vaccinatedB3_fromV2Campaign + frac_recRPV_vaccinatedB3_fromV3Campaign

    dRA_B3 = gammaA * A_B3 - 2 * gammaRAB[2] * RA_B3 \
             + frac_recRAP_vaccinatedV3 + frac_recRAV1_vaccinatedB3 + frac_recRAV2_vaccinatedB3 + frac_recRAV3_vaccinatedB3 \
             + frac_recRAPV_vaccinatedB3_fromV1Campaign + frac_recRAPV_vaccinatedB3_fromV2Campaign + frac_recRAPV_vaccinatedB3_fromV3Campaign

    dRH_B3 = gammaH * H_B3 - 2 * gammaRHB[2] * RH_B3 \
             + frac_recRHP_vaccinatedV3 + frac_recRHV1_vaccinatedB3 + frac_recRHV2_vaccinatedB3 + frac_recRHV3_vaccinatedB3 \
             + frac_recRHPV_vaccinatedB3_fromV1Campaign + frac_recRHPV_vaccinatedB3_fromV2Campaign + frac_recRHPV_vaccinatedB3_fromV3Campaign

    dR_RB3 = 2 * gammaRB[2] * R_B3 - 2 * gammaRB[2] * R_RB3 \
             + frac_recRRP_vaccinatedV3 + frac_recRRV1_vaccinatedB3 + frac_recRRV2_vaccinatedB3 + frac_recRRV3_vaccinatedB3 \
             + frac_recRRPV_vaccinatedB3_fromV1Campaign + frac_recRRPV_vaccinatedB3_fromV2Campaign + frac_recRRPV_vaccinatedB3_fromV3Campaign

    dRA_RB3 = 2 * gammaRAB[2] * RA_B3 - 2 * gammaRAB[2] * RA_RB3 \
              + frac_recRARP_vaccinatedV3 + frac_recRARV1_vaccinatedB3 + frac_recRARV2_vaccinatedB3 + frac_recRARV3_vaccinatedB3 \
              + frac_recRARPV_vaccinatedB3_fromV1Campaign + frac_recRARPV_vaccinatedB3_fromV2Campaign + frac_recRARPV_vaccinatedB3_fromV3Campaign

    dRH_RB3 = 2 * gammaRHB[2] * RH_B3 - 2 * gammaRHB[2] * RH_RB3 \
              + frac_recRHRP_vaccinatedV3 + frac_recRHRV1_vaccinatedB3 + frac_recRHRV2_vaccinatedB3 + frac_recRHRV3_vaccinatedB3 \
              + frac_recRHRPV_vaccinatedB3_fromV1Campaign + frac_recRHRPV_vaccinatedB3_fromV2Campaign + frac_recRHRPV_vaccinatedB3_fromV3Campaign

    ddeaths = deathRate * (H + H_P + H_PV + H_V1 + H_V2 + H_V3 + H_B1 + H_B2 + H_B3)

    dydt = np.array([dS, dE, dA, dP, dI, dH, dR, dRA, dRH, dR_R, dRA_R, dRH_R,
                     dS_P, dE_P, dA_P, dP_P, dI_P, dH_P, dR_P, dRA_P, dRH_P, dR_RP, dRA_RP, dRH_RP,
                     dS_PV, dE_PV, dA_PV, dP_PV, dI_PV, dH_PV, dR_PV, dRA_PV, dRH_PV, dR_RPV, dRA_RPV, dRH_RPV,
                     dS_V1, dE_V1, dA_V1, dP_V1, dI_V1, dH_V1, dR_V1, dRA_V1, dRH_V1, dR_RV1, dRA_RV1, dRH_RV1,
                     dS_V2, dE_V2, dA_V2, dP_V2, dI_V2, dH_V2, dR_V2, dRA_V2, dRH_V2, dR_RV2, dRA_RV2, dRH_RV2,
                     dS_V3, dE_V3, dA_V3, dP_V3, dI_V3, dH_V3, dR_V3, dRA_V3, dRH_V3, dR_RV3, dRA_RV3, dRH_RV3,
                     dS_B1, dE_B1, dA_B1, dP_B1, dI_B1, dH_B1, dR_B1, dRA_B1, dRH_B1, dR_RB1, dRA_RB1, dRH_RB1,
                     dS_B2, dE_B2, dA_B2, dP_B2, dI_B2, dH_B2, dR_B2, dRA_B2, dRH_B2, dR_RB2, dRA_RB2, dRH_RB2,
                     dS_B3, dE_B3, dA_B3, dP_B3, dI_B3, dH_B3, dR_B3, dRA_B3, dRH_B3, dR_RB3, dRA_RB3, dRH_RB3,
                     ddeaths
                     ]).reshape((numGroups * 109))  # 545 EQS
    return dydt

