# Predictions Frontend

Interactive web frontend for the family prediction game, built with Svelte 5 and Vite.

## Setup

```bash
npm install
```

## Development

```bash
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build
```

## Data Encryption

The game data is encrypted client-side to protect it even when hosted publicly. The Arrow data file is encrypted with AES-256-GCM using a password-derived key.

### How It Works

1. **Build time**: The Arrow file is encrypted using a password
2. **Runtime**: Users enter the password, which decrypts the data in the browser
3. **Security**: Without the correct password, the hosted `.encrypted` file is unreadable

### Setting Up a Password

1. **Generate a password hash** by opening `generate-password-hash.html` in a browser
2. Enter your chosen password and copy the output
3. Update `src/lib/authStore.svelte.js` with the generated salt and hash:

```javascript
const PASSWORD_HASH = {
  salt: 'your-generated-salt',
  hash: 'your-generated-hash',
  iterations: 100000,
}
```

### Encrypting the Data

After exporting Arrow data from the backend, encrypt it:

```bash
npm run encrypt "your-password"
```

This reads `public/game_data.arrow` and outputs `public/game_data.encrypted`.

### Full Build Workflow

```bash
# 1. Export data from backend (from repo root)
uv run python main.py

# 2. Encrypt the data (from predictions-frontend/)
cd predictions-frontend
npm run encrypt "your-password"

# 3. Build for production
npm run build
```

### Technical Details

- **Encryption**: AES-256-GCM (authenticated encryption)
- **Key derivation**: PBKDF2 with SHA-256, 100,000 iterations
- **File format**: 16-byte salt + 12-byte IV + encrypted data (includes auth tag)
- **Browser API**: Web Crypto API (native, no external dependencies)

The unencrypted `game_data.arrow` is gitignored - only the encrypted file should be committed and deployed.
