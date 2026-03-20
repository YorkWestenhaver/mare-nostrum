<script>
  let { title, subtitle = '', children } = $props();
</script>

<div class="chart-group">
  <h3 class="group-title">{title}</h3>
  {#if subtitle}<p class="group-subtitle">{subtitle}</p>{/if}
  <div class="group-grid">
    {@render children()}
  </div>
</div>
