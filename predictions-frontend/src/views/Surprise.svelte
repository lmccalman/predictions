<script>
  import * as aq from 'arquero'
  import * as Plot from "@observablehq/plot"
  import FilterControls from "../lib/FilterControls.svelte"
  import Modal from "../lib/Modal.svelte"
  import { dataReady, gameData, years, players, playerColors } from '../lib/gameDataStore.svelte.js'
  import { calculateScore, formatScore, formatProbability } from '../utils/scoring.js'

  let selectedYear = $state(null)
  let selectedCategory = $state(null)
  let selectedProposer = $state(null)
  let loading = $state(true)
  let error = $state(null)
  let selectedRow = $state(null)
  let sortColumn = $state('avgScore')
  let sortAscending = $state(true)

  $effect(() => {
    dataReady.then(() => {
      loading = false
    }).catch(e => {
      error = e.message
      loading = false
    })
  })

  // Compute statistics for each statement (across all participants)
  function computeStats(row) {
    const predictions = []
    const scores = []

    for (const player of players) {
      const pred = row[player]
      if (pred != null && !isNaN(pred)) {
        predictions.push(pred)
        if (row.outcome !== null) {
          const score = calculateScore(pred, row.outcome)
          if (score !== null && isFinite(score)) {
            scores.push(score)
          }
        }
      }
    }

    const avgProb = predictions.length > 0
      ? predictions.reduce((a, b) => a + b, 0) / predictions.length
      : null

    const stdProb = predictions.length > 1
      ? Math.sqrt(predictions.reduce((sum, p) => sum + (p - avgProb) ** 2, 0) / (predictions.length - 1))
      : null

    const avgScore = scores.length > 0
      ? scores.reduce((a, b) => a + b, 0) / scores.length
      : null

    const stdScore = scores.length > 1
      ? Math.sqrt(scores.reduce((sum, s) => sum + (s - avgScore) ** 2, 0) / (scores.length - 1))
      : null

    return { avgProb, stdProb, avgScore, stdScore, nPredictions: predictions.length, nScores: scores.length }
  }

  const processedData = $derived.by(() => {
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

    const rows = filtered.objects()

    // Add computed stats to each row
    const withStats = rows.map(row => ({
      ...row,
      stats: computeStats(row)
    }))

    // Sort by selected column
    withStats.sort((a, b) => {
      let aVal, bVal

      switch (sortColumn) {
        case 'avgProb':
          aVal = a.stats.avgProb
          bVal = b.stats.avgProb
          break
        case 'stdProb':
          aVal = a.stats.stdProb
          bVal = b.stats.stdProb
          break
        case 'avgScore':
          aVal = a.stats.avgScore
          bVal = b.stats.avgScore
          break
        case 'stdScore':
          aVal = a.stats.stdScore
          bVal = b.stats.stdScore
          break
        default:
          return 0
      }

      // Handle nulls - push to end
      if (aVal === null && bVal === null) return 0
      if (aVal === null) return 1
      if (bVal === null) return -1

      return sortAscending ? aVal - bVal : bVal - aVal
    })

    return withStats
  })

  function toggleSort(column) {
    if (sortColumn === column) {
      sortAscending = !sortAscending
    } else {
      sortColumn = column
      sortAscending = column === 'avgScore' // Default ascending for avgScore (most surprising = lowest)
    }
  }

  function formatStat(value, decimals = 2) {
    if (value === null) return '-'
    return value.toFixed(decimals)
  }

  function formatOutcome(outcome) {
    if (outcome === true) return 'TRUE'
    if (outcome === false) return 'FALSE'
    return '?'
  }

  function getSortIndicator(column) {
    if (sortColumn !== column) return ''
    return sortAscending ? ' ↑' : ' ↓'
  }

  // Modal plot for prediction distribution
  let plotContainer = $state(null)

  const predictionData = $derived.by(() => {
    if (!selectedRow) return []
    return players.map((player, i) => ({
      player,
      prediction: selectedRow[player],
      color: playerColors[i]
    })).filter(d => d.prediction != null)
  })

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
        Plot.ruleX([0.5], { stroke: '#4a4a4f', strokeWidth: 1, strokeDasharray: '4,3' }),
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
        Plot.dot(predictionData, {
          x: 'prediction',
          y: 0,
          fill: 'player',
          r: 8,
          title: d => `${d.player}: ${Math.round(d.prediction * 100)}%`
        }),
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
</script>

