<script>
  let { value = $bindable(), label = "Display", offLabel = "Probabilities", onLabel = "Scores" } = $props()
</script>

<div class="flex flex-col gap-1">
  <span class="text-xs font-medium uppercase tracking-wider text-text-secondary">{label}</span>
  <button
    onclick={() => value = !value}
    class="flex items-center gap-2 px-3 py-3 md:py-2 rounded border transition-all duration-150 min-h-[44px] md:min-h-0
      {value
        ? 'border-phosphor-green bg-phosphor-green/10 text-phosphor-green'
        : 'border-panel-border text-text-secondary hover:border-text-secondary'}"
  >
    <span class="w-8 h-5 rounded-full relative transition-colors duration-150
      {value ? 'bg-phosphor-green/30' : 'bg-panel-inset'}">
      <span class="absolute top-0.5 w-4 h-4 rounded-full transition-all duration-150
        {value ? 'left-3.5 bg-phosphor-green' : 'left-0.5 bg-text-dim'}"></span>
    </span>
    <span class="text-sm">{value ? onLabel : offLabel}</span>
  </button>
</div>
