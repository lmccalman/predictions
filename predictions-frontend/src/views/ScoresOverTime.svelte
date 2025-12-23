<script>
  import * as aq from 'arquero'
  import * as Plot from "@observablehq/plot"
  import PlotContainer from "../lib/PlotContainer.svelte"
  import FilterControls from "../lib/FilterControls.svelte"
  import { dataReady, gameData, years, players, playerColors } from '../lib/gameDataStore.svelte.js'
  import { calculateScore, formatScore } from '../utils/scoring.js'

  let selectedYear = $state(null)
  let selectedCategory = $state(null)
  let selectedProposer = $state(null)
  let selectedPlayers = $state([...players])
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

  const scoreData = $derived.by(() => {
    if (!gameData || !selectedYear) return []

    let filtered = gameData.filter(aq.escape(d => d.year === selectedYear && d.outcome !== null))

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

      let totalScore = 0
      let count = 0

      for (const row of rows) {
        const score = calculateScore(row[player], row.outcome)
        if (score !== null && isFinite(score)) {
          totalScore += score
          count++
        }
      }

      results.push({
        player,
        score: totalScore,
        count,
        color: playerColors[players.indexOf(player)]
      })
    }

    return results.sort((a, b) => b.score - a.score)
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
    if (!plotContainer || scoreData.length === 0 || containerWidth < 100) return

    const isMobile = containerWidth < 500
    const plotHeight = isMobile ? 300 : 400

    const plot = Plot.plot({
      width: containerWidth,
      height: plotHeight,
      style: { background: 'transparent', color: '#9a9a9a', fontFamily: 'IBM Plex Sans' },
      x: { label: null, tickSize: 0 },
      y: { label: 'Total Score', grid: true, gridColor: '#2a2a2f' },
      color: { domain: players, range: playerColors },
      marks: [
        Plot.barY(scoreData, {
          x: 'player',
          y: 'score',
          fill: 'player',
          sort: { x: '-y' }
        }),
        Plot.ruleY([0], { stroke: '#3a3a3f' }),
        Plot.text(scoreData, {
          x: 'player',
          y: 'score',
          text: d => formatScore(d.score),
          dy: d => d.score >= 0 ? -8 : 8,
          fill: d => d.score >= 0 ? '#00ff88' : '#ff4444',
          fontSize: isMobile ? 10 : 12,
          fontWeight: 600
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
    />

    <PlotContainer title="Player Scores for {selectedYear}{selectedCategory ? ` - ${selectedCategory}` : ''}{selectedProposer ? ` (${selectedProposer})` : ''}">
      <div bind:this={plotContainer} class="min-h-[300px] md:min-h-[400px]"></div>
    </PlotContainer>

    {#if scoreData.length > 0}
      <div class="text-text-dim text-sm">
        Based on {scoreData[0]?.count ?? 0} resolved statements
      </div>
    {/if}
  {/if}
</div>
