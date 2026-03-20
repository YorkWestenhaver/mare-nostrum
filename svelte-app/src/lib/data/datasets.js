// Datasets processed from downloaded academic sources (see data/process_all.py)
import _lead from './lead_mcconnell.json';
import _treeRings from './tree_rings_buentgen.json';
import _volcanic from './volcanic_evolv2k.json';
import _timber from './timber_tegel.json';
import _cattle from './cattle_trentacoste.json';
import _gdp from './gdp_maddison.json';

export const LEAD_DATA = _lead;
export const TREE_RINGS = _treeRings;
export const VOLCANIC_EVENTS = _volcanic;
export const TIMBER_DATA = _timber;
export const CATTLE_DATA = _cattle;
export const GDP_DATA = _gdp;

export const SHIPWRECKS_25 = [{"mid": -587.5, "total": 4.12, "western": 3.01, "eastern": 0.57, "adriatic": 0.29, "black_sea": 0.25}, {"mid": -562.5, "total": 6.38, "western": 4.3, "eastern": 1.54, "adriatic": 0.29, "black_sea": 0.25}, {"mid": -537.5, "total": 8.64, "western": 7.14, "eastern": 0.96, "adriatic": 0.29, "black_sea": 0.25}, {"mid": -512.5, "total": 10.69, "western": 8.23, "eastern": 0.92, "adriatic": 1.29, "black_sea": 0.25}, {"mid": -487.5, "total": 11.11, "western": 5.99, "eastern": 3.09, "adriatic": 1.32, "black_sea": 0.72}, {"mid": -462.5, "total": 9.9, "western": 3.84, "eastern": 3.03, "adriatic": 0.31, "black_sea": 2.72}, {"mid": -437.5, "total": 12.41, "western": 6.57, "eastern": 4.92, "adriatic": 0.13, "black_sea": 0.8}, {"mid": -412.5, "total": 13.83, "western": 6.09, "eastern": 6.9, "adriatic": 0.12, "black_sea": 0.72}, {"mid": -387.5, "total": 16.23, "western": 7.63, "eastern": 6.15, "adriatic": 0.88, "black_sea": 1.57}, {"mid": -362.5, "total": 12.17, "western": 5.13, "eastern": 5.25, "adriatic": 0.88, "black_sea": 0.92}, {"mid": -337.5, "total": 13.89, "western": 5.49, "eastern": 6.78, "adriatic": 0.88, "black_sea": 0.73}, {"mid": -312.5, "total": 19.63, "western": 8.62, "eastern": 8.26, "adriatic": 0.88, "black_sea": 1.86}, {"mid": -287.5, "total": 26.33, "western": 15.94, "eastern": 6.2, "adriatic": 2.4, "black_sea": 1.79}, {"mid": -262.5, "total": 19.1, "western": 12.14, "eastern": 4.72, "adriatic": 1.41, "black_sea": 0.83}, {"mid": -237.5, "total": 16.27, "western": 10.71, "eastern": 3.86, "adriatic": 0.9, "black_sea": 0.81}, {"mid": -212.5, "total": 17.05, "western": 12.04, "eastern": 3.33, "adriatic": 0.88, "black_sea": 0.81}, {"mid": -187.5, "total": 39.38, "western": 32.52, "eastern": 4.63, "adriatic": 1.57, "black_sea": 0.67}, {"mid": -162.5, "total": 36.76, "western": 28.88, "eastern": 4.1, "adriatic": 3.14, "black_sea": 0.64}, {"mid": -137.5, "total": 53.54, "western": 41.22, "eastern": 7.56, "adriatic": 4.33, "black_sea": 0.16}, {"mid": -112.5, "total": 64.08, "western": 52.59, "eastern": 6.59, "adriatic": 4.49, "black_sea": 0.14}, {"mid": -87.5, "total": 81.03, "western": 65.91, "eastern": 8.27, "adriatic": 6.36, "black_sea": 0.14}, {"mid": -62.5, "total": 65.42, "western": 50.66, "eastern": 7.59, "adriatic": 6.68, "black_sea": 0.14}, {"mid": -37.5, "total": 78.03, "western": 60.11, "eastern": 9.2, "adriatic": 7.79, "black_sea": 0.05}, {"mid": -12.5, "total": 67.97, "western": 49.07, "eastern": 8.63, "adriatic": 8.89, "black_sea": 0.05}, {"mid": 12.5, "total": 87.95, "western": 69.14, "eastern": 6.14, "adriatic": 10.62, "black_sea": 0.0}, {"mid": 37.5, "total": 88.48, "western": 68.73, "eastern": 7.17, "adriatic": 10.38, "black_sea": 0.0}, {"mid": 62.5, "total": 88.27, "western": 67.53, "eastern": 6.2, "adriatic": 10.3, "black_sea": 0.0}, {"mid": 87.5, "total": 84.38, "western": 57.04, "eastern": 6.36, "adriatic": 13.47, "black_sea": 0.0}, {"mid": 112.5, "total": 45.16, "western": 24.57, "eastern": 5.11, "adriatic": 6.31, "black_sea": 1.0}, {"mid": 137.5, "total": 38.82, "western": 25.08, "eastern": 3.61, "adriatic": 4.54, "black_sea": 0.04}, {"mid": 162.5, "total": 37.75, "western": 22.69, "eastern": 4.58, "adriatic": 2.89, "black_sea": 0.0}, {"mid": 187.5, "total": 39.0, "western": 24.86, "eastern": 3.48, "adriatic": 2.75, "black_sea": 0.0}, {"mid": 212.5, "total": 40.97, "western": 30.08, "eastern": 3.59, "adriatic": 1.95, "black_sea": 0.0}, {"mid": 237.5, "total": 31.24, "western": 23.75, "eastern": 4.03, "adriatic": 1.88, "black_sea": 0.0}, {"mid": 262.5, "total": 33.8, "western": 26.7, "eastern": 3.73, "adriatic": 1.9, "black_sea": 0.0}, {"mid": 287.5, "total": 35.12, "western": 23.29, "eastern": 4.79, "adriatic": 2.78, "black_sea": 0.0}, {"mid": 312.5, "total": 38.3, "western": 29.61, "eastern": 3.83, "adriatic": 2.47, "black_sea": 0.21}, {"mid": 337.5, "total": 25.58, "western": 18.07, "eastern": 3.51, "adriatic": 2.96, "black_sea": 0.21}, {"mid": 362.5, "total": 20.33, "western": 15.01, "eastern": 2.33, "adriatic": 2.16, "black_sea": 0.21}, {"mid": 387.5, "total": 25.04, "western": 16.89, "eastern": 4.8, "adriatic": 2.16, "black_sea": 0.58}, {"mid": 412.5, "total": 23.7, "western": 9.26, "eastern": 3.54, "adriatic": 1.57, "black_sea": 1.8}, {"mid": 437.5, "total": 12.4, "western": 7.29, "eastern": 2.37, "adriatic": 0.94, "black_sea": 1.8}, {"mid": 462.5, "total": 10.26, "western": 4.66, "eastern": 2.9, "adriatic": 0.8, "black_sea": 1.9}, {"mid": 487.5, "total": 11.63, "western": 5.23, "eastern": 3.3, "adriatic": 0.79, "black_sea": 2.3}, {"mid": 512.5, "total": 10.87, "western": 2.94, "eastern": 5.75, "adriatic": 0.31, "black_sea": 1.87}, {"mid": 537.5, "total": 10.98, "western": 4.08, "eastern": 5.34, "adriatic": 0.29, "black_sea": 1.27}, {"mid": 562.5, "total": 9.93, "western": 2.71, "eastern": 5.5, "adriatic": 0.29, "black_sea": 1.43}, {"mid": 587.5, "total": 10.43, "western": 2.17, "eastern": 6.54, "adriatic": 0.29, "black_sea": 1.43}, {"mid": 612.5, "total": 8.94, "western": 1.78, "eastern": 6.36, "adriatic": 0.17, "black_sea": 0.63}, {"mid": 637.5, "total": 9.86, "western": 2.64, "eastern": 6.65, "adriatic": 0.17, "black_sea": 0.4}, {"mid": 662.5, "total": 6.8, "western": 2.21, "eastern": 4.03, "adriatic": 0.17, "black_sea": 0.4}, {"mid": 687.5, "total": 6.85, "western": 2.17, "eastern": 4.12, "adriatic": 0.17, "black_sea": 0.4}, {"mid": 712.5, "total": 2.12, "western": 0.42, "eastern": 1.62, "adriatic": 0.01, "black_sea": 0.08}, {"mid": 737.5, "total": 1.57, "western": 0.33, "eastern": 1.17, "adriatic": 0.0, "black_sea": 0.06}, {"mid": 762.5, "total": 0.91, "western": 0.28, "eastern": 0.57, "adriatic": 0.0, "black_sea": 0.06}, {"mid": 787.5, "total": 0.88, "western": 0.28, "eastern": 0.54, "adriatic": 0.0, "black_sea": 0.06}, {"mid": 812.5, "total": 1.54, "western": 0.12, "eastern": 1.29, "adriatic": 0.12, "black_sea": 0.0}, {"mid": 837.5, "total": 1.53, "western": 0.11, "eastern": 1.29, "adriatic": 0.12, "black_sea": 0.0}, {"mid": 862.5, "total": 1.07, "western": 0.11, "eastern": 0.67, "adriatic": 0.29, "black_sea": 0.0}, {"mid": 887.5, "total": 2.05, "western": 0.11, "eastern": 1.64, "adriatic": 0.29, "black_sea": 0.0}, {"mid": 912.5, "total": 2.39, "western": 0.86, "eastern": 1.24, "adriatic": 0.29, "black_sea": 0.0}, {"mid": 937.5, "total": 2.84, "western": 1.36, "eastern": 1.19, "adriatic": 0.29, "black_sea": 0.0}, {"mid": 962.5, "total": 2.84, "western": 1.36, "eastern": 1.19, "adriatic": 0.29, "black_sea": 0.0}, {"mid": 987.5, "total": 2.56, "western": 0.88, "eastern": 1.39, "adriatic": 0.29, "black_sea": 0.0}];

