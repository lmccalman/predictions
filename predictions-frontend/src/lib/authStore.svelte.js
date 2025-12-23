// Authentication store with salted hash verification
// Uses Web Crypto API for secure password hashing (PBKDF2)

// IMPORTANT: Replace this hash with your own!
// Generate a new hash by opening generate-password-hash.html in a browser
// Then copy the output here.
const PASSWORD_HASH = {
  salt: 'e1b7193c821c6ff3fbc6595331fa5df5',
  hash: 'd06c75f6c8d24dce4ea6816773a6784151f9c582282da172c91fc96d405675da',
  iterations: 100000,
}

// Password stored in memory only (not localStorage) for data decryption
let storedPassword = null

// Use object pattern for exportable reactive state (Svelte 5 requirement)
// Always start unauthenticated - password required to decrypt data
export const auth = $state({ authenticated: false })

/**
 * Get the stored password for decryption.
 * Returns null if not authenticated or password not available.
 */
export function getPassword() {
  return storedPassword
}

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
    storedPassword = password
    auth.authenticated = true
  }

  return valid
}

// Log out (clear auth state)
export function logout() {
  storedPassword = null
  auth.authenticated = false
}
