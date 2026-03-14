<script>
  import { activeTab } from '$lib/stores/activeTab.js';

  function setTab(tab) {
    $activeTab = tab;
    window.scrollTo({ top: 0, behavior: 'instant' });
  }
</script>

<nav>
  <div class="nav-tabs">
    <button class="tab-btn" class:active={$activeTab === 'world'} onclick={() => setTab('world')}>World Civilizations</button>
    <button class="tab-btn" class:active={$activeTab === 'med'} onclick={() => setTab('med')}>Mediterranean Economy</button>
  </div>
  {#if $activeTab === 'med'}
    <div class="nav-links">
      <a href="#geocron" style="color:var(--accent)">Map</a>
      <a href="#shipwrecks">Trade</a>
      <a href="#shipwreck-source-criticism" style="color:var(--red)">Criticism</a>
      <a href="#currency">Money</a>
      <a href="#lead">Industry</a>
      <a href="#inscriptions">Institutions</a>
      <a href="#climate">Climate</a>
      <a href="#overlay">Overlay</a>
      <a href="#scholars">Scholars</a>
    </div>
  {/if}
</nav>

<style>
  nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100;
    background: rgba(12, 15, 19, 0.85);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border);
    padding: 0 1.5rem;
    display: flex;
    align-items: center;
    height: 56px;
    font-family: var(--font-sans);
    font-size: 13px;
    letter-spacing: 0.04em;
    gap: 0;
  }

  .nav-tabs {
    display: flex;
    gap: 2px;
    margin-right: auto;
    flex-shrink: 0;
  }

  .tab-btn {
    background: none;
    border: none;
    color: var(--text-muted);
    font-family: var(--font-sans);
    font-size: 13px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    padding: 0.5rem 1rem;
    cursor: pointer;
    border-radius: 4px;
    transition: color 0.15s, background 0.15s;
    white-space: nowrap;
  }
  .tab-btn:hover {
    color: var(--accent-light);
    background: rgba(201, 148, 74, 0.08);
  }
  .tab-btn.active {
    color: var(--accent);
    background: rgba(201, 148, 74, 0.12);
    font-weight: 700;
  }

  .nav-links {
    display: flex;
    align-items: center;
  }
  .nav-links a {
    color: var(--text-muted);
    text-decoration: none;
    padding: 0 0.75rem;
    text-transform: uppercase;
    transition: color 0.2s;
    white-space: nowrap;
  }
  .nav-links a:hover { color: var(--accent-light); }

  @media (max-width: 900px) {
    .nav-links { display: none; }
  }
</style>