export const SHIPWRECKS_50 = [{"mid": -575.0, "total": 10.51, "western": 7.31, "eastern": 2.11, "adriatic": 0.58, "black_sea": 0.5}, {"mid": -525.0, "total": 19.33, "western": 15.37, "eastern": 1.87, "adriatic": 1.58, "black_sea": 0.5}, {"mid": -475.0, "total": 21.02, "western": 9.83, "eastern": 6.13, "adriatic": 1.63, "black_sea": 3.43}, {"mid": -425.0, "total": 26.25, "western": 12.66, "eastern": 11.82, "adriatic": 0.26, "black_sea": 1.51}, {"mid": -375.0, "total": 28.39, "western": 12.75, "eastern": 11.4, "adriatic": 1.75, "black_sea": 2.49}, {"mid": -325.0, "total": 33.51, "western": 14.12, "eastern": 15.05, "adriatic": 1.75, "black_sea": 2.6}, {"mid": -275.0, "total": 45.43, "western": 28.08, "eastern": 10.91, "adriatic": 3.81, "black_sea": 2.62}, {"mid": -225.0, "total": 33.32, "western": 22.75, "eastern": 7.19, "adriatic": 1.77, "black_sea": 1.61}, {"mid": -175.0, "total": 76.14, "western": 61.39, "eastern": 8.73, "adriatic": 4.71, "black_sea": 1.31}, {"mid": -125.0, "total": 117.62, "western": 93.81, "eastern": 14.15, "adriatic": 8.83, "black_sea": 0.3}, {"mid": -75.0, "total": 146.44, "western": 116.56, "eastern": 15.86, "adriatic": 13.04, "black_sea": 0.28}, {"mid": -25.0, "total": 146.0, "western": 109.18, "eastern": 17.83, "adriatic": 16.68, "black_sea": 0.1}, {"mid": 25.0, "total": 176.43, "western": 137.87, "eastern": 13.31, "adriatic": 20.99, "black_sea": 0.0}, {"mid": 75.0, "total": 172.66, "western": 124.56, "eastern": 12.56, "adriatic": 23.77, "black_sea": 0.0}, {"mid": 125.0, "total": 83.98, "western": 49.64, "eastern": 8.72, "adriatic": 10.85, "black_sea": 1.04}, {"mid": 175.0, "total": 76.75, "western": 47.55, "eastern": 8.06, "adriatic": 5.64, "black_sea": 0.0}, {"mid": 225.0, "total": 72.21, "western": 53.83, "eastern": 7.62, "adriatic": 3.82, "black_sea": 0.0}, {"mid": 275.0, "total": 68.92, "western": 49.99, "eastern": 8.52, "adriatic": 4.68, "black_sea": 0.0}, {"mid": 325.0, "total": 63.88, "western": 47.68, "eastern": 7.34, "adriatic": 5.42, "black_sea": 0.42}, {"mid": 375.0, "total": 45.36, "western": 31.9, "eastern": 7.12, "adriatic": 4.32, "black_sea": 0.78}, {"mid": 425.0, "total": 36.11, "western": 16.55, "eastern": 5.91, "adriatic": 2.51, "black_sea": 3.61}, {"mid": 475.0, "total": 21.89, "western": 9.9, "eastern": 6.2, "adriatic": 1.59, "black_sea": 4.21}, {"mid": 525.0, "total": 21.85, "western": 7.02, "eastern": 11.08, "adriatic": 0.6, "black_sea": 3.14}, {"mid": 575.0, "total": 20.36, "western": 4.88, "eastern": 12.04, "adriatic": 0.58, "black_sea": 2.86}, {"mid": 625.0, "total": 18.8, "western": 4.42, "eastern": 13.01, "adriatic": 0.34, "black_sea": 1.03}, {"mid": 675.0, "total": 13.65, "western": 4.37, "eastern": 8.16, "adriatic": 0.33, "black_sea": 0.79}, {"mid": 725.0, "total": 3.69, "western": 0.75, "eastern": 2.79, "adriatic": 0.01, "black_sea": 0.14}, {"mid": 775.0, "total": 1.79, "western": 0.56, "eastern": 1.11, "adriatic": 0.0, "black_sea": 0.12}, {"mid": 825.0, "total": 3.07, "western": 0.23, "eastern": 2.58, "adriatic": 0.25, "black_sea": 0.0}, {"mid": 875.0, "total": 3.12, "western": 0.22, "eastern": 2.31, "adriatic": 0.58, "black_sea": 0.0}, {"mid": 925.0, "total": 5.23, "western": 2.22, "eastern": 2.43, "adriatic": 0.58, "black_sea": 0.0}, {"mid": 975.0, "total": 5.4, "western": 2.24, "eastern": 2.57, "adriatic": 0.58, "black_sea": 0.0}];

