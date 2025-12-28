/**
 * Calculate score for a single prediction using standardized log probability.
 * Formula: log(probability assigned to actual outcome) - log(0.5)
 *
 * @param {number|null|undefined} prediction - Probability assigned (0 to 1)
 * @param {boolean|null|undefined} outcome - Actual outcome (true/false)
 * @returns {number|null} - Score, or null if inputs are invalid
 */
export function calculateScore(prediction, outcome) {
  if (prediction === null || prediction === undefined || isNaN(prediction)) return null
  if (outcome === null || outcome === undefined) return null

  // Probability assigned to the actual outcome
  const pAssigned = outcome ? prediction : 1 - prediction
  // Score = log(p_assigned) - log(0.5)
  return Math.log(pAssigned) - Math.log(0.5)
}

/**
 * Calculate total score for a player across multiple statements.
 *
 * @param {Array} rows - Array of statement objects
 * @param {string} player - Player name (column key in rows)
 * @returns {number} - Total score (sum of individual scores, ignoring nulls)
 */
export function calculateTotalScore(rows, player) {
  let total = 0
  for (const row of rows) {
    const score = calculateScore(row[player], row.outcome)
    if (score !== null && isFinite(score)) {
      total += score
    }
  }
  return total
}

/**
 * Format a score for display.
 *
 * @param {number|null} score - Score value
 * @returns {string} - Formatted score string with sign
 */
export function formatScore(score) {
  if (score === null || score === undefined) return '-'
  if (score === -Infinity) return '-∞'
  if (score === Infinity) return '+∞'
  const sign = score >= 0 ? '+' : ''
  return sign + score.toFixed(2)
}

/**
 * Format a probability for display as decimal.
 *
 * @param {number|null|undefined} value - Probability value (0 to 1)
 * @returns {string} - Formatted decimal string
 */
export function formatProbability(value) {
  if (value === null || value === undefined || isNaN(value)) return '-'
  return value.toFixed(2)
}

/**
 * Calculate win/loss score for a single prediction.
 * Awards 1 point if prediction is on the correct side of 0.5.
 * - outcome=false: win if prediction < 0.5
 * - outcome=true: win if prediction > 0.5
 * - prediction exactly 0.5 never wins
 *
 * @param {number|null|undefined} prediction - Probability assigned (0 to 1)
 * @param {boolean|null|undefined} outcome - Actual outcome (true/false)
 * @returns {number|null} - 1 for win, 0 for loss, null if inputs invalid
 */
export function calculateWinLoss(prediction, outcome) {
  if (prediction === null || prediction === undefined || isNaN(prediction)) return null
  if (outcome === null || outcome === undefined) return null

  if (prediction === 0.5) return 0

  if (outcome) {
    return prediction > 0.5 ? 1 : 0
  } else {
    return prediction < 0.5 ? 1 : 0
  }
}
