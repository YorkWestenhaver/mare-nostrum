// All data is imported from JSON files produced by data/process.py.
// No inline data. Every dataset traces back to a raw source file.

import _lead from './lead-emissions_mcconnell2018.json';
import _treeRings from './tree-rings_buentgen2011.json';
import _volcanic from './volcanic-events_evolv2k.json';
import _timber from './timber-construction_tegel2025.json';
import _cattle from './cattle-biometry_trentacoste.json';
import _gdp from './gdp-per-capita_maddison2023.json';
import _shipwrecks25 from './shipwrecks-25yr_strauss.json';
import _shipwrecks50 from './shipwrecks-50yr_strauss.json';
import _metTimeline from './met-timeline-25yr_metmuseum.json';
import _metByDept from './met-by-department_metmuseum.json';
import _metByClass from './met-by-classification_metmuseum.json';
import _metByCulture from './met-by-culture_metmuseum.json';
import _metGR from './met-greek-roman_metmuseum.json';
import _metComposite from './met-composite-index_metmuseum.json';

export const LEAD_DATA = _lead;
export const TREE_RINGS = _treeRings;
export const VOLCANIC_EVENTS = _volcanic;
export const TIMBER_DATA = _timber;
export const CATTLE_DATA = _cattle;
export const GDP_DATA = _gdp;
export const SHIPWRECKS_25 = _shipwrecks25;
export const SHIPWRECKS_50 = _shipwrecks50;
export const MET_TIMELINE = _metTimeline;
export const MET_BY_DEPARTMENT = _metByDept;
export const MET_BY_CLASSIFICATION = _metByClass;
export const MET_BY_CULTURE = _metByCulture;
export const MET_GREEK_ROMAN = _metGR;
export const MET_COMPOSITE = _metComposite;
