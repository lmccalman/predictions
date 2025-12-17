# Frontend Design Specification

A design language inspired by analogue synthesizers and CRT terminals for the Family Predictions game interface.

## Design Philosophy

The aesthetic draws from:
- **Analogue synthesizers**: Panel layouts, knob/slider controls, backlit labels, functional typography
- **CRT terminals**: Phosphor glow effects, scan lines (subtle), monospace data, slight warmth

Keep it **functional first** - the retro touches should enhance readability and create visual hierarchy, not distract from the data.

---

## Colour Palette

### Background Colours

| Name | Hex | Usage |
|------|-----|-------|
| `panel-dark` | `#1a1a1e` | Main application background |
| `panel-mid` | `#252529` | Card/section backgrounds |
| `panel-raised` | `#2d2d32` | Elevated elements, hover states |
| `panel-inset` | `#141416` | Inset areas, input backgrounds |

### Text Colours

| Name | Hex | Usage |
|------|-----|-------|
| `text-primary` | `#e8e6e3` | Primary text, headings |
| `text-secondary` | `#9a9a9a` | Labels, secondary information |
| `text-dim` | `#5a5a5a` | Disabled states, subtle hints |

### Accent Colours (Phosphor-inspired)

| Name | Hex | Usage |
|------|-----|-------|
| `phosphor-green` | `#4ade80` | Primary accent, positive scores, active states |
| `phosphor-amber` | `#fbbf24` | Warnings, neutral scores, highlights |
| `phosphor-red` | `#f87171` | Errors, negative scores |
| `phosphor-cyan` | `#22d3ee` | Links, interactive elements |
| `phosphor-blue` | `#60a5fa` | Charts secondary, information |

### Glow Effects

For CRT-style glow, use box-shadow with accent colours at low opacity:
```css
/* Subtle phosphor glow */
box-shadow: 0 0 8px rgba(74, 222, 128, 0.3);

/* Stronger active glow */
box-shadow: 0 0 12px rgba(74, 222, 128, 0.5), 0 0 24px rgba(74, 222, 128, 0.2);
```

---

## Typography

### Font Stack

```css
/* Primary - UI elements, labels */
font-family: 'IBM Plex Sans', system-ui, sans-serif;

/* Monospace - data values, scores, code */
font-family: 'IBM Plex Mono', 'Consolas', monospace;
```