export const DENARIUS = [{"year": -210, "silver": 97.0, "emperor": "Republic (post-Second Punic War)"}, {"year": -150, "silver": 97.0, "emperor": "Republic"}, {"year": -100, "silver": 97.0, "emperor": "Late Republic"}, {"year": -50, "silver": 97.5, "emperor": "Late Republic"}, {"year": -27, "silver": 98.0, "emperor": "Augustus (early)"}, {"year": 14, "silver": 97.5, "emperor": "Augustus (late) / Tiberius"}, {"year": 37, "silver": 97.5, "emperor": "Caligula"}, {"year": 54, "silver": 97.0, "emperor": "Claudius"}, {"year": 64, "silver": 93.5, "emperor": "Nero (post-reform)"}, {"year": 68, "silver": 93.0, "emperor": "Galba"}, {"year": 69, "silver": 93.0, "emperor": "Vitellius"}, {"year": 79, "silver": 92.0, "emperor": "Vespasian"}, {"year": 81, "silver": 92.0, "emperor": "Titus"}, {"year": 96, "silver": 92.0, "emperor": "Domitian"}, {"year": 98, "silver": 93.0, "emperor": "Nerva / Trajan (early)"}, {"year": 107, "silver": 89.0, "emperor": "Trajan (middle)"}, {"year": 117, "silver": 87.0, "emperor": "Trajan (late) / Hadrian"}, {"year": 138, "silver": 83.0, "emperor": "Hadrian (late) / Antoninus Pius"}, {"year": 161, "silver": 79.0, "emperor": "Marcus Aurelius"}, {"year": 180, "silver": 75.0, "emperor": "Commodus"}, {"year": 193, "silver": 60.0, "emperor": "Pertinax / Septimius Severus (early)"}, {"year": 200, "silver": 56.0, "emperor": "Septimius Severus"}, {"year": 211, "silver": 52.0, "emperor": "Caracalla (pre-antoninianus)"}, {"year": 215, "silver": 51.5, "emperor": "Caracalla (antoninianus introduced)"}, {"year": 222, "silver": 47.0, "emperor": "Severus Alexander"}, {"year": 238, "silver": 45.0, "emperor": "Maximinus / Gordian III"}, {"year": 253, "silver": 40.0, "emperor": "Valerian / Gallienus (early)"}, {"year": 260, "silver": 20.0, "emperor": "Gallienus (sole reign)"}, {"year": 268, "silver": 2.5, "emperor": "Claudius II"}, {"year": 270, "silver": 2.0, "emperor": "Aurelian (pre-reform)"}, {"year": 274, "silver": 5.0, "emperor": "Aurelian (post-reform)"}, {"year": 284, "silver": 4.0, "emperor": "Diocletian (pre-reform)"}, {"year": 294, "silver": 3.0, "emperor": "Diocletian (argenteus)"}];

