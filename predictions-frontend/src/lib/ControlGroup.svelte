<script>
  let { label, children } = $props()
</script>

<div class="flex flex-col gap-1.5">
  <span class="text-xs font-medium uppercase tracking-wider text-text-secondary">
    {label}
  </span>
  {@render children()}
</div>
