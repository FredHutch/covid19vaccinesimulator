import { DateTime } from "luxon";

export var systemName = "Covid19Vaxplorer"; // 'Vaccine Allocator';

export const fileFormatVersion = "0.0.1";

export const  propor0to100OutOfScopeMsg = "All numbers should be between 0 - 100. Please adjust before moving on.";

export const  proporSumOver100Msg = "The sum of all numbers should be between 0 - 100. Please adjust before moving on.";


export const  fulldoseLessThanTotalMsg = "Not all proportion of the primary series is allocated.";
export const  fulldoseMoreThanTotalMsg = "Can not allocate more than the available proportion for the primary series. Please reduce the proportion for certain age groups.";
export const  boosterLessThanTotalMsg = "Not all proportion of the booster is allocated.";
export const  boosterMoreThanTotalMsg = "Can not allocate more than the available proportion for the booster. Please reduce the proportion for certain age groups.";
export const  lessThan100Msg = "Not all 100% of vaccine is allocated.";
export const  moreThan100Msg = "Can not allocate more than 100% of the vaccines. Please reduce the proportion for certain age groups.";


let nowDate = DateTime.now(); //.utc().startOf("day");
let jsDate = nowDate.toJSDate();
let nowDateString = nowDate.toISO();

console.log(`nowDateString: ${nowDateString}`);


export var colorList = ["#ffa600", "#ff6361", "#bc5090", "#58508d", "#003f5c"];

export var vaccineList = [
  {
    name: "None",
    code: "NONE",
    type: "pre-defined",
    efficacyData: [
      {
        category: "Infection",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Symptomatic infection",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Hospitalization",
        fulldose: 0,
        booster: 0,
      },
      /*
      {
        category: "Infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Symptomatic infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Hospitalization after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      */
    ],
  },
  {
    name: "COMIRNATY (Pfizer/BioNTech)",
    code: "COMIRNATY",
    type: "pre-defined",
    efficacyData: [
      {
        category: "Infection",
        fulldose: 44,
        booster: 86,
      },
      {
        category: "Symptomatic infection",
        fulldose: 30,
        booster: 88,
      },
      {
        category: "Hospitalization",
        fulldose: 72,
        booster: 95,
      },
      /*
      {
        category: "Infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Symptomatic infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Hospitalization after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      */
    ],
  },
  {
    name: "VAXZEVRIA (AstraZeneca)",
    code: "VAXZEVRIA",
    type: "pre-defined",
    efficacyData: [
      {
        category: "Infection",
        fulldose: 36,
        booster: 63,
      },
      {
        category: "Symptomatic infection",
        fulldose: 29,
        booster: 63,
      },
      {
        category: "Hospitalization",
        fulldose: 71,
        booster: 94,
      },
      /*
      {
        category: "Infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Symptomatic infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Hospitalization after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      */
    ],
  },
  {
    name: "COVISHIELD",
    code: "COVISHIELD",
    type: "pre-defined",
    efficacyData: [
      {
        category: "Infection",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Symptomatic infection",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Hospitalization",
        fulldose: 0,
        booster: 0,
      },
      /*
      {
        category: "Infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Symptomatic infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Hospitalization after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      */
    ],
  },
  {
    name: "JANSEN (Johnson & Johnson)",
    code: "JANSEN",
    type: "pre-defined",
    efficacyData: [
      {
        category: "Infection",
        fulldose: 33,
        booster: 72,
      },
      {
        category: "Symptomatic infection",
        fulldose: 26,
        booster: 67,
      },
      {
        category: "Hospitalization",
        fulldose: 57,
        booster: 86,
      },
      /*
      {
        category: "Infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Symptomatic infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Hospitalization after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      */
    ],
  },
  {
    name: "SPIKEVAX (Moderna)",
    code: "SPIKEVAX",
    type: "pre-defined",
    efficacyData: [
      {
        category: "Infection",
        fulldose: 48,
        booster: 92,
      },
      {
        category: "Symptomatic infection",
        fulldose: 36,
        booster: 92,
      },
      {
        category: "Hospitalization",
        fulldose: 73,
        booster: 97,
      },
      /*
      {
        category: "Infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Symptomatic infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Hospitalization after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      */
    ],
  },
  {
    name: "VERO CELL (SINOPHARM)",
    code: "VERO CELL",
    type: "pre-defined",
    efficacyData: [
      {
        category: "Infection",
        fulldose: 35,
        booster: 68,
      },
      {
        category: "Symptomatic infection",
        fulldose: 31,
        booster: 78,
      },
      {
        category: "Hospitalization",
        fulldose: 53,
        booster: 73,
      },
      /*
      {
        category: "Infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Symptomatic infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Hospitalization after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      */
    ],
  },
  {
    name: "CORONAVAC (Sinovac)",
    code: "CORONAVAC",
    type: "pre-defined",
    efficacyData: [
      {
        category: "Infection",
        fulldose: 24,
        booster: 50,
      },
      {
        category: "Symptomatic infection",
        fulldose: 26,
        booster: 47,
      },
      {
        category: "Hospitalization",
        fulldose: 37,
        booster: 65,
      },
      /*
      {
        category: "Infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Symptomatic infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Hospitalization after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      */
    ],
  },
  {
    name: "COVOVAX",
    code: "COVOVAX",
    type: "pre-defined",
    efficacyData: [
      {
        category: "Infection",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Symptomatic infection",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Hospitalization",
        fulldose: 0,
        booster: 0,
      },
      /*
      {
        category: "Infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Symptomatic infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Hospitalization after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      */
    ],
  },
  {
    name: "NUVAXOVID (Novavax)",
    code: "NUVAXOVID",
    type: "pre-defined",
    efficacyData: [
      {
        category: "Infection",
        fulldose: 43,
        booster: 83,
      },
      {
        category: "Symptomatic infection",
        fulldose: 36,
        booster: 90,
      },
      {
        category: "Hospitalization",
        fulldose: 65,
        booster: 89,
      },
      /*
      {
        category: "Infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Symptomatic infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Hospitalization after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      */
    ],
  },
  {
    name: "CONVIDECIA (CanSino)",
    code: "CONVIDECIA",
    type: "pre-defined",
    efficacyData: [
      {
        category: "Infection",
        fulldose: 32,
        booster: 62,
      },
      {
        category: "Symptomatic infection",
        fulldose: 26,
        booster: 66,
      },
      {
        category: "Hospitalization",
        fulldose: 48,
        booster: 66,
      },
      /*
      {
        category: "Infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Symptomatic infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Hospitalization after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      */
    ],
  },
  // "customized"
  {
    name: "(Enter vaccine name here)",
    code: "(customized)",
    type: "customized",
    efficacyData: [
      {
        category: "Infection",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Symptomatic infection",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Hospitalization",
        fulldose: 0,
        booster: 0,
      },
      /*
      {
        category: "Infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Symptomatic infection after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      {
        category: "Hospitalization after 6 months (wanned)",
        fulldose: 0,
        booster: 0,
      },
      */
    ],
  },
];

