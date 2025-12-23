<script>
  let { title = '', children } = $props()
</script>

<div class="bg-panel-inset border border-panel-border rounded p-4 shadow-inset-panel relative">
  {#if title}
    <h2 class="text-sm font-semibold uppercase tracking-wider text-text-secondary mb-4">{title}</h2>
  {/if}
  {@render children()}
</div>
