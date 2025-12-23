import * as aq from 'arquero'
import { decrypt } from '../utils/crypto.js'

// Player configuration
export const players = ['Andrew', 'Bruce', 'Christine', 'David', 'Eileen', 'Gael', 'Iain', 'Jac', 'James', 'Kate', 'Lachy', 'Pete', 'Rohan']
export const playerColors = ['#4ade80', '#fbbf24', '#22d3ee', '#f87171', '#60a5fa', '#a78bfa', '#fb923c', '#e879f9', '#4ade80', '#fbbf24', '#22d3ee', '#f87171', '#60a5fa']

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
