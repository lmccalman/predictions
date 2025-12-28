<script>
  import * as aq from 'arquero'
  import * as Plot from "@observablehq/plot"
  import PlotContainer from "../lib/PlotContainer.svelte"
  import FilterControls from "../lib/FilterControls.svelte"
  import DisplayToggle from "../lib/DisplayToggle.svelte"
  import { dataReady, gameData, years, players, playerColors } from '../lib/gameDataStore.svelte.js'
  import { calculateWinLoss } from '../utils/scoring.js'

  let selectedYear = $state(null)
  let selectedCategory = $state(null)
  let selectedProposer = $state(null)
  let selectedPlayers = $state([...players])
  let showRate = $state(false)
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

  const winLossData = $derived.by(() => {
    if (!gameData) return []

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

      let wins = 0
      let count = 0

      for (const row of rows) {
        const result = calculateWinLoss(row[player], row.outcome)
        if (result !== null) {
          wins += result
          count++
        }
      }

      results.push({
        player,
        wins,
        count,
        winRate: count > 0 ? wins / count : 0,
        color: playerColors[players.indexOf(player)]
      })
    }

    return results.sort((a, b) => showRate ? b.winRate - a.winRate : b.wins - a.wins)
  })

  let plotContainer = $state(null)
  let containerWidth = $state(600)

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
    if (!plotContainer || winLossData.length === 0 || containerWidth < 100) return

    const isMobile = containerWidth < 500
    const plotHeight = isMobile ? 300 : 400
    const yField = showRate ? 'winRate' : 'wins'

    const plot = Plot.plot({
      width: containerWidth,
      height: plotHeight,
      marginBottom: isMobile ? 60 : 30,
      style: { background: 'transparent', color: '#9a9a9a', fontFamily: 'IBM Plex Sans' },
      x: { label: null, tickSize: 0, tickRotate: isMobile ? -45 : 0 },
      y: {
        label: showRate ? 'Win Rate' : 'Wins',
        grid: true,
        gridColor: '#2a2a2f',
        ...(showRate ? { domain: [0, 1], tickFormat: d => `${Math.round(d * 100)}%` } : {})
      },
      color: { domain: players, range: playerColors },
      marks: [
        Plot.barY(winLossData, {
          x: 'player',
          y: yField,
          fill: 'player',
          sort: { x: '-y' }
        }),
        Plot.ruleY([0], { stroke: '#3a3a3f' }),
        Plot.text(winLossData, {
          x: 'player',
          y: yField,
          text: d => showRate ? `${Math.round(d.winRate * 100)}%` : `${d.wins}/${d.count}`,
          dy: -8,
          fill: '#00ff88',
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
    {#snippet displayToggle()}
      <DisplayToggle bind:value={showRate} offLabel="Total Wins" onLabel="Win Rate" />
    {/snippet}

    <FilterControls
      bind:selectedYear
      bind:selectedCategory
      bind:selectedProposer
      bind:selectedPlayers
      extraControls={displayToggle}
    />

    <PlotContainer title="{showRate ? 'Win Rate' : 'Win/Loss'}{selectedYear ? ` for ${selectedYear}` : ' (All Years)'}{selectedCategory ? ` - ${selectedCategory}` : ''}{selectedProposer ? ` (${selectedProposer})` : ''}">
      <div bind:this={plotContainer} class="min-h-[300px] md:min-h-[400px]"></div>
    </PlotContainer>

    {#if winLossData.length > 0}
      <div class="text-text-dim text-sm">
        Based on {winLossData[0]?.count ?? 0} resolved statements. Win = prediction on correct side of 0.5.
      </div>
    {/if}
  {/if}
</div>
