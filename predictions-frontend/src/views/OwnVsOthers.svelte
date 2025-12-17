<script>
  import * as Plot from "@observablehq/plot"
  import PlotContainer from "../lib/PlotContainer.svelte"
  import ControlGroup from "../lib/ControlGroup.svelte"

  let showDifference = $state(false)

  // Performance on own predictions vs others' predictions
  const data = [
    { player: 'Alice', type: 'Own', score: 6.2 },
    { player: 'Alice', type: 'Others', score: 5.8 },
    { player: 'Bob', type: 'Own', score: 4.8 },
    { player: 'Bob', type: 'Others', score: 5.5 },
    { player: 'Charlie', type: 'Own', score: 5.1 },
    { player: 'Charlie', type: 'Others', score: 5.9 },
    { player: 'Diana', type: 'Own', score: 6.8 },
    { player: 'Diana', type: 'Others', score: 5.2 },
  ]

  const differenceData = [
    { player: 'Alice', diff: 0.4 },
    { player: 'Bob', diff: -0.7 },
    { player: 'Charlie', diff: -0.8 },
    { player: 'Diana', diff: 1.6 },
  ]

  const typeColors = { 'Own': '#4ade80', 'Others': '#60a5fa' }

  let plotContainer = $state(null)

  $effect(() => {
    if (!plotContainer) return

    let plot
    if (showDifference) {
      plot = Plot.plot({
        width: 700,
        height: 400,
        style: { background: 'transparent', color: '#9a9a9a', fontFamily: 'IBM Plex Sans' },
        x: { label: 'Player' },
        y: { label: 'Score Difference (Own - Others)', grid: true, gridColor: '#2a2a2f' },
        marks: [
          Plot.barY(differenceData, {
            x: 'player',
            y: 'diff',
            fill: d => d.diff >= 0 ? '#4ade80' : '#f87171',
            fillOpacity: 0.8,
          }),
          Plot.ruleY([0], { stroke: '#5a5a5a', strokeWidth: 1 }),
          Plot.text(differenceData, {
            x: 'player',
            y: d => d.diff >= 0 ? d.diff + 0.15 : d.diff - 0.15,
            text: d => (d.diff >= 0 ? '+' : '') + d.diff.toFixed(1),
            fill: d => d.diff >= 0 ? '#4ade80' : '#f87171',
            fontSize: 12,
            fontWeight: 600,
          }),
        ]
      })
    } else {
      plot = Plot.plot({
        width: 700,
        height: 400,
        style: { background: 'transparent', color: '#9a9a9a', fontFamily: 'IBM Plex Sans' },
        x: { label: 'Player' },
        y: { label: 'Average Score per Prediction', grid: true, gridColor: '#2a2a2f' },
        fx: { label: null },
        color: { domain: ['Own', 'Others'], range: ['#4ade80', '#60a5fa'] },
        marks: [
          Plot.barY(data, {
            x: 'type',
            y: 'score',
            fx: 'player',
            fill: 'type',
            fillOpacity: 0.8,
          }),
          Plot.ruleY([0], { stroke: '#3a3a3f' }),
        ]
      })
    }

    plotContainer.replaceChildren(plot)
  })
</script>

<div class="flex flex-col gap-4">
  <PlotContainer title="Own Predictions vs Others'">
    <div bind:this={plotContainer} class="min-h-[400px]"></div>
  </PlotContainer>

  <div class="bg-panel-mid border border-panel-border rounded p-4">
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <ControlGroup label="View">
        <button
          onclick={() => showDifference = !showDifference}
          class="flex items-center gap-2 px-3 py-2 rounded border transition-all duration-150
            {showDifference
              ? 'border-phosphor-green text-phosphor-green bg-phosphor-green/10'
              : 'border-panel-border text-text-secondary hover:border-text-primary'}"
        >
          <span class="w-3 h-3 rounded-sm transition-all duration-150
            {showDifference ? 'bg-phosphor-green shadow-glow-green' : 'bg-panel-inset border border-panel-border'}">
          </span>
          Show Difference
        </button>
      </ControlGroup>

      <div class="col-span-2 sm:col-span-3 flex items-end gap-4">
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-sm bg-phosphor-green"></span>
          <span class="text-xs text-text-secondary">Own predictions</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-sm bg-phosphor-blue"></span>
          <span class="text-xs text-text-secondary">Others' predictions</span>
        </div>
      </div>
    </div>
  </div>
</div>
