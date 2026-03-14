<script>
  let { tooltip, children } = $props();
</script>
<span class="data-term" data-tooltip={tooltip}>{@render children()}</span>
