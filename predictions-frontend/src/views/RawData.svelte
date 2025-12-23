<script>
  import * as aq from 'arquero'
  import FilterControls from "../lib/FilterControls.svelte"
  import DisplayToggle from "../lib/DisplayToggle.svelte"
  import { dataReady, gameData, years, players, playerColors } from '../lib/gameDataStore.svelte.js'
  import { calculateScore, formatScore, formatProbability } from '../utils/scoring.js'

  let selectedYear = $state(null)
  let selectedCategory = $state(null)
  let selectedProposer = $state(null)
  let selectedPlayers = $state([...players])
  let showScores = $state(false)
  let loading = $state(true)
  let error = $state(null)

  $effect(() => {
    dataReady.then(() => {
      if (!selectedYear && years.length > 0) {
        selectedYear = years[0]
      }
      loading = false
    }).catch(e => {
      error = e.message
      loading = false
    })
  })

  const filteredData = $derived.by(() => {
    if (!gameData || !selectedYear) return []

    let filtered = gameData.filter(aq.escape(d => d.year === selectedYear))

    if (selectedCategory) {
      filtered = filtered.filter(aq.escape(d => d.category === selectedCategory))
    }

    if (selectedProposer) {
      filtered = filtered.filter(aq.escape(d => d.proposer === selectedProposer))
    }

    return filtered.objects()
  })

  function formatScoreForRow(prediction, outcome) {
    const score = calculateScore(prediction, outcome)
    return formatScore(score)
  }

  function formatOutcome(outcome) {
    if (outcome === true) return 'TRUE'
    if (outcome === false) return 'FALSE'
    return '?'
  }
</script>

<div class="flex flex-col gap-4">
  <h2 class="text-xl font-semibold text-text-primary">Raw Data</h2>

  {#if loading}
    <div class="text-text-secondary">Loading data...</div>
  {:else if error}
    <div class="text-phosphor-red">Error loading data: {error}</div>
  {:else}
    {#snippet displayToggle()}
      <DisplayToggle bind:showScores />
    {/snippet}

    <FilterControls
      bind:selectedYear
      bind:selectedCategory
      bind:selectedProposer
      bind:selectedPlayers
      extraControls={displayToggle}
    />

    <!-- Table -->
    <div class="bg-panel-inset border border-panel-border rounded overflow-hidden shadow-inset-panel">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-panel-mid border-b border-panel-border">
              <th class="px-2 md:px-3 py-2 text-left text-xs font-semibold uppercase tracking-wider text-text-secondary sticky left-0 bg-panel-mid z-10 min-w-[50px] md:min-w-[60px]">ID</th>
              <th class="px-2 md:px-3 py-2 text-left text-xs font-semibold uppercase tracking-wider text-text-secondary min-w-[200px] md:min-w-[300px] max-w-[500px]">Statement</th>
              <th class="px-2 md:px-3 py-2 text-left text-xs font-semibold uppercase tracking-wider text-text-secondary min-w-[80px] md:min-w-[100px]">Category</th>
              <th class="px-2 md:px-3 py-2 text-left text-xs font-semibold uppercase tracking-wider text-text-secondary min-w-[70px] md:min-w-[80px]">Proposer</th>
              <th class="px-2 md:px-3 py-2 text-center text-xs font-semibold uppercase tracking-wider text-text-secondary min-w-[55px] md:min-w-[60px]">Outcome</th>
              {#each players.filter(p => selectedPlayers.includes(p)) as player, i}
                <th
                  class="px-2 md:px-3 py-2 text-center text-xs font-semibold uppercase tracking-wider min-w-[50px] md:min-w-[60px]"
                  style="color: {playerColors[players.indexOf(player)]}"
                >
                  {player}
                </th>
              {/each}
            </tr>
          </thead>
          <tbody>
            {#each filteredData as row, rowIndex}
              <tr class="border-b border-panel-border/50 hover:bg-panel-mid/50 transition-colors duration-100">
                <td class="px-2 md:px-3 py-2 font-mono text-text-secondary sticky left-0 bg-panel-inset z-10">{row.id}</td>
                <td class="px-2 md:px-3 py-2 text-text-primary max-w-[500px] break-words">{row.text}</td>
                <td class="px-2 md:px-3 py-2 text-text-secondary">{row.category}</td>
                <td class="px-2 md:px-3 py-2 text-text-secondary">{row.proposer}</td>
                <td class="px-2 md:px-3 py-2 text-center font-mono {row.outcome === true ? 'text-phosphor-green' : row.outcome === false ? 'text-phosphor-red' : 'text-text-dim'}">
                  {formatOutcome(row.outcome)}
                </td>
                {#each players.filter(p => selectedPlayers.includes(p)) as player}
                  {@const score = showScores ? calculateScore(row[player], row.outcome) : null}
                  <td class="px-2 md:px-3 py-2 text-center font-mono
                    {showScores && score !== null
                      ? (score >= 0 ? 'text-phosphor-green' : 'text-phosphor-red')
                      : 'text-text-secondary'}">
                    {showScores ? formatScoreForRow(row[player], row.outcome) : formatProbability(row[player])}
                  </td>
                {/each}
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>

    <div class="text-text-dim text-sm">
      Showing {filteredData.length} statements for {selectedYear}{#if selectedCategory} in {selectedCategory}{/if}{#if selectedProposer} by {selectedProposer}{/if}
    </div>
  {/if}
</div>