export const LEAD_SEGMENTS = [
  {start: -599.5, end: -335.5, mean: 0.377},
  {start: -334.5, end: -10.5, mean: 0.683},
  {start: -9.5, end: 174.5, mean: 0.909},
  {start: 175.5, end: 674.5, mean: 0.330},
  {start: 675.5, end: 765.5, mean: 0.658},
  {start: 766.5, end: 799.5, mean: 1.766}
];

export const SEGMENT_COLORS = [
  'rgba(91, 141, 217, 0.12)',
  'rgba(79, 173, 122, 0.12)',
  'rgba(201, 148, 74, 0.12)',
  'rgba(217, 79, 79, 0.12)',
  'rgba(155, 109, 215, 0.12)',
  'rgba(79, 181, 173, 0.12)'
];

export const AUREUS_DATA = [
  {year: -46, weight: 8.02, label: 'Caesar', purity: 99},
  {year: -27, weight: 7.87, label: 'Augustus', purity: 99},
  {year: 14, weight: 7.78, label: 'Tiberius', purity: 99},
  {year: 54, weight: 7.75, label: 'Claudius', purity: 99},
  {year: 64, weight: 7.28, label: 'Nero (reform)', purity: 99},
  {year: 79, weight: 7.35, label: 'Vespasian', purity: 99},
  {year: 96, weight: 7.38, label: 'Domitian', purity: 99},
  {year: 107, weight: 7.12, label: 'Trajan', purity: 98},
  {year: 138, weight: 7.08, label: 'Hadrian / Antoninus Pius', purity: 98},
  {year: 161, weight: 7.06, label: 'Marcus Aurelius', purity: 98},
  {year: 193, weight: 7.01, label: 'Septimius Severus', purity: 97},
  {year: 215, weight: 6.55, label: 'Caracalla', purity: 97},
  {year: 235, weight: 6.08, label: 'Severus Alexander', purity: 97},
  {year: 253, weight: 4.70, label: 'Valerian', purity: 95},
  {year: 260, weight: 3.00, label: 'Gallienus', purity: 88},
  {year: 284, weight: 5.05, label: 'Diocletian', purity: 96}
];

