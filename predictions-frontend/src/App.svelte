<script>
  import TabBar from './lib/TabBar.svelte'
  import ScoresOverTime from './views/ScoresOverTime.svelte'
  import RawData from './views/RawData.svelte'

  const tabs = [
    { label: 'Raw Data', component: RawData },
    { label: 'Scores', component: ScoresOverTime },
  ]

  let activeTab = $state(0)
</script>

<div class="flex flex-col md:flex-row min-h-screen bg-panel-dark">
  <TabBar {tabs} {activeTab} onTabChange={(i) => activeTab = i} />

  <main class="flex-1 p-3 md:p-6 overflow-auto">
    {#key activeTab}
      {@const ActiveComponent = tabs[activeTab].component}
      <ActiveComponent />
    {/key}
  </main>
</div>
