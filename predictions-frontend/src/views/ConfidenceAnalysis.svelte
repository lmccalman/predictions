<script>
  import * as aq from 'arquero'
  import * as Plot from "@observablehq/plot"
  import PlotContainer from "../lib/PlotContainer.svelte"
  import FilterControls from "../lib/FilterControls.svelte"
  import ControlGroup from "../lib/ControlGroup.svelte"
  import { dataReady, gameData, years, players, playerColors } from '../lib/gameDataStore.svelte.js'
  import { calculateScore } from '../utils/scoring.js'

  let selectedYear = $state(null)
  let selectedCategory = $state(null)
  let selectedProposer = $state(null)
  let selectedPlayers = $state([...players])
  let loading = $state(true)
  let error = $state(null)

  // Bin configuration - confidence ranges from 0.5 to 1.0
  let numBins = $state(5)
  const binWidth = $derived(0.5 / numBins)

  $effect(() => {
    dataReady.then(() => {
      loading = false
    }).catch(e => {
      error = e.message
      loading = false
    })
  })

  /**
   * Calculate confidence as max(P, 1-P).
   * Returns 0.5 for p=0.5 (uncertain), 1.0 for p=0 or p=1 (confident)
   */
  function calculateConfidence(p) {
    return Math.max(p, 1 - p)
  }

  // Calculate score by confidence bin for each player
  const confidenceData = $derived.by(() => {
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

      // Group predictions into bins by confidence (0.5 to 1.0)
      const bins = Array.from({ length: numBins }, () => ({ totalScore: 0, count: 0 }))

      for (const row of rows) {
        const prediction = row[player]
        if (prediction == null || prediction < 0 || prediction > 1) continue

        const confidence = calculateConfidence(prediction)
        const score = calculateScore(prediction, row.outcome)
        if (score === null || !isFinite(score)) continue

        // Determine which bin this confidence falls into (confidence is 0.5-1.0)
        const binIndex = confidence === 1 ? numBins - 1 : Math.floor((confidence - 0.5) / binWidth)

        bins[binIndex].totalScore += score
        bins[binIndex].count++
      }

      // Convert bins to data points
      for (let i = 0; i < numBins; i++) {
        const bin = bins[i]
        const binStart = 0.5 + i * binWidth
        const binEnd = 0.5 + (i + 1) * binWidth
        const binCenter = (binStart + binEnd) / 2

        results.push({
          player,
          binCenter,
          binLabel: `${(binStart * 100).toFixed(0)}%-${(binEnd * 100).toFixed(0)}%`,
          totalScore: bin.totalScore,
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

    // Reference line at y=0
    const zeroLine = [
      { x: 0.5, y: 0 },
      { x: 1, y: 0 }
    ]

    const plot = Plot.plot({
      width: containerWidth,
      height: plotHeight,
      style: { background: 'transparent', color: '#9a9a9a', fontFamily: 'IBM Plex Sans' },
      x: {
        label: 'Confidence: max(P, 1-P)',
        domain: [0.5, 1],
        grid: true,
        gridColor: '#2a2a2f',
        tickFormat: d => `${(d * 100).toFixed(0)}%`
      },
      y: {
        label: 'Points accrued',
        grid: true,
        gridColor: '#2a2a2f'
      },
      color: { domain: players, range: playerColors },
      marks: [
        // Zero reference line
        Plot.line(zeroLine, {
          x: 'x',
          y: 'y',
          stroke: '#4a4a4f',
          strokeWidth: 1,
          strokeDasharray: '4,4'
        }),
        // Player lines
        Plot.line(confidenceData, {
          x: 'binCenter',
          y: 'totalScore',
          stroke: 'player',
          strokeWidth: 2,
          curve: 'linear'
        }),
        // Points at each bin
        Plot.dot(confidenceData, {
          x: 'binCenter',
          y: 'totalScore',
          fill: 'player',
          r: isMobile ? 4 : 5,
          title: d => `${d.player}\nConfidence: ${d.binLabel}\nPoints: ${d.totalScore >= 0 ? '+' : ''}${d.totalScore.toFixed(2)}\n(${d.count} predictions)`
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

    <PlotContainer title="Score by Confidence{selectedYear ? ` for ${selectedYear}` : ' (All Years)'}{selectedCategory ? ` - ${selectedCategory}` : ''}{selectedProposer ? ` (${selectedProposer})` : ''}">
      <div bind:this={plotContainer} class="min-h-[350px] md:min-h-[450px]"></div>
    </PlotContainer>

    <div class="text-text-dim text-sm">
      Based on {totalCount} resolved statements.
      Confidence is max(P, 1-P): 50% = uncertain, 100% = confident.
      Hover over points for details.
    </div>
  {/if}
</div>
