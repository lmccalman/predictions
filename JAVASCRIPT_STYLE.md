# JavaScript/Svelte Style Guide

This document defines the JavaScript and Svelte coding standards for this project, building on the global preferences and project-specific patterns.

## Core Principles

- **Clarity over cleverness**: Code should be self-documenting and immediately understandable
- **Functional over object-oriented**: Prefer functions and immutable data patterns
- **YAGNI (You Ain't Gonna Need It)**: Implement only what's needed now
- **DRY (Don't Repeat Yourself)**: Reuse existing code where possible

## Technology Stack

- **Vite**: Build tool and dev server
- **Svelte 5**: UI framework (using runes and modern syntax)
- **Observable Plot**: Data visualisation library
- **Tailwind CSS**: Styling (v4)

## Svelte Components

### Component Structure

Follow Svelte 5 conventions:
- Use `<script>` for component logic
- Use runes for reactivity (`$state`, `$derived`, `$effect`)
- Keep components focused and small
- Extract reusable logic to composable functions

```svelte
<script>
  import * as Plot from "@observablehq/plot";
  import { onMount } from "svelte";

  let plotContainer;

  const data = [
    { year: 2020, value: 45 },
    { year: 2021, value: 67 },
  ];

  onMount(() => {
    const plot = Plot.plot({
      marks: [Plot.barY(data, { x: "year", y: "value" })]
    });
    plotContainer.appendChild(plot);
    return () => plot.remove();
  });
</script>

<div bind:this={plotContainer}></div>
```

### Reactivity

Use Svelte 5 runes for state management:
- `let` for simple reactive state (Svelte 5 makes this reactive)
- `$state` for explicit reactive state
- `$derived` for computed values
- `$effect` for side effects

## Styling

### Tailwind First

**IMPORTANT**: Use Tailwind classes rather than CSS properties whenever possible.

```svelte
<!-- Good: Tailwind classes -->
<div class="my-8 mx-auto flex justify-center items-center">
  <div class="bg-white rounded-lg p-4 shadow-md">
    Content here
  </div>
</div>

<!-- Avoid: Inline styles or <style> blocks for standard styling -->
<div style="margin: 2rem auto;">
  <div style="background: white; padding: 1rem;">
    Content here
  </div>
</div>
```

Only use `<style>` blocks for:
- Complex animations
- Component-specific styling that can't be expressed with Tailwind
- Dynamic styles that depend on JavaScript values

### Australian Spelling

Use Australian spelling in:
- Comments
- User-facing text
- Variable names where appropriate

Examples: visualisation, colour, centre, behaviour

## JavaScript Patterns

### Functional Approach

Prefer functional patterns:
- Use `map`, `filter`, `reduce` over imperative loops
- Avoid mutation where possible
- Use destructuring for clarity

```javascript
// Good: functional approach
const activeYears = predictions
  .filter(p => p.active)
  .map(p => p.year);

// Avoid: imperative approach
const activeYears = [];
for (const p of predictions) {
  if (p.active) {
    activeYears.push(p.year);
  }
}
```

### Variable Naming

- Use `camelCase` for variables and functions
- Use `PascalCase` for component names
- Use descriptive names that indicate purpose
- Prefer `const` over `let` where possible

```javascript
// Good
const playerScores = calculateScores(predictions);
const hasActiveGames = games.some(g => g.active);

// Avoid
const ps = calc(predictions);
let x = games.some(g => g.active);
```

## Observable Plot

Use Observable Plot for all data visualisations:
- Declarative mark-based API
- Prefer built-in marks over custom rendering
- Use `tip: true` for interactivity

```javascript
const plot = Plot.plot({
  title: "Performance Over Time",
  width: 640,
  height: 400,
  grid: true,
  marks: [
    Plot.barY(data, {
      x: "year",
      y: "score",
      fill: "steelblue",
      tip: true
    }),
    Plot.ruleY([0])
  ],
  x: { label: "Year" },
  y: { label: "Score" }
});
```

## Code Organisation

### Imports

Group imports in order:
1. External libraries
2. Svelte core (`svelte`, `svelte/motion`, etc.)
3. Local components
4. Local utilities/helpers

```javascript
import * as Plot from "@observablehq/plot";
import { onMount } from "svelte";
import PlayerCard from "./lib/PlayerCard.svelte";
import { calculateScore } from "./utils/scoring.js";
```

### File Structure

- Components in `src/lib/`
- Utilities in `src/utils/`
- Shared data/config in `src/data/`
- Keep related files together

## Comments

- Write self-documenting code; use comments sparingly
- Only comment for non-obvious logic or business rules
- Prefer extracting complex logic to well-named functions

```javascript
// Good: clear function name, no comment needed
const isValidProbability = (p) => p >= 0 && p <= 1;

// Avoid: unnecessary comment for obvious code
// Check if probability is valid
const check = (p) => p >= 0 && p <= 1;
```

## Development Commands

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
```

## Modern JavaScript

Use modern JavaScript features:
- Arrow functions
- Template literals
- Destructuring
- Spread operator
- Optional chaining (`?.`)
- Nullish coalescing (`??`)

```javascript
// Modern JavaScript patterns
const { year, score } = prediction;
const title = `${player.name}'s Score`;
const validScore = score ?? 0;
const category = prediction?.category?.toLowerCase();
```
