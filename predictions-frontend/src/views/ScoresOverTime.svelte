<script>
  import * as Plot from "@observablehq/plot"
  import PlotContainer from "../lib/PlotContainer.svelte"
  import ControlGroup from "../lib/ControlGroup.svelte"

  const players = ['Alice', 'Bob', 'Charlie', 'Diana']
  const playerColors = ['#4ade80', '#fbbf24', '#22d3ee', '#f87171']

  let selectedPlayers = $state([...players])

  const data = [
    { year: 2022, player: 'Alice', score: 12.5 },
    { year: 2022, player: 'Bob', score: 8.3 },
    { year: 2022, player: 'Charlie', score: 15.2 },
    { year: 2022, player: 'Diana', score: 10.1 },
    { year: 2023, player: 'Alice', score: 18.7 },
    { year: 2023, player: 'Bob', score: 14.1 },
    { year: 2023, player: 'Charlie', score: 11.8 },
    { year: 2023, player: 'Diana', score: 16.4 },
    { year: 2024, player: 'Alice', score: 22.3 },
    { year: 2024, player: 'Bob', score: 19.5 },
    { year: 2024, player: 'Charlie', score: 20.1 },
    { year: 2024, player: 'Diana', score: 18.9 },
    { year: 2025, player: 'Alice', score: 25.8 },
    { year: 2025, player: 'Bob', score: 23.2 },
    { year: 2025, player: 'Charlie', score: 24.5 },
    { year: 2025, player: 'Diana', score: 26.1 },
  ]

  const filteredData = $derived(data.filter(d => selectedPlayers.includes(d.player)))

  let plotContainer = $state(null)

  $effect(() => {
    if (!plotContainer) return

    const plot = Plot.plot({
      width: 700,
      height: 400,
      style: { background: 'transparent', color: '#9a9a9a', fontFamily: 'IBM Plex Sans' },
      x: { label: 'Year', tickFormat: d => d.toString() },
      y: { label: 'Cumulative Score', grid: true, gridColor: '#2a2a2f' },
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
</script>

<div class="flex flex-col gap-4">
  <PlotContainer title="Player Scores Over Time">
    <div bind:this={plotContainer} class="min-h-[400px]"></div>
  </PlotContainer>

  <div class="bg-panel-mid border border-panel-border rounded p-4">
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <ControlGroup label="Players">
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
      </ControlGroup>
    </div>
  </div>
</div>
