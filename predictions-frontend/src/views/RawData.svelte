<script>
  import * as aq from 'arquero'
  import * as Plot from "@observablehq/plot"
  import FilterControls from "../lib/FilterControls.svelte"
  import DisplayToggle from "../lib/DisplayToggle.svelte"
  import Modal from "../lib/Modal.svelte"
  import { dataReady, gameData, years, players, playerColors } from '../lib/gameDataStore.svelte.js'
  import { calculateScore, formatScore, formatProbability } from '../utils/scoring.js'

  let selectedYear = $state(null)
  let selectedCategory = $state(null)
  let selectedProposer = $state(null)
  let selectedPlayers = $state([...players])
  let showScores = $state(false)
  let loading = $state(true)
  let error = $state(null)
  let selectedRow = $state(null)
  let plotContainer = $state(null)

  // Prediction distribution data for the selected row
  const predictionData = $derived.by(() => {
    if (!selectedRow) return []
    return players.map((player, i) => ({
      player,
      prediction: selectedRow[player],
      color: playerColors[i]
    })).filter(d => d.prediction != null)
  })

  // Render the prediction distribution plot
  $effect(() => {
    if (!plotContainer || !selectedRow || predictionData.length === 0) return

    const plot = Plot.plot({
      width: 400,
      height: 100,
      marginTop: 20,
      marginBottom: 30,
      marginLeft: 40,
      marginRight: 20,
      style: { background: 'transparent', color: '#9a9a9a', fontFamily: 'IBM Plex Sans' },
      x: {
        label: 'Prediction',
        domain: [0, 1],
        tickFormat: d => `${Math.round(d * 100)}%`,
        grid: true,
        gridColor: '#2a2a2f'
      },
      y: { axis: null },
      color: { domain: players, range: playerColors },
      marks: [
        // Vertical line at 50% (prior)
        Plot.ruleX([0.5], { stroke: '#4a4a4f', strokeWidth: 1, strokeDasharray: '4,3' }),
        // Outcome indicator (if resolved)
        ...(selectedRow.outcome !== null ? [
          Plot.ruleX([selectedRow.outcome ? 1 : 0], {
            stroke: selectedRow.outcome ? '#4ade80' : '#f87171',
            strokeWidth: 3
          }),
          Plot.text([{ x: selectedRow.outcome ? 1 : 0 }], {
            x: 'x',
            y: 0,
            text: selectedRow.outcome ? 'TRUE' : 'FALSE',
            dy: 28,
            fill: selectedRow.outcome ? '#4ade80' : '#f87171',
            fontSize: 9,
            fontWeight: 'bold'
          })
        ] : []),
        // Player prediction dots
        Plot.dot(predictionData, {
          x: 'prediction',
          y: 0,
          fill: 'player',
          r: 8,
          title: d => `${d.player}: ${Math.round(d.prediction * 100)}%`
        }),
        // Labels above dots
        Plot.text(predictionData, {
          x: 'prediction',
          y: 0,
          text: d => d.player.charAt(0),
          dy: -16,
          fill: 'player',
          fontSize: 11,
          fontWeight: 'bold'
        })
      ]
    })

    plotContainer.replaceChildren(plot)
  })

  $effect(() => {
    dataReady.then(() => {
      loading = false
    }).catch(e => {
      error = e.message
      loading = false
    })
  })

  const filteredData = $derived.by(() => {
    if (!gameData) return []

    let filtered = gameData

    if (selectedYear) {
      filtered = filtered.filter(aq.escape(d => d.year === selectedYear))
    }

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
              <tr
                class="border-b border-panel-border/50 hover:bg-panel-mid/50 transition-colors duration-100 cursor-pointer"
                onclick={() => selectedRow = row}
              >
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
      Showing {filteredData.length} statements{#if selectedYear} for {selectedYear}{:else} across all years{/if}{#if selectedCategory} in {selectedCategory}{/if}{#if selectedProposer} by {selectedProposer}{/if}
    </div>

    <Modal open={selectedRow !== null} onClose={() => selectedRow = null}>
      {#if selectedRow}
        <div class="p-4 flex flex-col gap-4">
          <!-- Statement text -->
          <div>
            <div class="text-xs text-text-dim uppercase tracking-wider mb-1">Statement</div>
            <div class="text-text-primary text-base">{selectedRow.text}</div>
          </div>

          <!-- Metadata row -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <div class="text-xs text-text-dim uppercase tracking-wider mb-1">ID</div>
              <div class="font-mono text-text-secondary">{selectedRow.id}</div>
            </div>
            <div>
              <div class="text-xs text-text-dim uppercase tracking-wider mb-1">Year</div>
              <div class="text-text-secondary">{selectedRow.year}</div>
            </div>
            <div>
              <div class="text-xs text-text-dim uppercase tracking-wider mb-1">Category</div>
              <div class="text-text-secondary">{selectedRow.category}</div>
            </div>
            <div>
              <div class="text-xs text-text-dim uppercase tracking-wider mb-1">Proposer</div>
              <div class="text-text-secondary">{selectedRow.proposer}</div>
            </div>
          </div>

          <!-- Outcome -->
          <div>
            <div class="text-xs text-text-dim uppercase tracking-wider mb-1">Outcome</div>
            <div class="font-mono text-lg {selectedRow.outcome === true ? 'text-phosphor-green' : selectedRow.outcome === false ? 'text-phosphor-red' : 'text-text-dim'}">
              {formatOutcome(selectedRow.outcome)}
            </div>
          </div>

          <!-- Prediction Distribution Plot -->
          <div>
            <div class="text-xs text-text-dim uppercase tracking-wider mb-2">Prediction Distribution</div>
            <div bind:this={plotContainer} class="bg-panel-inset rounded border border-panel-border/50 p-2"></div>
          </div>

          <!-- Predictions -->
          <div>
            <div class="text-xs text-text-dim uppercase tracking-wider mb-2">Predictions</div>
            <div class="flex flex-col gap-2">
              {#each players as player, i}
                {@const prediction = selectedRow[player]}
                {@const score = calculateScore(prediction, selectedRow.outcome)}
                <div class="flex items-center justify-between py-2 px-3 bg-panel-inset rounded border border-panel-border/50">
                  <span class="font-medium" style="color: {playerColors[i]}">{player}</span>
                  <div class="flex items-center gap-4">
                    <span class="font-mono text-text-secondary">{formatProbability(prediction)}</span>
                    {#if selectedRow.outcome !== null}
                      <span class="font-mono text-sm {score >= 0 ? 'text-phosphor-green' : 'text-phosphor-red'}">
                        {formatScore(score)}
                      </span>
                    {/if}
                  </div>
                </div>
              {/each}
            </div>
          </div>
        </div>
      {/if}
    </Modal>
  {/if}
</div>
