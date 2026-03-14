<script>
  import { CHARTS } from '$lib/charts/charts.js';
  import { activeTab } from '$lib/stores/activeTab.js';
  import Hero from '$lib/components/Hero.svelte';
  import GeoCronMap from '$lib/components/GeoCronMap.svelte';
  import CliopatriaMap from '$lib/components/CliopatriaMap.svelte';
  import ChartSection from '$lib/components/ChartSection.svelte';
  import PlotlyChart from '$lib/components/PlotlyChart.svelte';
  import StatGrid from '$lib/components/StatGrid.svelte';
  import ScholarGrid from '$lib/components/ScholarGrid.svelte';
  import DataTerm from '$lib/components/DataTerm.svelte';
  import PartDivider from '$lib/components/PartDivider.svelte';
  import Collapsible from '$lib/components/Collapsible.svelte';
</script>

{#if $activeTab === 'world'}
  <CliopatriaMap />
{:else}

<Hero />

<PartDivider number="I" title="The Map" />

<GeoCronMap />

<!-- THE QUESTION -->
<section id="question">
  <div class="section-label">The Question</div>
  <h2>What killed Mediterranean trade?</h2>
  <p>
    For nearly a century, historians have debated the economic collapse of the ancient Mediterranean world. Was it the Germanic migrations? The rise of Islam? Plagues? A slow structural unwinding? Each scholar has a theory &mdash; and each cites different evidence.
  </p>
  <p>
    This project takes a different approach: <span class="highlight">start from the numbers, find the structural breaks, then see which story the data supports.</span> No priors. No thesis to defend. Just change-point detection on sixteen independent quantitative proxies that span 2,000 years &mdash; from the Roman Republic to the Carolingian revival.
  </p>
  <StatGrid items={[
    { value: '16', label: 'Independent datasets' },
    { value: '2,037', label: 'Annual lead measurements' },
    { value: '1,784', label: 'Shipwrecks catalogued' },
    { value: '2,000 yrs', label: 'Time span covered' }
  ]} />
</section>

<div class="divider"><hr></div>

<!-- THE EVIDENCE -->
<section id="proxies">
  <div class="section-label">The Evidence</div>
  <h2>Sixteen windows into the ancient economy</h2>
  <p>Each proxy measures a different facet of economic activity. They were collected independently, by different research teams, using different methods. When they converge, the signal is real.</p>
  <div class="proxy-grid">
    <div class="proxy-card">
      <div class="icon" style="color: var(--teal);">Pb</div>
      <h4>Lead Emissions</h4>
      <p><DataTerm tooltip="Lead pollution preserved in Greenland NGRIP2 ice core. Smelting silver ore releases lead into the atmosphere; it drifts to the Arctic and is trapped in annual ice layers.">Ice-core lead</DataTerm> from Roman smelting, annual resolution, 600 BCE&ndash;800 CE.</p>
    </div>
    <div class="proxy-card">
      <div class="icon" style="color: var(--blue);">&#9875;</div>
      <h4>Shipwrecks</h4>
      <p><DataTerm tooltip="From the Oxford Roman Economy Project (OxREP) v2.1 (Strauss, Wilson & Flohr 2017), updating Parker's 1992 catalogue. More ships sailing = more sinkings — but this proxy has well-documented limitations (barrel bias, discovery bias). Wrecks are dated using equal-probability methods (Wilson 2011) to avoid midpoint bias.">1,784 catalogued wrecks</DataTerm> across the Mediterranean, a <a href="#shipwreck-source-criticism" style="color: var(--red); font-size: 0.85em;">contested</a> proxy for trade volume.</p>
    </div>
    <div class="proxy-card">
      <div class="icon" style="color: var(--accent);">Au &middot; Ag</div>
      <h4>Coinage</h4>
      <p>Silver <DataTerm tooltip="Rome's primary silver coin, introduced ~211 BCE. Contained 97% silver at first, fell to 2.5% by 268 CE under Gallienus.">denarius</DataTerm>, gold <DataTerm tooltip="Rome's gold coin, ~8g under Caesar. Weight declined but gold purity stayed high much longer than silver purity.">aureus</DataTerm>, Byzantine <DataTerm tooltip="Constantine's gold coin (309 CE), ~4.5g at 98% purity. Remained stable for 500+ years until debasement in the 11th century.">solidus</DataTerm>, and Islamic <DataTerm tooltip="Silver coin of the Umayyad/Abbasid caliphates, introduced 696 CE. Standard weight ~2.97g, high silver purity. Became the dominant Mediterranean silver currency.">dirham</DataTerm>.</p>
    </div>
  </div>
</section>

<div class="divider"><hr></div>
<PartDivider number="II" title="Trade &amp; Commerce" />

<!-- SHIPWRECKS -->
<ChartSection id="shipwrecks" label="Proxy 2 &mdash; Maritime Trade"
  heading="Shipwrecks: counting the vessels that never arrived"
  chartId="chart-shipwrecks" chartFn={CHARTS.shipwrecks}
  caption="Mediterranean shipwreck density in 25-year bins with equal-probability dating (Wilson 2011 method). Regional totals stacked. Hover for breakdown by region."
  sourceHtml='Source: <a href="https://oxrep.classics.ox.ac.uk/databases/shipwrecks_database/" target="_blank">OxREP Shipwrecks Database v2.1</a> (Strauss, Wilson &amp; Flohr 2017), 1,784 wrecks.'
  keyFinding="<strong>Trade peaks around 25&ndash;75 CE</strong>, then begins a two-stage decline: a moderate drop after 125 CE and a steep collapse after 375 CE. But the critical story is in the regional breakdown&hellip;">
  <p>
    The number of <DataTerm tooltip="Archaeologically documented ships that sank in antiquity. Found by divers and underwater surveys. Dated by their cargo (amphorae, coins) and construction techniques.">shipwrecks</DataTerm> per period is one proxy for the volume of maritime trade. The <DataTerm tooltip="Major research project at Oxford University cataloguing ancient Mediterranean trade data. The shipwreck database v2.1 (2017) contains 1,784 wrecks with location, date range, cargo type, and construction details.">Oxford Roman Economy Project (OxREP)</DataTerm> database v2.1 catalogues 1,784 wrecks across the Mediterranean.
  </p>
  <p style="font-size: 0.92rem; color: var(--text-muted); margin-top: 0.5rem;">
    <strong>Important:</strong> Shipwreck counts are a contested proxy. The data has <a href="#shipwreck-source-criticism" style="color: var(--red); border-bottom: 1px solid rgba(217, 79, 79, 0.4);">well-documented limitations</a> that readers should understand before drawing conclusions.
  </p>
</ChartSection>

<div class="divider"><hr></div>

<!-- REGIONAL DIVERGENCE -->
<section id="divergence" class="wide">
  <div class="section-label">The Key Discovery</div>
  <h2>Two Mediterraneans: a tale of East and West</h2>
  <p>
    When you split the shipwreck data by region, the most important finding emerges. The Western and Eastern Mediterranean didn't decline together &mdash; <span class="highlight">the West collapsed first, by at least 250 years.</span>
  </p>
  <div class="chart-container">
    <PlotlyChart id="chart-divergence" chartFn={CHARTS.divergence} />
    <p class="chart-caption">Western vs. Eastern Mediterranean shipwreck counts (50-year bins). The West drops below 10% of peak by 475 CE; the East sustains near-peak trade until ~625 CE.
      <span class="source-link">Source: <a href="https://oxrep.classics.ox.ac.uk/databases/shipwrecks_database/" target="_blank">OxREP v2.1</a> (Strauss, Wilson &amp; Flohr 2017).</span>
    </p>
  </div>
  <StatGrid items={[
    { value: '8:1', label: 'West-to-East ratio at Roman peak' },
    { value: '1:2', label: 'West-to-East ratio by 500\u2013650 CE' },
    { value: '250 yrs', label: 'West collapses before the East' }
  ]} />
  <div class="chart-container">
    <PlotlyChart id="chart-ratio" chartFn={CHARTS.ratio} />
    <p class="chart-caption">Ratio of Western to Eastern Mediterranean shipwreck counts over time. The dramatic reversal occurs in the 5th century.
      <span class="source-link">Source: Derived from <a href="https://oxrep.classics.ox.ac.uk/databases/shipwrecks_database/" target="_blank">OxREP v2.1</a> regional data.</span>
    </p>
  </div>
  <div class="key-finding">
    <strong>The Western collapse precedes the Islamic conquests by roughly two centuries.</strong> By the time Muslim armies reached the Levant in the 630s, Western Mediterranean trade had already been at less than 10% of its peak for 150 years.
  </div>
</section>

<div class="divider"><hr></div>

<!-- SOURCE CRITICISM -->
<section id="shipwreck-source-criticism" class="wide">
  <Collapsible summary="How much should you trust the shipwreck data?">
    <p>The OxREP shipwreck database is the best available dataset for ancient Mediterranean maritime activity &mdash; but &ldquo;best available&rdquo; does not mean &ldquo;unproblematic.&rdquo;</p>
    <div class="source-criticism-box">
      <h3>Known problems with shipwreck &rarr; trade inference</h3>
      <ul>
        <li><strong>Unequal sinking probability.</strong> A decline in wrecks could reflect safer sailing, not less trade.</li>
        <li><strong>Unequal wreck visibility &mdash; the barrel problem.</strong> After the 2nd&ndash;4th century CE, Western trade shifted from ceramic amphorae to wooden barrels &mdash; which rot on the seabed.</li>
        <li><strong>Massive geographic discovery bias.</strong> Italy, France, and Spain account for over 70% of all wrecks &mdash; not because more ships sank there, but because those coastlines have been more heavily surveyed.</li>
        <li><strong>Ceramic dating uncertainty.</strong> Manning, Lorentzen &amp; Demesticha (2022, <em>Antiquity</em>) demonstrated that radiocarbon dating can produce significantly different results than ceramic-based dates.</li>
        <li><strong>Inconsistency with land-based archaeology.</strong> During the supposed decline, archaeological evidence shows massive port expansion at Portus and intensification of olive oil production across North Africa.</li>
        <li><strong>Small-n fragility.</strong> The entire database contains 1,784 wrecks spread across ~1,600 years. When split by region and time bin, individual data points rest on very small numbers.</li>
      </ul>
    </div>
    <p><strong>So why show it at all?</strong> Because even flawed proxies are informative when understood in context. We show it alongside 15 other independent datasets precisely so that no single proxy bears the full interpretive weight.</p>
  </Collapsible>
</section>

<div class="divider"><hr></div>
<PartDivider number="III" title="Money &amp; Prices" />

<!-- CURRENCY -->
<section id="currency" class="wide">
  <div class="section-label">The Money</div>
  <h2>Three currencies, two civilizations, two collapses</h2>
  <p>
    Rome ran a <DataTerm tooltip="A monetary system using two metals (gold and silver) as the basis for coinage.">bimetallic</DataTerm> system: the silver <DataTerm tooltip="Rome's workhorse silver coin, introduced ~211 BCE. Originally ~4.5g of 97% silver.">denarius</DataTerm> for everyday transactions, the gold <DataTerm tooltip="Rome's gold coin. Under Caesar ~8.0g, officially valued at 25 denarii.">aureus</DataTerm> for large payments. When the silver currency collapsed, Constantine replaced the aureus with the <DataTerm tooltip="Gold coin introduced by Constantine ~309 CE at 4.5g, 98% pure. Most stable currency in world history.">solidus</DataTerm> &mdash; which then held stable for 500 years.
  </p>

  <h3>Silver: the denarius death spiral</h3>
  <div class="chart-container">
    <PlotlyChart id="chart-denarius" chartFn={CHARTS.denarius} />
    <p class="chart-caption">Silver content of the Roman denarius, 210 BCE to 294 CE (Butcher &amp; Ponting 2015; Walker 1976).</p>
  </div>

  <h3>Gold: from aureus to solidus</h3>
  <p>While silver was debased ruthlessly, gold told a different story. Constantine's solidus reset the gold standard at 4.5g &mdash; and it held at ~98% purity from 309 CE until the 11th century.</p>
  <div class="chart-container">
    <PlotlyChart id="chart-gold" chartFn={CHARTS.gold} />
    <p class="chart-caption">Gold coin weight: Roman aureus (46 BCE&ndash;309 CE) and Byzantine solidus (309&ndash;1092 CE).
      <span class="source-link">Sources: Walker (ANS, 1976&ndash;78); <a href="https://numismatics.org/ocre/" target="_blank">OCRE</a>; <a href="https://hdl.handle.net/1887/43427" target="_blank">Vrij (2016)</a>.</span>
    </p>
  </div>

  <h3>The other Mediterranean: the Islamic dirham</h3>
  <p>After 696 CE, the Umayyad silver dirham became the dominant currency from Morocco to Central Asia.</p>
  <div class="chart-container">
    <PlotlyChart id="chart-dirham" chartFn={CHARTS.dirham} />
    <p class="chart-caption">Islamic silver dirham weight standard, 696&ndash;940 CE.
      <span class="source-link">Sources: Jonsson &amp; Herschend, <em>Antiquity</em> (2023). <a href="https://doi.org/10.15184/aqy.2022.165" target="_blank">doi:10.15184/aqy.2022.165</a></span>
    </p>
  </div>

  <div class="key-finding">
    <strong>The denarius lost 95% of its silver in under two centuries.</strong> The solidus held steady for 500 years. The dirham introduced a new silver standard for the Islamic world.
  </div>
</section>

<div class="divider"><hr></div>

<!-- WHEAT -->
<ChartSection id="wheat" label="Prices"
  heading="Egyptian wheat: the only ancient price series"
  chartId="chart-wheat" chartFn={CHARTS.wheat}
  caption="Egyptian wheat prices in drachmas per artaba. Stable at ~8 dr/artaba for a century, then doubling after 160 CE."
  sourceHtml='Source: Rathbone (1997); Temin (2013). <em>The Roman Market Economy</em>, Princeton.'
  keyFinding="<strong>Prices doubled between 160&ndash;190 CE</strong> &mdash; the same window as the lead crash and the Antonine Plague.">
  <p>Thousands of <DataTerm tooltip="Documents written on papyrus, preserved by Egypt's dry climate. They record everyday transactions.">papyrus documents</DataTerm> from Roman Egypt record wheat prices. This is the only usable long-run price series from anywhere in the Roman Empire.</p>
</ChartSection>

<div class="divider"><hr></div>

<!-- COIN HOARDS -->
<ChartSection id="hoards" label="Fear Index"
  heading="Coin hoards: burying your savings and never coming back"
  chartId="chart-hoards" chartFn={CHARTS.hoards}
  caption="Coin hoard frequency by 25-year period (terminal date). Spikes correspond to civil wars, invasions, and plagues."
  sourceHtml='Source: <a href="https://chre.ashmus.ox.ac.uk/" target="_blank">Coin Hoards of the Roman Empire (CHRE)</a>, Oxford. 18,315 hoards.'
  keyFinding="<strong>The massive 250&ndash;275 CE spike is unmistakable</strong> &mdash; the Crisis of the Third Century, when the Empire nearly disintegrated.">
  <p>When people bury coins, it means they fear for the future. When they never return to dig them up, it means the worst happened. The <DataTerm tooltip="Coin Hoards of the Roman Empire, Oxford. Database of 18,315 hoards containing 7,026,455 coins.">CHRE database</DataTerm> catalogues over 18,000 hoards.</p>
</ChartSection>

<div class="divider"><hr></div>

<!-- PAS COINS -->
<ChartSection id="pas-coins" label="Monetization"
  heading="Britain's lost coins: the Anglo-Saxon gap"
  chartId="chart-pas" chartFn={CHARTS.pas}
  caption='Coin finds per period from the Portable Antiquities Scheme database (Britain). The "Anglo-Saxon gap" (~410&ndash;680 CE) represents near-total de-monetization.'
  sourceHtml='Source: <a href="https://finds.org.uk/" target="_blank">Portable Antiquities Scheme (PAS)</a>, UK Government.'
  keyFinding="<strong>For roughly 270 years, Britain barely used coins at all.</strong> The transition from a fully monetized Roman province to a near-barter economy is one of the most dramatic economic reversals in European history.">
  <p>The <DataTerm tooltip="UK government scheme recording archaeological objects found by the public. Over 1.7 million objects catalogued.">Portable Antiquities Scheme</DataTerm> has recorded over 1.7 million archaeological finds across Britain. The coin loss data tells an extraordinary story.</p>
</ChartSection>

<div class="divider"><hr></div>
<PartDivider number="IV" title="Industry &amp; Agriculture" />

<!-- LEAD EMISSIONS -->
<ChartSection id="lead" label="Proxy 1 &mdash; Industrial Activity"
  heading="Lead pollution: a 1,400-year record of mining"
  chartId="chart-lead" chartFn={CHARTS.lead}
  caption="Annual European lead emissions estimated from NGRIP2 ice core. Colored bands show segments identified by blind change-point detection."
  sourceHtml='Source: <a href="https://doi.org/10.1073/pnas.1721818115" target="_blank">McConnell et al. (2018)</a>, PNAS.'
  keyFinding="<strong>The 174 CE crash is the largest break in the record.</strong> Emissions drop 64% &mdash; coincident with the Antonine Plague. Industrial mining doesn't recover for 500 years.">
  <p><DataTerm tooltip="Lead isotopes in ice layers act as a timestamp for European mining activity.">Lead isotopes</DataTerm> trapped in Greenland ice record the rise and fall of European metal smelting with annual precision. The signal is unambiguous: a massive industrial expansion under the Roman Republic, then a catastrophic crash around <span class="highlight">174 CE</span>.</p>
</ChartSection>

<div class="divider"><hr></div>

<!-- LEAD ZOOM -->
<ChartSection id="lead-spike" label="Zoom In"
  heading="The Augustan peak: why lead spiked around 5 CE"
  chartId="chart-lead-zoom" chartFn={CHARTS.leadZoom}
  caption="Zoomed view of lead emissions from 100 BCE to 200 CE. The Augustan peak is driven by Iberian silver mining."
  sourceHtml='Source: <a href="https://doi.org/10.1073/pnas.1721818115" target="_blank">McConnell et al. (2018)</a>, PNAS.'>
  <p>The single highest point &mdash; ~1.35 kt/yr around 5&ndash;10 CE &mdash; demands explanation. After the <DataTerm tooltip="Roman military campaigns (29&ndash;19 BCE) to conquer the Iberian Peninsula.">Cantabrian Wars</DataTerm>, Augustus consolidated control of the silver-lead mines at Rio Tinto, Cartagena, and Las M&eacute;dulas.</p>
</ChartSection>

<div class="divider"><hr></div>

<!-- POLLEN -->
<ChartSection id="pollen" label="Biology"
  heading="The forests grew back: pollen as a collapse indicator"
  chartId="chart-pollen" chartFn={CHARTS.pollen}
  caption="Percentage of arboreal pollen in European sediment cores. Higher values = more forest, less farmland."
  sourceHtml='Source: <a href="https://doi.org/10.1016/j.quascirev.2015.09.012" target="_blank">Fyfe et al. (2015)</a>. Data: <a href="https://doi.org/10.1594/PANGAEA.855674" target="_blank">PANGAEA</a>.'
  keyFinding="<strong>Forest regrowth is the biological mirror of lead pollution decline.</strong> When the mines closed and farms were abandoned, the trees returned.">
  <p><DataTerm tooltip="Study of pollen preserved in lake sediments and peat bogs.">Palynological evidence</DataTerm> from nearly 1,000 pollen cores across Europe reveals a dramatic surge in tree pollen between 250 and 550 CE &mdash; forests literally reclaimed Roman farmland.</p>
</ChartSection>

<div class="divider"><hr></div>
<PartDivider number="V" title="Institutions &amp; Population" />

<!-- INSCRIPTIONS -->
<ChartSection id="inscriptions" label="State Capacity"
  heading="Latin inscriptions: when the bureaucracy stopped writing"
  chartId="chart-inscriptions" chartFn={CHARTS.inscriptions}
  caption="Latin inscription density by 25-year period (equal-probability dating)."
  sourceHtml='Source: <a href="https://edh.ub.uni-heidelberg.de/" target="_blank">Epigraphic Database Heidelberg (EDH)</a> via <a href="https://doi.org/10.5281/zenodo.4888168" target="_blank">SDAM/Zenodo</a>. 81,476 inscriptions.'
  keyFinding="<strong>Inscriptions peak around 175&ndash;200 CE, then crash.</strong> By 300 CE, inscription production has fallen by over 80%.">
  <p>When Rome&rsquo;s civic life was functioning, people carved inscriptions. When it collapsed, they stopped. The <DataTerm tooltip="Epigraphic Database Heidelberg. Contains over 81,000 Latin inscriptions.">EDH database</DataTerm> of over 81,000 inscriptions provides a direct measure of institutional continuity.</p>
</ChartSection>

<div class="divider"><hr></div>

<!-- POPULATION -->
<ChartSection id="population" label="The Denominator"
  heading="Population: the number that explains everything else"
  chartId="chart-population" chartFn={CHARTS.population}
  caption="Estimated population of the Roman Empire. Shaded band shows scholarly uncertainty range."
  sourceHtml='Sources: <a href="https://www.princeton.edu/~pswpc/pdfs/scheidel/070604.pdf" target="_blank">Scheidel (2006)</a>; Frier (2000).'
  keyFinding="<strong>An estimated 20&ndash;30% of the population died in the Antonine Plague.</strong> When you lose a quarter of your people, everything else follows.">
  <p>All other indicators depend on how many people were alive. Roman population estimates are uncertain, but scholars broadly agree: growth through the 1st century, catastrophic loss from the Antonine Plague, and never a full recovery.</p>
</ChartSection>

<div class="divider"><hr></div>

<!-- CHURCHES -->
<ChartSection id="recovery" label="Building Again"
  heading="Churches: the medieval recovery signal"
  chartId="chart-churches" chartFn={CHARTS.churches}
  caption="Major church construction starts per 25-year period across Western Europe (~1,695 churches)."
  sourceHtml='Source: Rijpma (2016). Cathedral construction dataset.'
  keyFinding="<strong>The church construction boom begins exactly when lead emissions surge.</strong> Around 750&ndash;800 CE, mines reopened. Construction follows within a generation.">
  <p>After centuries of contraction, Europe began building again. Church construction is one of the clearest quantitative signals of renewed economic capacity.</p>
</ChartSection>

<div class="divider"><hr></div>
<PartDivider number="VI" title="Climate &amp; Environment" />

<!-- CLIMATE -->
<ChartSection id="climate" label="Climate"
  heading="536 CE: the worst year to be alive"
  chartId="chart-climate" chartFn={CHARTS.climate}
  caption="Summer temperature anomaly from Central European tree rings. Bottom: Major volcanic eruptions (sulfur injection in Tg SO&#8322;)."
  sourceHtml='Sources: <a href="https://doi.org/10.1126/science.1197175" target="_blank">B&uuml;ntgen et al. (2011)</a>; <a href="https://doi.org/10.5194/essd-9-809-2017" target="_blank">Toohey &amp; Sigl (2017)</a>, eVolv2k v3.'
  keyFinding="<strong>Tree rings show the 536 CE event as the sharpest cooling in 2,500 years.</strong> The climate shock links volcanic forcing &rarr; crop failure &rarr; famine &rarr; plague susceptibility &rarr; economic collapse.">
  <p>In 536 CE, a massive volcanic eruption threw enough sulfur into the stratosphere to dim the sun across Europe for 18 months. Together with a second eruption in 540 CE, it triggered the <DataTerm tooltip="Period of unusually cold climate in Europe from ~536 to 660 CE.">Late Antique Little Ice Age</DataTerm>, which coincided with the <DataTerm tooltip="First plague pandemic (541&ndash;750 CE). Yersinia pestis arrived in Constantinople in 541 CE.">Plague of Justinian</DataTerm>.</p>
</ChartSection>

<div class="divider"><hr></div>
<PartDivider number="VII" title="Synthesis" />

<!-- OVERLAY -->
<ChartSection id="overlay" label="Synthesis"
  heading="All proxies, overlaid"
  chartId="chart-overlay" chartFn={CHARTS.overlay}
  caption="All proxies normalized to their respective peak values (100%). Historical events annotated."
  sourceHtml='Sources: Lead &mdash; McConnell et al. (2018); Shipwrecks &mdash; OxREP v2.1; Denarius &mdash; Butcher &amp; Ponting; Hoards &mdash; CHRE; Inscriptions &mdash; EDH.'>
  <p>When we normalize each dataset to its peak value and plot them together, the convergence is striking. Lead, shipwrecks, and the denarius all agree on the general arc: a peak in the 1st century CE, a sharp decline beginning in the 2nd&ndash;3rd century, and a deep trough lasting centuries.</p>
</ChartSection>

<div class="divider"><hr></div>

<!-- CHANGE-POINTS -->
<section id="changepoints" class="wide">
  <div class="section-label">Methodology</div>
  <h2>Blind change-point detection</h2>
  <p>Every structural break shown in this analysis was detected algorithmically, using <DataTerm tooltip="A change-point detection method that recursively splits a time series at the point that most reduces total cost.">binary segmentation with an RBF kernel</DataTerm> (<code>ruptures</code> library). No historical dates were supplied as priors.</p>
  <div class="chart-container">
    <PlotlyChart id="chart-changepoints" chartFn={CHARTS.changepoints} />
    <p class="chart-caption">All detected change-points across proxies and regions. They cluster around known historical crises &mdash; but the algorithm didn't know that.
      <span class="source-link">Method: Binary segmentation with RBF kernel, <a href="https://centre-borelli.github.io/ruptures-docs/" target="_blank">ruptures</a> library (Truong, Oudre &amp; Vayer 2020).</span>
    </p>
  </div>
  <div class="event-markers">
    <span class="event-tag plague">Antonine Plague (165 CE)</span>
    <span class="event-tag plague">Plague of Cyprian (249 CE)</span>
    <span class="event-tag plague">Plague of Justinian (541 CE)</span>
    <span class="event-tag political">Fall of Western Empire (476 CE)</span>
    <span class="event-tag military">Islamic Conquests (630s CE)</span>
    <span class="event-tag economic">Merovingian Mines Reopen (~750 CE)</span>
  </div>
</section>

<div class="divider"><hr></div>

<!-- SCHOLARS -->
<section id="scholars">
  <div class="section-label">The Debate</div>
  <h2>Five historians, five theories &mdash; what does the data say?</h2>
  <p>Each of these scholars proposed a different explanation for the collapse of Mediterranean trade. We compared their claims against the quantitative evidence, line by line.</p>
  <ScholarGrid />
</section>

<div class="divider"><hr></div>

<!-- CAVEATS -->
<section id="caveats">
  <div class="section-label">Caveats</div>
  <h2>What the data can&rsquo;t tell us</h2>
  <p style="margin-bottom: 1.5rem;">
    Every dataset on this page has limitations. The convergence of multiple imperfect proxies is more informative than any single dataset alone &mdash; but intellectual honesty requires listing what each proxy can and cannot show.
  </p>
  <ul class="caveat-list">
    <li><strong>Shipwreck barrel bias.</strong> After the 2nd century, a shift from amphorae to wooden barrels means late-period trade is systematically undercounted.</li>
    <li><strong>Shipwreck discovery bias.</strong> Italy, France, and Spain account for &gt;70% of all wrecks due to survey intensity, not actual sinking rates.</li>
    <li><strong>Lead proxy scope.</strong> The NGRIP2 record reflects primarily Iberian and northern European mining.</li>
    <li><strong>Correlation is not causation.</strong> Change-points align with known events but don&rsquo;t prove causation.</li>
    <li><strong>Pollen resolution.</strong> The pollen data uses 200-year bins, far coarser than other proxies.</li>
    <li><strong>PAS geographic bias.</strong> The Portable Antiquities Scheme covers Britain only.</li>
    <li><strong>Population estimates.</strong> The &ldquo;high count&rdquo; and &ldquo;low count&rdquo; schools differ by nearly 2&times;.</li>
    <li><strong>Compiled numismatic data.</strong> Individual coins varied; values shown are scholarly averages.</li>
    <li><strong>Inscription survival bias.</strong> Stone inscriptions from arid climates are over-represented.</li>
    <li><strong>Selection of proxies itself.</strong> Aspects of ancient economies that don&rsquo;t leave measurable traces are invisible to this analysis.</li>
  </ul>
  <Collapsible summary="Methodology Details" className="method-detail">
    <p><strong>Equal-probability dating:</strong> Shipwrecks and inscriptions with date ranges contribute fractional counts to each year in the range. Method: <a href="https://oxrep.classics.ox.ac.uk/databases/shipwrecks_database/" target="_blank" style="color: var(--accent);">Wilson (2011)</a>.</p>
    <p><strong>Change-point detection:</strong> Binary segmentation with RBF kernel (<a href="https://centre-borelli.github.io/ruptures-docs/" target="_blank" style="color: var(--accent);">ruptures</a> library). No historical priors. Penalty via BIC.</p>
    <p><strong>Regional classification (shipwrecks):</strong> 1,713 of 1,784 wrecks classified using Country, Sea Area, and name-based heuristics from <a href="https://oxrep.classics.ox.ac.uk/databases/shipwrecks_database/" target="_blank" style="color: var(--accent);">OxREP v2.1</a>.</p>
    <p><strong>Tree-ring data:</strong> Central European JJA temperature anomalies from <a href="https://doi.org/10.1126/science.1197175" target="_blank" style="color: var(--accent);">B&uuml;ntgen et al. (2011)</a>.</p>
    <p><strong>Volcanic forcing:</strong> <a href="https://doi.org/10.5194/essd-9-809-2017" target="_blank" style="color: var(--accent);">eVolv2k v3 (Toohey &amp; Sigl 2017)</a>.</p>
    <p><strong>Numismatic data:</strong> Walker (ANS, 1976&ndash;78), <a href="https://numismatics.org/ocre/" target="_blank" style="color: var(--accent);">OCRE</a>, <a href="https://hdl.handle.net/1887/43427" target="_blank" style="color: var(--accent);">Vrij (2016)</a>. Dirham data from <a href="https://doi.org/10.15184/aqy.2022.165" target="_blank" style="color: var(--accent);">Antiquity (2023)</a>.</p>
  </Collapsible>
</section>

<!-- FOOTER -->
<footer>
  <p>Data:
    <a href="https://doi.org/10.1073/pnas.1721818115" target="_blank">McConnell et al. 2018</a> (PNAS) &middot;
    <a href="https://oxrep.classics.ox.ac.uk/databases/shipwrecks_database/" target="_blank">OxREP Shipwrecks v2.1</a> &middot;
    Butcher &amp; Ponting 2015 &middot; Walker 1976 &middot;
    <a href="https://doi.org/10.1126/science.1197175" target="_blank">B&uuml;ntgen et al. 2011</a> &middot;
    <a href="https://doi.org/10.5194/essd-9-809-2017" target="_blank">eVolv2k v3</a> &middot;
    Rathbone &amp; Temin &middot;
    <a href="https://www.princeton.edu/~pswpc/pdfs/scheidel/070604.pdf" target="_blank">Scheidel 2006</a> &middot;
    <a href="https://chre.ashmus.ox.ac.uk/" target="_blank">CHRE</a> (Oxford) &middot;
    <a href="https://doi.org/10.1016/j.quascirev.2015.09.012" target="_blank">Fyfe et al. 2015</a> &middot;
    Rijpma 2016 &middot;
    <a href="https://finds.org.uk/" target="_blank">Portable Antiquities Scheme</a> &middot;
    <a href="https://hdl.handle.net/1887/43427" target="_blank">Vrij 2016</a> &middot;
    <a href="https://doi.org/10.15184/aqy.2022.165" target="_blank">Antiquity 2023</a> &middot;
    <a href="https://edh.ub.uni-heidelberg.de/" target="_blank">EDH</a> via <a href="https://doi.org/10.5281/zenodo.4888168" target="_blank">SDAM/Zenodo</a>
  </p>
  <p style="margin-top: 0.5rem;">Analysis: blind change-point detection with <a href="https://centre-borelli.github.io/ruptures-docs/" target="_blank">ruptures</a> &middot; Visualization: <a href="https://plotly.com/javascript/" target="_blank">Plotly.js</a> &middot; Map: <a href="https://maplibre.org/" target="_blank">MapLibre GL JS</a></p>
  <p style="margin-top: 0.5rem;">GeoCron data: <a href="https://zenodo.org/records/13363121" target="_blank">Cliopatria</a> (CC BY 4.0) &middot; <a href="https://orbis.stanford.edu/" target="_blank">ORBIS v2, Stanford</a> (CC BY 3.0)</p>
</footer>

{/if}