export var regionList = [
  {
    name: "Afghanistan",
    code: "AFG",
    populationList: [20910291, 14533976, 2452836, 757309, 273929],
  },
  {
    name: "Albania",
    code: "ALB",
    populationList: [695610, 1186471, 572550, 251915, 171254],
  },
  {
    name: "Algeria",
    code: "DZA",
    populationList: [16409237, 19297569, 5187398, 1867138, 1089700],
  },
  {
    name: "Angola",
    code: "AGO",
    populationList: [18780947, 11418501, 1946570, 516442, 203808],
  },
  {
    name: "Argentina",
    code: "ARG",
    populationList: [14583179, 19166740, 6308673, 2982232, 2154953],
  },
  {
    name: "Armenia",
    code: "ARM",
    populationList: [787789, 1265965, 559734, 215664, 134082],
  },
  {
    name: "Australia",
    code: "AUS",
    populationList: [6439454, 10399858, 4526261, 2316040, 1818268],
  },
  {
    name: "Austria",
    code: "AUT",
    populationList: [1750390, 3537058, 1989363, 858245, 871343],
  },
  {
    name: "Azerbaijan",
    code: "AZE",
    populationList: [3021496, 4656480, 1777662, 459761, 223775],
  },
  {
    name: "Bahamas",
    code: "BHS",
    populationList: [117449, 178521, 66806, 19869, 10602],
  },
  {
    name: "Bahrain",
    code: "BHR",
    populationList: [399990, 1071124, 185351, 32410, 12708],
  },
  {
    name: "Bangladesh",
    code: "BGD",
    populationList: [59647032, 76927936, 19506092, 5153607, 3454716],
  },
  {
    name: "Barbados",
    code: "BRB",
    populationList: [67130, 113769, 58476, 26922, 21074],
  },
  {
    name: "Belarus",
    code: "BLR",
    populationList: [2072723, 3893551, 2010825, 847756, 624466],
  },
  {
    name: "Belgium",
    code: "BEL",
    populationList: [2614954, 4408521, 2334648, 1189567, 1041926],
  },
  {
    name: "Belize",
    code: "BLZ",
    populationList: [155956, 179492, 42260, 12383, 7529],
  },
  {
    name: "Benin",
    code: "BEN",
    populationList: [6376436, 4480043, 869267, 271638, 125814],
  },
  {
    name: "Bhutan",
    code: "BTN",
    populationList: [261821, 381599, 80317, 28359, 19516],
  },
  {
    name: "Bolivia (Plurinational State of)",
    code: "BOL",
    populationList: [4662283, 4916976, 1219783, 504567, 369420],
  },
  {
    name: "Bosnia and Herzegovina",
    code: "BIH",
    populationList: [641487, 1309395, 742149, 365256, 222528],
  },
  {
    name: "Botswana",
    code: "BWA",
    populationList: [1011038, 1028813, 205668, 74712, 31394],
  },
  {
    name: "Brazil",
    code: "BRA",
    populationList: [60237356, 98043411, 33889361, 12738122, 7651159],
  },
  {
    name: "Brunei Darussalam",
    code: "BRN",
    populationList: [131439, 214267, 67407, 17538, 6831],
  },
  {
    name: "Bulgaria",
    code: "BGR",
    populationList: [1335263, 2709493, 1412002, 879894, 611792],
  },
  {
    name: "Burkina Faso",
    code: "BFA",
    populationList: [11581731, 7523231, 1294332, 370056, 133928],
  },
  {
    name: "Burundi",
    code: "BDI",
    populationList: [6597739, 4316760, 693265, 208710, 74307],
  },
  {
    name: "Cabo Verde",
    code: "CPV",
    populationList: [205013, 261037, 63326, 15690, 10922],
  },
  {
    name: "Cambodia",
    code: "KHM",
    populationList: [6630656, 7435960, 1841003, 584495, 226856],
  },
  {
    name: "Cameroon",
    code: "CMR",
    populationList: [14022485, 10093472, 1708877, 522811, 198219],
  },
  {
    name: "Canada",
    code: "CAN",
    populationList: [7942241, 15221944, 7744998, 3943032, 2889942],
  },
  {
    name: "Central African Republic",
    code: "CAF",
    populationList: [2700217, 1680854, 313550, 95792, 39351],
  },
  {
    name: "Chad",
    code: "TCD",
    populationList: [9491277, 5633494, 890671, 293509, 116908],
  },
  {
    name: "Chile",
    code: "CHL",
    populationList: [4921958, 8519346, 3334570, 1390787, 949547],
  },
  {
    name: "China",
    code: "CHN",
    populationList: [337272230, 630089358, 299700012, 119099455, 53162719],
  },
  {
    name: "China, Hong Kong SAR",
    code: "HKG",
    populationList: [1216854, 3118924, 1796996, 803918, 560296],
  },
  {
    name: "China, Macao SAR",
    code: "MAC",
    populationList: [115651, 311536, 144418, 54850, 22887],
  },
  {
    name: "Colombia",
    code: "COL",
    populationList: [15534031, 23108147, 7630430, 2872544, 1737731],
  },
  {
    name: "Comoros",
    code: "COM",
    populationList: [428906, 345258, 68426, 19267, 7738],
  },
  {
    name: "Congo",
    code: "COG",
    populationList: [2850299, 2090154, 425187, 111313, 41138],
  },
  {
    name: "Costa Rica",
    code: "CRI",
    populationList: [1424435, 2300673, 846702, 317341, 204963],
  },
  {
    name: "Cote d'Ivoire",
    code: "CIV",
    populationList: [13855144, 9950761, 1811995, 561933, 198441],
  },
  {
    name: "Croatia",
    code: "HRV",
    populationList: [793882, 1568493, 870431, 482366, 390096],
  },
  {
    name: "Cuba",
    code: "CUB",
    populationList: [2446108, 4506034, 2574289, 1016157, 784027],
  },
  {
    name: "Cyprus",
    code: "CYP",
    populationList: [274050, 546819, 212527, 101256, 72709],
  },
  {
    name: "Czechia",
    code: "CZE",
    populationList: [2174977, 4381903, 1994992, 1293670, 863439],
  },
  {
    name: "Dem. People's Republic of Korea",
    code: "PRK",
    populationList: [6991600, 11281926, 5095303, 1407248, 1002738],
  },
  {
    name: "Democratic Republic of the Congo",
    code: "COD",
    populationList: [50487326, 30537099, 5833414, 1888440, 815125],
  },
  {
    name: "Denmark",
    code: "DNK",
    populationList: [1281977, 2186459, 1155829, 660128, 507810],
  },
  {
    name: "Djibouti",
    code: "DJI",
    populationList: [376430, 460666, 104405, 31943, 14558],
  },
  {
    name: "Dominican Republic",
    code: "DOM",
    populationList: [3935223, 4693188, 1402899, 497725, 318869],
  },
  {
    name: "Ecuador",
    code: "ECU",
    populationList: [6393715, 7717267, 2192773, 814174, 525131],
  },
  {
    name: "Egypt",
    code: "EGY",
    populationList: [43413971, 42658081, 10806207, 3826961, 1629183],
  },
  {
    name: "El Salvador",
    code: "SLV",
    populationList: [2312646, 2823398, 789038, 324934, 236185],
  },
  {
    name: "Equatorial Guinea",
    code: "GNQ",
    populationList: [636960, 650728, 81885, 24335, 9077],
  },
  {
    name: "Eritrea",
    code: "ERI",
    populationList: [1832395, 1313842, 240371, 107129, 52690],
  },
  {
    name: "Estonia",
    code: "EST",
    populationList: [281149, 524123, 251008, 136894, 133365],
  },
  {
    name: "Eswatini",
    code: "SWZ",
    populationList: [563638, 478615, 71356, 30434, 16120],
  },
  {
    name: "Ethiopia",
    code: "ETH",
    populationList: [58866542, 44270576, 7760330, 2756725, 1309410],
  },
  {
    name: "Fiji",
    code: "FJI",
    populationList: [335275, 383422, 125597, 38376, 13774],
  },
  {
    name: "Finland",
    code: "FIN",
    populationList: [1175339, 2038493, 1077203, 713279, 536404],
  },
  {
    name: "France",
    code: "FRA",
    populationList: [15410951, 23707746, 12608305, 7315154, 6231356],
  },
  {
    name: "Gabon",
    code: "GAB",
    populationList: [1022776, 949643, 174765, 52760, 25784],
  },
  {
    name: "Gambia",
    code: "GMB",
    populationList: [1319167, 886377, 149947, 44252, 16921],
  },
  {
    name: "Georgia",
    code: "GEO",
    populationList: [1024220, 1583720, 772753, 361114, 247368],
  },
  {
    name: "Germany",
    code: "DEU",
    populationList: [15811520, 30492732, 19309096, 8657262, 9513335],
  },
  {
    name: "Ghana",
    code: "GHA",
    populationList: [14674592, 12620259, 2802291, 722099, 253703],
  },
  {
    name: "Greece",
    code: "GRC",
    populationList: [1949982, 3968140, 2182222, 1130098, 1192613],
  },
  {
    name: "Guatemala",
    code: "GTM",
    populationList: [7919072, 7647216, 1445969, 548130, 355180],
  },
  {
    name: "Guinea",
    code: "GIN",
    populationList: [7165078, 4735044, 844951, 283558, 104161],
  },
  {
    name: "Guinea-Bissau",
    code: "GNB",
    populationList: [1032378, 753465, 125363, 42850, 13942],
  },
  {
    name: "Guyana",
    code: "GUY",
    populationList: [292979, 328940, 109582, 36135, 18923],
  },
  {
    name: "Haiti",
    code: "HTI",
    populationList: [4847308, 4882600, 1082578, 381790, 208257],
  },
  {
    name: "Honduras",
    code: "HND",
    populationList: [4070630, 4424091, 917313, 305507, 187067],
  },
  {
    name: "Hungary",
    code: "HUN",
    populationList: [1877773, 3997045, 1837707, 1145884, 801941],
  },
  {
    name: "Iceland",
    code: "ISL",
    populationList: [87778, 137635, 62522, 31066, 22249],
  },
  {
    name: "India",
    code: "IND",
    populationList: [487063152, 625198523, 177022758, 62351726, 28368226],
  },
  {
    name: "Indonesia",
    code: "IDN",
    populationList: [94259451, 122584773, 39549945, 11753908, 5375544],
  },
  {
    name: "Iran (Islamic Republic of)",
    code: "IRN",
    populationList: [26313784, 40737969, 11427605, 3712632, 1800962],
  },
  {
    name: "Iraq",
    code: "IRQ",
    populationList: [19320987, 16505893, 3010868, 954622, 430133],
  },
  {
    name: "Ireland",
    code: "IRL",
    populationList: [1340690, 2026493, 850781, 427743, 292088],
  },
  {
    name: "Israel",
    code: "ISR",
    populationList: [3076159, 3359397, 1145453, 642385, 432147],
  },
  {
    name: "Italy",
    code: "ITA",
    populationList: [10728443, 22123874, 13520759, 6923093, 7165659],
  },
  {
    name: "Jamaica",
    code: "JAM",
    populationList: [931389, 1316309, 444658, 161135, 107670],
  },
  {
    name: "Japan",
    code: "JPN",
    populationList: [21447140, 45075816, 24037637, 17506431, 18409434],
  },
  {
    name: "Jordan",
    code: "JOR",
    populationList: [4392416, 4434489, 972830, 260567, 142838],
  },
  {
    name: "Kazakhstan",
    code: "KAZ",
    populationList: [6588933, 7853108, 2850779, 947553, 536334],
  },
  {
    name: "Kenya",
    code: "KEN",
    populationList: [26760789, 21967465, 3693818, 1011678, 337550],
  },
  {
    name: "Kuwait",
    code: "KWT",
    populationList: [1141552, 2288807, 710562, 103152, 26490],
  },
  {
    name: "Kyrgyzstan",
    code: "KGZ",
    populationList: [2630151, 2784080, 801504, 222374, 86082],
  },
  {
    name: "Lao People's Democratic Republic",
    code: "LAO",
    populationList: [3032993, 3221838, 710847, 218338, 91540],
  },
  {
    name: "Latvia",
    code: "LVA",
    populationList: [396493, 705332, 394173, 194934, 195270],
  },
  {
    name: "Lebanon",
    code: "LBN",
    populationList: [2287154, 3048963, 974069, 329957, 185299],
  },
  {
    name: "Lesotho",
    code: "LSO",
    populationList: [907569, 932724, 195941, 71331, 34687],
  },
  {
    name: "Liberia",
    code: "LBR",
    populationList: [2593841, 1914857, 381140, 116165, 51674],
  },
  {
    name: "Libya",
    code: "LBY",
    populationList: [2471165, 3308084, 781058, 200146, 110834],
  },
  {
    name: "Lithuania",
    code: "LTU",
    populationList: [543516, 1010352, 607141, 274685, 286597],
  },
  {
    name: "Luxembourg",
    code: "LUX",
    populationList: [131807, 278449, 125637, 49565, 40518],
  },
  {
    name: "Madagascar",
    code: "MDG",
    populationList: [14105865, 10657502, 2069040, 610655, 247956],
  },
  {
    name: "Malawi",
    code: "MWI",
    populationList: [10400572, 7100282, 1123770, 355392, 149939],
  },
  {
    name: "Malaysia",
    code: "MYS",
    populationList: [10258958, 15412119, 4369854, 1585428, 739639],
  },
  {
    name: "Maldives",
    code: "MDV",
    populationList: [132259, 341940, 46923, 10938, 8482],
  },
  {
    name: "Mali",
    code: "MLI",
    populationList: [11769781, 6850234, 1129177, 362466, 139176],
  },
  {
    name: "Malta",
    code: "MLT",
    populationList: [84029, 180011, 83343, 55519, 38637],
  },
  {
    name: "Mauritania",
    code: "MRT",
    populationList: [2315383, 1830313, 356201, 103708, 44055],
  },
  {
    name: "Mauritius",
    code: "MUS",
    populationList: [308050, 554007, 250484, 107429, 51797],
  },
  {
    name: "Mexico",
    code: "MEX",
    populationList: [44519716, 57163381, 17427425, 6062206, 3760025],
  },
  {
    name: "Mongolia",
    code: "MNG",
    populationList: [1237918, 1487342, 411661, 96377, 44994],
  },
  {
    name: "Montenegro",
    code: "MNE",
    populationList: [152480, 256466, 120074, 61725, 37316],
  },
  {
    name: "Morocco",
    code: "MAR",
    populationList: [12849811, 15942066, 5311022, 1849886, 957773],
  },
  {
    name: "Mozambique",
    code: "MOZ",
    populationList: [17313240, 11172522, 1875197, 630852, 263624],
  },
  {
    name: "Myanmar",
    code: "MMR",
    populationList: [18937905, 24456050, 7622797, 2445682, 947360],
  },
  {
    name: "Namibia",
    code: "NAM",
    populationList: [1180960, 1067113, 201725, 60350, 30768],
  },
  {
    name: "Nepal",
    code: "NPL",
    populationList: [11583113, 12724769, 3130791, 1138720, 559415],
  },
  {
    name: "Netherlands",
    code: "NLD",
    populationList: [3706455, 6346447, 3649029, 1956993, 1475949],
  },
  {
    name: "New Zealand",
    code: "NZL",
    populationList: [1240237, 1882175, 910504, 454105, 335212],
  },
  {
    name: "Nicaragua",
    code: "NIC",
    populationList: [2557307, 2984489, 706650, 232833, 143274],
  },
  {
    name: "Niger",
    code: "NER",
    populationList: [14659151, 7505066, 1413994, 467259, 161166],
  },
  {
    name: "Nigeria",
    code: "NGA",
    populationList: [111555631, 74582930, 14356794, 4318815, 1325417],
  },
  {
    name: "North Macedonia",
    code: "MKD",
    populationList: [461003, 908861, 411897, 194756, 106863],
  },
  {
    name: "Norway",
    code: "NOR",
    populationList: [1257354, 2190037, 1023691, 541753, 408407],
  },
  {
    name: "Oman",
    code: "OMN",
    populationList: [1362877, 3210332, 405184, 81466, 46763],
  },
  {
    name: "Pakistan",
    code: "PAK",
    populationList: [98889668, 91995132, 20401703, 6329068, 3276759],
  },
  {
    name: "Panama",
    code: "PAN",
    populationList: [1500388, 1853245, 592706, 214524, 153904],
  },
  {
    name: "Papua New Guinea",
    code: "PNG",
    populationList: [4068231, 3713105, 846139, 244863, 74689],
  },
  {
    name: "Paraguay",
    code: "PRY",
    populationList: [2720189, 3157807, 768740, 309296, 176498],
  },
  {
    name: "Peru",
    code: "PER",
    populationList: [10580004, 14953611, 4561351, 1761246, 1115634],
  },
  {
    name: "Philippines",
    code: "PHL",
    populationList: [43383989, 47397268, 12760106, 4147114, 1892608],
  },
  {
    name: "Poland",
    code: "POL",
    populationList: [7494007, 15971922, 7288428, 4304740, 2787508],
  },
  {
    name: "Portugal",
    code: "PRT",
    populationList: [1856242, 3864918, 2153526, 1188248, 1133773],
  },
  {
    name: "Puerto Rico",
    code: "PRI",
    populationList: [634990, 1019514, 610500, 322299, 273537],
  },
  {
    name: "Qatar",
    code: "QAT",
    populationList: [498936, 2025351, 308110, 40711, 7952],
  },
  {
    name: "Republic of Korea",
    code: "KOR",
    populationList: [8907071, 22014977, 12251265, 4677231, 3418639],
  },
  {
    name: "Republic of Moldova",
    code: "MDA",
    populationList: [843344, 1907517, 779140, 335579, 168382],
  },
  {
    name: "Romania",
    code: "ROU",
    populationList: [3980353, 7698632, 3859118, 2173446, 1526133],
  },
  {
    name: "Russian Federation",
    code: "RUS",
    populationList: [33878644, 60451657, 28971289, 13818127, 8814743],
  },
  {
    name: "Rwanda",
    code: "RWA",
    populationList: [6466818, 5093691, 987684, 295381, 108635],
  },
  {
    name: "Saint Lucia",
    code: "LCA",
    populationList: [46147, 86780, 31792, 11018, 7892],
  },
  {
    name: "Saint Vincent and the Grenadines",
    code: "VCT",
    populationList: [33375, 47697, 18879, 6608, 4388],
  },
  {
    name: "Samoa",
    code: "WSM",
    populationList: [93121, 72867, 22335, 6837, 3249],
  },
  {
    name: "Sao Tome and Principe",
    code: "STP",
    populationList: [116520, 78936, 17112, 4494, 2098],
  },
  {
    name: "Saudi Arabia",
    code: "SAU",
    populationList: [10816497, 18743912, 4035509, 847625, 370323],
  },
  {
    name: "Senegal",
    code: "SEN",
    populationList: [8896283, 6206654, 1120566, 365521, 154906],
  },
  {
    name: "Serbia",
    code: "SRB",
    populationList: [1855551, 3547244, 1669362, 1058758, 606455],
  },
  {
    name: "Sierra Leone",
    code: "SLE",
    populationList: [4093081, 3095458, 554932, 166565, 66948],
  },
  {
    name: "Singapore",
    code: "SGP",
    populationList: [984831, 2694546, 1389853, 545922, 235191],
  },
  {
    name: "Slovakia",
    code: "SVK",
    populationList: [1112086, 2364788, 1071055, 570194, 341520],
  },
  {
    name: "Slovenia",
    code: "SVN",
    populationList: [406547, 794469, 446795, 236856, 194264],
  },
  {
    name: "Solomon Islands",
    code: "SLB",
    populationList: [344995, 262550, 54120, 16710, 8503],
  },
  {
    name: "Somalia",
    code: "SOM",
    populationList: [9152954, 5282174, 996847, 334492, 126752],
  },
  {
    name: "South Africa",
    code: "ZAF",
    populationList: [21994779, 27340089, 6706247, 2264943, 1002632],
  },
  {
    name: "South Sudan",
    code: "SSD",
    populationList: [5827583, 4193942, 796902, 255790, 119512],
  },
  {
    name: "Spain",
    code: "ESP",
    populationList: [8970564, 18458091, 9985638, 4605493, 4734997],
  },
  {
    name: "Sri Lanka",
    code: "LKA",
    populationList: [6736255, 8602983, 3668690, 1626755, 778567],
  },
  {
    name: "State of Palestine",
    code: "PSE",
    populationList: [2474021, 2078161, 385170, 112341, 51723],
  },
  {
    name: "Sudan",
    code: "SDN",
    populationList: [22252463, 16557722, 3428007, 1116034, 495042],
  },
  {
    name: "Suriname",
    code: "SUR",
    populationList: [207062, 251282, 86429, 26670, 15191],
  },
  {
    name: "Sweden",
    code: "SWE",
    populationList: [2321078, 3861352, 1863780, 1090884, 962176],
  },
  {
    name: "Switzerland",
    code: "CHE",
    populationList: [1719812, 3425541, 1856445, 863131, 789689],
  },
  {
    name: "Syrian Arab Republic",
    code: "SYR",
    populationList: [6961028, 7936077, 1750492, 566539, 286520],
  },
  {
    name: "Taiwan",
    code: "TWN",
    populationList: [8907071, 22014977, 12251265, 4677231, 3418639],
  },
  {
    name: "Tajikistan",
    code: "TJK",
    populationList: [4365977, 3921252, 947140, 219632, 83640],
  },
  {
    name: "Thailand",
    code: "THA",
    populationList: [15932143, 29774292, 15049047, 5539041, 3505455],
  },
  {
    name: "Timor-Leste",
    code: "TLS",
    populationList: [638594, 504723, 118657, 37892, 18575],
  },
  {
    name: "Togo",
    code: "TGO",
    populationList: [4255177, 3184335, 598726, 179696, 60803],
  },
  {
    name: "Tonga",
    code: "TON",
    populationList: [48161, 39613, 11664, 3985, 2273],
  },
  {
    name: "Trinidad and Tobago",
    code: "TTO",
    populationList: [370261, 617305, 250779, 104136, 57010],
  },
  {
    name: "Tunisia",
    code: "TUN",
    populationList: [3657697, 5211881, 1900378, 674085, 374577],
  },
  {
    name: "Turkey",
    code: "TUR",
    populationList: [27014419, 37395473, 12354623, 4716688, 2857864],
  },
  {
    name: "Turkmenistan",
    code: "TKM",
    populationList: [2341673, 2665497, 736453, 202094, 85470],
  },
  {
    name: "Uganda",
    code: "UGA",
    populationList: [26305376, 16107179, 2420169, 668080, 240196],
  },
  {
    name: "Ukraine",
    code: "UKR",
    populationList: [8973028, 18513853, 8834381, 4381289, 3031208],
  },
  {
    name: "United Arab Emirates",
    code: "ARE",
    populationList: [1854704, 6926766, 983879, 93001, 32049],
  },
  {
    name: "United Kingdom",
    code: "GBR",
    populationList: [15686529, 26457982, 13078481, 6770249, 5892763],
  },
  {
    name: "United Republic of Tanzania",
    code: "TZA",
    populationList: [32451358, 21828904, 3874824, 1146824, 432303],
  },
  {
    name: "United States of America",
    code: "USA",
    populationList: [82053879, 131110742, 62789220, 32173890, 22874915],
  },
  {
    name: "Uruguay",
    code: "URY",
    populationList: [951999, 1427726, 569901, 272908, 251193],
  },
  {
    name: "Uzbekistan",
    code: "UZB",
    populationList: [12174578, 15454682, 4237146, 1115189, 487603],
  },
  {
    name: "Vanuatu",
    code: "VUT",
    populationList: [147811, 120963, 27295, 7836, 3245],
  },
  {
    name: "Venezuela (Bolivarian Republic of)",
    code: "VEN",
    populationList: [10253167, 11723234, 4192424, 1468695, 798423],
  },
  {
    name: "Viet Nam",
    code: "VNM",
    populationList: [29077615, 45163382, 15440922, 4663691, 2992973],
  },
  {
    name: "Yemen",
    code: "YEM",
    populationList: [14783682, 12235988, 1932102, 629161, 245035],
  },
  {
    name: "Zambia",
    code: "ZMB",
    populationList: [10213723, 6779466, 998813, 279044, 112909],
  },
  {
    name: "Zimbabwe",
    code: "ZWE",
    populationList: [7868115, 5608289, 938531, 299631, 148361],
  },
];

