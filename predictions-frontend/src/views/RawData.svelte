<script>
  import * as aq from 'arquero'
  import ControlGroup from "../lib/ControlGroup.svelte"
  import { dataReady, gameData, years, players, playerColors } from '../lib/gameDataStore.svelte.js'

  let selectedYear = $state(null)
  let selectedPlayers = $state([...players])
  let showScores = $state(false)
  let loading = $state(true)
  let error = $state(null)

  // Wait for data to be ready
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

    const yearFiltered = gameData.filter(aq.escape(d => d.year === selectedYear))
    return yearFiltered.objects()
  })

  function togglePlayer(player) {
    if (selectedPlayers.includes(player)) {
      selectedPlayers = selectedPlayers.filter(p => p !== player)
    } else {
      selectedPlayers = [...selectedPlayers, player]
    }
  }

  function selectAllPlayers() {
    selectedPlayers = [...players]
  }

  function clearAllPlayers() {
    selectedPlayers = []
  }

  function formatProbability(value) {
    if (value === null || value === undefined || isNaN(value)) return '-'
    return (value * 100).toFixed(0) + '%'
  }

  function calculateScore(prediction, outcome) {
    if (prediction === null || prediction === undefined || isNaN(prediction)) return null
    if (outcome === null || outcome === undefined) return null

    // Probability assigned to the actual outcome
    const pAssigned = outcome ? prediction : 1 - prediction
    // Score = log(p_assigned) - log(0.5)
    return Math.log(pAssigned) - Math.log(0.5)
  }

  function formatScore(prediction, outcome) {
    const score = calculateScore(prediction, outcome)
    if (score === null) return '-'
    if (score === -Infinity) return '-∞'
    if (score === Infinity) return '+∞'
    // Show with sign and 2 decimal places
    const sign = score >= 0 ? '+' : ''
    return sign + score.toFixed(2)
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
    <!-- Controls -->
    <div class="bg-panel-mid border border-panel-border rounded p-4">
      <div class="flex flex-col gap-4">
        <div class="flex flex-wrap gap-4 items-end">
          <ControlGroup label="Year">
            <select
              bind:value={selectedYear}
              class="bg-panel-inset border border-panel-border rounded px-3 py-2 text-text-primary
                focus:border-phosphor-green focus:outline-none focus:ring-2 focus:ring-phosphor-green/20"
            >
              {#each years as year}
                <option value={year}>{year}</option>
              {/each}
            </select>
          </ControlGroup>

          <ControlGroup label="Display">
            <button
              onclick={() => showScores = !showScores}
              class="flex items-center gap-2 px-3 py-2 rounded border transition-all duration-150
                {showScores
                  ? 'border-phosphor-green bg-phosphor-green/10 text-phosphor-green'
                  : 'border-panel-border text-text-secondary hover:border-text-secondary'}"
            >
              <span class="w-8 h-5 rounded-full relative transition-colors duration-150
                {showScores ? 'bg-phosphor-green/30' : 'bg-panel-inset'}">
                <span class="absolute top-0.5 w-4 h-4 rounded-full transition-all duration-150
                  {showScores ? 'left-3.5 bg-phosphor-green' : 'left-0.5 bg-text-dim'}"></span>
              </span>
              <span class="text-sm">{showScores ? 'Scores' : 'Probabilities'}</span>
            </button>
          </ControlGroup>
        </div>

        <ControlGroup label="Players">
          <div class="flex flex-col gap-2">
            <div class="flex gap-2">
              <button
                onclick={selectAllPlayers}
                class="px-2 py-1 text-xs rounded border border-panel-border text-text-secondary
                  hover:border-text-secondary hover:text-text-primary transition-all duration-150"
              >
                Select All
              </button>
              <button
                onclick={clearAllPlayers}
                class="px-2 py-1 text-xs rounded border border-panel-border text-text-secondary
                  hover:border-text-secondary hover:text-text-primary transition-all duration-150"
              >
                Clear All
              </button>
            </div>
            <div class="flex flex-wrap gap-2">
              {#each players as player, i}
                <button
                  onclick={() => togglePlayer(player)}
                  class="px-3 py-1.5 text-sm rounded border transition-all duration-150
                    {selectedPlayers.includes(player)
                      ? 'border-current bg-current/10 shadow-glow-green'
                      : 'border-panel-border text-text-dim hover:border-text-secondary'}"
                  style="color: {selectedPlayers.includes(player) ? playerColors[i] : ''}"
                >
                  {player}
                </button>
              {/each}
            </div>
          </div>
        </ControlGroup>
      </div>
    </div>

    <!-- Table -->
    <div class="bg-panel-inset border border-panel-border rounded overflow-hidden shadow-inset-panel">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-panel-mid border-b border-panel-border">
              <th class="px-3 py-2 text-left text-xs font-semibold uppercase tracking-wider text-text-secondary sticky left-0 bg-panel-mid z-10 min-w-[60px]">ID</th>
              <th class="px-3 py-2 text-left text-xs font-semibold uppercase tracking-wider text-text-secondary min-w-[300px] max-w-[500px]">Statement</th>
              <th class="px-3 py-2 text-left text-xs font-semibold uppercase tracking-wider text-text-secondary min-w-[100px]">Category</th>
              <th class="px-3 py-2 text-left text-xs font-semibold uppercase tracking-wider text-text-secondary min-w-[80px]">Proposer</th>
              <th class="px-3 py-2 text-center text-xs font-semibold uppercase tracking-wider text-text-secondary min-w-[60px]">Outcome</th>
              {#each players.filter(p => selectedPlayers.includes(p)) as player, i}
                <th
                  class="px-3 py-2 text-center text-xs font-semibold uppercase tracking-wider min-w-[60px]"
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
                <td class="px-3 py-2 font-mono text-text-secondary sticky left-0 bg-panel-inset z-10">{row.id}</td>
                <td class="px-3 py-2 text-text-primary max-w-[500px] break-words">{row.text}</td>
                <td class="px-3 py-2 text-text-secondary">{row.category}</td>
                <td class="px-3 py-2 text-text-secondary">{row.proposer}</td>
                <td class="px-3 py-2 text-center font-mono {row.outcome === true ? 'text-phosphor-green' : row.outcome === false ? 'text-phosphor-red' : 'text-text-dim'}">
                  {formatOutcome(row.outcome)}
                </td>
                {#each players.filter(p => selectedPlayers.includes(p)) as player}
                  {@const score = showScores ? calculateScore(row[player], row.outcome) : null}
                  <td class="px-3 py-2 text-center font-mono
                    {showScores && score !== null
                      ? (score >= 0 ? 'text-phosphor-green' : 'text-phosphor-red')
                      : 'text-text-secondary'}">
                    {showScores ? formatScore(row[player], row.outcome) : formatProbability(row[player])}
                  </td>
                {/each}
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>

    <div class="text-text-dim text-sm">
      Showing {filteredData.length} statements for {selectedYear}
    </div>
  {/if}
</div>
