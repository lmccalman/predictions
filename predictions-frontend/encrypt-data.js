#!/usr/bin/env node
/**
 * Encrypts the game data Arrow file and updates the password hash in authStore.
 *
 * Usage: node encrypt-data.js <password> [input] [output]
 *
 * This script:
 *   1. Generates a password hash and updates src/lib/authStore.svelte.js
 *   2. Encrypts the Arrow file using AES-GCM with a password-derived key
 *
 * Encrypted file format:
 *   - Bytes 0-15: Salt (16 bytes, random)
 *   - Bytes 16-27: IV (12 bytes, random)
 *   - Bytes 28+: AES-GCM encrypted data (includes 16-byte auth tag)
 */

import { readFile, writeFile } from 'node:fs/promises'
import { webcrypto } from 'node:crypto'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const ITERATIONS = 100000
const SALT_LENGTH = 16
const IV_LENGTH = 12

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)
const AUTH_STORE_PATH = join(__dirname, 'src/lib/authStore.svelte.js')

function bytesToHex(bytes) {
  return Array.from(bytes)
    .map(b => b.toString(16).padStart(2, '0'))
    .join('')
}

async function deriveKey(password, salt) {
  const encoder = new TextEncoder()
  const keyMaterial = await webcrypto.subtle.importKey(
    'raw',
    encoder.encode(password),
    'PBKDF2',
    false,
    ['deriveKey']
  )

  return webcrypto.subtle.deriveKey(
    {
      name: 'PBKDF2',
      salt,
      iterations: ITERATIONS,
      hash: 'SHA-256',
    },
    keyMaterial,
    { name: 'AES-GCM', length: 256 },
    false,
    ['encrypt']
  )
}

async function generatePasswordHash(password) {
  const encoder = new TextEncoder()
  const salt = webcrypto.getRandomValues(new Uint8Array(SALT_LENGTH))

  const keyMaterial = await webcrypto.subtle.importKey(
    'raw',
    encoder.encode(password),
    'PBKDF2',
    false,
    ['deriveBits']
  )

  const derivedBits = await webcrypto.subtle.deriveBits(
    {
      name: 'PBKDF2',
      salt,
      iterations: ITERATIONS,
      hash: 'SHA-256',
    },
    keyMaterial,
    256
  )

  return {
    salt: bytesToHex(salt),
    hash: bytesToHex(new Uint8Array(derivedBits)),
    iterations: ITERATIONS,
  }
}

async function updateAuthStore(passwordHash) {
  const content = await readFile(AUTH_STORE_PATH, 'utf-8')

  // Match the PASSWORD_HASH object (handles various formatting)
  const hashRegex = /const PASSWORD_HASH = \{[^}]+\}/s

  if (!hashRegex.test(content)) {
    throw new Error('Could not find PASSWORD_HASH in authStore.svelte.js')
  }

  const newHashBlock = `const PASSWORD_HASH = {
  salt: '${passwordHash.salt}',
  hash: '${passwordHash.hash}',
  iterations: ${passwordHash.iterations},
}`

  const updatedContent = content.replace(hashRegex, newHashBlock)
  await writeFile(AUTH_STORE_PATH, updatedContent)
  console.log('Updated password hash in src/lib/authStore.svelte.js')
}

async function encryptData(password, inputPath, outputPath) {
  // Read the input file
  const data = await readFile(inputPath)
  console.log(`Read ${data.length} bytes from ${inputPath}`)

  // Generate random salt and IV for encryption
  const salt = webcrypto.getRandomValues(new Uint8Array(SALT_LENGTH))
  const iv = webcrypto.getRandomValues(new Uint8Array(IV_LENGTH))

  // Derive encryption key from password
  const key = await deriveKey(password, salt)

  // Encrypt the data
  const encrypted = await webcrypto.subtle.encrypt(
    { name: 'AES-GCM', iv },
    key,
    data
  )

  // Combine salt + iv + encrypted data
  const output = new Uint8Array(SALT_LENGTH + IV_LENGTH + encrypted.byteLength)
  output.set(salt, 0)
  output.set(iv, SALT_LENGTH)
  output.set(new Uint8Array(encrypted), SALT_LENGTH + IV_LENGTH)

  // Write the output file
  await writeFile(outputPath, output)
  console.log(`Wrote ${output.length} bytes to ${outputPath}`)
}

async function main(password, inputPath, outputPath) {
  // Step 1: Generate and update password hash
  console.log('Generating password hash...')
  const passwordHash = await generatePasswordHash(password)
  await updateAuthStore(passwordHash)

  // Step 2: Encrypt the data file
  console.log('Encrypting data...')
  await encryptData(password, inputPath, outputPath)

  console.log('Done!')
}

// Parse command line arguments
const args = process.argv.slice(2)

if (args.length < 1) {
  console.error('Usage: node encrypt-data.js <password> [input] [output]')
  console.error('')
  console.error('Arguments:')
  console.error('  password  The encryption password')
  console.error('  input     Input Arrow file (default: public/game_data.arrow)')
  console.error('  output    Output encrypted file (default: public/game_data.encrypted)')
  console.error('')
  console.error('This script updates both the encrypted data file and the password')
  console.error('hash in src/lib/authStore.svelte.js')
  process.exit(1)
}

const password = args[0]
const inputPath = args[1] || 'public/game_data.arrow'
const outputPath = args[2] || 'public/game_data.encrypted'

main(password, inputPath, outputPath).catch(err => {
  console.error('Failed:', err.message)
  process.exit(1)
})
