<script>
  import * as Plot from "@observablehq/plot"
  import PlotContainer from "../lib/PlotContainer.svelte"
  import ControlGroup from "../lib/ControlGroup.svelte"

  const years = [2022, 2023, 2024, 2025]
  let selectedYear = $state(2025)

  const data = [
    { year: 2022, category: 'Politics', avgScore: 2.3, count: 8 },
    { year: 2022, category: 'Science', avgScore: 1.8, count: 5 },
    { year: 2022, category: 'Sports', avgScore: 3.1, count: 6 },
    { year: 2022, category: 'Entertainment', avgScore: 2.0, count: 4 },
    { year: 2022, category: 'Personal', avgScore: 2.7, count: 7 },
    { year: 2023, category: 'Politics', avgScore: 2.8, count: 9 },
    { year: 2023, category: 'Science', avgScore: 2.1, count: 6 },
    { year: 2023, category: 'Sports', avgScore: 2.5, count: 5 },
    { year: 2023, category: 'Entertainment', avgScore: 1.9, count: 5 },
    { year: 2023, category: 'Personal', avgScore: 3.2, count: 8 },
    { year: 2024, category: 'Politics', avgScore: 3.1, count: 10 },
    { year: 2024, category: 'Science', avgScore: 2.4, count: 7 },
    { year: 2024, category: 'Sports', avgScore: 2.9, count: 6 },
    { year: 2024, category: 'Entertainment', avgScore: 2.2, count: 6 },
    { year: 2024, category: 'Personal', avgScore: 3.5, count: 9 },
    { year: 2025, category: 'Politics', avgScore: 3.4, count: 11 },
    { year: 2025, category: 'Science', avgScore: 2.6, count: 8 },
    { year: 2025, category: 'Sports', avgScore: 3.2, count: 7 },
    { year: 2025, category: 'Entertainment', avgScore: 2.5, count: 7 },
    { year: 2025, category: 'Personal', avgScore: 3.8, count: 10 },
  ]

  const categoryColors = {
    'Politics': '#f87171',
    'Science': '#60a5fa',
    'Sports': '#4ade80',
    'Entertainment': '#fbbf24',
    'Personal': '#22d3ee',
  }

  const filteredData = $derived(data.filter(d => d.year === selectedYear))

  let plotContainer = $state(null)

  $effect(() => {
    if (!plotContainer) return

    const plot = Plot.plot({
      width: 700,
      height: 400,
      style: { background: 'transparent', color: '#9a9a9a', fontFamily: 'IBM Plex Sans' },
      x: { label: 'Category' },
      y: { label: 'Average Score', grid: true, gridColor: '#2a2a2f' },
      marks: [
        Plot.barY(filteredData, {
          x: 'category',
          y: 'avgScore',
          fill: d => categoryColors[d.category],
          fillOpacity: 0.8,
        }),
        Plot.ruleY([0], { stroke: '#3a3a3f' }),
        Plot.text(filteredData, {
          x: 'category',
          y: 'avgScore',
          text: d => d.count + ' predictions',
          dy: -10,
          fill: '#9a9a9a',
          fontSize: 11,
        }),
      ]
    })

    plotContainer.replaceChildren(plot)
  })
</script>

<div class="flex flex-col gap-4">
  <PlotContainer title="Performance by Category">
    <div bind:this={plotContainer} class="min-h-[400px]"></div>
  </PlotContainer>

  <div class="bg-panel-mid border border-panel-border rounded p-4">
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <ControlGroup label="Year">
        <select
          bind:value={selectedYear}
          class="bg-panel-inset border border-panel-border rounded px-3 py-2 text-text-primary
            focus:border-phosphor-green focus:outline-none focus:ring-2 focus:ring-phosphor-green/20"
        >
          {#each years as year}
            <option value={year}>{year}</option>
          {/each}
        </select>
      </ControlGroup>
    </div>
  </div>
</div>
