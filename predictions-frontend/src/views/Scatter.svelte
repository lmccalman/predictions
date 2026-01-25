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
  let modalPlotContainer = $state(null)

  // Default to latest year to avoid overwhelming the plot
  $effect(() => {
    if (!loading && years.length > 0 && selectedYear === null) {
      selectedYear = years[0]
    }
  })

  $effect(() => {
    dataReady.then(() => {
      loading = false
    }).catch(e => {
      error = e.message
      loading = false
    })
  })

  // Filter and transform data for the scatter plot
  const filteredStatements = $derived.by(() => {
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

    // In score mode, only show resolved statements
    if (showScores) {
      filtered = filtered.filter(aq.escape(d => d.outcome !== null))
    }

    return filtered.objects()
  })

  // Transform to long format for plotting
  const scatterData = $derived.by(() => {
    const dots = []

    for (const row of filteredStatements) {
      for (const player of selectedPlayers) {
        const prediction = row[player]
        if (prediction === null || prediction === undefined) continue

        let x
        if (showScores) {
          const score = calculateScore(prediction, row.outcome)
          // Filter out infinite scores (from 0 or 1 predictions)
          if (score === null || !isFinite(score)) continue
          x = score
        } else {
          x = prediction
        }

        dots.push({
          statementId: row.id,
          player,
          x,
          prediction,
          outcome: row.outcome,
          row
        })
      }
    }

    return dots
  })

  // Plot layout constants
  const ROW_HEIGHT = 24
  const MARGIN_TOP = 10
  const MARGIN_BOTTOM = 30

  // Computed plot dimensions
  const plotHeight = $derived(Math.max(200, filteredStatements.length * ROW_HEIGHT + MARGIN_TOP + MARGIN_BOTTOM))

  // Render the main scatter plot
  $effect(() => {
    if (!plotContainer || filteredStatements.length === 0) return

    const statementIds = filteredStatements.map(s => s.id)

    const plot = Plot.plot({
      width: plotContainer.clientWidth,
      height: plotHeight,
      marginLeft: 10,
      marginRight: 20,
      marginTop: MARGIN_TOP,
      marginBottom: MARGIN_BOTTOM,
      style: { background: 'transparent', color: '#9a9a9a', fontFamily: 'IBM Plex Sans' },
      x: {
        label: showScores ? 'Score' : 'Probability',
        domain: showScores ? null : [0, 1],
        tickFormat: showScores ? null : d => `${Math.round(d * 100)}%`,
        grid: true,
        gridColor: '#2a2a2f'
      },
      y: {
        domain: statementIds,
        axis: null  // Hide Y-axis - we render clickable labels separately
      },
      color: { domain: players, range: playerColors },
      marks: [
        // Horizontal grid lines for each statement
        Plot.ruleY(statementIds, {
          stroke: '#2a2a2f',
          strokeWidth: 1
        }),
        // Reference line at 50% (probability mode) or 0 (score mode)
        Plot.ruleX([showScores ? 0 : 0.5], {
          stroke: '#4a4a4f',
          strokeWidth: 1,
          strokeDasharray: '4,3'
        }),
        // Player prediction dots
        Plot.dot(scatterData, {
          x: 'x',
          y: 'statementId',
          fill: 'player',
          r: 5,
          opacity: 0.85,
          title: d => `${d.player}: ${showScores ? formatScore(d.x) : formatProbability(d.prediction)}`
        })
      ]
    })

    plotContainer.replaceChildren(plot)
  })

  // Prediction distribution data for the selected row (modal)
  const predictionData = $derived.by(() => {
    if (!selectedRow) return []
    return players.map((player, i) => ({
      player,
      prediction: selectedRow[player],
      color: playerColors[i]
    })).filter(d => d.prediction != null)
  })

  // Predictions sorted by probability for modal display
  const sortedPredictions = $derived.by(() => {
    if (!selectedRow) return []
    return players
      .map((player, i) => ({
        player,
        prediction: selectedRow[player],
        colorIndex: i
      }))
      .filter(d => d.prediction != null)
      .sort((a, b) => a.prediction - b.prediction)
  })

  // Render the modal prediction distribution plot
  $effect(() => {
    if (!modalPlotContainer || !selectedRow || predictionData.length === 0) return

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

    modalPlotContainer.replaceChildren(plot)
  })

  function formatOutcome(outcome) {
    if (outcome === true) return 'TRUE'
    if (outcome === false) return 'FALSE'
    return '?'
  }

  function handleRowClick(row) {
    selectedRow = row
  }
</script>

<div class="flex flex-col gap-4">
  <h2 class="text-xl font-semibold text-text-primary">Scatter Plot</h2>

  {#if loading}
    <div class="text-text-secondary">Loading data...</div>
  {:else if error}
    <div class="text-phosphor-red">Error loading data: {error}</div>
  {:else}
    {#snippet displayToggle()}
      <DisplayToggle bind:value={showScores} />
    {/snippet}

    <FilterControls
      bind:selectedYear
      bind:selectedCategory
      bind:selectedProposer
      bind:selectedPlayers
      extraControls={displayToggle}
    />

    <div class="text-text-dim text-sm">
      Showing {filteredStatements.length} statements. Click on a statement ID to view details.
    </div>

    {#if filteredStatements.length === 0}
      <div class="text-text-secondary text-center py-8">
        No statements match the current filters{#if showScores} (score mode requires resolved statements){/if}.
      </div>
    {:else}
      <div class="bg-panel-inset border border-panel-border rounded overflow-hidden shadow-inset-panel">
        <div class="overflow-y-auto max-h-[70vh]">
          <div class="flex">
            <!-- Clickable ID labels -->
            <div class="flex flex-col shrink-0" style="width: 80px; padding-top: {MARGIN_TOP}px; padding-bottom: {MARGIN_BOTTOM}px;">
              {#each filteredStatements as row}
                <button
                  class="flex items-center justify-end pr-2 font-mono text-xs text-text-secondary
                    hover:text-phosphor-green hover:bg-panel-mid/50 transition-colors cursor-pointer"
                  style="height: {ROW_HEIGHT}px;"
                  onclick={() => handleRowClick(row)}
                  title="Click to view: {row.text}"
                >
                  {row.id}
                </button>
              {/each}
            </div>
            <!-- Plot container -->
            <div class="flex-1 min-w-0" bind:this={plotContainer}></div>
          </div>
        </div>
      </div>
    {/if}

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
            <div bind:this={modalPlotContainer} class="bg-panel-inset rounded border border-panel-border/50 p-2"></div>
          </div>

          <!-- Predictions -->
          <div>
            <div class="text-xs text-text-dim uppercase tracking-wider mb-2">Predictions</div>
            <div class="flex flex-col gap-2">
              {#each sortedPredictions as { player, prediction, colorIndex }}
                {@const score = calculateScore(prediction, selectedRow.outcome)}
                <div class="flex items-center justify-between py-2 px-3 bg-panel-inset rounded border border-panel-border/50">
                  <span class="font-medium" style="color: {playerColors[colorIndex]}">{player}</span>
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
