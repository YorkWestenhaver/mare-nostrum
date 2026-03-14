<script>
  let { summary, className = 'source-criticism-detail', children } = $props();
</script>
<details class={className}>
  <summary>{summary}</summary>
  <div>{@render children()}</div>
</details>