Load from Google Fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
```

### Type Scale

| Name | Size | Weight | Usage |
|------|------|--------|-------|
| `heading-lg` | 1.5rem (24px) | 600 | Page/tab titles |
| `heading-md` | 1.125rem (18px) | 600 | Section headings |
| `heading-sm` | 0.875rem (14px) | 600 | Card titles, labels |
| `body` | 0.875rem (14px) | 400 | General text |
| `body-sm` | 0.75rem (12px) | 400 | Captions, hints |
| `data` | 0.875rem (14px) | 500 | Data values (monospace) |
| `data-lg` | 1.25rem (20px) | 600 | Featured numbers (monospace) |

### Text Styling

- **Letter-spacing**: Slightly expanded for labels (`0.02em`) to mimic panel engraving
- **Text-transform**: Uppercase for tab labels and control labels only
- **Line-height**: 1.5 for body text, 1.2 for headings

---

## Layout Structure

### Overall Layout

```
+------------------+----------------------------------------+
|                  |                                        |
|   VERTICAL       |         MAIN CONTENT AREA              |
|   TAB BAR        |                                        |
|                  |   +--------------------------------+   |
|   [Tab 1]        |   |                                |   |
|   [Tab 2]        |   |         PLOT AREA              |   |
|   [Tab 3]        |   |                                |   |
|   [Tab 4]        |   |                                |   |
|                  |   +--------------------------------+   |
|                  |                                        |
|                  |   +--------------------------------+   |
|                  |   |       CONTROLS PANEL           |   |
|                  |   +--------------------------------+   |
|                  |                                        |
+------------------+----------------------------------------+
```

### Dimensions

| Element | Value |
|---------|-------|
| Tab bar width | 200px |
| Content max-width | None (fluid) |
| Content padding | 24px |
| Plot area min-height | 400px |
| Controls panel height | Auto (content-driven) |

### Spacing Scale

Use consistent spacing increments:
- `4px` - Tight (within components)
- `8px` - Compact (related elements)
- `12px` - Default (component internal padding)
- `16px` - Comfortable (between components)
- `24px` - Spacious (section separation)
- `32px` - Generous (major sections)

---

## Components

### Vertical Tab Bar

```
Background: panel-mid
Width: 200px
Border-right: 1px solid #3a3a3f
```

**Tab Item (inactive)**:
```
Padding: 12px 16px
Color: text-secondary
Background: transparent
Border-left: 3px solid transparent
Font: heading-sm, uppercase, letter-spacing: 0.05em
```

**Tab Item (active)**:
```
Color: phosphor-green
Background: panel-dark
Border-left: 3px solid phosphor-green
Box-shadow: inset 0 0 20px rgba(74, 222, 128, 0.05)
```

**Tab Item (hover)**:
```
Color: text-primary
Background: panel-raised
```

### Plot Container

The main visualisation area:

```
Background: panel-inset
Border: 1px solid #3a3a3f
Border-radius: 4px
Padding: 16px
Box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3)
```

Apply subtle scan-line effect (optional, CSS only):
```css
.plot-container::after {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0, 0, 0, 0.03) 2px,
    rgba(0, 0, 0, 0.03) 4px
  );
  pointer-events: none;
}
```

### Controls Panel

Below the plot, containing interactive controls:

```
Background: panel-mid
Border: 1px solid #3a3a3f
Border-radius: 4px
Padding: 16px
Margin-top: 16px
```

Layout controls in a flexible grid:
```css
display: grid;
grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
gap: 16px;
```

### Control Group

A labelled control (dropdown, slider, toggle, etc.):

```
+---------------------------+
|  PLAYER FILTER            |  <- Label
|  [================v]      |  <- Control
+---------------------------+
```

**Label**:
```
Font: body-sm, uppercase
Color: text-secondary
Letter-spacing: 0.05em
Margin-bottom: 6px
```

### Select/Dropdown

```
Background: panel-inset
Border: 1px solid #3a3a3f
Border-radius: 3px
Padding: 8px 12px
Color: text-primary
Font: body (IBM Plex Sans)

Focus:
  Border-color: phosphor-green
  Box-shadow: 0 0 0 2px rgba(74, 222, 128, 0.2)
```

### Toggle/Checkbox

Styled as synth-style LED indicators:

```
OFF:
  Background: panel-inset
  Border: 1px solid #3a3a3f

ON:
  Background: phosphor-green
  Border: 1px solid phosphor-green
  Box-shadow: 0 0 8px rgba(74, 222, 128, 0.5)
```

### Buttons

**Primary Button**:
```
Background: transparent
Border: 1px solid phosphor-green
Color: phosphor-green
Padding: 8px 16px
Border-radius: 3px
Font: heading-sm, uppercase
Letter-spacing: 0.03em

Hover:
  Background: rgba(74, 222, 128, 0.1)
  Box-shadow: 0 0 8px rgba(74, 222, 128, 0.3)
```

**Secondary Button**:
```
Border-color: #5a5a5a
Color: text-secondary

Hover:
  Border-color: text-primary
  Color: text-primary
```

### Data Cards

For displaying statistics or summaries:

```
Background: panel-mid
Border: 1px solid #3a3a3f
Border-radius: 4px
Padding: 16px

Title: heading-sm, text-secondary, uppercase
Value: data-lg, phosphor-green (or appropriate accent)
```

### Tooltips

```
Background: panel-raised
Border: 1px solid #4a4a4f
Border-radius: 3px
Padding: 8px 12px
Color: text-primary
Font: body-sm
Box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4)
```

---

## Chart Styling (Observable Plot)

### Colour Sequences

**Categorical (players)**:
```javascript
const playerColors = [
  '#4ade80', // phosphor-green
  '#fbbf24', // phosphor-amber
  '#22d3ee', // phosphor-cyan
  '#f87171', // phosphor-red
  '#60a5fa', // phosphor-blue
  '#a78bfa', // violet
  '#fb923c', // orange
  '#e879f9', // pink
];
```

**Sequential (scores, performance)**:
```javascript
// Green-based for positive metrics
const positiveScale = ['#064e3b', '#059669', '#34d399', '#6ee7b7'];

