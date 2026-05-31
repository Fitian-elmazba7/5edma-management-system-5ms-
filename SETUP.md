# Setup Guide - 5edma Management System

Complete setup instructions for developers and system administrators.

## Table of Contents

1. [Developer Setup](#developer-setup)
2. [Firebase Project Setup](#firebase-project-setup)
3. [Environment Configuration](#environment-configuration)
4. [Local Development](#local-development)
5. [CI/CD Setup](#cicd-setup)
6. [Production Deployment](#production-deployment)

---

## Developer Setup

### 1. System Requirements

- **Node.js 18+** — [Download](https://nodejs.org/)
- **pnpm 8+** — `npm install -g pnpm`
- **Git** — [Download](https://git-scm.com/)
- **Windows 10+** — For Electron packaging
- **Visual Studio Build Tools** — For native modules (Windows)

### 2. Clone Repository

```bash
git clone https://github.com/your-org/5edma-management-system.git
cd 5edma-management-system

# Checkout the modern stack branch
git checkout rebuild/modern-stack
```

### 3. Install Dependencies

```bash
# Install all workspace dependencies
pnpm install

# Verify installation
pnpm list

# Check Node/pnpm versions
node -v    # Should be 18.x or higher
pnpm -v    # Should be 8.x or higher
```

### 4. Setup Git Hooks (Optional)

For code quality checks before commits:

```bash
# Install husky for git hooks
pnpm add -D husky
npx husky install

# Add pre-commit hook
npx husky add .husky/pre-commit "pnpm lint"
```

---

## Firebase Project Setup

### Step 1: Create Firebase Project

**Via Firebase Console:**

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add Project"
3. **Project ID:** `fitian-el-mazba7`
4. **Project Name:** 5edma Management System
5. Enable Analytics (optional)
6. Wait for creation

**Alternatively, via CLI:**

```bash
firebase projects:create fitian-el-mazba7 \
  --display-name="5edma Management System"
```

### Step 2: Enable Services

**Authentication:**
```bash
firebase auth:upload-users users.json
```

**Firestore:**
```bash
firebase firestore:indexes:list  # Check existing indexes
```

**Hosting:**
- Required for web deployment

**Cloud Functions:**
- Required for user management

### Step 3: Install Firebase CLI

```bash
npm install -g firebase-tools

# Login to your Google account
firebase login

# Verify login
firebase projects:list
```

### Step 4: Select Project

```bash
# Set default project
firebase use --add

# Choose "fitian-el-mazba7" from the list
# Alias: default (or custom alias)
```

---

## Environment Configuration

### 1. Web App Configuration

Create `apps/web/.env.local`:

```env
# Get these from Firebase Console → Project Settings
VITE_FIREBASE_API_KEY=AIzaSyD1234567890...
VITE_FIREBASE_AUTH_DOMAIN=fitian-el-mazba7.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=fitian-el-mazba7
VITE_FIREBASE_STORAGE_BUCKET=fitian-el-mazba7.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789...
VITE_FIREBASE_APP_ID=1:123456789:web:abcd1234...

# Optional: Analytics
VITE_MEASUREMENT_ID=G-1234567890
```

### 2. Electron App Configuration

Create `apps/electron/.env.local`:

```env
# Same Firebase config as web app
VITE_FIREBASE_API_KEY=...
VITE_FIREBASE_PROJECT_ID=fitian-el-mazba7
# ... other Firebase config
```

### 3. Get Firebase Config

**Via Console:**
1. Firebase Console → Project Settings
2. Scroll to "Your apps"
3. Select your web app
4. Copy the firebaseConfig object

**Via CLI:**
```bash
firebase projects:list
firebase projects:describe fitian-el-mazba7
```

### 4. Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `VITE_FIREBASE_API_KEY` | Firebase API key | `AIzaSy...` |
| `VITE_FIREBASE_PROJECT_ID` | GCP project ID | `fitian-el-mazba7` |
| `VITE_FIREBASE_AUTH_DOMAIN` | Auth domain | `fitian-el-mazba7.firebaseapp.com` |
| `VITE_FIREBASE_STORAGE_BUCKET` | Storage bucket | `fitian-el-mazba7.appspot.com` |

---

## Local Development

### 1. Start Web Dev Server

```bash
# From project root
pnpm --filter web dev

# Output:
# ➜  Local:   http://localhost:5173/
# ➜  press h to show help
```

Open http://localhost:5173/ in your browser.

### 2. Start Electron App

```bash
# In separate terminal
pnpm --filter electron dev

# Electron window opens with app

# Press F12 to open DevTools
```

### 3. Start Firebase Emulator (Optional)

```bash
firebase emulators:start

# Emulator UI: http://localhost:4000/
# Firestore: localhost:8080
# Auth: localhost:9099
```

When using emulator, set in `.env.local`:
```env
VITE_USE_EMULATOR=true
```

### 4. Project Structure

```
5edma-management-system-5ms-/
├── apps/
│   ├── web/                 # React web app
│   │   ├── src/
│   │   ├── dist/            # Build output
│   │   ├── vite.config.ts
│   │   └── package.json
│   └── electron/            # Electron desktop app
│       ├── src/
│       ├── dist/            # Electron build output
│       └── package.json
├── packages/
│   └── shared/              # Shared types
├── functions/               # Cloud Functions
├── firebase.json            # Firebase config
├── firestore.rules          # Security rules
└── package.json             # Root monorepo
```

### 5. Common Commands

```bash
# Development
pnpm dev                        # Run all apps in dev mode
pnpm --filter web dev          # Web app only
pnpm --filter electron dev     # Electron only

# Building
pnpm build                      # Build all apps
pnpm --filter web build        # Build web SPA
pnpm --filter electron build   # Build Electron app

# Type checking
pnpm typecheck                 # Check all TypeScript
pnpm --filter web typecheck    # Web only

# Linting (if configured)
pnpm lint                       # Lint all code
```

---

## CI/CD Setup

### 1. GitHub Actions Setup

#### A. Create GitHub Repository

```bash
git remote add origin https://github.com/your-org/5edma-management-system.git
git branch -M main
git push -u origin main
```

#### B. Add Secrets to GitHub

Go to GitHub → Settings → Secrets and variables → Actions

**Required secrets:**

1. `FIREBASE_SERVICE_ACCOUNT_FITIAN_EL_MAZBA7`
   ```bash
   # Get from Firebase Console → Project Settings → Service Accounts
   # Download private key JSON and convert to base64
   cat service-account-key.json | base64 -w 0
   ```

2. `FIREBASE_DEPLOY_TOKEN`
   ```bash
   firebase login:ci
   # Copy the token output
   ```

3. `SLACK_WEBHOOK_URL` (optional)
   - For build notifications

#### C. Verify Workflows

Check `.github/workflows/`:
- `deploy.yml` — Deploys on push to main
- `build-electron.yml` — Builds Windows installer on tags

### 2. Deployment Workflow

**Auto-Deploy to Hosting:**
```
Push to main
    ↓
Test job runs (type check, build)
    ↓
Deploy job runs (if test passes)
    ↓
Firebase Hosting updated
    ↓
Cloud Functions deployed
    ↓
Security rules updated
```

**Manual Tag Release:**
```bash
# Tag a new version
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions automatically:
# - Builds Electron app
# - Creates Windows installer
# - Uploads to GitHub Releases
# - Sends Slack notification
```

### 3. Monitoring CI/CD

```bash
# View workflow runs
gh workflow list
gh run list

# View specific run logs
gh run view <run-id>
```

---

## Production Deployment

### Quick Start

**Prerequisites:**
- Firebase CLI installed and authenticated
- Web app built: `pnpm --filter web build`
- Functions built: `pnpm --filter functions build`

**Deploy everything:**
```bash
firebase deploy
```

**Deploy specific services:**
```bash
firebase deploy --only hosting        # Web app only
firebase deploy --only functions      # Cloud Functions only
firebase deploy --only firestore:rules # Security rules only
```

### Full Deployment Checklist

- [ ] Code committed and pushed to main
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Firebase project created
- [ ] Services enabled in Firebase Console
- [ ] Web app built: `pnpm --filter web build`
- [ ] Functions built: `pnpm --filter functions build`
- [ ] Rules and indexes ready: `firestore.rules`, `firestore.indexes.json`
- [ ] GitHub secrets configured (for CI/CD)
- [ ] Slack webhook configured (optional)

### Deploy Command

```bash
# From project root
firebase deploy \
  --project=fitian-el-mazba7 \
  --only hosting,functions,firestore:rules,firestore:indexes

# Verify
firebase hosting:channel:list
firebase functions:list
firebase firestore:rules:list
```

### Post-Deployment

1. **Verify Hosting:**
   ```bash
   firebase hosting:channel:open live
   ```

2. **Test Functions:**
   - Call inviteUser() function
   - Verify custom claims are set

3. **Monitor:**
   - Firebase Console → Usage & billing
   - Check error logs
   - Monitor Firestore reads/writes

### Rollback

If issues occur:

```bash
# Rollback web app
firebase hosting:delete-channel <channel-id>

# Rollback functions
gcloud functions deploy <function-name> --source=/path/to/previous/version

# Rollback rules
git checkout <previous-commit>
firebase deploy --only firestore:rules
```

---

## Troubleshooting

### Common Issues

**Error: "Project fitian-el-mazba7 not found"**
```bash
# Fix: Set correct project
firebase use fitian-el-mazba7
firebase projects:list  # Verify it's there
```

**Error: "Authentication required"**
```bash
# Fix: Login again
firebase logout
firebase login
```

**Build fails: "Cannot find module '@5edma/shared'"**
```bash
# Fix: Install dependencies
pnpm install
# Or rebuild shared package
pnpm --filter shared build
```

**Firestore rules deployment fails**
```bash
# Validate rules locally
firebase emulators:start --only firestore

# Then deploy
firebase deploy --only firestore:rules
```

### Getting Help

1. **Check logs:**
   ```bash
   firebase hosting:logs <project-id>
   firebase functions:log
   ```

2. **Debug locally:**
   ```bash
   firebase emulators:start
   # Test with emulator first
   ```

3. **Contact support:**
   - Firebase Console → Support
   - GitHub Issues: Report bugs
   - Stack Overflow: Ask questions (tag: firebase)

---

## Next Steps

1. **Development:**
   - Start web dev server: `pnpm --filter web dev`
   - Create a feature branch: `git checkout -b feature/your-feature`
   - Make changes and test locally
   - Push to GitHub and create Pull Request

2. **Deployment:**
   - Merge PR to main
   - GitHub Actions automatically deploys
   - Verify deployment via Firebase Console

3. **Electron Builds:**
   - Tag a version: `git tag v1.0.0`
   - Push tag: `git push origin v1.0.0`
   - GitHub Actions builds Windows installer
   - Download from GitHub Releases

---

## Support Contacts

| Issue | Contact |
|-------|---------|
| Firebase | Firebase Support (console.firebase.google.com) |
| GitHub | GitHub Issues or GitHub Support |
| Development Help | Team Lead or Tech Lead |
| Deployment Issues | DevOps Team |

---

## Useful Links

- [Firebase Console](https://console.firebase.google.com/)
- [GitHub Repository](https://github.com/your-org/5edma-management-system)
- [Firebase Documentation](https://firebase.google.com/docs)
- [Electron Documentation](https://www.electronjs.org/docs)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
