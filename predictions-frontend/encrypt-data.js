#!/usr/bin/env node
/**
 * Encrypts the game data Arrow file using AES-GCM with a password-derived key.
 *
 * Usage: node encrypt-data.js <password> [input] [output]
 *
 * File format:
 *   - Bytes 0-15: Salt (16 bytes, random)
 *   - Bytes 16-27: IV (12 bytes, random)
 *   - Bytes 28+: AES-GCM encrypted data (includes 16-byte auth tag)
 */

import { readFile, writeFile } from 'node:fs/promises'
import { webcrypto } from 'node:crypto'

const ITERATIONS = 100000
const SALT_LENGTH = 16
const IV_LENGTH = 12

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

async function encrypt(password, inputPath, outputPath) {
  // Read the input file
  const data = await readFile(inputPath)
  console.log(`Read ${data.length} bytes from ${inputPath}`)

  // Generate random salt and IV
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
  console.log('Encryption complete!')
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
  process.exit(1)
}

const password = args[0]
const inputPath = args[1] || 'public/game_data.arrow'
const outputPath = args[2] || 'public/game_data.encrypted'

encrypt(password, inputPath, outputPath).catch(err => {
  console.error('Encryption failed:', err.message)
  process.exit(1)
})
