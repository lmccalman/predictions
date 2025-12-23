// Authentication store with salted hash verification
// Uses Web Crypto API for secure password hashing (PBKDF2)

// IMPORTANT: Replace this hash with your own!
// Generate a new hash by opening generate-password-hash.html in a browser
// Then copy the output here.
const PASSWORD_HASH = {
  salt: '620da25bd8e904d5835ec0ac8333690b',
  hash: 'dd1c083f9bab127b218d90a0d1e73a4edb3438ade12821e57ae47aadd4ecf5b4',
  iterations: 100000,
}

const STORAGE_KEY = 'predictions_auth'

// Check localStorage for existing auth
const storedAuth = typeof localStorage !== 'undefined'
  ? localStorage.getItem(STORAGE_KEY)
  : null

// Use object pattern for exportable reactive state (Svelte 5 requirement)
export const auth = $state({ authenticated: storedAuth === 'true' })

// Convert hex string to Uint8Array
function hexToBytes(hex) {
  const bytes = new Uint8Array(hex.length / 2)
  for (let i = 0; i < hex.length; i += 2) {
    bytes[i / 2] = parseInt(hex.substr(i, 2), 16)
  }
  return bytes
}

// Convert Uint8Array to hex string
function bytesToHex(bytes) {
  return Array.from(bytes)
    .map(b => b.toString(16).padStart(2, '0'))
    .join('')
}

// Hash a password with the stored salt using PBKDF2
async function hashPassword(password, saltHex) {
  const encoder = new TextEncoder()
  const salt = hexToBytes(saltHex)

  const keyMaterial = await crypto.subtle.importKey(
    'raw',
    encoder.encode(password),
    'PBKDF2',
    false,
    ['deriveBits']
  )

  const derivedBits = await crypto.subtle.deriveBits(
    {
      name: 'PBKDF2',
      salt: salt,
      iterations: PASSWORD_HASH.iterations,
      hash: 'SHA-256',
    },
    keyMaterial,
    256
  )

  return bytesToHex(new Uint8Array(derivedBits))
}

// Verify a password against the stored hash
export async function verifyPassword(password) {
  if (PASSWORD_HASH.salt === 'REPLACE_WITH_GENERATED_SALT') {
    console.error('Password hash not configured! Run generatePasswordHash() to create one.')
    return false
  }

  const computedHash = await hashPassword(password, PASSWORD_HASH.salt)
  const valid = computedHash === PASSWORD_HASH.hash

  if (valid) {
    auth.authenticated = true
    localStorage.setItem(STORAGE_KEY, 'true')
  }

  return valid
}

// Log out (clear auth state)
export function logout() {
  auth.authenticated = false
  localStorage.removeItem(STORAGE_KEY)
}
