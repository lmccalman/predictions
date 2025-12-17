<script>
  import TabBar from './lib/TabBar.svelte'
  import ScoresOverTime from './views/ScoresOverTime.svelte'
  import CategoryBreakdown from './views/CategoryBreakdown.svelte'
  import PlayerComparison from './views/PlayerComparison.svelte'
  import ConfidenceCalibration from './views/ConfidenceCalibration.svelte'
  import OwnVsOthers from './views/OwnVsOthers.svelte'

  const tabs = [
    { label: 'Scores', component: ScoresOverTime },
    { label: 'Categories', component: CategoryBreakdown },
    { label: 'Players', component: PlayerComparison },
    { label: 'Calibration', component: ConfidenceCalibration },
    { label: 'Own vs Others', component: OwnVsOthers },
  ]

  let activeTab = $state(0)
</script>

<div class="flex min-h-screen bg-panel-dark">
  <TabBar {tabs} {activeTab} onTabChange={(i) => activeTab = i} />

  <main class="flex-1 p-6 overflow-auto">
    {#key activeTab}
      {@const ActiveComponent = tabs[activeTab].component}
      <ActiveComponent />
    {/key}
  </main>
</div>
