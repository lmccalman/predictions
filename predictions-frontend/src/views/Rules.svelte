<script>
  import { marked } from 'marked'
  import rulesMarkdown from '../../../RULES.md?raw'

  const htmlContent = marked(rulesMarkdown)
</script>

<div class="flex flex-col gap-4">
  <h2 class="text-xl font-semibold text-text-primary">Rules</h2>

  <div class="bg-panel-inset border border-panel-border rounded p-4 md:p-6 shadow-inset-panel">
    <article class="prose">
      {@html htmlContent}
    </article>
  </div>
</div>

<style>
  .prose :global(h1) {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--color-text-primary);
    margin-top: 0;
    margin-bottom: 1rem;
  }

  .prose :global(h2) {
    font-size: 1.35rem;
    font-weight: 600;
    color: var(--color-text-primary);
    margin-top: 2rem;
    margin-bottom: 0.75rem;
    border-bottom: 1px solid var(--color-panel-border);
    padding-bottom: 0.5rem;
  }

  .prose :global(h3) {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--color-text-primary);
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
  }

  .prose :global(h4) {
    font-size: 1rem;
    font-weight: 600;
    color: var(--color-text-secondary);
    margin-top: 1.25rem;
    margin-bottom: 0.5rem;
  }

  .prose :global(p) {
    color: var(--color-text-secondary);
    line-height: 1.7;
    margin-bottom: 1rem;
  }

  .prose :global(ul) {
    list-style-type: disc;
    padding-left: 1.5rem;
    margin-bottom: 1rem;
    color: var(--color-text-secondary);
  }

  .prose :global(ol) {
    list-style-type: decimal;
    padding-left: 1.5rem;
    margin-bottom: 1rem;
    color: var(--color-text-secondary);
  }

  .prose :global(li) {
    margin-bottom: 0.5rem;
    line-height: 1.6;
  }

  .prose :global(li ul),
  .prose :global(li ol) {
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .prose :global(strong) {
    font-weight: 600;
    color: var(--color-text-primary);
  }

  .prose :global(em) {
    font-style: italic;
    color: var(--color-text-primary);
  }

  .prose :global(code) {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.9em;
    background-color: var(--color-panel-mid);
    padding: 0.15rem 0.4rem;
    border-radius: 0.25rem;
    color: var(--color-phosphor-green);
  }

  .prose :global(pre) {
    background-color: var(--color-panel-mid);
    padding: 1rem;
    border-radius: 0.375rem;
    overflow-x: auto;
    margin-bottom: 1rem;
  }

  .prose :global(pre code) {
    background-color: transparent;
    padding: 0;
  }

  .prose :global(blockquote) {
    border-left: 3px solid var(--color-phosphor-green);
    padding-left: 1rem;
    margin-left: 0;
    margin-bottom: 1rem;
    color: var(--color-text-dim);
    font-style: italic;
  }

  .prose :global(hr) {
    border: none;
    border-top: 1px solid var(--color-panel-border);
    margin: 2rem 0;
  }
</style>
