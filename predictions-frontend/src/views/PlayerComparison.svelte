<script>
  import * as Plot from "@observablehq/plot"
  import PlotContainer from "../lib/PlotContainer.svelte"
  import ControlGroup from "../lib/ControlGroup.svelte"

  const players = ['Alice', 'Bob', 'Charlie', 'Diana']
  const metrics = ['accuracy', 'confidence', 'score']

  let selectedMetric = $state('score')

  const data = [
    { player: 'Alice', year: 2022, accuracy: 0.68, confidence: 0.72, score: 12.5 },
    { player: 'Alice', year: 2023, accuracy: 0.74, confidence: 0.70, score: 18.7 },
    { player: 'Alice', year: 2024, accuracy: 0.79, confidence: 0.75, score: 22.3 },
    { player: 'Alice', year: 2025, accuracy: 0.82, confidence: 0.78, score: 25.8 },
    { player: 'Bob', year: 2022, accuracy: 0.55, confidence: 0.65, score: 8.3 },
    { player: 'Bob', year: 2023, accuracy: 0.67, confidence: 0.68, score: 14.1 },
    { player: 'Bob', year: 2024, accuracy: 0.73, confidence: 0.72, score: 19.5 },
    { player: 'Bob', year: 2025, accuracy: 0.76, confidence: 0.74, score: 23.2 },
    { player: 'Charlie', year: 2022, accuracy: 0.72, confidence: 0.80, score: 15.2 },
    { player: 'Charlie', year: 2023, accuracy: 0.65, confidence: 0.75, score: 11.8 },
    { player: 'Charlie', year: 2024, accuracy: 0.75, confidence: 0.73, score: 20.1 },
    { player: 'Charlie', year: 2025, accuracy: 0.78, confidence: 0.76, score: 24.5 },
    { player: 'Diana', year: 2022, accuracy: 0.62, confidence: 0.60, score: 10.1 },
    { player: 'Diana', year: 2023, accuracy: 0.70, confidence: 0.66, score: 16.4 },
    { player: 'Diana', year: 2024, accuracy: 0.72, confidence: 0.70, score: 18.9 },
    { player: 'Diana', year: 2025, accuracy: 0.80, confidence: 0.77, score: 26.1 },
  ]

  const playerColors = ['#4ade80', '#fbbf24', '#22d3ee', '#f87171']

  let plotContainer = $state(null)

  $effect(() => {
    if (!plotContainer) return

    const yLabel = selectedMetric === 'accuracy' ? 'Accuracy (%)'
      : selectedMetric === 'confidence' ? 'Average Confidence (%)'
      : 'Total Score'

    const yFormat = selectedMetric === 'score' ? undefined : d => (d * 100).toFixed(0) + '%'

    const plot = Plot.plot({
      width: 700,
      height: 400,
      style: { background: 'transparent', color: '#9a9a9a', fontFamily: 'IBM Plex Sans' },
      x: { label: 'Year', tickFormat: d => d.toString() },
      y: { label: yLabel, grid: true, gridColor: '#2a2a2f', tickFormat: yFormat },
      color: { domain: players, range: playerColors },
      facet: { data, x: 'player' },
      marks: [
        Plot.barY(data, {
          x: 'year',
          y: selectedMetric,
          fill: 'player',
          fillOpacity: 0.8,
        }),
        Plot.ruleY([0], { stroke: '#3a3a3f' }),
      ]
    })

    plotContainer.replaceChildren(plot)
  })
</script>

<div class="flex flex-col gap-4">
  <PlotContainer title="Player Comparison">
    <div bind:this={plotContainer} class="min-h-[400px]"></div>
  </PlotContainer>

  <div class="bg-panel-mid border border-panel-border rounded p-4">
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <ControlGroup label="Metric">
        <div class="flex gap-2">
          {#each metrics as metric}
            <button
              onclick={() => selectedMetric = metric}
              class="px-3 py-1.5 text-sm rounded border transition-all duration-150 capitalize
                {selectedMetric === metric
                  ? 'border-phosphor-green text-phosphor-green bg-phosphor-green/10'
                  : 'border-panel-border text-text-secondary hover:border-text-primary hover:text-text-primary'}"
            >
              {metric}
            </button>
          {/each}
        </div>
      </ControlGroup>
    </div>
  </div>
</div>
