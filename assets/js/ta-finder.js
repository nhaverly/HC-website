// TA Acquisition Finder: appraises sample listings against nightly-paid temporary accommodation.
// Data: sample listings at real postcodes with VOA LHA rates (current and January 2011),
// 2024-25 nightly-paid TA costs by London borough (London TA Atlas, OGL), and the live
// PWLB certainty rate from the daily rates.json gist.
(function () {
const LISTINGS=[{"listing_id":"L01","borough":"Luton","region":"Outside London","postcode":"LU2 0FU","brma":"Luton","property_type":"Terraced house","beds":2,"asking_price":235000,"works_cost":8000,"floor_area_sqm":68,"epc":"D","days_listed":1,"lha_2026_weekly":201.37,"lha_jan2011_weekly":138.46},{"listing_id":"L02","borough":"Harlow","region":"Outside London","postcode":"CM20 2UE","brma":"Harlow & Stortford","property_type":"Flat","beds":2,"asking_price":215000,"works_cost":4000,"floor_area_sqm":62,"epc":"C","days_listed":0,"lha_2026_weekly":235.89,"lha_jan2011_weekly":161.54},{"listing_id":"L03","borough":"Dartford","region":"Outside London","postcode":"DA1 1QT","brma":"North West Kent","property_type":"Semi-detached house","beds":3,"asking_price":365000,"works_cost":12000,"floor_area_sqm":88,"epc":"D","days_listed":3,"lha_2026_weekly":276.16,"lha_jan2011_weekly":173.08},{"listing_id":"L04","borough":"Croydon","region":"Outer London","postcode":"CR0 6DX","brma":"Outer South London","property_type":"Flat","beds":1,"asking_price":230000,"works_cost":3000,"floor_area_sqm":46,"epc":"C","days_listed":2,"lha_2026_weekly":218.63,"lha_jan2011_weekly":155.77},{"listing_id":"L05","borough":"Basildon","region":"Outside London","postcode":"SS14 2PE","brma":"South West Essex","property_type":"Terraced house","beds":3,"asking_price":320000,"works_cost":15000,"floor_area_sqm":82,"epc":"E","days_listed":1,"lha_2026_weekly":276.16,"lha_jan2011_weekly":196.15},{"listing_id":"L06","borough":"Slough","region":"Outside London","postcode":"SL1 0HZ","brma":"East Thames Valley","property_type":"Flat","beds":2,"asking_price":240000,"works_cost":5000,"floor_area_sqm":64,"epc":"C","days_listed":6,"lha_2026_weekly":276.16,"lha_jan2011_weekly":196.15},{"listing_id":"L07","borough":"Enfield","region":"Outer London","postcode":"EN3 4JY","brma":"Outer North London","property_type":"Terraced house","beds":3,"asking_price":450000,"works_cost":18000,"floor_area_sqm":90,"epc":"D","days_listed":2,"lha_2026_weekly":390.08,"lha_jan2011_weekly":300},{"listing_id":"L08","borough":"Reading","region":"Outside London","postcode":"RG1 7ED","brma":"Reading","property_type":"Terraced house","beds":4,"asking_price":420000,"works_cost":25000,"floor_area_sqm":108,"epc":"E","days_listed":0,"lha_2026_weekly":380.65,"lha_jan2011_weekly":300},{"listing_id":"L09","borough":"Portsmouth","region":"Outside London","postcode":"PO4 8JN","brma":"Portsmouth","property_type":"Terraced house","beds":4,"asking_price":285000,"works_cost":20000,"floor_area_sqm":96,"epc":"D","days_listed":4,"lha_2026_weekly":299.18,"lha_jan2011_weekly":249.23},{"listing_id":"L10","borough":"Gosport","region":"Outside London","postcode":"PO12 2RW","brma":"Portsmouth","property_type":"Terraced house","beds":2,"asking_price":185000,"works_cost":9000,"floor_area_sqm":66,"epc":"D","days_listed":1,"lha_2026_weekly":194.47,"lha_jan2011_weekly":144.23},{"listing_id":"L11","borough":"Barking and Dagenham","region":"Outer London","postcode":"IG11 9SH","brma":"Outer North East London","property_type":"Flat","beds":2,"asking_price":295000,"works_cost":4000,"floor_area_sqm":63,"epc":"B","days_listed":5,"lha_2026_weekly":287.67,"lha_jan2011_weekly":196.15},{"listing_id":"L12","borough":"Southend","region":"Outside London","postcode":"SS2 5GE","brma":"Southend","property_type":"Terraced house","beds":3,"asking_price":330000,"works_cost":10000,"floor_area_sqm":84,"epc":"D","days_listed":0,"lha_2026_weekly":253.15,"lha_jan2011_weekly":189.23},{"listing_id":"L13","borough":"Chatham","region":"Outside London","postcode":"ME4 6QT","brma":"Medway & Swale","property_type":"Terraced house","beds":3,"asking_price":275000,"works_cost":14000,"floor_area_sqm":80,"epc":"E","days_listed":2,"lha_2026_weekly":216.33,"lha_jan2011_weekly":155.77},{"listing_id":"L14","borough":"Stevenage","region":"Outside London","postcode":"SG1 5SB","brma":"Stevenage & North Herts","property_type":"Flat","beds":2,"asking_price":245000,"works_cost":3000,"floor_area_sqm":61,"epc":"C","days_listed":7,"lha_2026_weekly":224.38,"lha_jan2011_weekly":150},{"listing_id":"L15","borough":"Guildford","region":"Outside London","postcode":"GU1 3JD","brma":"Guildford","property_type":"Semi-detached house","beds":3,"asking_price":480000,"works_cost":8000,"floor_area_sqm":92,"epc":"C","days_listed":3,"lha_2026_weekly":340.6,"lha_jan2011_weekly":276.92},{"listing_id":"L16","borough":"Sittingbourne","region":"Outside London","postcode":"ME10 1BP","brma":"Medway & Swale","property_type":"Terraced house","beds":3,"asking_price":300000,"works_cost":11000,"floor_area_sqm":83,"epc":"D","days_listed":1,"lha_2026_weekly":216.33,"lha_jan2011_weekly":155.77},{"listing_id":"L17","borough":"Watford","region":"Outside London","postcode":"WD24 5HU","brma":"South West Herts","property_type":"Flat","beds":1,"asking_price":210000,"works_cost":2000,"floor_area_sqm":44,"epc":"C","days_listed":0,"lha_2026_weekly":218.63,"lha_jan2011_weekly":150},{"listing_id":"L18","borough":"Luton","region":"Outside London","postcode":"LU4 0RS","brma":"Luton","property_type":"Semi-detached house","beds":4,"asking_price":340000,"works_cost":16000,"floor_area_sqm":104,"epc":"D","days_listed":2,"lha_2026_weekly":310.68,"lha_jan2011_weekly":207.69},{"listing_id":"B01","borough":"Camden","region":"Inner London","postcode":"NW5 1UE","brma":"Inner North London","property_type":"Flat","beds":2,"asking_price":725000,"works_cost":3000,"floor_area_sqm":64,"epc":"C","days_listed":0,"lha_2026_weekly":412.86,"lha_jan2011_weekly":340},{"listing_id":"B02","borough":"City of London","region":"Inner London","postcode":"EC2Y 5AG","brma":"Central London","property_type":"Flat","beds":1,"asking_price":620000,"works_cost":5000,"floor_area_sqm":45,"epc":"D","days_listed":1,"lha_2026_weekly":331.39,"lha_jan2011_weekly":370},{"listing_id":"B03","borough":"Hackney","region":"Inner London","postcode":"E5 8QE","brma":"Inner East London","property_type":"Flat","beds":2,"asking_price":520000,"works_cost":8000,"floor_area_sqm":64,"epc":"C","days_listed":2,"lha_2026_weekly":402.74,"lha_jan2011_weekly":300},{"listing_id":"B04","borough":"Hammersmith and Fulham","region":"Inner London","postcode":"W12 0NS","brma":"Inner West London","property_type":"Flat","beds":2,"asking_price":560000,"works_cost":12000,"floor_area_sqm":64,"epc":"D","days_listed":3,"lha_2026_weekly":373.97,"lha_jan2011_weekly":315},{"listing_id":"B05","borough":"Haringey","region":"Inner London","postcode":"N17 0NB","brma":"Outer North London","property_type":"Terraced house","beds":3,"asking_price":575000,"works_cost":15000,"floor_area_sqm":86,"epc":"D","days_listed":4,"lha_2026_weekly":390.08,"lha_jan2011_weekly":300},{"listing_id":"B06","borough":"Islington","region":"Inner London","postcode":"N19 4HG","brma":"Inner North London","property_type":"Flat","beds":2,"asking_price":600000,"works_cost":3000,"floor_area_sqm":64,"epc":"C","days_listed":0,"lha_2026_weekly":412.86,"lha_jan2011_weekly":340},{"listing_id":"B07","borough":"Kensington and Chelsea","region":"Inner London","postcode":"W10 6BY","brma":"Inner North London","property_type":"Flat","beds":2,"asking_price":700000,"works_cost":5000,"floor_area_sqm":64,"epc":"B","days_listed":1,"lha_2026_weekly":412.86,"lha_jan2011_weekly":340},{"listing_id":"B08","borough":"Lambeth","region":"Inner London","postcode":"SW16 3DU","brma":"Inner South East London","property_type":"Flat","beds":2,"asking_price":430000,"works_cost":8000,"floor_area_sqm":64,"epc":"D","days_listed":2,"lha_2026_weekly":356.71,"lha_jan2011_weekly":253.85},{"listing_id":"B09","borough":"Lewisham","region":"Inner London","postcode":"SE6 1SS","brma":"Inner South East London","property_type":"Terraced house","beds":3,"asking_price":480000,"works_cost":20000,"floor_area_sqm":86,"epc":"C","days_listed":3,"lha_2026_weekly":448.77,"lha_jan2011_weekly":300},{"listing_id":"B10","borough":"Newham","region":"Inner London","postcode":"E13 8QT","brma":"Outer East London","property_type":"Terraced house","beds":3,"asking_price":440000,"works_cost":10000,"floor_area_sqm":86,"epc":"D","days_listed":4,"lha_2026_weekly":385.48,"lha_jan2011_weekly":255},{"listing_id":"B11","borough":"Southwark","region":"Inner London","postcode":"SE15 6QT","brma":"Inner South East London","property_type":"Flat","beds":2,"asking_price":475000,"works_cost":3000,"floor_area_sqm":64,"epc":"E","days_listed":0,"lha_2026_weekly":356.71,"lha_jan2011_weekly":253.85},{"listing_id":"B12","borough":"Tower Hamlets","region":"Inner London","postcode":"E3 4DH","brma":"Inner East London","property_type":"Flat","beds":2,"asking_price":470000,"works_cost":5000,"floor_area_sqm":64,"epc":"C","days_listed":1,"lha_2026_weekly":402.74,"lha_jan2011_weekly":300},{"listing_id":"B13","borough":"Wandsworth","region":"Inner London","postcode":"SW17 9HN","brma":"Inner South West London","property_type":"Flat","beds":2,"asking_price":520000,"works_cost":8000,"floor_area_sqm":64,"epc":"C","days_listed":2,"lha_2026_weekly":391.23,"lha_jan2011_weekly":311.54},{"listing_id":"B14","borough":"Westminster","region":"Inner London","postcode":"W9 1PS","brma":"Central London","property_type":"Flat","beds":1,"asking_price":550000,"works_cost":12000,"floor_area_sqm":45,"epc":"D","days_listed":3,"lha_2026_weekly":331.39,"lha_jan2011_weekly":370},{"listing_id":"B15","borough":"Barnet","region":"Outer London","postcode":"N11 3HY","brma":"Outer North London","property_type":"Flat","beds":2,"asking_price":400000,"works_cost":15000,"floor_area_sqm":64,"epc":"C","days_listed":4,"lha_2026_weekly":322.19,"lha_jan2011_weekly":231},{"listing_id":"B16","borough":"Bexley","region":"Outer London","postcode":"DA17 5QX","brma":"Outer South East London","property_type":"Terraced house","beds":3,"asking_price":390000,"works_cost":10000,"floor_area_sqm":86,"epc":"D","days_listed":0,"lha_2026_weekly":356.71,"lha_jan2011_weekly":229.62},{"listing_id":"B17","borough":"Brent","region":"Outer London","postcode":"NW10 9NS","brma":"Inner North London","property_type":"Flat","beds":2,"asking_price":420000,"works_cost":5000,"floor_area_sqm":64,"epc":"D","days_listed":1,"lha_2026_weekly":412.86,"lha_jan2011_weekly":340},{"listing_id":"B18","borough":"Bromley","region":"Outer London","postcode":"SE20 8JS","brma":"Outer South East London","property_type":"Flat","beds":2,"asking_price":340000,"works_cost":8000,"floor_area_sqm":64,"epc":"C","days_listed":2,"lha_2026_weekly":299.18,"lha_jan2011_weekly":190.38},{"listing_id":"B19","borough":"Ealing","region":"Outer London","postcode":"UB2 4HW","brma":"Outer West London","property_type":"Terraced house","beds":3,"asking_price":480000,"works_cost":10000,"floor_area_sqm":86,"epc":"B","days_listed":3,"lha_2026_weekly":339.45,"lha_jan2011_weekly":253.85},{"listing_id":"B20","borough":"Greenwich","region":"Outer London","postcode":"SE2 9HJ","brma":"Outer South East London","property_type":"Terraced house","beds":3,"asking_price":420000,"works_cost":15000,"floor_area_sqm":86,"epc":"D","days_listed":4,"lha_2026_weekly":356.71,"lha_jan2011_weekly":229.62},{"listing_id":"B21","borough":"Harrow","region":"Outer London","postcode":"HA3 7PN","brma":"North West London","property_type":"Flat","beds":2,"asking_price":360000,"works_cost":3000,"floor_area_sqm":64,"epc":"C","days_listed":0,"lha_2026_weekly":310.68,"lha_jan2011_weekly":219.23},{"listing_id":"B22","borough":"Havering","region":"Outer London","postcode":"RM3 9EL","brma":"Outer North East London","property_type":"Terraced house","beds":3,"asking_price":385000,"works_cost":10000,"floor_area_sqm":86,"epc":"D","days_listed":1,"lha_2026_weekly":345.21,"lha_jan2011_weekly":242.31},{"listing_id":"B23","borough":"Hillingdon","region":"Outer London","postcode":"UB3 2BY","brma":"Outer West London","property_type":"Terraced house","beds":3,"asking_price":430000,"works_cost":15000,"floor_area_sqm":86,"epc":"E","days_listed":2,"lha_2026_weekly":339.45,"lha_jan2011_weekly":253.85},{"listing_id":"B24","borough":"Hounslow","region":"Outer London","postcode":"TW4 6LT","brma":"Outer West London","property_type":"Terraced house","beds":3,"asking_price":445000,"works_cost":20000,"floor_area_sqm":86,"epc":"C","days_listed":3,"lha_2026_weekly":339.45,"lha_jan2011_weekly":253.85},{"listing_id":"B25","borough":"Kingston upon Thames","region":"Outer London","postcode":"KT6 4AP","brma":"Outer South West London","property_type":"Flat","beds":2,"asking_price":380000,"works_cost":15000,"floor_area_sqm":64,"epc":"C","days_listed":4,"lha_2026_weekly":344.05,"lha_jan2011_weekly":253.85},{"listing_id":"B26","borough":"Merton","region":"Outer London","postcode":"CR4 3HG","brma":"Outer South London","property_type":"Terraced house","beds":3,"asking_price":450000,"works_cost":15000,"floor_area_sqm":86,"epc":"D","days_listed":0,"lha_2026_weekly":345.21,"lha_jan2011_weekly":242.31},{"listing_id":"B27","borough":"Redbridge","region":"Outer London","postcode":"IG3 8AX","brma":"Outer North East London","property_type":"Terraced house","beds":3,"asking_price":455000,"works_cost":20000,"floor_area_sqm":86,"epc":"C","days_listed":1,"lha_2026_weekly":345.21,"lha_jan2011_weekly":242.31},{"listing_id":"B28","borough":"Richmond upon Thames","region":"Outer London","postcode":"TW2 7NJ","brma":"Outer West London","property_type":"Flat","beds":2,"asking_price":430000,"works_cost":8000,"floor_area_sqm":64,"epc":"D","days_listed":2,"lha_2026_weekly":299.18,"lha_jan2011_weekly":207.69},{"listing_id":"B29","borough":"Sutton","region":"Outer London","postcode":"SM1 1NR","brma":"Outer South London","property_type":"Flat","beds":2,"asking_price":315000,"works_cost":12000,"floor_area_sqm":64,"epc":"D","days_listed":3,"lha_2026_weekly":276.16,"lha_jan2011_weekly":196.15},{"listing_id":"B30","borough":"Waltham Forest","region":"Outer London","postcode":"E17 8JH","brma":"Outer East London","property_type":"Flat","beds":2,"asking_price":420000,"works_cost":15000,"floor_area_sqm":64,"epc":"C","days_listed":4,"lha_2026_weekly":322.19,"lha_jan2011_weekly":207.69}];
const NIGHTLY=[{"borough":"Barking and Dagenham","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"Barnet","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"Bexley","cost_per_night":91,"basis":"Borough's own figure"},{"borough":"Brent","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"Bromley","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"Camden","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"City of London","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"Croydon","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"Ealing","cost_per_night":109,"basis":"Borough's own figure"},{"borough":"Enfield","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"Greenwich","cost_per_night":75,"basis":"Borough's own figure"},{"borough":"Hackney","cost_per_night":82,"basis":"Borough's own figure"},{"borough":"Hammersmith and Fulham","cost_per_night":147,"basis":"Borough's own figure"},{"borough":"Haringey","cost_per_night":69,"basis":"Borough's own figure"},{"borough":"Harrow","cost_per_night":88,"basis":"Borough's own figure"},{"borough":"Havering","cost_per_night":113,"basis":"Borough's own figure"},{"borough":"Hillingdon","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"Hounslow","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"Islington","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"Kensington and Chelsea","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"Kingston upon Thames","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"Lambeth","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"Lewisham","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"Merton","cost_per_night":104,"basis":"Borough's own figure"},{"borough":"Newham","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"Redbridge","cost_per_night":86,"basis":"Borough's own figure"},{"borough":"Richmond upon Thames","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"Southwark","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"Sutton","cost_per_night":84,"basis":"Borough's own figure"},{"borough":"Tower Hamlets","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"Waltham Forest","cost_per_night":123,"basis":"Borough's own figure"},{"borough":"Wandsworth","cost_per_night":94,"basis":"London average (borough's returns don't isolate nightly-paid)"},{"borough":"Westminster","cost_per_night":132,"basis":"Borough's own figure"}];
const ASSUMPTIONS={"pwlb_term_years": 40, "pwlb_certainty_discount_pct": 0.2, "pwlb_fallback_rate_pct": 6.38, "pwlb_fallback_as_of": "2026-10-30", "mrp_pct": 2.5, "purchase_costs_pct": 6, "mm_pct_of_lha_rent": 30, "rent_loss_pct": 5, "subsidy_pct_of_2011_lha": 90, "subsidy_cap_inner_london": 500, "subsidy_cap_elsewhere": 375, "nightly_cost_outside_london": 75, "min_annual_saving": 0};


// ---------- Appraisal ----------
const CAP500 = new Set(['Central London','Inner East London','Inner North London','Inner South East London','Inner South West London','Inner West London']);
function appraise(l, a, cost, ratePct){
  const capital = l.asking_price*(1+a.purchase_costs_pct/100) + l.works_cost;
  const financing = capital*(ratePct + a.mrp_pct)/100;
  const rentGross = l.lha_2026_weekly*52;
  const ownNet = financing + rentGross*a.mm_pct_of_lha_rent/100 - rentGross*(1-a.rent_loss_pct/100);
  const c = cost[l.borough];
  const nightly = c ? c.cost_per_night : a.nightly_cost_outside_london;
  const subWk = Math.min(l.lha_jan2011_weekly*a.subsidy_pct_of_2011_lha/100, CAP500.has(l.brma) ? a.subsidy_cap_inner_london : a.subsidy_cap_elsewhere);
  const saving = nightly*365 - subWk*52 - ownNet;
  return {
    id:l.listing_id, property:l.beds+' bed '+l.property_type.toLowerCase()+', '+l.postcode, borough:l.borough, region:l.region,
    asking_price:l.asking_price, epc:l.epc, lha:l.lha_2026_weekly, nightly, subWk,
    capital:Math.round(capital), ownNet:Math.round(ownNet), taNet:Math.round(nightly*365 - subWk*52), saving:Math.round(saving), breakeven:Math.round((ownNet+subWk*52)/365),
    meets: saving > a.min_annual_saving,
  };
}
const COST = Object.fromEntries(NIGHTLY.map(r => [r.borough, r]));
// ---------- PWLB certainty rate, read live from the daily rates file ----------
const RATES_URL = 'https://gist.githubusercontent.com/nhaverly/2221652235336db07f5df927d45ffad5/raw/rates.json';
const PWLB = { rate: ASSUMPTIONS.pwlb_fallback_rate_pct, asOf: ASSUMPTIONS.pwlb_fallback_as_of, live: false };
let ALL = [];
function appraiseAll(){
  ALL = LISTINGS.map(l => appraise(l, ASSUMPTIONS, COST, PWLB.rate)).sort((x,y) => y.saving-x.saving);
  let k = 0; ALL.forEach(x => { x.rank = x.meets ? ++k : null; });
}
appraiseAll();
async function loadRate(){
  try {
    const r = await fetch(RATES_URL + '?t=' + Date.now(), { cache: 'no-store' });
    if (!r.ok) throw new Error('HTTP ' + r.status);
    const j = await r.json();
    const curve = Array.isArray(j.pwlbMaturityCurve) ? j.pwlbMaturityCurve : [];
    const pt = curve.reduce((best, p) => (!best || Math.abs(p.term - ASSUMPTIONS.pwlb_term_years) < Math.abs(best.term - ASSUMPTIONS.pwlb_term_years) ? p : best), null);
    const std = pt && Number(pt.rate);
    if (!(std > 0 && std < 0.2)) throw new Error('No usable maturity rate');
    PWLB.rate = Math.round((std*100 - ASSUMPTIONS.pwlb_certainty_discount_pct)*100)/100;
    PWLB.asOf = j.asOf || PWLB.asOf; PWLB.live = true;
  } catch (e) { PWLB.live = false; }
  appraiseAll(); renderRate(); update();
}
const AREAS = [...new Map(LISTINGS.map(x => [x.borough, x.region])).entries()]
  .map(([borough, region]) => ({borough, region}))
  .sort((p,q) => ['Inner London','Outer London','Outside London'].indexOf(p.region)-['Inner London','Outer London','Outside London'].indexOf(q.region) || p.borough.localeCompare(q.borough));

// ---------- State ----------
const state = { chosen: new Set(AREAS.map(a => a.borough)), epc:'', misses:false, q:'', sort:{key:'saving', dir:-1}, view:'search' };
try {
  const s = JSON.parse(localStorage.getItem('ta-finder') || 'null');
  if (s && Array.isArray(s.chosen)) { state.chosen = new Set(s.chosen.filter(b => AREAS.some(a => a.borough === b))); state.epc = s.epc || ''; }
} catch (e) {}
const save = () => { try { localStorage.setItem('ta-finder', JSON.stringify({chosen:[...state.chosen], epc:state.epc})); } catch (e) {} };

// ---------- Helpers ----------
const fmtInt = v => Math.round(v).toLocaleString('en-GB');
const gbp = v => (v < 0 ? '−£' : '£') + Math.round(Math.abs(v)).toLocaleString('en-GB');
const gbp2 = v => '£' + v.toLocaleString('en-GB', {minimumFractionDigits:2, maximumFractionDigits:2});
const gbpm = v => '£' + (v/1e6).toFixed(1) + 'm';
const $ = id => document.getElementById(id);
const epcOk = x => !state.epc || (x.epc && x.epc <= state.epc);
const inSearch = () => ALL.filter(x => state.chosen.has(x.borough) && epcOk(x));
const el = (tag, props, ...kids) => { const e = document.createElement(tag); Object.assign(e, props || {}); kids.forEach(c => e.append(c)); return e; };

// ---------- Search page ----------
function renderPicker(){
  const box = $('picker'); box.replaceChildren();
  const q = state.q;
  let shown = 0;
  ['Inner London','Outer London','Outside London'].forEach(region => {
    const areas = AREAS.filter(a => a.region === region);
    const list = areas.filter(a => !q || a.borough.toLowerCase().includes(q));
    if (!list.length) return;
    shown += list.length;
    const names = areas.map(a => a.borough);
    const on = names.filter(b => state.chosen.has(b)).length;
    const allBtn = el('button', {type:'button', className:'lnk', textContent:'Select all'});
    allBtn.onclick = () => { names.forEach(b => state.chosen.add(b)); update(); };
    const noneBtn = el('button', {type:'button', className:'lnk', textContent:'Clear'});
    noneBtn.onclick = () => { names.forEach(b => state.chosen.delete(b)); update(); };
    const head = el('div', {className:'grp-head'}, el('strong', {textContent:region}), el('span', {className:'note', textContent:on+' of '+areas.length+' chosen'}), allBtn, noneBtn);
    const chips = el('div', {className:'chips'});
    list.forEach(a => {
      const n = ALL.filter(x => x.borough === a.borough && x.meets && epcOk(x)).length;
      const b = el('button', {type:'button', className:'chip'}, el('span', {textContent:a.borough}), el('span', {className:'c', textContent:String(n)}));
      b.setAttribute('aria-pressed', String(state.chosen.has(a.borough)));
      b.onclick = () => { state.chosen.has(a.borough) ? state.chosen.delete(a.borough) : state.chosen.add(a.borough); update(); };
      chips.append(b);
    });
    box.append(el('div', {className:'grp'}, head, chips));
  });
  if (!shown) box.append(el('p', {className:'note', textContent:'No area matches that search.'}));
  const n = state.chosen.size;
  $('sel-count').textContent = n === AREAS.length ? 'All '+AREAS.length+' areas chosen' : n === 0 ? 'No areas chosen' : n+' of '+AREAS.length+' areas chosen';
}

// ---------- Results page ----------
function renderTotals(){
  const m = inSearch().filter(x => x.meets);
  const n = m.length, s = m.reduce((t,x) => t+x.saving, 0), c = m.reduce((t,x) => t+x.capital, 0);
  const best = n ? Math.max(...m.map(x => x.saving)) : null;
  $('go-n').textContent = fmtInt(n); $('go-s').textContent = gbp(s);
  $('t-n').textContent = fmtInt(n); $('t-c').textContent = gbpm(c); $('t-s').textContent = gbp(s);
  $('k-n').textContent = fmtInt(n); $('k-s').textContent = gbp(s); $('k-c').textContent = gbpm(c); $('k-b').textContent = best == null ? '—' : gbp(best);
  const nAreas = state.chosen.size;
  $('crit').textContent = (nAreas === AREAS.length ? 'All '+AREAS.length+' areas' : nAreas+' of '+AREAS.length+' areas') + ' · ' + (state.epc ? 'EPC '+state.epc+' or better' : 'Any EPC rating') + ' · Any price and size';
}
function renderTable(){
  const tb = $('rows'); tb.replaceChildren();
  let rows = inSearch(); if (!state.misses) rows = rows.filter(x => x.meets);
  const {key, dir} = state.sort;
  rows = rows.slice().sort((a,b) => {
    const va = a[key], vb = b[key];
    if (va == null && vb == null) return 0; if (va == null) return 1; if (vb == null) return -1;
    return (typeof va === 'string' ? va.localeCompare(vb) : va - vb) * dir;
  });
  if (!rows.length) { const td = el('td', {colSpan:12, className:'note', textContent:'No homes in the chosen areas create a saving.'}); tb.append(el('tr', {}, td)); return; }
  rows.forEach(x => {
    const tr = el('tr', {className: x.meets ? '' : 'miss'});
    const td = (t, c) => tr.append(el('td', {className:c||'', textContent:t}));
    td(x.rank == null ? '–' : String(x.rank), 'n');
    const p = el('td', {textContent:x.property}); if (!x.meets) p.append(el('span', {className:'why', textContent:'Costs more than nightly-paid TA'})); tr.append(p);
    td(x.borough); td(gbp(x.asking_price), 'n'); td(x.epc || '–');
    td(gbp2(x.lha), 'n opt'); td(gbp(x.nightly), 'n opt'); td(gbp2(x.subWk), 'n opt');
    td(gbp(x.ownNet), 'n'); td(gbp(x.taNet), 'n');
    td(gbp(x.saving), 'n save'); td(gbp(x.breakeven), 'n opt');
    tb.append(tr);
  });
  document.querySelectorAll('th button[data-sort]').forEach(b => {
    const th = b.parentElement;
    if (b.dataset.sort === key) th.setAttribute('aria-sort', dir < 0 ? 'descending' : 'ascending'); else th.removeAttribute('aria-sort');
  });
}

// ---------- Pages ----------
const VIEWS = ['search','results','method'];
function show(v){
  state.view = VIEWS.includes(v) ? v : 'search';
  document.querySelectorAll('.page').forEach(p => p.hidden = p.id !== state.view);
  document.querySelectorAll('.steps [data-view]').forEach(b => b.dataset.view === state.view ? b.setAttribute('aria-current','page') : b.removeAttribute('aria-current'));
}
document.querySelectorAll('[data-view]').forEach(b => b.addEventListener('click', () => {
  if (location.hash.slice(1) !== b.dataset.view) location.hash = b.dataset.view; else show(b.dataset.view);
  window.scrollTo({top:0});
}));
window.addEventListener('hashchange', () => show(location.hash.slice(1)));

// ---------- Controls ----------
$('pick-all').onclick = () => { AREAS.forEach(a => state.chosen.add(a.borough)); update(); };
$('pick-none').onclick = () => { state.chosen.clear(); update(); };
$('area-q').addEventListener('input', e => { state.q = e.target.value.trim().toLowerCase(); renderPicker(); });
$('epc-min').addEventListener('change', e => { state.epc = e.target.value; update(); });
$('show-miss').addEventListener('change', e => { state.misses = e.target.checked; renderTable(); });
document.querySelectorAll('th button[data-sort]').forEach(b => b.addEventListener('click', () => {
  const key = b.dataset.sort;
  state.sort = state.sort.key === key ? {key, dir:-state.sort.dir} : {key, dir: ['saving','ownNet','taNet','asking_price','lha','nightly','subWk','breakeven'].includes(key) ? -1 : 1};
  renderTable();
}));

function update(){ save(); renderPicker(); renderTotals(); renderTable(); }

// ---------- Method values ----------
const A = ASSUMPTIONS;
$('a-term').textContent = A.pwlb_term_years; $('a-mrp').textContent = A.mrp_pct;
$('a-buy').textContent = A.purchase_costs_pct; $('a-mm').textContent = A.mm_pct_of_lha_rent; $('a-loss').textContent = A.rent_loss_pct;
$('a-sub').textContent = A.subsidy_pct_of_2011_lha; $('a-cap1').textContent = gbp(A.subsidy_cap_inner_london);
$('a-cap2').textContent = gbp(A.subsidy_cap_elsewhere); $('a-out').textContent = gbp(A.nightly_cost_outside_london);

function renderRate(){
  $('a-pwlb').textContent = PWLB.rate.toFixed(2);
  const when = new Date(PWLB.asOf + 'T12:00:00').toLocaleDateString('en-GB', {day:'numeric', month:'long', year:'numeric'});
  const txt = PWLB.live
    ? 'PWLB certainty rate ' + PWLB.rate.toFixed(2) + '% (' + A.pwlb_term_years + '-year maturity, DMO rates of ' + when + ') plus MRP at ' + A.mrp_pct + '%'
    : 'PWLB certainty rate ' + PWLB.rate.toFixed(2) + '% (' + A.pwlb_term_years + '-year maturity, DMO rates of ' + when + '; the live rate could not be loaded) plus MRP at ' + A.mrp_pct + '%';
  $('rate-src').textContent = (PWLB.live ? 'Live rate: the standard rate the DMO published on ' : 'Live rate unavailable, so this uses the standard rate the DMO published on ') + when + ', less the ' + A.pwlb_certainty_discount_pct.toFixed(2) + '% certainty discount.';
  $('rate-line').textContent = 'Financing: ' + txt + '.';
}
$('epc-min').value = state.epc;
show(location.hash.slice(1));
renderRate();
update();
loadRate();
})();