// Red-based for negative metrics
const negativeScale = ['#7f1d1d', '#dc2626', '#f87171', '#fca5a5'];
```

### Axes and Gridlines

```javascript
Plot.plot({
  style: {
    background: 'transparent',
    color: '#9a9a9a',
    fontFamily: 'IBM Plex Sans',
    fontSize: 12,
  },
  x: {
    line: true,
    tickColor: '#3a3a3f',
    labelColor: '#9a9a9a',
  },
  y: {
    grid: true,
    gridColor: '#2a2a2f',
    tickColor: '#3a3a3f',
  },
  marks: [
    // ...
  ]
})
```

### Plot Marks

- **Lines**: 2px stroke, accent colours
- **Points**: 6px radius, filled with stroke matching line
- **Bars**: 1px gap between, accent fill with slight transparency (0.8)
- **Area**: Fill with 0.3 opacity of accent colour

---

## Tailwind Configuration

Add to `tailwind.config.js`:

```javascript
export default {
  theme: {
    extend: {
      colors: {
        panel: {
          dark: '#1a1a1e',
          mid: '#252529',
          raised: '#2d2d32',
          inset: '#141416',
        },
        phosphor: {
          green: '#4ade80',
          amber: '#fbbf24',
          red: '#f87171',
          cyan: '#22d3ee',
          blue: '#60a5fa',
        },
      },
      fontFamily: {
        sans: ['IBM Plex Sans', 'system-ui', 'sans-serif'],
        mono: ['IBM Plex Mono', 'Consolas', 'monospace'],
      },
      boxShadow: {
        'glow-green': '0 0 8px rgba(74, 222, 128, 0.3)',
        'glow-green-lg': '0 0 12px rgba(74, 222, 128, 0.5), 0 0 24px rgba(74, 222, 128, 0.2)',
        'inset-panel': 'inset 0 2px 4px rgba(0, 0, 0, 0.3)',
      },
      borderColor: {
        panel: '#3a3a3f',
      },
    },
  },
}
```

---

## Responsive Behaviour

### Breakpoints

| Name | Width | Behaviour |
|------|-------|-----------|
| Mobile | < 768px | Tabs collapse to horizontal top bar, controls stack vertically |
| Tablet | 768px - 1024px | Narrower tab bar (160px), smaller padding |
| Desktop | > 1024px | Full layout as specified |

### Mobile Adaptations

- Tab bar becomes horizontal strip at top
- Tab labels may truncate or use icons
- Controls panel becomes scrollable if needed
- Plot maintains aspect ratio but scales down

---

## Animation Guidelines

Keep animations **subtle and functional**:

- **Duration**: 150ms for micro-interactions, 250ms for transitions
- **Easing**: `ease-out` for entering, `ease-in` for exiting
- **Properties to animate**: opacity, transform, box-shadow, border-color
- **Avoid**: Large movements, bouncy effects, anything distracting

Example tab transition:
```css
.tab-item {
  transition: color 150ms ease-out,
              background-color 150ms ease-out,
              border-color 150ms ease-out;
}
```

---

## Accessibility

- Maintain minimum contrast ratio of 4.5:1 for text
- All interactive elements must have visible focus states
- Glow effects are decorative; don't rely on them for state indication
- Provide text alternatives for any icon-only controls
- Ensure keyboard navigation works for all controls

---

## Implementation Notes

1. **Start with the layout shell** - Get the tab bar and content area structure working first
2. **Apply colours and typography globally** - Set up CSS custom properties or Tailwind config early
3. **Build components incrementally** - Each control type as a reusable Svelte component
4. **Add glow effects last** - They're polish; get functionality working first
5. **Test with real data** - Ensure colours work with actual chart data ranges
