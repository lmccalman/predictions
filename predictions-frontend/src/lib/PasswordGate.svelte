<script>
  import { verifyPassword } from './authStore.svelte.js'
  import { loadData } from './gameDataStore.svelte.js'

  let password = $state('')
  let error = $state('')
  let checking = $state(false)
  let status = $state('')

  async function handleSubmit(event) {
    event.preventDefault()
    error = ''
    checking = true
    status = 'Verifying...'

    const valid = await verifyPassword(password)

    if (!valid) {
      checking = false
      error = 'Incorrect password'
      password = ''
      status = ''
      return
    }

    // Password verified - now load and decrypt data
    status = 'Loading data...'
    try {
      await loadData(password)
    } catch (err) {
      checking = false
      error = 'Failed to decrypt data'
      password = ''
      status = ''
    }
    // If loadData succeeds, auth.authenticated is already true from verifyPassword
  }

  function handleKeydown(event) {
    if (event.key === 'Enter') {
      handleSubmit(event)
    }
  }
</script>

<div class="min-h-screen bg-panel-dark flex items-center justify-center p-4">
  <div class="bg-panel-raised border border-panel-border rounded-lg p-8 w-full max-w-sm shadow-lg">
    <h1 class="text-text-primary text-xl font-medium mb-2 text-center">
      Family Predictions
    </h1>
    <p class="text-text-secondary text-sm mb-6 text-center">
      Enter password to continue
    </p>

    <form onsubmit={handleSubmit}>
      <input
        type="password"
        bind:value={password}
        onkeydown={handleKeydown}
        placeholder="Password"
        disabled={checking}
        class="w-full px-4 py-3 bg-panel-inset border border-panel-border rounded
               text-text-primary placeholder-text-dim
               focus:outline-none focus:border-phosphor-green focus:ring-1 focus:ring-phosphor-green
               disabled:opacity-50"
      />

      {#if error}
        <p class="text-phosphor-red text-sm mt-2">{error}</p>
      {/if}

      <button
        type="submit"
        disabled={checking || !password}
        class="w-full mt-4 px-4 py-3 bg-panel-mid border border-panel-border rounded
               text-text-primary font-medium
               hover:bg-panel-raised hover:border-phosphor-green
               focus:outline-none focus:border-phosphor-green
               disabled:opacity-50 disabled:cursor-not-allowed
               transition-colors"
      >
        {checking ? status : 'Enter'}
      </button>
    </form>
  </div>
</div>