export const SOLIDUS_DATA = [
  {year: 309, weight: 4.50, label: 'Constantine I', purity: 98},
  {year: 337, weight: 4.48, label: 'Constantius II', purity: 98},
  {year: 364, weight: 4.47, label: 'Valentinian I', purity: 98},
  {year: 395, weight: 4.45, label: 'Theodosius I', purity: 98},
  {year: 450, weight: 4.45, label: 'Marcian', purity: 98},
  {year: 527, weight: 4.45, label: 'Justinian I', purity: 98},
  {year: 610, weight: 4.42, label: 'Heraclius', purity: 97},
  {year: 685, weight: 4.40, label: 'Justinian II', purity: 97},
  {year: 741, weight: 4.40, label: 'Constantine V', purity: 97},
  {year: 843, weight: 4.38, label: 'Michael III', purity: 96},
  {year: 913, weight: 4.35, label: 'Constantine VII', purity: 95},
  {year: 959, weight: 4.32, label: 'Romanos II', purity: 94},
  {year: 1034, weight: 4.20, label: 'Michael IV', purity: 85},
  {year: 1042, weight: 4.10, label: 'Constantine IX', purity: 75},
  {year: 1059, weight: 4.05, label: 'Constantine X', purity: 62},
  {year: 1071, weight: 3.90, label: 'Romanos IV', purity: 50},
  {year: 1078, weight: 3.70, label: 'Nicephorus III', purity: 33},
  {year: 1092, weight: 4.05, label: 'Alexios I (hyperpyron)', purity: 83}
];