// TW data
/*
0 -  20: 3921489
20 - 49: 10057596
50 - 64: 5237628
65 - 74: 2521788
  >= 75: 1457677

3921489 + 10057596 + 5237628 + 2521788 + 1457677 = 23196178
*/

export var regionNameInfectionMap = {
  Afghanistan: 84.8,
  Albania: 86.9,
  Algeria: 18.4,
  Angola: 84.0,
  Argentina: 27.0,
  Armenia: 81.4,
  Australia: 1.4,
  Austria: 22.2,
  Azerbaijan: 77.4,
  Bahamas: 29.5,
  Bahrain: 55.2,
  Bangladesh: 74.3,
  Barbados: 15.4,
  Belarus: 59.4,
  Belgium: 32.0,
  Belize: 38.6,
  Benin: 32.2,
  Bhutan: 2.2,
  "Bolivia (Plurinational State of)": 85.8,
  "Bosnia and Herzegovina": 76.7,
  Botswana: 65.8,
  Brazil: 59.0,
  "Brunei Darussalam": 7.8,
  Bulgaria: 74.3,
  "Burkina Faso": 68.5,
  Burundi: 15.3,
  "Cabo Verde": 65.2,
  Cambodia: 21.7,
  Cameroon: 61.8,
  Canada: 12.4,
  "Central African Republic": 61.9,
  Chad: 54.0,
  Chile: 21.1,
  China: 0.2,
  "China, Hong Kong SAR": 0.2,
  "China, Macao SAR": 0.2,
  Colombia: 45.2,
  Comoros: 67.0,
  Congo: 71.7,
  "Costa Rica": 44.6,
  "Cote d'Ivoire": 68.2,
  Croatia: 55.5,
  Cuba: 17.9,
  Cyprus: 13.9,
  Czechia: 70.1,
  "Dem. People's Republic of Korea": 0.3,
  "Democratic Republic of the Congo": 75.1,
  Denmark: 13.5,
  Djibouti: 58.2,
  "Dominican Republic": 33.3,
  Ecuador: 70.2,
  Egypt: 65.4,
  "El Salvador": 36.0,
  "Equatorial Guinea": 70.2,
  Eritrea: 27.7,
  Estonia: 30.9,
  Eswatini: 67.4,
  Ethiopia: 83.2,
  Fiji: 32.8,
  Finland: 8.6,
  France: 23.3,
  Gabon: 65.5,
  Gambia: 75.2,
  Georgia: 79.4,
  Germany: 14.4,
  Ghana: 62.3,
  Greece: 15.2,
  Guatemala: 62.8,
  Guinea: 77.5,
  "Guinea-Bissau": 65.3,
  Guyana: 42.7,
  Haiti: 29.6,
  Honduras: 81.4,
  Hungary: 53.6,
  Iceland: 7.9,
  India: 64.3,
  Indonesia: 56.6,
  "Iran (Islamic Republic of)": 60.5,
  Iraq: 82.4,
  Ireland: 22.3,
  Israel: 24.3,
  Italy: 19.6,
  Jamaica: 20.6,
  Japan: 5.0,
  Jordan: 64.9,
  Kazakhstan: 58.6,
  Kenya: 84.1,
  Kuwait: 41.9,
  Kyrgyzstan: 76.1,
  "Lao People's Democratic Republic": 17.1,
  Latvia: 49.8,
  Lebanon: 67.3,
  Lesotho: 61.9,
  Liberia: 60.8,
  Libya: 83.8,
  Lithuania: 61.1,
  Luxembourg: 24.1,
  Madagascar: 75.5,
  Malawi: 86.7,
  Malaysia: 31.7,
  Maldives: 35.4,
  Mali: 75.0,
  Malta: 14.9,
  Mauritius: 14.1,
  Mexico: 65.7,
  Mongolia: 58.2,
  Montenegro: 89.4,
  Morocco: 67.2,
  Mozambique: 89.3,
  Myanmar: 31.4,
  Namibia: 66.4,
  Nepal: 73.4,
  Netherlands: 27.1,
  "New Zealand": 0.3,
  Nicaragua: 55.4,
  Niger: 51.0,
  Nigeria: 72.3,
  "North Macedonia": 84.2,
  Norway: 11.2,
  Oman: 42.0,
  Pakistan: 68.3,
  Panama: 40.5,
  "Papua New Guinea": 39.3,
  Paraguay: 62.8,
  Peru: 62.3,
  Philippines: 48.6,
  Poland: 50.6,
  Portugal: 21.9,
  "Puerto Rico": 12.6,
  Qatar: 61.0,
  "Republic of Korea": 1.8,
  Romania: 62.1,
  "Russian Federation": 78.2,
  Rwanda: 44.2,
  "Saint Lucia": 24.3,
  "Sao Tome and Principe": 52.9,
  "Saudi Arabia": 22.4,
  Senegal: 78.3,
  Serbia: 64.5,
  "Sierra Leone": 40.5,
  Singapore: 7.1,
  Slovakia: 47.9,
  Slovenia: 42.2,
  Somalia: 80.5,
  "South Africa": 64.0,
  "South Sudan": 56.5,
  Spain: 24.9,
  "Sri Lanka": 15.3,
  "State of Palestine": 79.9,
  Sudan: 49.7,
  Suriname: 52.1,
  Sweden: 22.4,
  Switzerland: 19.7,
  "Syrian Arab Republic": 20.2,
  Taiwan: 0.4,
  Tajikistan: 69.9,
  Thailand: 11.4,
  "Timor-Leste": 29.6,
  Togo: 53.9,
  "Trinidad and Tobago": 25.1,
  Tunisia: 77.9,
  Turkey: 49.6,
  Turkmenistan: 70.0,
  Uganda: 51.4,
  Ukraine: 64.4,
  "United Arab Emirates": 26.0,
  "United Republic of Tanzania": 64.7,
  "United States of America": 33.0,
  Uruguay: 22.3,
  Uzbekistan: 56.8,
  Vanuatu: 0.8,
  "Venezuela (Bolivarian Republic of)": 54.3,
  "Viet Nam": 8.7,
  Yemen: 37.5,
  Zambia: 87.7,
  Zimbabwe: 83.1,
};

export var ageGroupList = [
  { field: "group1", header: "< 20" },
  { field: "group2", header: "20 - 49" },
  { field: "group3", header: "50 - 64" },
  { field: "group4", header: "65 - 74" },
  { field: "group5", header: ">= 75" },
];

export var sampleResponse = {
  cases: [
    0.88, 0.9437198177308129, 1.019772950341143, 1.1090527864322957,
    1.2126244456077078, 1.3317371932855013, 1.4678389121250537,
    1.622593239370075, 1.7978992562948832, 1.9959140062710705,
    2.219078448441898, 2.470146287363109, 2.752216729638569, 3.068771301458902,
    3.4237148900427052, 3.821421589255444, 4.266785714343155, 4.765278441582342,
    5.323010554285442, 5.946801817807441, 6.644257329749204, 7.423851835591509,
    8.295021843855848, 9.268266558165509, 10.355257730757781,
    11.568959073014918, 12.923755201262601, 14.435590272172265,
    16.122116080203753, 18.002849181941606, 20.099336134120502,
    22.435325295331083, 25.0369431647486, 27.932872433063586,
    31.154527677639027, 34.73622317227727, 38.71532670765046,
    43.132390608523785, 48.03124898383608, 53.45906844739264, 59.46633710904659,
    66.10677250276112, 73.43712587235906, 81.5168597256555, 90.4076691783948,
    100.17281577204089, 110.87624224700475, 122.58143546939606,
    135.3500040462997, 149.23994485698395, 164.30357890985908,
    180.5851436914546, 198.11806793154577, 216.92192922423547,
    236.9991950814619, 258.33180897532264, 280.8777737370085,
    304.56789692541395, 329.3029080278485, 354.9511882395751,
    381.34736773194624, 408.292047127026, 435.55287213603026, 462.8671394740987,
    489.9460301424045, 516.4804605053474, 542.1484178953817, 566.6235183765534,
    589.5843984662803, 610.7244701753601, 629.761484912207, 646.4463660076348,
    660.5707914454549, 671.9731054161365, 680.5422594859631, 686.2196341441003,
    688.9987456840951, 688.9229875827325, 686.0816649047485, 680.6046924761499,
    672.656322080759, 662.4283209969074, 650.1329779408132, 635.9962632456409,
    620.2514204104936, 603.1331807460049, 584.8727368049972, 565.6935418489803,
    545.8079494488154, 525.4146656913489, 504.6969550771943, 483.8215190553129,
    462.93795812794383, 442.1787198752931, 421.6594411490905, 401.4795966961329,
    381.72337509065306, 362.4607125970262, 343.74842612724876,
    325.63139670140856, 308.14376418972006, 291.3101026410667,
    275.1465532862418, 259.6618984794335, 244.85856564466818,
    230.73355431017902, 217.27928299012632, 204.48435566996744,
    192.33424878953284, 180.81192275034252, 169.89836137095548,
    159.5730442258592, 149.81435718973998, 140.59994647106984,
    131.90702139923837, 123.71261115817047, 115.99378046909183,
    108.727808819105, 101.89233757733899, 95.46548913970021, 89.42596128635616,
    83.75310068206934, 78.42695791402372, 73.42832709670148, 68.73877212227006,
    64.34064184422434, 60.21707581307207, 56.352002408448925,
    52.730130437356244, 49.33693578097144, 46.158643756151896,
    43.182208376072005, 40.39528912183735, 37.78622586032878, 35.34401262339548,
    33.058270473293476, 30.91921995699459, 28.917653598882403,
    27.044908414972095, 25.292838863065803, 23.653790308622735,
    22.120573214810822, 20.686438083579237, 19.345051229754603,
    18.090471509113286, 16.917127959395525, 15.819798408331765,
    14.793589151173677, 13.83391533977192, 12.936482672669596,
    12.097269737278143, 11.312511502340879, 10.578683501251318,
    9.892487056177524, 9.250835191942791, 8.650839458646137, 8.089797443924375,
    7.565181067228961, 7.074625524648731, 6.615918933639821, 6.186992583461567,
    5.785911788385999, 5.410867301560412, 5.060167259185924, 4.73222962987344,
    4.425575132164022, 4.13882060618285, 3.870672794122369, 3.619922524012422,
    3.385439257718437, 3.1661659931338586, 2.961114487828887, 2.769360794186865,
    2.590041078216094, 2.4223477099046886, 2.2655256067037617,
    2.118868812582029, 1.9817173002500152, 1.853453978411148,
    1.7335018971162417, 1.621321630122294, 1.5164088332789076,
    1.4182919559671148, 1.3265301084674046, 1.2407110570157232,
    1.1604493641664955, 1.08538464167275, 1.0151799162300361,
    0.9495201084630038, 0.8881106009310619, 0.8306759146497581,
    0.7769584531328846, 0.7267173488079007, 0.6797273652435486,
    0.63577788735273, 0.594671963845012, 0.5562254239308466, 0.52026604286442,
    0.48663276679155004, 0.4551749865402198,
  ],
  deaths: [
    0.0088, 0.009437198177308129, 0.01019772950341143, 0.011090527864322956,
    0.012126244456077078, 0.013317371932855013, 0.014678389121250537,
    0.01622593239370075, 0.017978992562948833, 0.019959140062710705,
    0.02219078448441898, 0.02470146287363109, 0.02752216729638569,
    0.030687713014589023, 0.034237148900427054, 0.03821421589255444,
    0.04266785714343155, 0.04765278441582342, 0.053230105542854414,
    0.059468018178074414, 0.06644257329749204, 0.07423851835591509,
    0.08295021843855847, 0.0926826655816551, 0.10355257730757782,
    0.11568959073014919, 0.12923755201262602, 0.14435590272172266,
    0.16122116080203752, 0.18002849181941608, 0.20099336134120502,
    0.22435325295331082, 0.250369431647486, 0.2793287243306359,
    0.31154527677639027, 0.3473622317227727, 0.3871532670765046,
    0.43132390608523785, 0.4803124898383608, 0.5345906844739264,
    0.594663371090466, 0.6610677250276112, 0.7343712587235907,
    0.815168597256555, 0.904076691783948, 1.001728157720409, 1.1087624224700476,
    1.2258143546939606, 1.3535000404629969, 1.4923994485698395,
    1.643035789098591, 1.805851436914546, 1.9811806793154576,
    2.1692192922423548, 2.3699919508146188, 2.5833180897532264,
    2.808777737370085, 3.0456789692541397, 3.293029080278485,
    3.5495118823957514, 3.8134736773194624, 4.082920471270261,
    4.355528721360303, 4.628671394740987, 4.899460301424045, 5.164804605053474,
    5.4214841789538175, 5.666235183765535, 5.895843984662803, 6.107244701753602,
    6.297614849122071, 6.464463660076348, 6.605707914454549, 6.719731054161365,
    6.805422594859631, 6.8621963414410025, 6.8899874568409505,
    6.889229875827326, 6.860816649047486, 6.8060469247615, 6.72656322080759,
    6.624283209969073, 6.501329779408133, 6.3599626324564085,
    6.2025142041049355, 6.031331807460049, 5.848727368049972,
    5.6569354184898035, 5.458079494488154, 5.254146656913489,
    5.0469695507719425, 4.838215190553129, 4.629379581279438, 4.421787198752931,
    4.216594411490905, 4.014795966961329, 3.8172337509065306, 3.624607125970262,
    3.4374842612724876, 3.2563139670140857, 3.0814376418972005,
    2.913101026410667, 2.751465532862418, 2.596618984794335, 2.448585656446682,
    2.3073355431017903, 2.172792829901263, 2.0448435566996745,
    1.9233424878953285, 1.8081192275034252, 1.6989836137095549,
    1.595730442258592, 1.4981435718973999, 1.4059994647106984,
    1.3190702139923838, 1.2371261115817047, 1.1599378046909183,
    1.08727808819105, 1.01892337577339, 0.9546548913970021, 0.8942596128635616,
    0.8375310068206935, 0.7842695791402372, 0.7342832709670148,
    0.6873877212227006, 0.6434064184422433, 0.6021707581307207,
    0.5635200240844893, 0.5273013043735625, 0.49336935780971436,
    0.46158643756151896, 0.43182208376072007, 0.4039528912183735,
    0.37786225860328776, 0.35344012623395477, 0.3305827047329348,
    0.30919219956994587, 0.28917653598882403, 0.27044908414972096,
    0.25292838863065803, 0.23653790308622735, 0.22120573214810824,
    0.20686438083579237, 0.19345051229754603, 0.18090471509113287,
    0.16917127959395525, 0.15819798408331764, 0.14793589151173678,
    0.1383391533977192, 0.12936482672669597, 0.12097269737278143,
    0.11312511502340879, 0.10578683501251318, 0.09892487056177524,
    0.09250835191942791, 0.08650839458646138, 0.08089797443924375,
    0.07565181067228961, 0.07074625524648731, 0.06615918933639821,
    0.061869925834615674, 0.05785911788385999, 0.05410867301560412,
    0.05060167259185924, 0.0473222962987344, 0.044255751321640224,
    0.0413882060618285, 0.03870672794122369, 0.03619922524012422,
    0.033854392577184374, 0.031661659931338584, 0.029611144878288868,
    0.02769360794186865, 0.02590041078216094, 0.024223477099046885,
    0.022655256067037617, 0.021188688125820292, 0.019817173002500153,
    0.01853453978411148, 0.01733501897116242, 0.016213216301222938,
    0.015164088332789077, 0.014182919559671148, 0.013265301084674046,
    0.012407110570157231, 0.011604493641664954, 0.0108538464167275,
    0.010151799162300362, 0.009495201084630039, 0.00888110600931062,
    0.008306759146497582, 0.007769584531328846, 0.007267173488079008,
    0.006797273652435486, 0.0063577788735273005, 0.00594671963845012,
    0.005562254239308466, 0.0052026604286442004, 0.004866327667915501,
    0.004551749865402199,
  ],
};

