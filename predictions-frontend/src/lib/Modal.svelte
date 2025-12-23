<script>
  let { open = false, onClose, children } = $props()

  function handleBackdropClick(e) {
    if (e.target === e.currentTarget) {
      onClose?.()
    }
  }

  function handleKeydown(e) {
    if (e.key === 'Escape') {
      onClose?.()
    }
  }
</script>

<svelte:window onkeydown={handleKeydown} />

{#if open}
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4"
    role="dialog"
    aria-modal="true"
    onclick={handleBackdropClick}
  >
    <div class="bg-panel-raised border border-panel-border rounded-lg shadow-xl max-w-lg w-full max-h-[90vh] overflow-hidden flex flex-col">
      <div class="flex justify-end p-2 border-b border-panel-border">
        <button
          class="text-text-secondary hover:text-text-primary p-1 rounded hover:bg-panel-mid transition-colors"
          onclick={onClose}
          aria-label="Close"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <div class="overflow-y-auto flex-1">
        {@render children()}
      </div>
    </div>
  </div>
{/if}
