<script>
  import * as aq from 'arquero'
  import * as Plot from "@observablehq/plot"
  import PlotContainer from "../lib/PlotContainer.svelte"
  import FilterControls from "../lib/FilterControls.svelte"
  import ControlGroup from "../lib/ControlGroup.svelte"
  import { dataReady, gameData, years, players, playerColors } from '../lib/gameDataStore.svelte.js'

  let selectedYear = $state(null)
  let selectedCategory = $state(null)
  let selectedProposer = $state(null)
  let selectedPlayers = $state([...players])
  let loading = $state(true)
  let error = $state(null)

  // Bin configuration
  let numBins = $state(10)
  const binWidth = $derived(1 / numBins)

  $effect(() => {
    dataReady.then(() => {
      loading = false
    }).catch(e => {
      error = e.message
      loading = false
    })
  })

  // Calculate calibration data for each player
  const calibrationData = $derived.by(() => {
    if (!gameData) return []

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
    const results = []

    for (const player of players) {
      if (!selectedPlayers.includes(player)) continue

      const playerColor = playerColors[players.indexOf(player)]

      // Group predictions into bins
      const bins = Array.from({ length: numBins }, () => ({ count: 0, trueCount: 0 }))

      for (const row of rows) {
        const prediction = row[player]
        if (prediction == null || prediction < 0 || prediction > 1) continue

        // Determine which bin this prediction falls into
        // Handle edge case where prediction === 1 (should go in last bin)
        const binIndex = prediction === 1 ? numBins - 1 : Math.floor(prediction / binWidth)

        bins[binIndex].count++
        if (row.outcome === true) {
          bins[binIndex].trueCount++
        }
      }

      // Convert bins to data points
      for (let i = 0; i < numBins; i++) {
        const bin = bins[i]
        if (bin.count === 0) continue // Skip empty bins

        const binCenter = (i + 0.5) * binWidth
        const empiricalProbability = bin.trueCount / bin.count

        results.push({
          player,
          binCenter,
          binLabel: `${Math.round(i * binWidth * 100)}-${Math.round((i + 1) * binWidth * 100)}%`,
          empiricalProbability,
          count: bin.count,
          color: playerColor
        })
      }
    }

    return results
  })

  // Get total count for display
  const totalCount = $derived.by(() => {
    if (!gameData) return 0

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

    return filtered.numRows()
  })

  let plotContainer = $state(null)
  let containerWidth = $state(600)

  // Track container width for responsive plots
  $effect(() => {
    if (!plotContainer) return

    const observer = new ResizeObserver(entries => {
      const entry = entries[0]
      if (entry) {
        containerWidth = entry.contentRect.width
      }
    })

    observer.observe(plotContainer)
    return () => observer.disconnect()
  })

  $effect(() => {
    if (!plotContainer || containerWidth < 100) return

    const isMobile = containerWidth < 500
    const plotHeight = isMobile ? 350 : 450

    // Reference line data for perfect calibration
    const perfectCalibration = [
      { x: 0, y: 0 },
      { x: 1, y: 1 }
    ]

    const plot = Plot.plot({
      width: containerWidth,
      height: plotHeight,
      style: { background: 'transparent', color: '#9a9a9a', fontFamily: 'IBM Plex Sans' },
      x: {
        label: 'Predicted probability',
        domain: [0, 1],
        tickFormat: d => `${Math.round(d * 100)}%`,
        grid: true,
        gridColor: '#2a2a2f'
      },
      y: {
        label: 'Empirical probability',
        domain: [0, 1],
        tickFormat: d => `${Math.round(d * 100)}%`,
        grid: true,
        gridColor: '#2a2a2f'
      },
      color: { domain: players, range: playerColors },
      marks: [
        // Perfect calibration diagonal line
        Plot.line(perfectCalibration, {
          x: 'x',
          y: 'y',
          stroke: '#4a4a4f',
          strokeWidth: 2,
          strokeDasharray: '6,4'
        }),
        // Player calibration lines
        Plot.line(calibrationData, {
          x: 'binCenter',
          y: 'empiricalProbability',
          stroke: 'player',
          strokeWidth: 2,
          curve: 'linear'
        }),
        // Points at each bin
        Plot.dot(calibrationData, {
          x: 'binCenter',
          y: 'empiricalProbability',
          fill: 'player',
          r: isMobile ? 4 : 5,
          title: d => `${d.player}\nPredicted: ${d.binLabel}\nActual: ${Math.round(d.empiricalProbability * 100)}%\n(${d.count} predictions)`
        })
      ]
    })

    plotContainer.replaceChildren(plot)
  })
</script>

<div class="flex flex-col gap-4">
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
    >
      {#snippet extraControls()}
        <ControlGroup label="Bins">
          <div class="flex gap-1">
            <button
              onclick={() => numBins = 5}
              class="px-3 py-2 md:py-1.5 text-sm rounded border transition-all duration-150 min-h-[44px] md:min-h-0
                {numBins === 5
                  ? 'border-phosphor-green text-phosphor-green bg-phosphor-green/10'
                  : 'border-panel-border text-text-secondary hover:border-text-secondary'}"
            >
              5
            </button>
            <button
              onclick={() => numBins = 10}
              class="px-3 py-2 md:py-1.5 text-sm rounded border transition-all duration-150 min-h-[44px] md:min-h-0
                {numBins === 10
                  ? 'border-phosphor-green text-phosphor-green bg-phosphor-green/10'
                  : 'border-panel-border text-text-secondary hover:border-text-secondary'}"
            >
              10
            </button>
          </div>
        </ControlGroup>
      {/snippet}
    </FilterControls>

    <PlotContainer title="Calibration{selectedYear ? ` for ${selectedYear}` : ' (All Years)'}{selectedCategory ? ` - ${selectedCategory}` : ''}{selectedProposer ? ` (${selectedProposer})` : ''}">
      <div bind:this={plotContainer} class="min-h-[350px] md:min-h-[450px]"></div>
    </PlotContainer>

    <div class="text-text-dim text-sm">
      Based on {totalCount} resolved statements.
      Dashed line shows perfect calibration. Hover over points for details.
    </div>
  {/if}
</div>
