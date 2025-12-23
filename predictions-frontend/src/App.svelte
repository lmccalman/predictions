<script>
  import TabBar from './lib/TabBar.svelte'
  import ScoresOverTime from './views/ScoresOverTime.svelte'
  import RawData from './views/RawData.svelte'
  import Calibration from './views/Calibration.svelte'
  import ConfidenceAnalysis from './views/ConfidenceAnalysis.svelte'
  import PasswordGate from './lib/PasswordGate.svelte'
  import { auth } from './lib/authStore.svelte.js'

  const tabs = [
    { label: 'Raw Data', component: RawData },
    { label: 'Scores', component: ScoresOverTime },
    { label: 'Calibration', component: Calibration },
    { label: 'Confidence', component: ConfidenceAnalysis },
  ]

  let activeTab = $state(0)
</script>

{#if auth.authenticated}
  <div class="flex flex-col md:flex-row min-h-screen bg-panel-dark">
    <TabBar {tabs} {activeTab} onTabChange={(i) => activeTab = i} />

    <main class="flex-1 p-3 md:p-6 overflow-auto">
      {#key activeTab}
        {@const ActiveComponent = tabs[activeTab].component}
        <ActiveComponent />
      {/key}
    </main>
  </div>
{:else}
  <PasswordGate />
{/if}
