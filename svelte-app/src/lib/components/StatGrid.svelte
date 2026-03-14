<script>
  let { items } = $props();
</script>
<div class="stat-grid">
  {#each items as { value, label } (label)}
    <div class="stat-card">
      <div class="number">{value}</div>
      <div class="label">{label}</div>
    </div>
  {/each}
</div>
