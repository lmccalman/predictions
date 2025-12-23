<script>
  import ControlGroup from "./ControlGroup.svelte"
  import { gameData, years, players, playerColors } from './gameDataStore.svelte.js'

  let {
    selectedYear = $bindable(),
    selectedCategory = $bindable(),
    selectedProposer = $bindable(),
    selectedPlayers = $bindable(),
    extraControls
  } = $props()

  const categories = $derived.by(() => {
    if (!gameData) return []
    return [...new Set(gameData.array('category'))].filter(c => c).sort()
  })

  const proposers = $derived.by(() => {
    if (!gameData) return []
    return [...new Set(gameData.array('proposer'))].filter(p => p).sort()
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
</script>

<div class="bg-panel-mid border border-panel-border rounded p-4">
  <div class="flex flex-col gap-4">
    <div class="flex flex-wrap gap-4 items-end">
      <ControlGroup label="Year">
        <select
          bind:value={selectedYear}
          class="bg-panel-inset border border-panel-border rounded px-3 py-3 md:py-2 text-text-primary min-h-[44px] md:min-h-0
            focus:border-phosphor-green focus:outline-none focus:ring-2 focus:ring-phosphor-green/20"
        >
          <option value={null}>All</option>
          {#each years as year}
            <option value={year}>{year}</option>
          {/each}
        </select>
      </ControlGroup>

      <ControlGroup label="Category">
        <select
          bind:value={selectedCategory}
          class="bg-panel-inset border border-panel-border rounded px-3 py-3 md:py-2 text-text-primary min-h-[44px] md:min-h-0
            focus:border-phosphor-green focus:outline-none focus:ring-2 focus:ring-phosphor-green/20"
        >
          <option value={null}>All</option>
          {#each categories as category}
            <option value={category}>{category}</option>
          {/each}
        </select>
      </ControlGroup>

      <ControlGroup label="Proposer">
        <select
          bind:value={selectedProposer}
          class="bg-panel-inset border border-panel-border rounded px-3 py-3 md:py-2 text-text-primary min-h-[44px] md:min-h-0
            focus:border-phosphor-green focus:outline-none focus:ring-2 focus:ring-phosphor-green/20"
        >
          <option value={null}>All</option>
          {#each proposers as proposer}
            <option value={proposer}>{proposer}</option>
          {/each}
        </select>
      </ControlGroup>

      {#if extraControls}
        {@render extraControls()}
      {/if}
    </div>

    <ControlGroup label="Players">
      <div class="flex flex-col gap-2">
        <div class="flex gap-2">
          <button
            onclick={selectAllPlayers}
            class="px-3 py-2 md:px-2 md:py-1 text-xs rounded border border-panel-border text-text-secondary
              hover:border-text-secondary hover:text-text-primary transition-all duration-150 min-h-[36px] md:min-h-0"
          >
            Select All
          </button>
          <button
            onclick={clearAllPlayers}
            class="px-3 py-2 md:px-2 md:py-1 text-xs rounded border border-panel-border text-text-secondary
              hover:border-text-secondary hover:text-text-primary transition-all duration-150 min-h-[36px] md:min-h-0"
          >
            Clear All
          </button>
        </div>
        <div class="flex flex-wrap gap-2">
          {#each players as player, i}
            <button
              onclick={() => togglePlayer(player)}
              class="px-3 py-2.5 md:py-1.5 text-sm rounded border transition-all duration-150 min-h-[44px] md:min-h-0
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
</div>
