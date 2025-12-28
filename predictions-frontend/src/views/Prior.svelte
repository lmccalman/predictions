<script>
  import * as aq from 'arquero'
  import FilterControls from "../lib/FilterControls.svelte"
  import { dataReady, gameData, players } from '../lib/gameDataStore.svelte.js'

  let selectedYear = $state(null)
  let selectedCategory = $state(null)
  let selectedProposer = $state(null)
  let selectedPlayers = $state([...players])
  let loading = $state(true)
  let error = $state(null)

  $effect(() => {
    dataReady.then(() => {
      loading = false
    }).catch(e => {
      error = e.message
      loading = false
    })
  })

  // Calculate prior statistics and statement lists
  const priorData = $derived.by(() => {
    if (!gameData) return { trueStatements: [], falseStatements: [], total: 0, empiricalPrior: 0.5 }

    // Filter to resolved statements only
    let filtered = gameData.filter(aq.escape(d => d.outcome !== null))

    if (selectedYear) {
      filtered = filtered.filter(aq.escape(d => d.year === selectedYear))
    }

    if (selectedCategory) {
      filtered = filtered.filter(aq.escape(d => d.category === selectedCategory))
    }

    if (selectedProposer) {
      filtered = filtered.filter(aq.escape(d => d.proposer === selectedProposer))
    }

    const rows = filtered.objects()
    const trueStatements = rows.filter(r => r.outcome === true)
    const falseStatements = rows.filter(r => r.outcome === false)
    const total = trueStatements.length + falseStatements.length

    return {
      trueStatements,
      falseStatements,
      total,
      empiricalPrior: total > 0 ? trueStatements.length / total : 0.5
    }
  })
</script>

<div class="flex flex-col gap-6">
  {#if loading}
    <div class="text-text-secondary">Loading data...</div>
  {:else if error}
    <div class="text-phosphor-red">Error loading data: {error}</div>
  {:else}
    <FilterControls
      bind:selectedYear
      bind:selectedCategory
      bind:selectedProposer
      bind:selectedPlayers
      hidePlayerFilter={true}
    />

    <!-- Empirical prior display -->
    <div class="text-center">
      <div class="text-text-dim text-sm uppercase tracking-wider mb-2">Empirical Prior</div>
      <div class="text-6xl md:text-7xl font-light text-phosphor-green tabular-nums">
        {Math.round(priorData.empiricalPrior * 100)}%
      </div>
      <div class="text-text-secondary mt-2">
        of statements resolved true
      </div>
    </div>

    <!-- Two-column statement display -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- FALSE column -->
      <div class="bg-panel-mid border border-panel-border rounded-lg overflow-hidden">
        <div class="bg-phosphor-red/10 border-b border-phosphor-red/30 px-4 py-3 flex items-center justify-between">
          <span class="text-phosphor-red font-medium">False</span>
          <span class="text-phosphor-red/70 text-sm">{priorData.falseStatements.length}</span>
        </div>
        <div class="max-h-96 overflow-y-auto">
          {#if priorData.falseStatements.length === 0}
            <div class="px-4 py-8 text-text-dim text-center text-sm">No false statements</div>
          {:else}
            <ul class="divide-y divide-panel-border">
              {#each priorData.falseStatements as statement}
                <li class="px-4 py-3 text-sm text-text-secondary hover:bg-panel-raised/50">
                  {statement.text}
                </li>
              {/each}
            </ul>
          {/if}
        </div>
      </div>

      <!-- TRUE column -->
      <div class="bg-panel-mid border border-panel-border rounded-lg overflow-hidden">
        <div class="bg-phosphor-green/10 border-b border-phosphor-green/30 px-4 py-3 flex items-center justify-between">
          <span class="text-phosphor-green font-medium">True</span>
          <span class="text-phosphor-green/70 text-sm">{priorData.trueStatements.length}</span>
        </div>
        <div class="max-h-96 overflow-y-auto">
          {#if priorData.trueStatements.length === 0}
            <div class="px-4 py-8 text-text-dim text-center text-sm">No true statements</div>
          {:else}
            <ul class="divide-y divide-panel-border">
              {#each priorData.trueStatements as statement}
                <li class="px-4 py-3 text-sm text-text-secondary hover:bg-panel-raised/50">
                  {statement.text}
                </li>
              {/each}
            </ul>
          {/if}
        </div>
      </div>
    </div>

    <!-- Interpretation -->
    <div class="text-text-dim text-sm text-center">
      {#if priorData.total === 0}
        No resolved statements match the current filters.
      {:else if Math.abs(priorData.empiricalPrior - 0.5) < 0.05}
        Statements are nearly balanced between true and false outcomes.
      {:else if priorData.empiricalPrior > 0.5}
        Statements tend to resolve true more often than false.
      {:else}
        Statements tend to resolve false more often than true.
      {/if}
    </div>
  {/if}
</div>
