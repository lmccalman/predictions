import * as aq from 'arquero'

// Player configuration
export const players = ['Andrew', 'Bruce', 'Christine', 'David', 'Eileen', 'Gael', 'Iain', 'Jac', 'James', 'Kate', 'Lachy', 'Pete', 'Rohan']
export const playerColors = ['#4ade80', '#fbbf24', '#22d3ee', '#f87171', '#60a5fa', '#a78bfa', '#fb923c', '#e879f9', '#4ade80', '#fbbf24', '#22d3ee', '#f87171', '#60a5fa']

// Global data - populated when dataReady resolves
export let gameData = null
export let years = []

// Load data immediately on module import
export const dataReady = fetch(`${import.meta.env.BASE_URL}game_data.arrow`)
  .then(response => {
    if (!response.ok) {
      throw new Error(`Failed to fetch data: ${response.statusText}`)
    }
    return response.arrayBuffer()
  })
  .then(buffer => {
    gameData = aq.fromArrow(buffer)
    const yearArray = gameData.rollup({ years: aq.op.array_agg_distinct('year') }).get('years', 0)
    years = [...yearArray].sort((a, b) => b - a)
    return gameData
  })
