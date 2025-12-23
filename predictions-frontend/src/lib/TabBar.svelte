<script>
  let { tabs, activeTab, onTabChange } = $props()
</script>

<nav class="w-[200px] bg-panel-mid border-r border-panel-border flex flex-col">
  <div class="p-4 border-b border-panel-border">
    <h1 class="text-lg font-semibold text-text-primary tracking-wide">Predictions</h1>
  </div>

  <div class="flex flex-col py-2">
    {#each tabs as tab, i}
      <button
        onclick={() => onTabChange(i)}
        class="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wider
          border-l-[3px] transition-all duration-150 ease-out
          {activeTab === i
            ? 'text-phosphor-green bg-panel-dark border-l-phosphor-green shadow-[inset_0_0_20px_rgba(74,222,128,0.05)]'
            : 'text-text-secondary border-l-transparent hover:text-text-primary hover:bg-panel-raised'}"
      >
        {tab.label}
      </button>
    {/each}
  </div>
</nav>
