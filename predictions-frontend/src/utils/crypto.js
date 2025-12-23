/**
 * Client-side decryption utilities using Web Crypto API.
 *
 * Expected encrypted file format:
 *   - Bytes 0-15: Salt (16 bytes)
 *   - Bytes 16-27: IV (12 bytes)
 *   - Bytes 28+: AES-GCM encrypted data (includes auth tag)
 */

const ITERATIONS = 100000
const SALT_LENGTH = 16
const IV_LENGTH = 12

/**
 * Derive an AES-GCM key from a password and salt using PBKDF2.
 */
async function deriveKey(password, salt) {
  const encoder = new TextEncoder()
  const keyMaterial = await crypto.subtle.importKey(
    'raw',
    encoder.encode(password),
    'PBKDF2',
    false,
    ['deriveKey']
  )

  return crypto.subtle.deriveKey(
    {
      name: 'PBKDF2',
      salt,
      iterations: ITERATIONS,
      hash: 'SHA-256',
    },
    keyMaterial,
    { name: 'AES-GCM', length: 256 },
    false,
    ['decrypt']
  )
}

/**
 * Decrypt an encrypted ArrayBuffer using the provided password.
 * Returns the decrypted data as an ArrayBuffer.
 * Throws an error if decryption fails (wrong password or corrupted data).
 */
export async function decrypt(password, encryptedBuffer) {
  const data = new Uint8Array(encryptedBuffer)

  // Extract salt, IV, and encrypted content
  const salt = data.slice(0, SALT_LENGTH)
  const iv = data.slice(SALT_LENGTH, SALT_LENGTH + IV_LENGTH)
  const encrypted = data.slice(SALT_LENGTH + IV_LENGTH)

  // Derive the decryption key
  const key = await deriveKey(password, salt)

  // Decrypt the data (will throw if password is wrong due to AES-GCM auth)
  const decrypted = await crypto.subtle.decrypt(
    { name: 'AES-GCM', iv },
    key,
    encrypted
  )

  return decrypted
}