export const DIRHAM_DATA = [
  {year: 696, weight: 2.97, label: 'Abd al-Malik (reform)', purity: 97},
  {year: 715, weight: 2.95, label: 'Al-Walid I', purity: 97},
  {year: 724, weight: 2.94, label: 'Hisham', purity: 96},
  {year: 750, weight: 2.92, label: 'Early Abbasid', purity: 96},
  {year: 775, weight: 2.90, label: 'Al-Mahdi', purity: 95},
  {year: 800, weight: 2.88, label: 'Harun al-Rashid', purity: 95},
  {year: 833, weight: 2.85, label: "Al-Mu'tasim", purity: 94},
  {year: 862, weight: 2.80, label: "Al-Mu'tazz", purity: 92},
  {year: 892, weight: 2.75, label: "Al-Mu'tadid", purity: 90},
  {year: 940, weight: 2.60, label: 'Late Abbasid', purity: 85}
];

export const WHEAT_PRICES = [
  {year: 45, price: 7.5, note: 'Claudius'},
  {year: 60, price: 8.0, note: 'Nero'},
  {year: 75, price: 7.8, note: 'Vespasian'},
  {year: 90, price: 8.2, note: 'Domitian'},
  {year: 105, price: 8.0, note: 'Trajan'},
  {year: 120, price: 8.5, note: 'Hadrian'},
  {year: 135, price: 8.0, note: 'Hadrian / Antoninus Pius'},
  {year: 150, price: 8.5, note: 'Antoninus Pius'},
  {year: 160, price: 9.0, note: 'Marcus Aurelius (early)'},
  {year: 170, price: 12.0, note: 'Marcus Aurelius (plague)'},
  {year: 180, price: 16.0, note: 'Commodus'},
  {year: 190, price: 17.0, note: 'Late 2nd century'},
  {year: 200, price: 16.5, note: 'Septimius Severus'},
  {year: 220, price: 20.0, note: 'Elagabalus'},
  {year: 240, price: 24.0, note: 'Gordian III'},
  {year: 260, price: 48.0, note: 'Gallienus'},
  {year: 274, price: 200.0, note: 'Aurelian (hyperinflation)'},
  {year: 290, price: 330.0, note: 'Diocletian (pre-reform)'}
];

export const CHRE_HOARDS = [
  {mid: -187.5, total: 30, western: 18, eastern: 12},
  {mid: -162.5, total: 32, western: 24, eastern: 8},
  {mid: -137.5, total: 37, western: 25, eastern: 12},
  {mid: -112.5, total: 37, western: 21, eastern: 16},
  {mid: -87.5, total: 123, western: 59, eastern: 64},
  {mid: -62.5, total: 127, western: 65, eastern: 62},
  {mid: -37.5, total: 144, western: 61, eastern: 83},
  {mid: -12.5, total: 167, western: 68, eastern: 99},
  {mid: 12.5, total: 72, western: 46, eastern: 26},
  {mid: 37.5, total: 64, western: 51, eastern: 13},
  {mid: 62.5, total: 73, western: 46, eastern: 27},
  {mid: 87.5, total: 82, western: 59, eastern: 23},
  {mid: 112.5, total: 68, western: 45, eastern: 23},
  {mid: 137.5, total: 77, western: 62, eastern: 15},
  {mid: 162.5, total: 108, western: 92, eastern: 16},
  {mid: 187.5, total: 138, western: 108, eastern: 30},
  {mid: 212.5, total: 100, western: 77, eastern: 23},
  {mid: 237.5, total: 674, western: 439, eastern: 235},
  {mid: 262.5, total: 795, western: 448, eastern: 347},
  {mid: 287.5, total: 369, western: 173, eastern: 196},
  {mid: 312.5, total: 170, western: 82, eastern: 88},
  {mid: 337.5, total: 133, western: 66, eastern: 67},
  {mid: 362.5, total: 116, western: 62, eastern: 54},
  {mid: 387.5, total: 133, western: 71, eastern: 62},
  {mid: 412.5, total: 48, western: 33, eastern: 15},
  {mid: 437.5, total: 45, western: 27, eastern: 18},
  {mid: 462.5, total: 42, western: 29, eastern: 13},
  {mid: 487.5, total: 35, western: 17, eastern: 18}
];

