<script>
  import { PLOTLY_CONFIG } from '$lib/charts/plotly.js';
  let { id, chartFn } = $props();
  let container = $state();

  $effect(() => {
    const { traces, layout } = chartFn();
    let cleanup;
    import('plotly.js-dist-min').then(({ default: Plotly }) => {
      Plotly.newPlot(container, traces, layout, PLOTLY_CONFIG);
      const onResize = () => Plotly.Plots.resize(container);
      window.addEventListener('resize', onResize);
      cleanup = () => {
        Plotly.purge(container);
        window.removeEventListener('resize', onResize);
      };
    });
    return () => cleanup?.();
  });
</script>

<div bind:this={container} {id}></div>
