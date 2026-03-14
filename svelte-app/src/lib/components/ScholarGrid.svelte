<script>
  import { scholars } from '$lib/data/scholars.js';
</script>
<div class="scholar-grid">
  {#each scholars as s (s.id)}
    <div class="scholar-card" id="scholar-{s.id}">
      <div class="verdict-badge {s.verdictClass}">{s.verdict}</div>
      <div class="name">{s.name} ({s.year})</div>
      <div class="claim">{@html s.claim}</div>
      <div class="evidence">{@html s.evidence}</div>
    </div>
  {/each}
</div>
