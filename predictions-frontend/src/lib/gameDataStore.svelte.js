import * as aq from 'arquero'
import { decrypt } from '../utils/crypto.js'

// Player configuration - all players across all years (sorted alphabetically)
// Players: Andrew, Bruce, Christine, Claude (2026+), David, Eileen, Gael, Iain, Jac,
//          James F (2026+), James M (was "James"), Kate, Lachy, Leslie (2026+), Pete (2022-2024), Rohan
export const players = [
  'Andrew', 'Bruce', 'Christine', 'Claude', 'David', 'Eileen',
  'Gael', 'Iain', 'Jac', 'James F', 'James M', 'Kate', 'Lachy',
  'Leslie', 'Pete', 'Rohan'
]
export const playerColors = [
  '#4ade80', // Andrew - green
  '#fbbf24', // Bruce - amber
  '#22d3ee', // Christine - cyan
  '#c084fc', // Claude - purple
  '#f87171', // David - red
  '#60a5fa', // Eileen - blue
  '#a78bfa', // Gael - violet
  '#fb923c', // Iain - orange
  '#e879f9', // Jac - fuchsia
  '#38bdf8', // James F - sky
  '#2dd4bf', // James M - teal
  '#facc15', // Kate - yellow
  '#818cf8', // Lachy - indigo
  '#34d399', // Leslie - emerald
  '#94a3b8', // Pete - slate (historical only)
  '#fb7185', // Rohan - rose
]

// Global data - populated when loadData() completes
export let gameData = null
export let years = []

// Promise that resolves when data is loaded
let dataReadyResolve = null
let dataReadyReject = null
export let dataReady = new Promise((resolve, reject) => {
  dataReadyResolve = resolve
  dataReadyReject = reject
})

/**
 * Load and decrypt the game data.
 * Call this after successful password verification.
 * @param {string} password - The password to decrypt the data
 * @returns {Promise<void>} - Resolves when data is loaded
 */
export async function loadData(password) {
  try {
    const response = await fetch(`${import.meta.env.BASE_URL}game_data.encrypted`)
    if (!response.ok) {
      throw new Error(`Failed to fetch data: ${response.statusText}`)
    }

    const encryptedBuffer = await response.arrayBuffer()
    const decryptedBuffer = await decrypt(password, encryptedBuffer)

    gameData = aq.fromArrow(decryptedBuffer)
    const yearArray = gameData.rollup({ years: aq.op.array_agg_distinct('year') }).get('years', 0)
    years = [...yearArray].sort((a, b) => b - a)

    dataReadyResolve(gameData)
    return gameData
  } catch (err) {
    dataReadyReject(err)
    throw err
  }
}