export var presetStrategyList = [
  {
    "simulationInterval": [
      "2022-08-31T04:00:00.000Z",
      "2023-02-28T08:00:00.000Z"
    ],
    "simulationDays": 184,
    "regionParameters": {
      "region": {
        "name": "Afghanistan",
        "code": "AFG",
        "populationList": [
          20910291,
          14533976,
          2452836,
          757309,
          273929
        ]
      },
      "variant": {
        "name": "Delta",
        "code": "delta"
      },
      "infectiousnessLevel": 3,
      "socialDistancing": {
        "homeSCLevel": 0,
        "workSCLevel": 0,
        "schoolSCLevel": 0,
        "otherSCLevel": 0
      },
      "infectionStatus": [
        {
          "category": "Previously Infected",
          "group1": 84.8,
          "group2": 84.8,
          "group3": 84.8,
          "group4": 84.8,
          "group5": 84.8
        },
        {
          "category": "Currently Infected",
          "group1": 0.1,
          "group2": 0.1,
          "group3": 0.1,
          "group4": 0.1,
          "group5": 0.1
        },
        {
          "category": "Uninfected",
          "group1": 15.1,
          "group2": 15.1,
          "group3": 15.1,
          "group4": 15.1,
          "group5": 15.1
        }
      ]
    },
    "vaccineParameters": {
      "vaccineList": [
        {
          "category": "Vaccine 1",
          "name": "VAXZEVRIA",
          "code": "AstraZeneca",
          "type": "pre-defined",
          "usage": [
            {
              "name": "Primary series",
              "value": "full dose"
            },
            {
              "name": "Booster",
              "value": "booster"
            }
          ],
          "number": 0,
          "date": "2022-09-01T00:00:00.000Z",
          "rate": 0,
          "allocation": [
            {
              "category": "Full dose",
              "date": "2023-05-15T18:33:02.318Z",
              "proportion": 0,
              "group1": 0,
              "group2": 0,
              "group3": 0,
              "group4": 0,
              "group5": 0
            },
            {
              "category": "Booster",
              "date": "2023-05-15T18:33:02.318Z",
              "proportion": 0,
              "group1": 0,
              "group2": 0,
              "group3": 0,
              "group4": 0,
              "group5": 0,
              "primaryMatching": [
                {
                  "primary": "Vaccine 1",
                  "group1": 0,
                  "group2": 0,
                  "group3": 0,
                  "group4": 0,
                  "group5": 0
                },
                {
                  "primary": "Vaccine 2",
                  "group1": 0,
                  "group2": 0,
                  "group3": 0,
                  "group4": 0,
                  "group5": 0
                },
                {
                  "primary": "Vaccine 3",
                  "group1": 0,
                  "group2": 0,
                  "group3": 0,
                  "group4": 0,
                  "group5": 0
                }
              ]
            }
          ],
          "efficacyData": [
            {
              "category": "Infection",
              "fulldose": 36,
              "booster": 63
            },
            {
              "category": "Symptomatic infection",
              "fulldose": 29,
              "booster": 63
            },
            {
              "category": "Hospitalization",
              "fulldose": 71,
              "booster": 94
            }
          ]
        },
        {
          "category": "Vaccine 2",
          "name": "VERO CELL",
          "code": "SINOPHARM",
          "type": "pre-defined",
          "usage": [
            {
              "name": "Booster",
              "value": "booster"
            }
          ],
          "number": 0,
          "date": "2022-08-31T04:00:00.000Z",
          "rate": 0,
          "allocation": [
            {
              "category": "Full dose",
              "date": "2023-05-15T18:33:02.318Z",
              "proportion": 0,
              "group1": 0,
              "group2": 0,
              "group3": 0,
              "group4": 0,
              "group5": 0
            },
            {
              "category": "Booster",
              "date": "2023-05-15T18:33:02.318Z",
              "proportion": 0,
              "group1": 0,
              "group2": 0,
              "group3": 0,
              "group4": 0,
              "group5": 0,
              "primaryMatching": [
                {
                  "primary": "Vaccine 1",
                  "group1": 0,
                  "group2": 0,
                  "group3": 0,
                  "group4": 0,
                  "group5": 0
                },
                {
                  "primary": "Vaccine 2",
                  "group1": 0,
                  "group2": 0,
                  "group3": 0,
                  "group4": 0,
                  "group5": 0
                },
                {
                  "primary": "Vaccine 3",
                  "group1": 0,
                  "group2": 0,
                  "group3": 0,
                  "group4": 0,
                  "group5": 0
                }
              ]
            }
          ],
          "efficacyData": [
            {
              "category": "Infection",
              "fulldose": 35,
              "booster": 68
            },
            {
              "category": "Symptomatic infection",
              "fulldose": 31,
              "booster": 78
            },
            {
              "category": "Hospitalization",
              "fulldose": 53,
              "booster": 73
            }
          ]
        },
        {
          "category": "Vaccine 3",
          "name": "JANSEN",
          "code": "JANSEN",
          "type": "pre-defined",
          "usage": [
            {
              "name": "Primary series",
              "value": "full dose"
            }
          ],
          "number": 6829294,
          "date": "2022-08-31T04:00:00.000Z",
          "rate": 50000,
          "allocation": [
            {
              "category": "Full dose",
              "date": "2022-08-31T04:00:00.000Z",
              "proportion": 0,
              "group1": 0,
              "group2": 0,
              "group3": 0,
              "group4": 0,
              "group5": 0
            },
            {
              "category": "Booster",
              "date": "2022-08-31T04:00:00.000Z",
              "proportion": 100,
              "group1": 0,
              "group2": 0,
              "group3": 0,
              "group4": 0,
              "group5": 0,
              "primaryMatching": [
                {
                  "primary": "Vaccine 1",
                  "group1": 0,
                  "group2": 0,
                  "group3": 0,
                  "group4": 0,
                  "group5": 3.7
                },
                {
                  "primary": "Vaccine 2",
                  "group1": 0,
                  "group2": 0,
                  "group3": 13.2,
                  "group4": 11.1,
                  "group5": 0.4
                },
                {
                  "primary": "Vaccine 3",
                  "group1": 0,
                  "group2": 49,
                  "group3": 19.7,
                  "group4": 0,
                  "group5": 0
                }
              ]
            }
          ],
          "efficacyData": [
            {
              "category": "Infection",
              "fulldose": 33,
              "booster": 72
            },
            {
              "category": "Symptomatic infection",
              "fulldose": 26,
              "booster": 67
            },
            {
              "category": "Hospitalization",
              "fulldose": 57,
              "booster": 86
            }
          ]
        }
      ],
      "vaccinationStatusByAgeGroup": {
        "group1": [
          {
            "category": "Vaccine 1",
            "fulldose": 0,
            "booster": 0
          },
          {
            "category": "Vaccine 2",
            "fulldose": 0,
            "booster": 0
          },
          {
            "category": "Vaccine 3",
            "fulldose": 0,
            "booster": 0
          },
          {
            "category": "Unvaccinated",
            "fulldose": 100,
            "booster": 100
          }
        ],
        "group2": [
          {
            "category": "Vaccine 1",
            "fulldose": 0,
            "booster": 0
          },
          {
            "category": "Vaccine 2",
            "fulldose": 0,
            "booster": 0
          },
          {
            "category": "Vaccine 3",
            "fulldose": 50.02,
            "booster": 0
          },
          {
            "category": "Unvaccinated",
            "fulldose": 49.98,
            "booster": 100
          }
        ],
        "group3": [
          {
            "category": "Vaccine 1",
            "fulldose": 8.56,
            "booster": 0
          },
          {
            "category": "Vaccine 2",
            "fulldose": 36.6,
            "booster": 0
          },
          {
            "category": "Vaccine 3",
            "fulldose": 54.79,
            "booster": 0
          },
          {
            "category": "Unvaccinated",
            "fulldose": 0.05,
            "booster": 100
          }
        ],
        "group4": [
          {
            "category": "Vaccine 1",
            "fulldose": 0,
            "booster": 0
          },
          {
            "category": "Vaccine 2",
            "fulldose": 100,
            "booster": 0
          },
          {
            "category": "Vaccine 3",
            "fulldose": 0,
            "booster": 0
          },
          {
            "category": "Unvaccinated",
            "fulldose": 0,
            "booster": 100
          }
        ],
        "group5": [
          {
            "category": "Vaccine 1",
            "fulldose": 91.3,
            "booster": 0
          },
          {
            "category": "Vaccine 2",
            "fulldose": 8.7,
            "booster": 0
          },
          {
            "category": "Vaccine 3",
            "fulldose": 0,
            "booster": 0
          },
          {
            "category": "Unvaccinated",
            "fulldose": 0,
            "booster": 100
          }
        ]
      }
    },
    "fixedParameters": {
      "averageTimeBetweenSymptomOnsetAndHospitalization": 3.8,
      "meanDurationInfectiousnessPostSymptoms": 4,
      "meanDurationHospitalization": 7,
      "meanDurationLatentPeriod": 2,
      "meanDurationPreSymptomaticPeriod": 1.5,
      "meanDurationNatImmunityAfterInfection": 100,
      "meanDurationNatImmunityAfterInfection2": 180,
      "meanDurationImmunityWanedVaxHybrid": 100,
      "meanDurationPrimaryImmunity": [
        100,
        100,
        100
      ],
      "meanDurationHybridImmunity": [
        180,
        180,
        180
      ],
      "meanDurationBoosterImmunity": [
        180,
        180,
        180
      ],
      "meanDurationBoostedHybridImmunity": [
        180,
        180,
        180
      ],
      "propSymptomaticInfection": [
        0.25,
        0.4,
        0.4,
        0.4,
        0.4
      ],
      "relativeInfectiousnessAsymptomaticInfection": 1,
      "relativeInfectiousnessHospitalizedInfection": 0,
      "relativeInfectiousnessPreSymptomaticInfection": 1,
      "relativeSusceptibility": [
        1,
        1,
        1,
        1,
        1
      ],
      "VESUSpartiallySus": 0,
      "VEDISpartiallySus": 0,
      "VEHpartiallySus": 20,
      "VESUSpartiallySusVaccinated": 0,
      "VEDISpartiallySusVaccinated": 0,
      "VEHpartiallySusVaccinated": 40
    }
  },
  {
      "simulationInterval": [
        "2022-08-31T04:00:00.000Z",
        "2023-02-28T08:00:00.000Z"
      ],
      "simulationDays": 184,
      "regionParameters": {
        "region": {
          "name": "Afghanistan",
          "code": "AFG",
          "populationList": [
            20910291,
            14533976,
            2452836,
            757309,
            273929
          ]
        },
        "variant": {
          "name": "Delta",
          "code": "delta"
        },
        "infectiousnessLevel": 3,
        "socialDistancing": {
          "homeSCLevel": 0,
          "workSCLevel": 0,
          "schoolSCLevel": 0,
          "otherSCLevel": 0
        },
        "infectionStatus": [
          {
            "category": "Previously Infected",
            "group1": 84.8,
            "group2": 84.8,
            "group3": 84.8,
            "group4": 84.8,
            "group5": 84.8
          },
          {
            "category": "Currently Infected",
            "group1": 0.1,
            "group2": 0.1,
            "group3": 0.1,
            "group4": 0.1,
            "group5": 0.1
          },
          {
            "category": "Uninfected",
            "group1": 15.100000000000003,
            "group2": 15.100000000000003,
            "group3": 15.100000000000003,
            "group4": 15.100000000000003,
            "group5": 15.100000000000003
          }
        ]
      },
      "vaccineParameters": {
        "vaccineList": [
          {
            "category": "Vaccine 1",
            "name": "VAXZEVRIA",
            "code": "AstraZeneca",
            "type": "pre-defined",
            "usage": [
              {
                "name": "Primary series",
                "value": "full dose"
              },
              {
                "name": "Booster",
                "value": "booster"
              }
            ],
            "number": 0,
            "date": "2022-09-01T00:00:00.000Z",
            "rate": 0,
            "allocation": [
              {
                "category": "Full dose",
                "date": "2023-05-15T18:33:02.318Z",
                "proportion": 0,
                "group1": 0,
                "group2": 0,
                "group3": 0,
                "group4": 0,
                "group5": 0
              },
              {
                "category": "Booster",
                "date": "2023-05-15T18:33:02.318Z",
                "proportion": 0,
                "group1": 0,
                "group2": 0,
                "group3": 0,
                "group4": 0,
                "group5": 0,
                "primaryMatching": [
                  {
                    "primary": "Vaccine 1",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  },
                  {
                    "primary": "Vaccine 2",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  },
                  {
                    "primary": "Vaccine 3",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  }
                ]
              }
            ],
            "efficacyData": [
              {
                "category": "Infection",
                "fulldose": 36,
                "booster": 63
              },
              {
                "category": "Symptomatic infection",
                "fulldose": 29,
                "booster": 63
              },
              {
                "category": "Hospitalization",
                "fulldose": 71,
                "booster": 94
              }
            ]
          },
          {
            "category": "Vaccine 2",
            "name": "VERO CELL",
            "code": "SINOPHARM",
            "type": "pre-defined",
            "usage": [
              {
                "name": "Booster",
                "value": "booster"
              }
            ],
            "number": 0,
            "date": "2022-08-31T04:00:00.000Z",
            "rate": 0,
            "allocation": [
              {
                "category": "Full dose",
                "date": "2023-05-15T18:33:02.318Z",
                "proportion": 0,
                "group1": 0,
                "group2": 0,
                "group3": 0,
                "group4": 0,
                "group5": 0
              },
              {
                "category": "Booster",
                "date": "2023-05-15T18:33:02.318Z",
                "proportion": 0,
                "group1": 0,
                "group2": 0,
                "group3": 0,
                "group4": 0,
                "group5": 0,
                "primaryMatching": [
                  {
                    "primary": "Vaccine 1",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  },
                  {
                    "primary": "Vaccine 2",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  },
                  {
                    "primary": "Vaccine 3",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  }
                ]
              }
            ],
            "efficacyData": [
              {
                "category": "Infection",
                "fulldose": 35,
                "booster": 68
              },
              {
                "category": "Symptomatic infection",
                "fulldose": 31,
                "booster": 78
              },
              {
                "category": "Hospitalization",
                "fulldose": 53,
                "booster": 73
              }
            ]
          },
          {
            "category": "Vaccine 3",
            "name": "JANSEN",
            "code": "JANSEN",
            "type": "pre-defined",
            "usage": [
              {
                "name": "Primary series",
                "value": "full dose"
              }
            ],
            "number": 6829294,
            "date": "2022-08-31T04:00:00.000Z",
            "rate": 50000,
            "allocation": [
              {
                "category": "Full dose",
                "date": "2022-08-31T04:00:00.000Z",
                "proportion": 100,
                "group1": 0,
                "group2": 100,
                "group3": 0,
                "group4": 0,
                "group5": 0
              },
              {
                "category": "Booster",
                "date": "2022-08-31T04:00:00.000Z",
                "proportion": 0,
                "group1": 0,
                "group2": 0,
                "group3": 0,
                "group4": 0,
                "group5": 0,
                "primaryMatching": [
                  {
                    "primary": "Vaccine 1",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  },
                  {
                    "primary": "Vaccine 2",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  },
                  {
                    "primary": "Vaccine 3",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  }
                ]
              }
            ],
            "efficacyData": [
              {
                "category": "Infection",
                "fulldose": 33,
                "booster": 72
              },
              {
                "category": "Symptomatic infection",
                "fulldose": 26,
                "booster": 67
              },
              {
                "category": "Hospitalization",
                "fulldose": 57,
                "booster": 86
              }
            ]
          }
        ],
        "vaccinationStatusByAgeGroup": {
          "group1": [
            {
              "category": "Vaccine 1",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Vaccine 2",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Vaccine 3",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Unvaccinated",
              "fulldose": 100,
              "booster": 100
            }
          ],
          "group2": [
            {
              "category": "Vaccine 1",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Vaccine 2",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Vaccine 3",
              "fulldose": 50.02,
              "booster": 0
            },
            {
              "category": "Unvaccinated",
              "fulldose": 49.98,
              "booster": 100
            }
          ],
          "group3": [
            {
              "category": "Vaccine 1",
              "fulldose": 8.56,
              "booster": 0
            },
            {
              "category": "Vaccine 2",
              "fulldose": 36.6,
              "booster": 0
            },
            {
              "category": "Vaccine 3",
              "fulldose": 54.79,
              "booster": 0
            },
            {
              "category": "Unvaccinated",
              "fulldose": 0.05,
              "booster": 100
            }
          ],
          "group4": [
            {
              "category": "Vaccine 1",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Vaccine 2",
              "fulldose": 100,
              "booster": 0
            },
            {
              "category": "Vaccine 3",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Unvaccinated",
              "fulldose": 0,
              "booster": 100
            }
          ],
          "group5": [
            {
              "category": "Vaccine 1",
              "fulldose": 91.3,
              "booster": 0
            },
            {
              "category": "Vaccine 2",
              "fulldose": 8.7,
              "booster": 0
            },
            {
              "category": "Vaccine 3",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Unvaccinated",
              "fulldose": 0,
              "booster": 100
            }
          ]
        }
      },
      "fixedParameters": {
        "averageTimeBetweenSymptomOnsetAndHospitalization": 3.8,
        "meanDurationInfectiousnessPostSymptoms": 4,
        "meanDurationHospitalization": 7,
        "meanDurationLatentPeriod": 2,
        "meanDurationPreSymptomaticPeriod": 1.5,
        "meanDurationNatImmunityAfterInfection": 100,
        "meanDurationNatImmunityAfterInfection2": 180,
        "meanDurationImmunityWanedVaxHybrid": 100,
        "meanDurationPrimaryImmunity": [
          100,
          100,
          100
        ],
        "meanDurationHybridImmunity": [
          180,
          180,
          180
        ],
        "meanDurationBoosterImmunity": [
          180,
          180,
          180
        ],
        "meanDurationBoostedHybridImmunity": [
          180,
          180,
          180
        ],
        "propSymptomaticInfection": [
          0.25,
          0.4,
          0.4,
          0.4,
          0.4
        ],
        "relativeInfectiousnessAsymptomaticInfection": 1,
        "relativeInfectiousnessHospitalizedInfection": 0,
        "relativeInfectiousnessPreSymptomaticInfection": 1,
        "relativeSusceptibility": [
          1,
          1,
          1,
          1,
          1
        ],
        "VESUSpartiallySus": 0,
        "VEDISpartiallySus": 0,
        "VEHpartiallySus": 20,
        "VESUSpartiallySusVaccinated": 0,
        "VEDISpartiallySusVaccinated": 0,
        "VEHpartiallySusVaccinated": 40
      }
  },
  {
      "simulationInterval": [
        "2023-04-24T00:00:00.000Z",
        "2023-10-24T04:00:00.000Z"
      ],
      "simulationDays": 184,
      "regionParameters": {
        "region": {
          "name": "Haiti",
          "code": "HTI",
          "populationList": [
            4847308,
            4882600,
            1082578,
            381790,
            208257
          ]
        },
        "variant": {
          "name": "Delta",
          "code": "delta"
        },
        "infectiousnessLevel": 3,
        "socialDistancing": {
          "homeSCLevel": 0,
          "workSCLevel": 0,
          "schoolSCLevel": 0,
          "otherSCLevel": 0
        },
        "infectionStatus": [
          {
            "category": "Previously Infected",
            "group1": 29.6,
            "group2": 29.6,
            "group3": 29.6,
            "group4": 29.6,
            "group5": 29.6
          },
          {
            "category": "Currently Infected",
            "group1": 0.1,
            "group2": 0.1,
            "group3": 0.1,
            "group4": 0.1,
            "group5": 0.1
          },
          {
            "category": "Uninfected",
            "group1": 70.3,
            "group2": 70.3,
            "group3": 70.3,
            "group4": 70.3,
            "group5": 70.3
          }
        ]
      },
      "vaccineParameters": {
        "vaccineList": [
          {
            "category": "Vaccine 1",
            "name": "JANSEN (Johnson & Johnson)",
            "code": "JANSEN",
            "type": "pre-defined",
            "usage": [],
            "number": 1000000,
            "date": "2023-04-24T00:00:00.000Z",
            "rate": 50000,
            "allocation": [
              {
                "category": "Full dose",
                "date": "2023-04-24T07:00:00.000Z",
                "proportion": 76.5,
                "group1": 0,
                "group2": 0,
                "group3": 39.5,
                "group4": 37,
                "group5": 0
              },
              {
                "category": "Booster",
                "date": "2023-04-24T07:00:00.000Z",
                "proportion": 23.5,
                "group1": 0,
                "group2": 0,
                "group3": 0,
                "group4": 0,
                "group5": 0,
                "primaryMatching": [
                  {
                    "primary": "Vaccine 1",
                    "group1": 0,
                    "group2": 1.2,
                    "group3": 0.02,
                    "group4": 1.1,
                    "group5": 20.8
                  },
                  {
                    "primary": "Vaccine 2",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  },
                  {
                    "primary": "Vaccine 3",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  }
                ]
              }
            ],
            "efficacyData": [
              {
                "category": "Infection",
                "fulldose": 33,
                "booster": 72
              },
              {
                "category": "Symptomatic infection",
                "fulldose": 26,
                "booster": 67
              },
              {
                "category": "Hospitalization",
                "fulldose": 57,
                "booster": 86
              }
            ]
          },
          {
            "category": "Vaccine 2",
            "name": "CONVIDECIA (CanSino)",
            "code": "CONVIDECIA",
            "type": "pre-defined",
            "usage": [],
            "number": 1500000,
            "date": "2023-04-24T00:00:00.000Z",
            "rate": 50000,
            "allocation": [
              {
                "category": "Full dose",
                "date": "2023-06-14T07:00:00.000Z",
                "proportion": 49,
                "group1": 0,
                "group2": 0,
                "group3": 3.3,
                "group4": 45.7,
                "group5": 0
              },
              {
                "category": "Booster",
                "date": "2023-06-12T07:00:00.000Z",
                "proportion": 51,
                "group1": 0,
                "group2": 0,
                "group3": 0,
                "group4": 0,
                "group5": 0,
                "primaryMatching": [
                  {
                    "primary": "Vaccine 1",
                    "group1": 0,
                    "group2": 0,
                    "group3": 26,
                    "group4": 25,
                    "group5": 0
                  },
                  {
                    "primary": "Vaccine 2",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  },
                  {
                    "primary": "Vaccine 3",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  }
                ]
              }
            ],
            "efficacyData": [
              {
                "category": "Infection",
                "fulldose": 32,
                "booster": 62
              },
              {
                "category": "Symptomatic infection",
                "fulldose": 26,
                "booster": 66
              },
              {
                "category": "Hospitalization",
                "fulldose": 48,
                "booster": 66
              }
            ]
          },
          {
            "category": "Vaccine 3",
            "name": "VERO CELL (SINOPHARM)",
            "code": "VERO CELL",
            "type": "pre-defined",
            "usage": [],
            "number": 1000000,
            "date": "2023-04-24T00:00:00.000Z",
            "rate": 50000,
            "allocation": [
              {
                "category": "Full dose",
                "date": "2023-07-10T07:00:00.000Z",
                "proportion": 26.5,
                "group1": 0,
                "group2": 26.5,
                "group3": 0,
                "group4": 0,
                "group5": 0
              },
              {
                "category": "Booster",
                "date": "2023-07-10T07:00:00.000Z",
                "proportion": 73.5,
                "group1": 0,
                "group2": 0,
                "group3": 0,
                "group4": 0,
                "group5": 0,
                "primaryMatching": [
                  {
                    "primary": "Vaccine 1",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  },
                  {
                    "primary": "Vaccine 2",
                    "group1": 0,
                    "group2": 4.99,
                    "group3": 68.49,
                    "group4": 0,
                    "group5": 0
                  },
                  {
                    "primary": "Vaccine 3",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  }
                ]
              }
            ],
            "efficacyData": [
              {
                "category": "Infection",
                "fulldose": 35,
                "booster": 68
              },
              {
                "category": "Symptomatic infection",
                "fulldose": 31,
                "booster": 78
              },
              {
                "category": "Hospitalization",
                "fulldose": 53,
                "booster": 73
              }
            ]
          }
        ],
        "vaccinationStatusByAgeGroup": {
          "group1": [
            {
              "category": "Vaccine 1",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Vaccine 2",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Vaccine 3",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Unvaccinated",
              "fulldose": 100,
              "booster": 100
            }
          ],
          "group2": [
            {
              "category": "Vaccine 1",
              "fulldose": 0.25,
              "booster": 0
            },
            {
              "category": "Vaccine 2",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Vaccine 3",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Unvaccinated",
              "fulldose": 99.75,
              "booster": 100
            }
          ],
          "group3": [
            {
              "category": "Vaccine 1",
              "fulldose": 0.25,
              "booster": 0
            },
            {
              "category": "Vaccine 2",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Vaccine 3",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Unvaccinated",
              "fulldose": 99.75,
              "booster": 100
            }
          ],
          "group4": [
            {
              "category": "Vaccine 1",
              "fulldose": 3,
              "booster": 0
            },
            {
              "category": "Vaccine 2",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Vaccine 3",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Unvaccinated",
              "fulldose": 97,
              "booster": 100
            }
          ],
          "group5": [
            {
              "category": "Vaccine 1",
              "fulldose": 100,
              "booster": 0
            },
            {
              "category": "Vaccine 2",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Vaccine 3",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Unvaccinated",
              "fulldose": 0,
              "booster": 100
            }
          ]
        }
      },
      "fixedParameters": {
        "averageTimeBetweenSymptomOnsetAndHospitalization": 3.8,
        "meanDurationInfectiousnessPostSymptoms": 4,
        "meanDurationHospitalization": 7,
        "meanDurationLatentPeriod": 2,
        "meanDurationPreSymptomaticPeriod": 1.5,
        "meanDurationNatImmunityAfterInfection": 100,
        "meanDurationNatImmunityAfterInfection2": 180,
        "meanDurationImmunityWanedVaxHybrid": 100,
        "meanDurationPrimaryImmunity": [
          100,
          100,
          100
        ],
        "meanDurationHybridImmunity": [
          180,
          180,
          180
        ],
        "meanDurationBoosterImmunity": [
          180,
          180,
          180
        ],
        "meanDurationBoostedHybridImmunity": [
          180,
          180,
          180
        ],
        "propSymptomaticInfection": [
          0.25,
          0.4,
          0.4,
          0.4,
          0.4
        ],
        "relativeInfectiousnessAsymptomaticInfection": 1,
        "relativeInfectiousnessHospitalizedInfection": 0,
        "relativeInfectiousnessPreSymptomaticInfection": 1,
        "relativeSusceptibility": [
          1,
          1,
          1,
          1,
          1
        ],
        "VESUSpartiallySus": 0,
        "VEDISpartiallySus": 24.7,
        "VEHpartiallySus": 74.6,
        "VESUSpartiallySusVaccinated": 0,
        "VEDISpartiallySusVaccinated": 41,
        "VEHpartiallySusVaccinated": 95.3
      }
  },
  {
      "simulationInterval": [
        "2023-04-24T00:00:00.000Z",
        "2023-10-23T04:00:00.000Z"
      ],
      "simulationDays": 184,
      "regionParameters": {
        "region": {
          "name": "Haiti",
          "code": "HTI",
          "populationList": [
            4847308,
            4882600,
            1082578,
            381790,
            208257
          ]
        },
        "variant": {
          "name": "Delta",
          "code": "delta"
        },
        "infectiousnessLevel": 3,
        "socialDistancing": {
          "homeSCLevel": 0,
          "workSCLevel": 0,
          "schoolSCLevel": 0,
          "otherSCLevel": 0
        },
        "infectionStatus": [
          {
            "category": "Previously Infected",
            "group1": 29.6,
            "group2": 29.6,
            "group3": 29.6,
            "group4": 29.6,
            "group5": 29.6
          },
          {
            "category": "Currently Infected",
            "group1": 0.1,
            "group2": 0.1,
            "group3": 0.1,
            "group4": 0.1,
            "group5": 0.1
          },
          {
            "category": "Uninfected",
            "group1": 70.30000000000001,
            "group2": 70.30000000000001,
            "group3": 70.30000000000001,
            "group4": 70.30000000000001,
            "group5": 70.30000000000001
          }
        ]
      },
      "vaccineParameters": {
        "vaccineList": [
          {
            "category": "Vaccine 1",
            "name": "JANSEN (Johnson & Johnson)",
            "code": "JANSEN",
            "type": "pre-defined",
            "usage": [],
            "number": 1000000,
            "date": "2023-04-24T00:00:00.000Z",
            "rate": 50000,
            "allocation": [
              {
                "category": "Full dose",
                "date": "2023-04-24T07:00:00.000Z",
                "proportion": 100,
                "group1": 0,
                "group2": 0,
                "group3": 62.98,
                "group4": 37.01,
                "group5": 0
              },
              {
                "category": "Booster",
                "date": "2023-04-24T07:00:00.000Z",
                "proportion": 23.5,
                "group1": 0,
                "group2": 0,
                "group3": 0,
                "group4": 0,
                "group5": 0,
                "primaryMatching": [
                  {
                    "primary": "Vaccine 1",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  },
                  {
                    "primary": "Vaccine 2",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  },
                  {
                    "primary": "Vaccine 3",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  }
                ]
              }
            ],
            "efficacyData": [
              {
                "category": "Infection",
                "fulldose": 33,
                "booster": 72
              },
              {
                "category": "Symptomatic infection",
                "fulldose": 26,
                "booster": 67
              },
              {
                "category": "Hospitalization",
                "fulldose": 57,
                "booster": 86
              }
            ]
          },
          {
            "category": "Vaccine 2",
            "name": "CONVIDECIA (CanSino)",
            "code": "CONVIDECIA",
            "type": "pre-defined",
            "usage": [],
            "number": 1500000,
            "date": "2023-04-24T00:00:00.000Z",
            "rate": 50000,
            "allocation": [
              {
                "category": "Full dose",
                "date": "2023-06-14T07:00:00.000Z",
                "proportion": 100,
                "group1": 0,
                "group2": 70,
                "group3": 30,
                "group4": 0,
                "group5": 0
              },
              {
                "category": "Booster",
                "date": "2023-06-12T07:00:00.000Z",
                "proportion": 51,
                "group1": 0,
                "group2": 0,
                "group3": 0,
                "group4": 0,
                "group5": 0,
                "primaryMatching": [
                  {
                    "primary": "Vaccine 1",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  },
                  {
                    "primary": "Vaccine 2",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  },
                  {
                    "primary": "Vaccine 3",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  }
                ]
              }
            ],
            "efficacyData": [
              {
                "category": "Infection",
                "fulldose": 32,
                "booster": 62
              },
              {
                "category": "Symptomatic infection",
                "fulldose": 26,
                "booster": 66
              },
              {
                "category": "Hospitalization",
                "fulldose": 48,
                "booster": 66
              }
            ]
          },
          {
            "category": "Vaccine 3",
            "name": "VERO CELL (SINOPHARM)",
            "code": "VERO CELL",
            "type": "pre-defined",
            "usage": [],
            "number": 1000000,
            "date": "2023-04-24T00:00:00.000Z",
            "rate": 50000,
            "allocation": [
              {
                "category": "Full dose",
                "date": "2023-07-10T07:00:00.000Z",
                "proportion": 100,
                "group1": 0,
                "group2": 100,
                "group3": 0,
                "group4": 0,
                "group5": 0
              },
              {
                "category": "Booster",
                "date": "2023-07-10T07:00:00.000Z",
                "proportion": 73.5,
                "group1": 0,
                "group2": 0,
                "group3": 0,
                "group4": 0,
                "group5": 0,
                "primaryMatching": [
                  {
                    "primary": "Vaccine 1",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  },
                  {
                    "primary": "Vaccine 2",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  },
                  {
                    "primary": "Vaccine 3",
                    "group1": 0,
                    "group2": 0,
                    "group3": 0,
                    "group4": 0,
                    "group5": 0
                  }
                ]
              }
            ],
            "efficacyData": [
              {
                "category": "Infection",
                "fulldose": 35,
                "booster": 68
              },
              {
                "category": "Symptomatic infection",
                "fulldose": 31,
                "booster": 78
              },
              {
                "category": "Hospitalization",
                "fulldose": 53,
                "booster": 73
              }
            ]
          }
        ],
        "vaccinationStatusByAgeGroup": {
          "group1": [
            {
              "category": "Vaccine 1",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Vaccine 2",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Vaccine 3",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Unvaccinated",
              "fulldose": 100,
              "booster": 100
            }
          ],
          "group2": [
            {
              "category": "Vaccine 1",
              "fulldose": 0.25,
              "booster": 0
            },
            {
              "category": "Vaccine 2",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Vaccine 3",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Unvaccinated",
              "fulldose": 99.75,
              "booster": 100
            }
          ],
          "group3": [
            {
              "category": "Vaccine 1",
              "fulldose": 0.25,
              "booster": 0
            },
            {
              "category": "Vaccine 2",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Vaccine 3",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Unvaccinated",
              "fulldose": 99.75,
              "booster": 100
            }
          ],
          "group4": [
            {
              "category": "Vaccine 1",
              "fulldose": 3,
              "booster": 0
            },
            {
              "category": "Vaccine 2",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Vaccine 3",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Unvaccinated",
              "fulldose": 97,
              "booster": 100
            }
          ],
          "group5": [
            {
              "category": "Vaccine 1",
              "fulldose": 100,
              "booster": 0
            },
            {
              "category": "Vaccine 2",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Vaccine 3",
              "fulldose": 0,
              "booster": 0
            },
            {
              "category": "Unvaccinated",
              "fulldose": 0,
              "booster": 100
            }
          ]
        }
      },
      "fixedParameters": {
        "averageTimeBetweenSymptomOnsetAndHospitalization": 3.8,
        "meanDurationInfectiousnessPostSymptoms": 4,
        "meanDurationHospitalization": 7,
        "meanDurationLatentPeriod": 2,
        "meanDurationPreSymptomaticPeriod": 1.5,
        "meanDurationNatImmunityAfterInfection": 100,
        "meanDurationNatImmunityAfterInfection2": 180,
        "meanDurationImmunityWanedVaxHybrid": 100,
        "meanDurationPrimaryImmunity": [
          100,
          100,
          100
        ],
        "meanDurationHybridImmunity": [
          180,
          180,
          180
        ],
        "meanDurationBoosterImmunity": [
          180,
          180,
          180
        ],
        "meanDurationBoostedHybridImmunity": [
          180,
          180,
          180
        ],
        "propSymptomaticInfection": [
          0.25,
          0.4,
          0.4,
          0.4,
          0.4
        ],
        "relativeInfectiousnessAsymptomaticInfection": 1,
        "relativeInfectiousnessHospitalizedInfection": 0,
        "relativeInfectiousnessPreSymptomaticInfection": 1,
        "relativeSusceptibility": [
          1,
          1,
          1,
          1,
          1
        ],
        "VESUSpartiallySus": 0,
        "VEDISpartiallySus": 24.7,
        "VEHpartiallySus": 74.6,
        "VESUSpartiallySusVaccinated": 0,
        "VEDISpartiallySusVaccinated": 41,
        "VEHpartiallySusVaccinated": 95.3
      }
  }
];

