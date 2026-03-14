<script>
  import PlotlyChart from './PlotlyChart.svelte';
  let { id, label, heading, wide = true, chartId = null, chartFn = null,
        caption = '', sourceHtml = '', keyFinding = '', children } = $props();
</script>

<section {id} class:wide>
  <div class="section-label">{label}</div>
  <h2>{@html heading}</h2>
  {#if children}{@render children()}{/if}
  {#if chartFn}
    <div class="chart-container">
      <PlotlyChart id={chartId} {chartFn} />
      {#if caption}
        <p class="chart-caption">
          {@html caption}
          {#if sourceHtml}<span class="source-link">{@html sourceHtml}</span>{/if}
        </p>
      {/if}
    </div>
  {/if}
  {#if keyFinding}
    <div class="key-finding">{@html keyFinding}</div>
  {/if}
</section>