<div class="flex flex-col gap-4">
  <h2 class="text-xl font-semibold text-text-primary">Statement Statistics</h2>
  <p class="text-text-secondary text-sm">
    Statistics computed across all participants. Click column headers to sort.
  </p>

  {#if loading}
    <div class="text-text-secondary">Loading data...</div>
  {:else if error}
    <div class="text-phosphor-red">Error loading data: {error}</div>
  {:else}
    <FilterControls
      bind:selectedYear
      bind:selectedCategory
      bind:selectedProposer
      hidePlayerFilter={true}
    />

    <!-- Table -->
    <div class="bg-panel-inset border border-panel-border rounded overflow-hidden shadow-inset-panel">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-panel-mid border-b border-panel-border">
              <th class="px-2 md:px-3 py-2 text-left text-xs font-semibold uppercase tracking-wider text-text-secondary sticky left-0 bg-panel-mid z-10 min-w-[50px] md:min-w-[60px]">ID</th>
              <th class="px-2 md:px-3 py-2 text-left text-xs font-semibold uppercase tracking-wider text-text-secondary min-w-[200px] md:min-w-[300px] max-w-[500px]">Statement</th>
              <th class="px-2 md:px-3 py-2 text-center text-xs font-semibold uppercase tracking-wider text-text-secondary min-w-[55px] md:min-w-[60px]">Outcome</th>
              <th
                class="px-2 md:px-3 py-2 text-center text-xs font-semibold uppercase tracking-wider text-text-secondary min-w-[70px] cursor-pointer hover:text-text-primary transition-colors"
                onclick={() => toggleSort('avgProb')}
              >
                Avg P{getSortIndicator('avgProb')}
              </th>
              <th
                class="px-2 md:px-3 py-2 text-center text-xs font-semibold uppercase tracking-wider text-text-secondary min-w-[70px] cursor-pointer hover:text-text-primary transition-colors"
                onclick={() => toggleSort('stdProb')}
              >
                σ(P){getSortIndicator('stdProb')}
              </th>
              <th
                class="px-2 md:px-3 py-2 text-center text-xs font-semibold uppercase tracking-wider text-text-secondary min-w-[70px] cursor-pointer hover:text-text-primary transition-colors"
                onclick={() => toggleSort('avgScore')}
              >
                Avg Score{getSortIndicator('avgScore')}
              </th>
              <th
                class="px-2 md:px-3 py-2 text-center text-xs font-semibold uppercase tracking-wider text-text-secondary min-w-[70px] cursor-pointer hover:text-text-primary transition-colors"
                onclick={() => toggleSort('stdScore')}
              >
                σ(Score){getSortIndicator('stdScore')}
              </th>
            </tr>
          </thead>
          <tbody>
            {#each processedData as row, rowIndex}
              <tr
                class="border-b border-panel-border/50 hover:bg-panel-mid/50 transition-colors duration-100 cursor-pointer"
                onclick={() => selectedRow = row}
              >
                <td class="px-2 md:px-3 py-2 font-mono text-text-secondary sticky left-0 bg-panel-inset z-10">{row.id}</td>
                <td class="px-2 md:px-3 py-2 text-text-primary max-w-[500px] break-words">{row.text}</td>
                <td class="px-2 md:px-3 py-2 text-center font-mono {row.outcome === true ? 'text-phosphor-green' : row.outcome === false ? 'text-phosphor-red' : 'text-text-dim'}">
                  {formatOutcome(row.outcome)}
                </td>
                <td class="px-2 md:px-3 py-2 text-center font-mono text-text-secondary">
                  {formatStat(row.stats.avgProb)}
                </td>
                <td class="px-2 md:px-3 py-2 text-center font-mono text-text-secondary">
                  {formatStat(row.stats.stdProb)}
                </td>
                <td class="px-2 md:px-3 py-2 text-center font-mono {row.stats.avgScore !== null ? (row.stats.avgScore >= 0 ? 'text-phosphor-green' : 'text-phosphor-red') : 'text-text-dim'}">
                  {row.stats.avgScore !== null ? (row.stats.avgScore >= 0 ? '+' : '') + formatStat(row.stats.avgScore) : '-'}
                </td>
                <td class="px-2 md:px-3 py-2 text-center font-mono text-text-secondary">
                  {formatStat(row.stats.stdScore)}
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>

    <div class="text-text-dim text-sm">
      Showing {processedData.length} statements{#if selectedYear} for {selectedYear}{:else} across all years{/if}{#if selectedCategory} in {selectedCategory}{/if}{#if selectedProposer} by {selectedProposer}{/if}
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

          <!-- Statistics Summary -->
          <div>
            <div class="text-xs text-text-dim uppercase tracking-wider mb-2">Statistics</div>
            <div class="grid grid-cols-2 gap-3">
              <div class="bg-panel-inset rounded border border-panel-border/50 p-3">
                <div class="text-xs text-text-dim mb-1">Avg Probability</div>
                <div class="font-mono text-text-primary">{formatStat(selectedRow.stats.avgProb)}</div>
              </div>
              <div class="bg-panel-inset rounded border border-panel-border/50 p-3">
                <div class="text-xs text-text-dim mb-1">σ(Probability)</div>
                <div class="font-mono text-text-primary">{formatStat(selectedRow.stats.stdProb)}</div>
              </div>
              <div class="bg-panel-inset rounded border border-panel-border/50 p-3">
                <div class="text-xs text-text-dim mb-1">Avg Score</div>
                <div class="font-mono {selectedRow.stats.avgScore !== null ? (selectedRow.stats.avgScore >= 0 ? 'text-phosphor-green' : 'text-phosphor-red') : 'text-text-dim'}">
                  {selectedRow.stats.avgScore !== null ? (selectedRow.stats.avgScore >= 0 ? '+' : '') + formatStat(selectedRow.stats.avgScore) : '-'}
                </div>
              </div>
              <div class="bg-panel-inset rounded border border-panel-border/50 p-3">
                <div class="text-xs text-text-dim mb-1">σ(Score)</div>
                <div class="font-mono text-text-primary">{formatStat(selectedRow.stats.stdScore)}</div>
              </div>
            </div>
          </div>

          <!-- Prediction Distribution Plot -->
          <div>
            <div class="text-xs text-text-dim uppercase tracking-wider mb-2">Prediction Distribution</div>
            <div bind:this={plotContainer} class="bg-panel-inset rounded border border-panel-border/50 p-2"></div>
          </div>

          <!-- Individual Predictions -->
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