export const INSCRIPTIONS_DATA = [
  {mid: -187.5, total: 14.3, western: 7.1, eastern: 7.1},
  {mid: -162.5, total: 26.6, western: 9.4, eastern: 15.9},
  {mid: -137.5, total: 21.3, western: 8.7, eastern: 12.4},
  {mid: -112.5, total: 44.6, western: 22.4, eastern: 21.5},
  {mid: -87.5, total: 89.9, western: 59.6, eastern: 28.6},
  {mid: -62.5, total: 111.2, western: 86.1, eastern: 23.3},
  {mid: -37.5, total: 262.1, western: 211.7, eastern: 44.3},
  {mid: -12.5, total: 825.2, western: 696.9, eastern: 91.1},
  {mid: 12.5, total: 2331.3, western: 2022.6, eastern: 194.0},
  {mid: 37.5, total: 2618.8, western: 2292.8, eastern: 207.0},
  {mid: 62.5, total: 2952.4, western: 2584.8, eastern: 236.5},
  {mid: 87.5, total: 3822.2, western: 3357.3, eastern: 313.8},
  {mid: 112.5, total: 5082.1, western: 4143.1, eastern: 800.6},
  {mid: 137.5, total: 5489.1, western: 4438.4, eastern: 904.5},
  {mid: 162.5, total: 6057.0, western: 4687.3, eastern: 1224.1},
  {mid: 187.5, total: 6525.6, western: 5103.1, eastern: 1301.6},
  {mid: 212.5, total: 5993.1, western: 4573.8, eastern: 1297.3},
  {mid: 237.5, total: 5019.6, western: 3754.2, eastern: 1166.6},
  {mid: 262.5, total: 3253.7, western: 2530.3, eastern: 640.0},
  {mid: 287.5, total: 2729.7, western: 2280.2, eastern: 364.6},
  {mid: 312.5, total: 1083.4, western: 781.6, eastern: 249.4},
  {mid: 337.5, total: 695.5, western: 548.9, eastern: 119.8},
  {mid: 362.5, total: 699.0, western: 570.0, eastern: 104.6},
  {mid: 387.5, total: 638.6, western: 541.5, eastern: 78.1},
  {mid: 412.5, total: 405.7, western: 365.8, eastern: 33.1},
  {mid: 437.5, total: 328.3, western: 299.5, eastern: 22.9},
  {mid: 462.5, total: 291.6, western: 263.4, eastern: 24.5},
  {mid: 487.5, total: 293.6, western: 267.0, eastern: 22.7},
  {mid: 512.5, total: 210.8, western: 185.2, eastern: 23.6},
  {mid: 537.5, total: 194.4, western: 169.2, eastern: 23.6},
  {mid: 562.5, total: 193.6, western: 169.4, eastern: 22.1},
  {mid: 587.5, total: 202.1, western: 181.0, eastern: 19.5},
  {mid: 612.5, total: 73.7, western: 70.7, eastern: 2.4},
  {mid: 637.5, total: 52.8, western: 51.5, eastern: 1.1},
  {mid: 662.5, total: 49.6, western: 48.6, eastern: 0.8},
  {mid: 687.5, total: 54.1, western: 53.2, eastern: 0.8}
];

