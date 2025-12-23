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

  // Bin configuration
  let numBins = $state(5)
  const binWidth = $derived(1 / numBins)

  $effect(() => {
    dataReady.then(() => {
      loading = false
    }).catch(e => {
      error = e.message
      loading = false
    })
  })

  /**
   * Calculate binary entropy of a prediction.
   * H(p) = -p*log2(p) - (1-p)*log2(1-p)
   * Returns 0 for p=0 or p=1 (high confidence), 1 for p=0.5 (low confidence)
   */
  function calculateEntropy(p) {
    if (p <= 0 || p >= 1) return 0
    return -p * Math.log2(p) - (1 - p) * Math.log2(1 - p)
  }

  // Calculate score by entropy bin for each player
  const entropyData = $derived.by(() => {
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

      // Group predictions into bins by entropy
      const bins = Array.from({ length: numBins }, () => ({ totalScore: 0, count: 0 }))

      for (const row of rows) {
        const prediction = row[player]
        if (prediction == null || prediction < 0 || prediction > 1) continue

        const entropy = calculateEntropy(prediction)
        const score = calculateScore(prediction, row.outcome)
        if (score === null || !isFinite(score)) continue

        // Determine which bin this entropy falls into (entropy is 0-1)
        const binIndex = entropy === 1 ? numBins - 1 : Math.floor(entropy / binWidth)

        bins[binIndex].totalScore += score
        bins[binIndex].count++
      }

      // Convert bins to data points
      for (let i = 0; i < numBins; i++) {
        const bin = bins[i]
        const binCenter = (i + 0.5) * binWidth
        const binStart = i * binWidth
        const binEnd = (i + 1) * binWidth

        results.push({
          player,
          binCenter,
          binLabel: `${binStart.toFixed(2)}-${binEnd.toFixed(2)}`,
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
      { x: 0, y: 0 },
      { x: 1, y: 0 }
    ]

    const plot = Plot.plot({
      width: containerWidth,
      height: plotHeight,
      style: { background: 'transparent', color: '#9a9a9a', fontFamily: 'IBM Plex Sans' },
      x: {
        label: 'Entropy (0 = confident, 1 = uncertain)',
        domain: [0, 1],
        grid: true,
        gridColor: '#2a2a2f'
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
        Plot.line(entropyData, {
          x: 'binCenter',
          y: 'totalScore',
          stroke: 'player',
          strokeWidth: 2,
          curve: 'linear'
        }),
        // Points at each bin
        Plot.dot(entropyData, {
          x: 'binCenter',
          y: 'totalScore',
          fill: 'player',
          r: isMobile ? 4 : 5,
          title: d => `${d.player}\nEntropy: ${d.binLabel}\nPoints: ${d.totalScore >= 0 ? '+' : ''}${d.totalScore.toFixed(2)}\n(${d.count} predictions)`
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
      Entropy measures prediction uncertainty: 0 = confident (near 0% or 100%), 1 = uncertain (near 50%).
      Hover over points for details.
    </div>
  {/if}
</div>
