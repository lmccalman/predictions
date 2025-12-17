<script>
  import * as Plot from "@observablehq/plot"
  import PlotContainer from "../lib/PlotContainer.svelte"
  import ControlGroup from "../lib/ControlGroup.svelte"

  const players = ['All', 'Alice', 'Bob', 'Charlie', 'Diana']
  let selectedPlayer = $state('All')

  // Calibration data: bucketed by confidence level
  const data = [
    { player: 'Alice', confidenceBucket: 0.55, actualAccuracy: 0.52, count: 12 },
    { player: 'Alice', confidenceBucket: 0.65, actualAccuracy: 0.61, count: 18 },
    { player: 'Alice', confidenceBucket: 0.75, actualAccuracy: 0.72, count: 24 },
    { player: 'Alice', confidenceBucket: 0.85, actualAccuracy: 0.80, count: 15 },
    { player: 'Alice', confidenceBucket: 0.95, actualAccuracy: 0.88, count: 8 },
    { player: 'Bob', confidenceBucket: 0.55, actualAccuracy: 0.58, count: 14 },
    { player: 'Bob', confidenceBucket: 0.65, actualAccuracy: 0.68, count: 20 },
    { player: 'Bob', confidenceBucket: 0.75, actualAccuracy: 0.70, count: 22 },
    { player: 'Bob', confidenceBucket: 0.85, actualAccuracy: 0.78, count: 12 },
    { player: 'Bob', confidenceBucket: 0.95, actualAccuracy: 0.82, count: 6 },
    { player: 'Charlie', confidenceBucket: 0.55, actualAccuracy: 0.48, count: 10 },
    { player: 'Charlie', confidenceBucket: 0.65, actualAccuracy: 0.55, count: 16 },
    { player: 'Charlie', confidenceBucket: 0.75, actualAccuracy: 0.68, count: 28 },
    { player: 'Charlie', confidenceBucket: 0.85, actualAccuracy: 0.82, count: 18 },
    { player: 'Charlie', confidenceBucket: 0.95, actualAccuracy: 0.91, count: 10 },
    { player: 'Diana', confidenceBucket: 0.55, actualAccuracy: 0.60, count: 8 },
    { player: 'Diana', confidenceBucket: 0.65, actualAccuracy: 0.70, count: 15 },
    { player: 'Diana', confidenceBucket: 0.75, actualAccuracy: 0.78, count: 20 },
    { player: 'Diana', confidenceBucket: 0.85, actualAccuracy: 0.85, count: 14 },
    { player: 'Diana', confidenceBucket: 0.95, actualAccuracy: 0.92, count: 9 },
  ]

  const playerColors = { 'Alice': '#4ade80', 'Bob': '#fbbf24', 'Charlie': '#22d3ee', 'Diana': '#f87171' }

  const filteredData = $derived(
    selectedPlayer === 'All' ? data : data.filter(d => d.player === selectedPlayer)
  )

  let plotContainer = $state(null)

  $effect(() => {
    if (!plotContainer) return

    const plot = Plot.plot({
      width: 700,
      height: 400,
      style: { background: 'transparent', color: '#9a9a9a', fontFamily: 'IBM Plex Sans' },
      x: { label: 'Stated Confidence', domain: [0.5, 1], tickFormat: d => (d * 100) + '%' },
      y: { label: 'Actual Accuracy', domain: [0.4, 1], grid: true, gridColor: '#2a2a2f', tickFormat: d => (d * 100) + '%' },
      r: { range: [4, 20] },
      marks: [
        // Perfect calibration line
        Plot.line([[0.5, 0.5], [1, 1]], { stroke: '#3a3a3f', strokeWidth: 1, strokeDasharray: '4,4' }),
        // Data points
        Plot.dot(filteredData, {
          x: 'confidenceBucket',
          y: 'actualAccuracy',
          r: 'count',
          fill: d => playerColors[d.player],
          fillOpacity: 0.7,
          stroke: d => playerColors[d.player],
          strokeWidth: 2,
        }),
        // Annotation
        Plot.text([{ x: 0.92, y: 0.92 }], {
          x: 'x', y: 'y', text: ['Perfect calibration'],
          fill: '#5a5a5a', fontSize: 10, textAnchor: 'end'
        }),
      ]
    })

    plotContainer.replaceChildren(plot)
  })
</script>

<div class="flex flex-col gap-4">
  <PlotContainer title="Confidence Calibration">
    <div bind:this={plotContainer} class="min-h-[400px]"></div>
  </PlotContainer>

  <div class="bg-panel-mid border border-panel-border rounded p-4">
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <ControlGroup label="Player">
        <select
          bind:value={selectedPlayer}
          class="bg-panel-inset border border-panel-border rounded px-3 py-2 text-text-primary
            focus:border-phosphor-green focus:outline-none focus:ring-2 focus:ring-phosphor-green/20"
        >
          {#each players as player}
            <option value={player}>{player}</option>
          {/each}
        </select>
      </ControlGroup>

      <div class="col-span-2 sm:col-span-3 flex items-end">
        <p class="text-xs text-text-dim">
          Points above the dashed line indicate overconfidence; below indicates underconfidence.
          Point size reflects number of predictions in that bucket.
        </p>
      </div>
    </div>
  </div>
</div>