export const POPULATION = [
  {year: -200, pop: 35, lo: 30, hi: 40, label: 'Mid-Republic'},
  {year: -100, pop: 42, lo: 35, hi: 50, label: 'Late Republic'},
  {year: -30, pop: 50, lo: 44, hi: 56, label: 'Civil Wars'},
  {year: 14, pop: 55, lo: 45, hi: 65, label: 'Augustus'},
  {year: 100, pop: 62, lo: 55, hi: 72, label: 'Trajan'},
  {year: 164, pop: 65, lo: 59, hi: 76, label: 'Pre-Antonine Plague'},
  {year: 200, pop: 50, lo: 40, hi: 55, label: 'Post-Antonine Plague'},
  {year: 250, pop: 47, lo: 38, hi: 52, label: 'Pre-Cyprian'},
  {year: 280, pop: 40, lo: 33, hi: 48, label: 'Post-Cyprian'},
  {year: 350, pop: 42, lo: 35, hi: 50, label: 'Constantine era'},
  {year: 400, pop: 40, lo: 32, hi: 48, label: 'Late Empire'},
  {year: 500, pop: 30, lo: 22, hi: 38, label: 'Post-Western collapse'},
  {year: 600, pop: 26, lo: 18, hi: 34, label: 'Post-Justinianic Plague'}
];

export const POLLEN_DATA = [
  {mid: -500, arboreal: 72, open: 28},
  {mid: -300, arboreal: 68, open: 32},
  {mid: -100, arboreal: 58, open: 42},
  {mid: 100, arboreal: 48, open: 52},
  {mid: 300, arboreal: 52, open: 48},
  {mid: 500, arboreal: 62, open: 38},
  {mid: 700, arboreal: 65, open: 35},
  {mid: 900, arboreal: 55, open: 45},
  {mid: 1100, arboreal: 42, open: 58}
];

export const CHURCH_DATA = [
  {mid: 712, count: 2}, {mid: 737, count: 3}, {mid: 762, count: 4},
  {mid: 787, count: 5}, {mid: 812, count: 6}, {mid: 837, count: 5},
  {mid: 862, count: 7}, {mid: 887, count: 8}, {mid: 912, count: 10},
  {mid: 937, count: 12}, {mid: 962, count: 18}, {mid: 987, count: 28},
  {mid: 1012, count: 42}, {mid: 1037, count: 58}, {mid: 1062, count: 75},
  {mid: 1087, count: 95}, {mid: 1112, count: 120}, {mid: 1137, count: 135},
  {mid: 1162, count: 148}, {mid: 1187, count: 162}, {mid: 1212, count: 170},
  {mid: 1237, count: 155}, {mid: 1262, count: 142}, {mid: 1287, count: 128},
  {mid: 1312, count: 110}, {mid: 1337, count: 80}, {mid: 1362, count: 50},
  {mid: 1387, count: 65}, {mid: 1412, count: 85}, {mid: 1437, count: 105},
  {mid: 1462, count: 115}, {mid: 1487, count: 125}
];

export const PAS_COINS = [
  {mid: -50, coins: 180, label: 'Late Iron Age / Early Roman'},
  {mid: 0, coins: 350, label: 'Augustan'},
  {mid: 50, coins: 520, label: 'Julio-Claudian'},
  {mid: 100, coins: 680, label: 'Flavian / Trajanic'},
  {mid: 150, coins: 750, label: 'Antonine'},
  {mid: 200, coins: 600, label: 'Severan'},
  {mid: 250, coins: 480, label: 'Mid-3rd century'},
  {mid: 300, coins: 850, label: 'Tetrarchy'},
  {mid: 350, coins: 1100, label: 'Constantinian'},
  {mid: 400, coins: 350, label: 'Late Roman'},
  {mid: 450, coins: 15, label: 'Sub-Roman'},
  {mid: 500, coins: 5, label: 'Early Anglo-Saxon'},
  {mid: 550, coins: 3, label: 'Anglo-Saxon'},
  {mid: 600, coins: 4, label: 'Early 7th century'},
  {mid: 650, coins: 8, label: 'Mid-7th century'},
  {mid: 700, coins: 45, label: 'Sceattas'},
  {mid: 750, coins: 85, label: 'Late sceattas / early pennies'},
  {mid: 800, coins: 120, label: "Offa's pennies"},
  {mid: 850, coins: 180, label: 'Viking Age'},
  {mid: 900, coins: 250, label: 'Late Anglo-Saxon'},
  {mid: 950, coins: 320, label: 'Edgar / Aethelred'},
  {mid: 1000, coins: 400, label: 'Late Anglo-Saxon / Norman'}
];