export var sampleSimulationOutcome = {
  cumulativeNumberOfDeaths: 67424.0,
  deathTimeSeries: [
    [
      0.0, 12.0, 26.0, 40.0, 55.0, 69.0, 84.0, 98.0, 112.0, 126.0, 138.0, 150.0,
      162.0, 172.0, 182.0, 191.0, 199.0, 207.0, 214.0, 220.0, 226.0, 232.0,
      236.0, 241.0, 245.0, 248.0, 252.0, 255.0, 257.0, 260.0, 262.0, 264.0,
      265.0, 267.0, 268.0, 270.0, 271.0, 272.0, 273.0, 274.0, 274.0, 275.0,
      276.0, 276.0, 277.0, 277.0, 277.0, 278.0, 278.0, 278.0, 279.0, 279.0,
      279.0, 279.0, 280.0, 280.0, 280.0, 280.0, 280.0, 280.0, 280.0, 280.0,
      281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0,
      281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0,
      281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0,
      281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0,
      281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0,
      281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0,
      281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0, 281.0,
      281.0, 281.0, 281.0, 281.0, 281.0, 282.0, 282.0, 282.0, 282.0, 282.0,
      282.0, 282.0, 282.0, 282.0, 282.0, 282.0, 282.0, 282.0, 282.0, 282.0,
      282.0, 282.0, 282.0, 282.0, 282.0, 282.0, 282.0, 282.0, 282.0, 282.0,
      282.0, 282.0, 282.0, 282.0, 282.0, 282.0, 282.0, 282.0, 282.0, 282.0,
      282.0, 282.0, 282.0, 282.0, 282.0, 282.0, 282.0, 282.0,
    ],
    [
      0.0, 545.0, 1127.0, 1733.0, 2352.0, 2973.0, 3585.0, 4181.0, 4753.0,
      5298.0, 5812.0, 6293.0, 6741.0, 7155.0, 7537.0, 7887.0, 8208.0, 8499.0,
      8765.0, 9005.0, 9223.0, 9419.0, 9597.0, 9757.0, 9900.0, 10030.0, 10146.0,
      10250.0, 10343.0, 10427.0, 10502.0, 10570.0, 10630.0, 10684.0, 10732.0,
      10776.0, 10814.0, 10849.0, 10880.0, 10908.0, 10933.0, 10956.0, 10976.0,
      10994.0, 11010.0, 11025.0, 11038.0, 11050.0, 11061.0, 11070.0, 11079.0,
      11087.0, 11094.0, 11100.0, 11106.0, 11111.0, 11116.0, 11120.0, 11124.0,
      11127.0, 11131.0, 11134.0, 11136.0, 11139.0, 11141.0, 11143.0, 11145.0,
      11147.0, 11148.0, 11149.0, 11151.0, 11152.0, 11153.0, 11154.0, 11155.0,
      11156.0, 11157.0, 11157.0, 11158.0, 11159.0, 11159.0, 11160.0, 11160.0,
      11161.0, 11161.0, 11162.0, 11162.0, 11162.0, 11163.0, 11163.0, 11163.0,
      11164.0, 11164.0, 11164.0, 11164.0, 11165.0, 11165.0, 11165.0, 11165.0,
      11165.0, 11166.0, 11166.0, 11166.0, 11166.0, 11166.0, 11166.0, 11166.0,
      11166.0, 11167.0, 11167.0, 11167.0, 11167.0, 11167.0, 11167.0, 11167.0,
      11167.0, 11167.0, 11167.0, 11167.0, 11167.0, 11167.0, 11168.0, 11168.0,
      11168.0, 11168.0, 11168.0, 11168.0, 11168.0, 11168.0, 11168.0, 11168.0,
      11168.0, 11168.0, 11168.0, 11168.0, 11168.0, 11168.0, 11168.0, 11168.0,
      11168.0, 11168.0, 11168.0, 11168.0, 11168.0, 11168.0, 11168.0, 11168.0,
      11168.0, 11168.0, 11168.0, 11169.0, 11169.0, 11169.0, 11169.0, 11169.0,
      11169.0, 11169.0, 11169.0, 11169.0, 11169.0, 11169.0, 11169.0, 11169.0,
      11169.0, 11169.0, 11169.0, 11169.0, 11169.0, 11169.0, 11169.0, 11169.0,
      11169.0, 11169.0, 11169.0, 11169.0, 11169.0, 11169.0, 11169.0, 11169.0,
      11169.0,
    ],
    [
      0.0, 1805.0, 3611.0, 5404.0, 7162.0, 8864.0, 10494.0, 12035.0, 13478.0,
      14817.0, 16050.0, 17178.0, 18204.0, 19133.0, 19969.0, 20720.0, 21393.0,
      21994.0, 22530.0, 23006.0, 23430.0, 23805.0, 24139.0, 24434.0, 24696.0,
      24928.0, 25134.0, 25316.0, 25477.0, 25620.0, 25747.0, 25859.0, 25959.0,
      26048.0, 26127.0, 26197.0, 26260.0, 26315.0, 26365.0, 26410.0, 26449.0,
      26485.0, 26517.0, 26546.0, 26571.0, 26594.0, 26615.0, 26634.0, 26651.0,
      26666.0, 26680.0, 26693.0, 26704.0, 26714.0, 26724.0, 26732.0, 26740.0,
      26747.0, 26753.0, 26759.0, 26765.0, 26770.0, 26774.0, 26778.0, 26782.0,
      26786.0, 26789.0, 26792.0, 26795.0, 26797.0, 26799.0, 26802.0, 26804.0,
      26805.0, 26807.0, 26809.0, 26810.0, 26812.0, 26813.0, 26814.0, 26815.0,
      26816.0, 26817.0, 26818.0, 26819.0, 26820.0, 26821.0, 26821.0, 26822.0,
      26823.0, 26823.0, 26824.0, 26824.0, 26825.0, 26825.0, 26826.0, 26826.0,
      26826.0, 26827.0, 26827.0, 26827.0, 26828.0, 26828.0, 26828.0, 26829.0,
      26829.0, 26829.0, 26829.0, 26830.0, 26830.0, 26830.0, 26830.0, 26830.0,
      26831.0, 26831.0, 26831.0, 26831.0, 26831.0, 26831.0, 26831.0, 26832.0,
      26832.0, 26832.0, 26832.0, 26832.0, 26832.0, 26832.0, 26832.0, 26832.0,
      26833.0, 26833.0, 26833.0, 26833.0, 26833.0, 26833.0, 26833.0, 26833.0,
      26833.0, 26833.0, 26833.0, 26833.0, 26833.0, 26834.0, 26834.0, 26834.0,
      26834.0, 26834.0, 26834.0, 26834.0, 26834.0, 26834.0, 26834.0, 26834.0,
      26834.0, 26834.0, 26834.0, 26834.0, 26834.0, 26834.0, 26834.0, 26834.0,
      26834.0, 26835.0, 26835.0, 26835.0, 26835.0, 26835.0, 26835.0, 26835.0,
      26835.0, 26835.0, 26835.0, 26835.0, 26835.0, 26835.0, 26835.0, 26835.0,
      26835.0, 26835.0, 26835.0,
    ],
    [
      0.0, 1785.0, 3438.0, 4981.0, 6423.0, 7764.0, 9001.0, 10133.0, 11160.0,
      12086.0, 12914.0, 13651.0, 14303.0, 14879.0, 15385.0, 15829.0, 16219.0,
      16560.0, 16858.0, 17119.0, 17347.0, 17546.0, 17721.0, 17874.0, 18008.0,
      18126.0, 18230.0, 18321.0, 18401.0, 18472.0, 18534.0, 18590.0, 18639.0,
      18682.0, 18721.0, 18755.0, 18786.0, 18813.0, 18838.0, 18860.0, 18879.0,
      18897.0, 18913.0, 18927.0, 18940.0, 18951.0, 18962.0, 18971.0, 18980.0,
      18987.0, 18994.0, 19001.0, 19006.0, 19012.0, 19016.0, 19021.0, 19025.0,
      19028.0, 19032.0, 19035.0, 19038.0, 19040.0, 19043.0, 19045.0, 19047.0,
      19049.0, 19050.0, 19052.0, 19053.0, 19055.0, 19056.0, 19057.0, 19058.0,
      19059.0, 19060.0, 19061.0, 19062.0, 19062.0, 19063.0, 19064.0, 19064.0,
      19065.0, 19065.0, 19066.0, 19066.0, 19067.0, 19067.0, 19068.0, 19068.0,
      19068.0, 19069.0, 19069.0, 19069.0, 19069.0, 19070.0, 19070.0, 19070.0,
      19070.0, 19071.0, 19071.0, 19071.0, 19071.0, 19071.0, 19071.0, 19072.0,
      19072.0, 19072.0, 19072.0, 19072.0, 19072.0, 19072.0, 19072.0, 19073.0,
      19073.0, 19073.0, 19073.0, 19073.0, 19073.0, 19073.0, 19073.0, 19073.0,
      19073.0, 19073.0, 19073.0, 19074.0, 19074.0, 19074.0, 19074.0, 19074.0,
      19074.0, 19074.0, 19074.0, 19074.0, 19074.0, 19074.0, 19074.0, 19074.0,
      19074.0, 19074.0, 19074.0, 19074.0, 19074.0, 19074.0, 19074.0, 19074.0,
      19074.0, 19075.0, 19075.0, 19075.0, 19075.0, 19075.0, 19075.0, 19075.0,
      19075.0, 19075.0, 19075.0, 19075.0, 19075.0, 19075.0, 19075.0, 19075.0,
      19075.0, 19075.0, 19075.0, 19075.0, 19075.0, 19075.0, 19075.0, 19075.0,
      19075.0, 19075.0, 19075.0, 19075.0, 19075.0, 19075.0, 19075.0, 19075.0,
      19075.0, 19075.0, 19075.0,
    ],
    [
      0.0, 1238.0, 2293.0, 3218.0, 4043.0, 4781.0, 5442.0, 6030.0, 6551.0,
      7008.0, 7409.0, 7757.0, 8059.0, 8320.0, 8546.0, 8740.0, 8908.0, 9052.0,
      9177.0, 9285.0, 9378.0, 9459.0, 9529.0, 9590.0, 9644.0, 9690.0, 9731.0,
      9767.0, 9798.0, 9826.0, 9850.0, 9872.0, 9891.0, 9908.0, 9923.0, 9937.0,
      9949.0, 9959.0, 9969.0, 9977.0, 9985.0, 9992.0, 9998.0, 10004.0, 10009.0,
      10013.0, 10018.0, 10021.0, 10025.0, 10028.0, 10030.0, 10033.0, 10035.0,
      10037.0, 10039.0, 10041.0, 10043.0, 10044.0, 10045.0, 10047.0, 10048.0,
      10049.0, 10050.0, 10050.0, 10051.0, 10052.0, 10053.0, 10053.0, 10054.0,
      10054.0, 10055.0, 10055.0, 10056.0, 10056.0, 10057.0, 10057.0, 10057.0,
      10058.0, 10058.0, 10058.0, 10058.0, 10059.0, 10059.0, 10059.0, 10059.0,
      10059.0, 10060.0, 10060.0, 10060.0, 10060.0, 10060.0, 10060.0, 10060.0,
      10060.0, 10061.0, 10061.0, 10061.0, 10061.0, 10061.0, 10061.0, 10061.0,
      10061.0, 10061.0, 10061.0, 10061.0, 10061.0, 10061.0, 10061.0, 10062.0,
      10062.0, 10062.0, 10062.0, 10062.0, 10062.0, 10062.0, 10062.0, 10062.0,
      10062.0, 10062.0, 10062.0, 10062.0, 10062.0, 10062.0, 10062.0, 10062.0,
      10062.0, 10062.0, 10062.0, 10062.0, 10062.0, 10062.0, 10062.0, 10062.0,
      10062.0, 10062.0, 10062.0, 10062.0, 10062.0, 10062.0, 10062.0, 10062.0,
      10062.0, 10062.0, 10062.0, 10062.0, 10062.0, 10063.0, 10063.0, 10063.0,
      10063.0, 10063.0, 10063.0, 10063.0, 10063.0, 10063.0, 10063.0, 10063.0,
      10063.0, 10063.0, 10063.0, 10063.0, 10063.0, 10063.0, 10063.0, 10063.0,
      10063.0, 10063.0, 10063.0, 10063.0, 10063.0, 10063.0, 10063.0, 10063.0,
      10063.0, 10063.0, 10063.0, 10063.0, 10063.0, 10063.0, 10063.0,
    ],
  ],
  hospitalizationTimeSeries: [
    [
      1958.0, 2154.0, 2298.0, 2393.0, 2442.0, 2448.0, 2418.0, 2358.0, 2274.0,
      2173.0, 2060.0, 1939.0, 1814.0, 1689.0, 1565.0, 1444.0, 1329.0, 1218.0,
      1114.0, 1017.0, 926.0, 841.0, 764.0, 692.0, 626.0, 566.0, 511.0, 462.0,
      416.0, 375.0, 338.0, 305.0, 274.0, 247.0, 222.0, 200.0, 180.0, 162.0,
      146.0, 131.0, 118.0, 106.0, 96.0, 86.0, 78.0, 70.0, 63.0, 57.0, 52.0,
      47.0, 42.0, 38.0, 35.0, 31.0, 28.0, 26.0, 23.0, 21.0, 19.0, 17.0, 16.0,
      15.0, 13.0, 12.0, 11.0, 10.0, 9.0, 8.0, 8.0, 7.0, 7.0, 6.0, 6.0, 5.0, 5.0,
      4.0, 4.0, 4.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
      1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    ],
    [
      28948.0, 31353.0, 33064.0, 34097.0, 34478.0, 34267.0, 33553.0, 32435.0,
      31013.0, 29378.0, 27607.0, 25766.0, 23907.0, 22071.0, 20287.0, 18576.0,
      16954.0, 15430.0, 14007.0, 12689.0, 11472.0, 10356.0, 9334.0, 8403.0,
      7557.0, 6790.0, 6097.0, 5470.0, 4906.0, 4397.0, 3941.0, 3531.0, 3163.0,
      2833.0, 2538.0, 2273.0, 2037.0, 1825.0, 1636.0, 1467.0, 1315.0, 1180.0,
      1059.0, 951.0, 855.0, 769.0, 691.0, 622.0, 561.0, 505.0, 456.0, 411.0,
      372.0, 336.0, 304.0, 275.0, 249.0, 226.0, 205.0, 187.0, 170.0, 155.0,
      141.0, 129.0, 117.0, 107.0, 98.0, 90.0, 82.0, 76.0, 69.0, 64.0, 59.0,
      54.0, 50.0, 46.0, 43.0, 39.0, 37.0, 34.0, 31.0, 29.0, 27.0, 25.0, 24.0,
      22.0, 20.0, 19.0, 18.0, 17.0, 16.0, 15.0, 14.0, 13.0, 12.0, 11.0, 11.0,
      10.0, 10.0, 9.0, 9.0, 8.0, 8.0, 7.0, 7.0, 7.0, 6.0, 6.0, 6.0, 5.0, 5.0,
      5.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
      3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
      2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
    ],
    [
      22355.0, 22474.0, 22407.0, 22106.0, 21546.0, 20739.0, 19727.0, 18562.0,
      17299.0, 15987.0, 14669.0, 13376.0, 12132.0, 10955.0, 9854.0, 8835.0,
      7900.0, 7049.0, 6277.0, 5581.0, 4957.0, 4398.0, 3899.0, 3455.0, 3061.0,
      2712.0, 2402.0, 2128.0, 1886.0, 1672.0, 1483.0, 1317.0, 1169.0, 1039.0,
      925.0, 823.0, 734.0, 654.0, 584.0, 522.0, 467.0, 419.0, 375.0, 337.0,
      303.0, 273.0, 246.0, 221.0, 200.0, 181.0, 164.0, 148.0, 134.0, 122.0,
      111.0, 101.0, 92.0, 84.0, 77.0, 70.0, 64.0, 59.0, 54.0, 49.0, 45.0, 42.0,
      38.0, 35.0, 33.0, 30.0, 28.0, 26.0, 24.0, 22.0, 21.0, 19.0, 18.0, 17.0,
      15.0, 14.0, 13.0, 13.0, 12.0, 11.0, 10.0, 10.0, 9.0, 8.0, 8.0, 8.0, 7.0,
      7.0, 6.0, 6.0, 6.0, 5.0, 5.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 3.0, 3.0,
      3.0, 3.0, 3.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
      2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    ],
    [
      11569.0, 10638.0, 9905.0, 9261.0, 8636.0, 8002.0, 7354.0, 6701.0, 6057.0,
      5437.0, 4850.0, 4304.0, 3804.0, 3350.0, 2943.0, 2581.0, 2260.0, 1978.0,
      1730.0, 1512.0, 1323.0, 1158.0, 1014.0, 889.0, 780.0, 685.0, 602.0, 530.0,
      468.0, 413.0, 365.0, 323.0, 287.0, 254.0, 226.0, 201.0, 180.0, 160.0,
      143.0, 128.0, 115.0, 103.0, 93.0, 84.0, 75.0, 68.0, 61.0, 56.0, 50.0,
      46.0, 41.0, 38.0, 34.0, 31.0, 28.0, 26.0, 24.0, 22.0, 20.0, 18.0, 17.0,
      15.0, 14.0, 13.0, 12.0, 11.0, 10.0, 9.0, 9.0, 8.0, 7.0, 7.0, 6.0, 6.0,
      6.0, 5.0, 5.0, 4.0, 4.0, 4.0, 4.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.0, 2.0, 2.0,
      2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0,
    ],
    [
      5387.0, 4509.0, 3908.0, 3463.0, 3098.0, 2776.0, 2478.0, 2199.0, 1940.0,
      1701.0, 1483.0, 1288.0, 1115.0, 964.0, 831.0, 717.0, 618.0, 533.0, 460.0,
      398.0, 345.0, 299.0, 260.0, 227.0, 198.0, 173.0, 152.0, 133.0, 117.0,
      103.0, 91.0, 81.0, 72.0, 64.0, 57.0, 50.0, 45.0, 40.0, 36.0, 32.0, 29.0,
      26.0, 23.0, 21.0, 19.0, 17.0, 16.0, 14.0, 13.0, 12.0, 10.0, 10.0, 9.0,
      8.0, 7.0, 7.0, 6.0, 6.0, 5.0, 5.0, 4.0, 4.0, 4.0, 3.0, 3.0, 3.0, 3.0, 2.0,
      2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    ],
  ],
  index: 0,
  infectionTimeSeries: [
    [
      15730333.0, 15018819.0, 14097520.0, 13018752.0, 11864036.0, 10702501.0,
      9581993.0, 8531350.0, 7565320.0, 6689172.0, 5902226.0, 5200352.0,
      4577706.0, 4027591.0, 3543015.0, 3117079.0, 2743236.0, 2415422.0,
      2128124.0, 1876385.0, 1655796.0, 1462456.0, 1292928.0, 1144200.0,
      1013637.0, 898935.0, 798086.0, 709341.0, 631176.0, 562263.0, 501449.0,
      447727.0, 400221.0, 358168.0, 320903.0, 287846.0, 258491.0, 232394.0,
      209170.0, 188479.0, 170027.0, 153553.0, 138830.0, 125657.0, 113860.0,
      103283.0, 93790.0, 85262.0, 77592.0, 70688.0, 64466.0, 58854.0, 53787.0,
      49207.0, 45063.0, 41310.0, 37909.0, 34823.0, 32020.0, 29472.0, 27153.0,
      25042.0, 23117.0, 21360.0, 19756.0, 18290.0, 16949.0, 15721.0, 14595.0,
      13562.0, 12614.0, 11743.0, 10941.0, 10204.0, 9524.0, 8898.0, 8320.0,
      7786.0, 7293.0, 6836.0, 6414.0, 6022.0, 5659.0, 5322.0, 5010.0, 4719.0,
      4449.0, 4197.0, 3963.0, 3744.0, 3540.0, 3350.0, 3173.0, 3007.0, 2851.0,
      2706.0, 2570.0, 2442.0, 2322.0, 2210.0, 2104.0, 2005.0, 1912.0, 1824.0,
      1742.0, 1664.0, 1591.0, 1521.0, 1456.0, 1394.0, 1336.0, 1281.0, 1229.0,
      1180.0, 1133.0, 1089.0, 1047.0, 1007.0, 969.0, 933.0, 899.0, 867.0, 836.0,
      807.0, 779.0, 752.0, 727.0, 703.0, 680.0, 658.0, 637.0, 617.0, 598.0,
      580.0, 562.0, 545.0, 529.0, 514.0, 500.0, 485.0, 472.0, 459.0, 447.0,
      435.0, 423.0, 412.0, 402.0, 392.0, 382.0, 373.0, 364.0, 355.0, 347.0,
      339.0, 331.0, 323.0, 316.0, 309.0, 303.0, 296.0, 290.0, 284.0, 278.0,
      272.0, 267.0, 262.0, 257.0, 252.0, 247.0, 242.0, 238.0, 234.0, 229.0,
      225.0, 222.0, 218.0, 214.0, 210.0, 207.0, 204.0,
    ],
    [
      16748858.0, 16054138.0, 15108637.0, 13967025.0, 12726029.0, 11469289.0,
      10254827.0, 9117351.0, 8074274.0, 7131477.0, 6287738.0, 5537823.0,
      4874515.0, 4289755.0, 3775385.0, 3323588.0, 2927106.0, 2579338.0,
      2274356.0, 2006887.0, 1772266.0, 1566386.0, 1385643.0, 1226879.0,
      1087335.0, 964598.0, 856565.0, 761399.0, 677498.0, 603467.0, 538088.0,
      480296.0, 429166.0, 383886.0, 343751.0, 308141.0, 276516.0, 248403.0,
      223388.0, 201108.0, 181245.0, 163519.0, 147684.0, 133526.0, 120853.0,
      109500.0, 99319.0, 90180.0, 81969.0, 74584.0, 67935.0, 61944.0, 56540.0,
      51661.0, 47252.0, 43264.0, 39652.0, 36380.0, 33411.0, 30715.0, 28265.0,
      26037.0, 24007.0, 22158.0, 20471.0, 18931.0, 17524.0, 16236.0, 15058.0,
      13978.0, 12988.0, 12079.0, 11244.0, 10476.0, 9769.0, 9118.0, 8519.0,
      7965.0, 7454.0, 6982.0, 6545.0, 6141.0, 5766.0, 5419.0, 5097.0, 4798.0,
      4520.0, 4261.0, 4020.0, 3796.0, 3588.0, 3393.0, 3211.0, 3041.0, 2882.0,
      2734.0, 2595.0, 2465.0, 2343.0, 2228.0, 2121.0, 2020.0, 1925.0, 1836.0,
      1752.0, 1673.0, 1599.0, 1528.0, 1462.0, 1400.0, 1341.0, 1285.0, 1232.0,
      1182.0, 1135.0, 1090.0, 1048.0, 1008.0, 970.0, 934.0, 899.0, 867.0, 836.0,
      806.0, 778.0, 751.0, 726.0, 701.0, 678.0, 656.0, 635.0, 615.0, 596.0,
      578.0, 560.0, 543.0, 527.0, 512.0, 497.0, 483.0, 470.0, 457.0, 444.0,
      432.0, 421.0, 410.0, 399.0, 389.0, 379.0, 370.0, 361.0, 352.0, 344.0,
      336.0, 328.0, 321.0, 314.0, 307.0, 300.0, 294.0, 287.0, 281.0, 276.0,
      270.0, 265.0, 259.0, 254.0, 249.0, 245.0, 240.0, 236.0, 231.0, 227.0,
      223.0, 219.0, 215.0, 212.0, 208.0, 205.0, 201.0,
    ],
    [
      8349837.0, 8033094.0, 7544130.0, 6965578.0, 6354510.0, 5747499.0,
      5166413.0, 4623218.0, 4123480.0, 3668777.0, 3258295.0, 2889874.0,
      2560688.0, 2267549.0, 2007167.0, 1776320.0, 1571951.0, 1391217.0,
      1231512.0, 1090469.0, 965956.0, 856059.0, 759071.0, 673472.0, 597915.0,
      531206.0, 472291.0, 420240.0, 374232.0, 333545.0, 297543.0, 265668.0,
      237429.0, 212393.0, 190181.0, 170460.0, 152937.0, 137355.0, 123486.0,
      111132.0, 100118.0, 90291.0, 81513.0, 73667.0, 66647.0, 60359.0, 54723.0,
      49667.0, 45125.0, 41042.0, 37368.0, 34060.0, 31076.0, 28384.0, 25953.0,
      23754.0, 21765.0, 19962.0, 18328.0, 16845.0, 15497.0, 14272.0, 13157.0,
      12141.0, 11214.0, 10369.0, 9596.0, 8890.0, 8243.0, 7651.0, 7108.0, 6610.0,
      6152.0, 5732.0, 5344.0, 4988.0, 4659.0, 4356.0, 4077.0, 3818.0, 3579.0,
      3358.0, 3153.0, 2963.0, 2786.0, 2623.0, 2471.0, 2329.0, 2198.0, 2075.0,
      1961.0, 1855.0, 1755.0, 1662.0, 1575.0, 1494.0, 1418.0, 1347.0, 1280.0,
      1218.0, 1159.0, 1104.0, 1052.0, 1003.0, 958.0, 914.0, 874.0, 835.0, 799.0,
      765.0, 733.0, 702.0, 674.0, 646.0, 621.0, 596.0, 573.0, 551.0, 530.0,
      510.0, 492.0, 474.0, 457.0, 441.0, 425.0, 411.0, 397.0, 384.0, 371.0,
      359.0, 347.0, 336.0, 326.0, 316.0, 306.0, 297.0, 288.0, 280.0, 272.0,
      264.0, 257.0, 250.0, 243.0, 237.0, 230.0, 224.0, 219.0, 213.0, 208.0,
      203.0, 198.0, 193.0, 188.0, 184.0, 180.0, 176.0, 172.0, 168.0, 164.0,
      161.0, 157.0, 154.0, 151.0, 148.0, 145.0, 142.0, 139.0, 137.0, 134.0,
      131.0, 129.0, 127.0, 124.0, 122.0, 120.0, 118.0, 116.0, 114.0, 112.0,
      110.0,
    ],
    [
      7171076.0, 6881808.0, 6437263.0, 5922786.0, 5389347.0, 4866473.0,
      4370471.0, 3909568.0, 3487120.0, 3103578.0, 2757722.0, 2447429.0,
      2170172.0, 1923193.0, 1703694.0, 1508961.0, 1336428.0, 1183721.0,
      1048661.0, 929274.0, 823780.0, 730582.0, 648254.0, 575528.0, 511275.0,
      454496.0, 404309.0, 359932.0, 320677.0, 285936.0, 255173.0, 227919.0,
      203758.0, 182325.0, 163300.0, 146399.0, 131375.0, 118009.0, 106109.0,
      95505.0, 86048.0, 77607.0, 70067.0, 63325.0, 57292.0, 51887.0, 47042.0,
      42695.0, 38790.0, 35279.0, 32120.0, 29275.0, 26709.0, 24394.0, 22303.0,
      20413.0, 18702.0, 17152.0, 15747.0, 14472.0, 13313.0, 12260.0, 11301.0,
      10428.0, 9632.0, 8905.0, 8241.0, 7634.0, 7079.0, 6570.0, 6104.0, 5676.0,
      5282.0, 4921.0, 4589.0, 4282.0, 4000.0, 3740.0, 3500.0, 3278.0, 3073.0,
      2883.0, 2707.0, 2544.0, 2392.0, 2252.0, 2121.0, 2000.0, 1887.0, 1782.0,
      1684.0, 1592.0, 1507.0, 1427.0, 1353.0, 1283.0, 1218.0, 1157.0, 1100.0,
      1046.0, 995.0, 948.0, 904.0, 862.0, 822.0, 785.0, 750.0, 718.0, 686.0,
      657.0, 630.0, 603.0, 579.0, 555.0, 533.0, 512.0, 492.0, 473.0, 456.0,
      439.0, 422.0, 407.0, 393.0, 379.0, 366.0, 353.0, 341.0, 330.0, 319.0,
      308.0, 299.0, 289.0, 280.0, 272.0, 263.0, 255.0, 248.0, 241.0, 234.0,
      227.0, 221.0, 215.0, 209.0, 203.0, 198.0, 193.0, 188.0, 183.0, 179.0,
      174.0, 170.0, 166.0, 162.0, 158.0, 155.0, 151.0, 148.0, 144.0, 141.0,
      138.0, 135.0, 133.0, 130.0, 127.0, 125.0, 122.0, 120.0, 117.0, 115.0,
      113.0, 111.0, 109.0, 107.0, 105.0, 103.0, 102.0, 100.0, 98.0, 97.0, 95.0,
    ],
    [
      6835022.0, 6551015.0, 6118334.0, 5622714.0, 5112831.0, 4615723.0,
      4145769.0, 3709928.0, 3310819.0, 2948543.0, 2621774.0, 2328436.0,
      2066130.0, 1832271.0, 1624245.0, 1439521.0, 1275708.0, 1130588.0,
      1002130.0, 888485.0, 787987.0, 699138.0, 620598.0, 551172.0, 489799.0,
      435535.0, 387545.0, 345092.0, 307521.0, 274258.0, 244793.0, 218680.0,
      195524.0, 174977.0, 156733.0, 140524.0, 126112.0, 113288.0, 101868.0,
      91692.0, 82615.0, 74512.0, 67274.0, 60801.0, 55008.0, 49820.0, 45167.0,
      40993.0, 37243.0, 33872.0, 30838.0, 28106.0, 25643.0, 23420.0, 21412.0,
      19597.0, 17954.0, 16466.0, 15117.0, 13893.0, 12780.0, 11769.0, 10849.0,
      10010.0, 9246.0, 8548.0, 7911.0, 7328.0, 6795.0, 6307.0, 5859.0, 5448.0,
      5071.0, 4724.0, 4405.0, 4111.0, 3840.0, 3590.0, 3359.0, 3146.0, 2949.0,
      2767.0, 2598.0, 2442.0, 2296.0, 2162.0, 2036.0, 1920.0, 1811.0, 1710.0,
      1616.0, 1529.0, 1447.0, 1370.0, 1299.0, 1232.0, 1169.0, 1111.0, 1056.0,
      1004.0, 956.0, 910.0, 868.0, 827.0, 790.0, 754.0, 721.0, 689.0, 659.0,
      631.0, 605.0, 579.0, 556.0, 533.0, 512.0, 492.0, 473.0, 455.0, 438.0,
      421.0, 406.0, 391.0, 377.0, 364.0, 351.0, 339.0, 328.0, 317.0, 306.0,
      296.0, 287.0, 278.0, 269.0, 261.0, 253.0, 245.0, 238.0, 231.0, 225.0,
      218.0, 212.0, 206.0, 201.0, 195.0, 190.0, 185.0, 181.0, 176.0, 172.0,
      167.0, 163.0, 159.0, 156.0, 152.0, 149.0, 145.0, 142.0, 139.0, 136.0,
      133.0, 130.0, 127.0, 125.0, 122.0, 120.0, 117.0, 115.0, 113.0, 111.0,
      109.0, 107.0, 105.0, 103.0, 101.0, 99.0, 98.0, 96.0, 94.0, 93.0, 91.0,
    ],
  ],
  peakHospitalization: 34478.0,
  symptomaticInfectionTimeSeries: [
    [
      1009528.0, 961238.0, 905924.0, 839769.0, 766547.0, 691084.0, 617214.0,
      547436.0, 483133.0, 424884.0, 372755.0, 326501.0, 285722.0, 249939.0,
      218650.0, 191354.0, 167579.0, 146888.0, 128888.0, 113227.0, 99597.0,
      87726.0, 77379.0, 68351.0, 60465.0, 53569.0, 47529.0, 42234.0, 37583.0,
      33494.0, 29893.0, 26717.0, 23912.0, 21431.0, 19234.0, 17284.0, 15553.0,
      14013.0, 12641.0, 11417.0, 10325.0, 9348.0, 8473.0, 7689.0, 6985.0,
      6353.0, 5784.0, 5272.0, 4810.0, 4394.0, 4017.0, 3677.0, 3368.0, 3089.0,
      2836.0, 2606.0, 2397.0, 2207.0, 2033.0, 1876.0, 1732.0, 1600.0, 1480.0,
      1370.0, 1270.0, 1178.0, 1093.0, 1016.0, 945.0, 879.0, 819.0, 764.0, 713.0,
      666.0, 622.0, 582.0, 545.0, 511.0, 479.0, 449.0, 422.0, 397.0, 373.0,
      351.0, 331.0, 312.0, 295.0, 278.0, 263.0, 249.0, 235.0, 223.0, 211.0,
      200.0, 190.0, 180.0, 172.0, 163.0, 155.0, 148.0, 141.0, 134.0, 128.0,
      122.0, 117.0, 112.0, 107.0, 102.0, 98.0, 94.0, 90.0, 86.0, 83.0, 79.0,
      76.0, 73.0, 71.0, 68.0, 65.0, 63.0, 61.0, 59.0, 57.0, 55.0, 53.0, 51.0,
      49.0, 48.0, 46.0, 45.0, 43.0, 42.0, 41.0, 39.0, 38.0, 37.0, 36.0, 35.0,
      34.0, 33.0, 32.0, 31.0, 30.0, 30.0, 29.0, 28.0, 27.0, 27.0, 26.0, 25.0,
      25.0, 24.0, 24.0, 23.0, 23.0, 22.0, 22.0, 21.0, 21.0, 20.0, 20.0, 19.0,
      19.0, 19.0, 18.0, 18.0, 17.0, 17.0, 17.0, 17.0, 16.0, 16.0, 16.0, 15.0,
      15.0, 15.0, 15.0, 14.0, 14.0, 14.0,
    ],
    [
      1122697.0, 1076272.0, 1018264.0, 945110.0, 862270.0, 776184.0, 691818.0,
      612330.0, 539400.0, 473681.0, 415182.0, 363537.0, 318196.0, 278533.0,
      243914.0, 213739.0, 187453.0, 164558.0, 144613.0, 127230.0, 112068.0,
      98834.0, 87272.0, 77159.0, 68306.0, 60545.0, 53734.0, 47751.0, 42487.0,
      37851.0, 33763.0, 30153.0, 26963.0, 24138.0, 21636.0, 19416.0, 17444.0,
      15690.0, 14128.0, 12737.0, 11495.0, 10386.0, 9394.0, 8506.0, 7710.0,
      6996.0, 6355.0, 5779.0, 5260.0, 4793.0, 4372.0, 3992.0, 3649.0, 3338.0,
      3058.0, 2803.0, 2572.0, 2363.0, 2172.0, 1999.0, 1842.0, 1699.0, 1568.0,
      1448.0, 1339.0, 1240.0, 1149.0, 1065.0, 989.0, 919.0, 854.0, 795.0, 741.0,
      690.0, 644.0, 602.0, 562.0, 526.0, 493.0, 462.0, 433.0, 407.0, 382.0,
      359.0, 338.0, 318.0, 300.0, 283.0, 267.0, 252.0, 238.0, 226.0, 214.0,
      202.0, 192.0, 182.0, 173.0, 164.0, 156.0, 149.0, 141.0, 135.0, 128.0,
      122.0, 117.0, 112.0, 107.0, 102.0, 98.0, 93.0, 90.0, 86.0, 82.0, 79.0,
      76.0, 73.0, 70.0, 67.0, 65.0, 62.0, 60.0, 58.0, 56.0, 54.0, 52.0, 50.0,
      49.0, 47.0, 45.0, 44.0, 43.0, 41.0, 40.0, 39.0, 38.0, 36.0, 35.0, 34.0,
      33.0, 32.0, 31.0, 31.0, 30.0, 29.0, 28.0, 27.0, 27.0, 26.0, 25.0, 25.0,
      24.0, 24.0, 23.0, 23.0, 22.0, 22.0, 21.0, 21.0, 20.0, 20.0, 19.0, 19.0,
      18.0, 18.0, 18.0, 17.0, 17.0, 17.0, 16.0, 16.0, 16.0, 16.0, 15.0, 15.0,
      15.0, 14.0, 14.0, 14.0, 14.0, 14.0,
    ],
    [
      189473.0, 185045.0, 177754.0, 167138.0, 154243.0, 140282.0, 126209.0,
      112659.0, 100003.0, 88424.0, 77976.0, 68642.0, 60358.0, 53042.0, 46602.0,
      40946.0, 35986.0, 31641.0, 27837.0, 24508.0, 21595.0, 19044.0, 16811.0,
      14854.0, 13139.0, 11635.0, 10315.0, 9155.0, 8135.0, 7237.0, 6446.0,
      5748.0, 5132.0, 4588.0, 4106.0, 3680.0, 3301.0, 2966.0, 2667.0, 2401.0,
      2165.0, 1954.0, 1765.0, 1597.0, 1446.0, 1311.0, 1190.0, 1081.0, 984.0,
      896.0, 817.0, 745.0, 681.0, 623.0, 570.0, 522.0, 479.0, 440.0, 405.0,
      372.0, 343.0, 316.0, 292.0, 269.0, 249.0, 231.0, 214.0, 198.0, 184.0,
      171.0, 159.0, 148.0, 138.0, 128.0, 120.0, 112.0, 104.0, 98.0, 91.0, 86.0,
      80.0, 75.0, 71.0, 67.0, 63.0, 59.0, 56.0, 52.0, 49.0, 47.0, 44.0, 42.0,
      40.0, 37.0, 36.0, 34.0, 32.0, 30.0, 29.0, 27.0, 26.0, 25.0, 24.0, 23.0,
      22.0, 21.0, 20.0, 19.0, 18.0, 17.0, 17.0, 16.0, 15.0, 15.0, 14.0, 13.0,
      13.0, 12.0, 12.0, 12.0, 11.0, 11.0, 10.0, 10.0, 10.0, 9.0, 9.0, 9.0, 8.0,
      8.0, 8.0, 8.0, 7.0, 7.0, 7.0, 7.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 5.0, 5.0,
      5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0,
      4.0, 4.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
      3.0, 3.0, 3.0, 3.0, 3.0, 2.0,
    ],
    [
      58499.0, 57124.0, 54768.0, 51267.0, 46991.0, 42368.0, 37735.0, 33314.0,
      29231.0, 25543.0, 22261.0, 19373.0, 16848.0, 14651.0, 12746.0, 11097.0,
      9671.0, 8438.0, 7372.0, 6449.0, 5651.0, 4958.0, 4357.0, 3835.0, 3381.0,
      2985.0, 2639.0, 2337.0, 2073.0, 1841.0, 1638.0, 1459.0, 1301.0, 1162.0,
      1040.0, 931.0, 835.0, 750.0, 674.0, 607.0, 547.0, 494.0, 446.0, 403.0,
      365.0, 331.0, 300.0, 273.0, 248.0, 226.0, 206.0, 188.0, 172.0, 157.0,
      144.0, 132.0, 121.0, 111.0, 102.0, 94.0, 86.0, 80.0, 73.0, 68.0, 63.0,
      58.0, 54.0, 50.0, 46.0, 43.0, 40.0, 37.0, 35.0, 32.0, 30.0, 28.0, 26.0,
      24.0, 23.0, 21.0, 20.0, 19.0, 18.0, 17.0, 16.0, 15.0, 14.0, 13.0, 12.0,
      12.0, 11.0, 10.0, 10.0, 9.0, 9.0, 8.0, 8.0, 8.0, 7.0, 7.0, 7.0, 6.0, 6.0,
      6.0, 5.0, 5.0, 5.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 3.0, 3.0, 3.0,
      3.0, 3.0, 3.0, 3.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
      2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0,
    ],
    [
      21160.0, 20369.0, 19331.0, 17924.0, 16264.0, 14501.0, 12759.0, 11119.0,
      9626.0, 8297.0, 7133.0, 6125.0, 5259.0, 4517.0, 3885.0, 3347.0, 2889.0,
      2498.0, 2166.0, 1881.0, 1638.0, 1430.0, 1250.0, 1096.0, 963.0, 847.0,
      747.0, 660.0, 584.0, 518.0, 460.0, 409.0, 365.0, 326.0, 291.0, 260.0,
      233.0, 209.0, 188.0, 169.0, 153.0, 138.0, 124.0, 112.0, 102.0, 92.0, 84.0,
      76.0, 69.0, 63.0, 57.0, 52.0, 48.0, 44.0, 40.0, 36.0, 33.0, 31.0, 28.0,
      26.0, 24.0, 22.0, 20.0, 19.0, 17.0, 16.0, 15.0, 14.0, 13.0, 12.0, 11.0,
      10.0, 9.0, 9.0, 8.0, 8.0, 7.0, 7.0, 6.0, 6.0, 6.0, 5.0, 5.0, 5.0, 4.0,
      4.0, 4.0, 4.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
      2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0,
    ],
  ],
};
