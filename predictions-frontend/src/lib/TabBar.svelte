<script>
  let { tabs, activeTab, onTabChange } = $props()
</script>

<nav class="w-full md:w-[200px] bg-panel-mid border-b md:border-b-0 md:border-r border-panel-border flex flex-col">
  <!-- Logo/title - hidden on mobile to save space -->
  <div class="hidden md:block p-4 border-b border-panel-border">
    <h1 class="text-lg font-semibold text-text-primary tracking-wide">Predictions</h1>
  </div>

  <!-- Tabs - horizontal scroll on mobile, vertical on desktop -->
  <div class="flex flex-row md:flex-col overflow-x-auto md:overflow-x-visible py-1 md:py-2">
    {#each tabs as tab, i}
      <button
        onclick={() => onTabChange(i)}
        class="px-4 py-3.5 md:py-3 text-sm font-semibold uppercase tracking-wider whitespace-nowrap
          transition-all duration-150 ease-out min-h-[44px] md:min-h-0
          border-b-[3px] md:border-b-0 md:border-l-[3px]
          {activeTab === i
            ? 'text-phosphor-green bg-panel-dark border-b-phosphor-green md:border-b-transparent md:border-l-phosphor-green shadow-[inset_0_0_20px_rgba(74,222,128,0.05)]'
            : 'text-text-secondary border-b-transparent md:border-l-transparent hover:text-text-primary hover:bg-panel-raised'}"
      >
        {tab.label}
      </button>
    {/each}
  </div>
</nav>
