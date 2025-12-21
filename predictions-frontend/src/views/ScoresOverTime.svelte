<script>
  import * as aq from 'arquero'
  import * as Plot from "@observablehq/plot"
  import PlotContainer from "../lib/PlotContainer.svelte"
  import ControlGroup from "../lib/ControlGroup.svelte"
  import { dataReady, gameData, years, players, playerColors } from '../lib/gameDataStore.svelte.js'
  import { calculateScore } from '../utils/scoring.js'

  let selectedPlayers = $state([...players])
  let loading = $state(true)
  let error = $state(null)

  // Wait for data to be ready
  $effect(() => {
    dataReady.then(() => {
      loading = false
    }).catch(e => {
      error = e.message
      loading = false
    })
  })

  // Calculate scores per player per year
  const scoreData = $derived.by(() => {
    if (!gameData) return []

    const results = []

    for (const year of years) {
      // Get resolved statements for this year
      const yearData = gameData
        .filter(aq.escape(d => d.year === year && d.outcome !== null))
        .objects()

      for (const player of players) {
        let totalScore = 0
        let count = 0

        for (const row of yearData) {
          const score = calculateScore(row[player], row.outcome)
          if (score !== null && isFinite(score)) {
            totalScore += score
            count++
          }
        }

        results.push({
          year,
          player,
          score: totalScore,
          count
        })
      }
    }

    return results
  })

  const filteredData = $derived(scoreData.filter(d => selectedPlayers.includes(d.player)))

  let plotContainer = $state(null)

  $effect(() => {
    if (!plotContainer || filteredData.length === 0) return

    const plot = Plot.plot({
      width: 700,
      height: 400,
      style: { background: 'transparent', color: '#9a9a9a', fontFamily: 'IBM Plex Sans' },
      x: { label: 'Year', tickFormat: d => d.toString(), type: 'point' },
      y: { label: 'Total Score', grid: true, gridColor: '#2a2a2f' },
      color: { domain: players, range: playerColors },
      marks: [
        Plot.line(filteredData, { x: 'year', y: 'score', stroke: 'player', strokeWidth: 2 }),
        Plot.dot(filteredData, { x: 'year', y: 'score', fill: 'player', r: 5 }),
        Plot.ruleY([0], { stroke: '#3a3a3f' }),
      ]
    })

    plotContainer.replaceChildren(plot)
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

  // Get ranked scores per year for table (filtered by selected players)
  const rankedByYear = $derived.by(() => {
    if (scoreData.length === 0 || selectedPlayers.length === 0) return { years: [], rankings: [] }

    // Group scores by year, filter by selected players, and sort by score descending
    const byYear = {}
    for (const year of years) {
      byYear[year] = scoreData
        .filter(d => d.year === year && selectedPlayers.includes(d.player))
        .sort((a, b) => b.score - a.score)
    }

    // Create row data: each row is a rank position (1st, 2nd, 3rd, etc.)
    const maxPlayers = selectedPlayers.length
    const rankings = []
    for (let rank = 0; rank < maxPlayers; rank++) {
      const row = { rank: rank + 1 }
      for (const year of years) {
        const playerData = byYear[year][rank]
        if (playerData) {
          row[year] = playerData
        }
      }
      rankings.push(row)
    }

    return { years, rankings }
  })

  function formatScoreDisplay(score) {
    if (score === null || score === undefined) return '-'
    const sign = score >= 0 ? '+' : ''
    return sign + score.toFixed(2)
  }
</script>

<div class="flex flex-col gap-4">
  {#if loading}
    <div class="text-text-secondary">Loading data...</div>
  {:else if error}
    <div class="text-phosphor-red">Error loading data: {error}</div>
  {:else}
    <PlotContainer title="Player Scores Over Time">
      <div bind:this={plotContainer} class="min-h-[400px]"></div>
    </PlotContainer>

    <div class="bg-panel-mid border border-panel-border rounded p-4">
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

    <!-- Score table - ranked by year -->
    <div class="bg-panel-inset border border-panel-border rounded overflow-hidden shadow-inset-panel">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-panel-mid border-b border-panel-border">
              <th class="px-3 py-2 text-left text-xs font-semibold uppercase tracking-wider text-text-secondary sticky left-0 bg-panel-mid z-10 w-12">Rank</th>
              {#each years as year}
                <th class="px-3 py-2 text-center text-xs font-semibold uppercase tracking-wider text-text-secondary min-w-[120px]">{year}</th>
              {/each}
            </tr>
          </thead>
          <tbody>
            {#each rankedByYear.rankings as row}
              <tr class="border-b border-panel-border/50 hover:bg-panel-mid/50 transition-colors duration-100">
                <td class="px-3 py-2 font-medium text-text-secondary sticky left-0 bg-panel-inset z-10">
                  {row.rank}
                </td>
                {#each years as year}
                  {@const data = row[year]}
                  {#if data}
                    {@const playerIndex = players.indexOf(data.player)}
                    <td class="px-3 py-2 text-center">
                      <span style="color: {playerColors[playerIndex]}">{data.player}</span>
                      <span class="font-mono ml-1 {data.score >= 0 ? 'text-phosphor-green' : 'text-phosphor-red'}">
                        {formatScoreDisplay(data.score)}
                      </span>
                    </td>
                  {:else}
                    <td class="px-3 py-2 text-center text-text-dim">-</td>
                  {/if}
                {/each}
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>
  {/if}
</div>
