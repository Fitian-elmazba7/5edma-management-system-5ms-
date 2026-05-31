# Deployment Guide

Complete guide for deploying 5edma Management System to production.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Firebase Setup](#firebase-setup)
3. [Web Deployment](#web-deployment)
4. [Cloud Functions](#cloud-functions)
5. [Security Rules](#security-rules)
6. [Production Checklist](#production-checklist)
7. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Prerequisites

### Required Tools

- **Firebase CLI**: `npm install -g firebase-tools`
- **Node.js 18+**: For Cloud Functions
- **pnpm**: Package manager for monorepo
- **git**: Version control

### Required Accounts

- **Google Cloud Account** with billing enabled
- **Firebase Project** named "Fitian_El-mazba7"
- **GitHub Account** (for CI/CD, optional)

### Credentials

Firebase CLI will prompt for authentication:

```bash
firebase login
```

This opens a browser to grant permissions and saves credentials to `~/.config/firebase/`.

---

## Firebase Setup

### 1. Create Firebase Project

If not already created, create via Firebase Console:

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add Project"
3. **Project ID:** `fitian-el-mazba7`
4. **Project Name:** 5edma Management System
5. Enable Analytics (optional)
6. Wait for project creation (~2 min)

### 2. Enable Services

In Firebase Console, enable:

- **Authentication** → Email/Password
- **Firestore Database** → Create database
  - Location: `nam5` (North America) or closest to users
  - Security rules: Start with test mode (we'll deploy strict rules)
- **Hosting** → Set up (reserves the domain)
- **Cloud Functions** → Enable billing

### 3. Connect to Project

```bash
# From project root
firebase init

# Select:
# - Firestore
# - Hosting
# - Functions
# - Emulators (for local testing)

# Choose "fitian-el-mazba7" when prompted
```

This creates/updates `.firebaserc` and `firebase.json`.

### 4. Update .env.local

Create `.env.local` in the web app with Firebase config:

```bash
VITE_FIREBASE_API_KEY=<from Firebase Console>
VITE_FIREBASE_AUTH_DOMAIN=fitian-el-mazba7.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=fitian-el-mazba7
VITE_FIREBASE_STORAGE_BUCKET=fitian-el-mazba7.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=<from Firebase Console>
VITE_FIREBASE_APP_ID=<from Firebase Console>
```

Get these from Firebase Console → Project Settings → Web App.

---

## Web Deployment

### 1. Build the Web App

```bash
# From project root
pnpm --filter web build

# Verify dist directory was created
ls apps/web/dist
```

### 2. Preview Locally

```bash
firebase serve --only hosting
# Open http://localhost:5000
```

Test in browser:
- [ ] Login page loads
- [ ] Can login with test credentials
- [ ] Navigation works
- [ ] Data loads from Firestore

### 3. Deploy to Hosting

```bash
firebase deploy --only hosting

# Output:
# ✔ Deploy complete!
# Project Console: https://console.firebase.google.com/project/fitian-el-mazba7
# Hosting URL: https://fitian-el-mazba7.web.app
```

### 4. Verify Deployment

1. Open hosting URL from output
2. Verify:
   - [ ] Page loads (check for 404s)
   - [ ] Login works
   - [ ] Can perform basic operations
   - [ ] Dev tools show no errors
3. Check Firestore Console for data writes

---

## Cloud Functions

Cloud Functions handle user management and role synchronization.

### 1. Build Functions

```bash
cd functions
npm install
npm run build

# Verify lib/ directory created with compiled JS
```

### 2. Deploy Functions

```bash
# From project root
firebase deploy --only functions

# Output:
# ✔ functions[setCustomClaims]: Successful
# ✔ functions[createUserDocument]: Successful
# ✔ functions[updateLastSignIn]: Successful
# ✔ functions[inviteUser]: Successful
# ✔ functions[deleteUser]: Successful
# ✔ functions[updateUserRole]: Successful
```

### 3. Test Functions

Option A: Use Firebase Console → Functions tab → Test

Option B: Call from app:

```typescript
// In app code
import { httpsCallable } from 'firebase/functions'
import { functions } from '@/lib/firebase'

const inviteUser = httpsCallable(functions, 'inviteUser')
const result = await inviteUser({
  email: 'newuser@example.com',
  displayName: 'New User',
  role: 'servant'
})

console.log('User created:', result.data.uid)
```

---

## Security Rules

### 1. Deploy Firestore Rules

```bash
firebase deploy --only firestore:rules
```

This deploys the rules from `firestore.rules`.

### 2. Deploy Firestore Indexes

```bash
firebase deploy --only firestore:indexes
```

This creates indexes defined in `firestore.indexes.json`.

### 3. Verify Rules

Test in Firestore Emulator:

```bash
firebase emulators:start

# In another terminal, run tests
pnpm test --env=emulator
```

### 4. Security Rule Walkthrough

**Rule file:** `firestore.rules`

#### Authentication Check
```javascript
function isAuthenticated() {
  return request.auth != null;
}
```
All operations require logged-in user.

#### Role Extraction
```javascript
function getRole() {
  return request.auth.token.role;
}
```
Gets role from custom claims set by Cloud Functions.

#### Role-Based Access

**Admin:**
- Can CRUD children, attendance, settings
- Can manage users
- Can delete any document

**Servant:**
- Can read children, attendance
- Can write attendance (record presence/absence)
- Cannot modify children or settings

**Viewer:**
- Can only read data
- Cannot write anything

**User:**
- Same as viewer (future expansion)

#### Examples

```javascript
// Children - admins write, everyone reads
match /children/{code} {
  allow read: if isAuthenticated();
  allow write: if isAdmin();
}

// Attendance - servants and admins write
match /attendance/{date} {
  allow read: if hasRole(['admin', 'servant', 'viewer']);
  allow write: if hasRole(['admin', 'servant']);
}

// Users - users read own, admins manage all
match /users/{uid} {
  allow read: if request.auth.uid == uid;
  allow write: if isAdmin();
}
```

---

## Production Checklist

### Before Launch

- [ ] Firebase project created with correct name
- [ ] All services enabled (Auth, Firestore, Hosting, Functions)
- [ ] Web app built and deployed to Hosting
- [ ] Cloud Functions compiled and deployed
- [ ] Security rules deployed
- [ ] Firestore indexes created

### Initial Data Setup

- [ ] Create admin user(s)
- [ ] Import existing data (children, attendance)
- [ ] Verify counts match source system
- [ ] Set service day/time in settings
- [ ] Test all 7 feature pages work

### User Setup

- [ ] Create servant accounts (use inviteUser function)
- [ ] Create viewer accounts for reporting
- [ ] Send password reset links to users
- [ ] Verify users can login and see appropriate screens

### Testing

- [ ] Test as admin: full access
- [ ] Test as servant: can register, manage absence, no data management
- [ ] Test as viewer: read-only access
- [ ] Test role change: logout/login to verify claims updated
- [ ] Test offline (Electron): register child, go offline, disconnect, sync

### Performance

- [ ] Page load time < 3s on 4G
- [ ] Firestore queries have indexes (check console for warnings)
- [ ] Images and assets are cached (check Network tab)

### Security

- [ ] Auth redirects unauthenticated users to login
- [ ] Viewer cannot access data management page
- [ ] Cannot modify data as viewer (direct Firestore API attempt fails)
- [ ] Cannot read other users' documents

---

## Monitoring & Maintenance

### Firebase Console Tabs

**Firestore:**
- Monitor read/write operations
- Watch for quota warnings
- View document sizes and indexes

**Authentication:**
- Monitor user count
- Check for suspicious login patterns
- View password reset requests

**Hosting:**
- View traffic and bandwidth
- Monitor response times
- Check error rates

**Cloud Functions:**
- Monitor execution times
- Watch for function errors
- View logs

**Usage & billing:**
- Track costs
- Set up budget alerts
- Enable auto-scaling for peak hours

### Common Issues

#### "Permission denied" on Firestore writes

**Cause:** Security rules are blocking the operation

**Fix:**
1. Check user's role: Console → Auth → select user → Custom claims
2. Check rule: Ensure role is allowed for operation
3. Verify custom claims are set correctly

#### Indexes missing, queries slow

**Cause:** Firestore recommends indexes for composite queries

**Fix:**
1. Check Firestore console for index suggestions
2. Run: `firebase deploy --only firestore:indexes`
3. Wait 5-10 min for indexes to build

#### Functions failing to deploy

**Cause:** Build errors or missing dependencies

**Fix:**
```bash
cd functions
npm install
npm run build
cd ..
firebase deploy --only functions
```

#### High Firebase costs

**Causes:**
- Excessive reads from Firestore
- Large file uploads
- Frequent function invocations

**Solutions:**
- Enable Firestore caching in app
- Batch operations (multiple writes → single update)
- Use indexes for frequently-queried fields
- Set read quotas in Firebase Console

### Backups

Firebase has automatic backups, but for safety:

1. **Export Firestore data regularly:**
   ```bash
   gcloud firestore export gs://bucket-name/backup-name
   ```

2. **Archive Excel reports:**
   - Export attendance reports monthly
   - Store in secure location

3. **Keep git history:**
   - All code changes tracked in git
   - Can revert to any version

### Upgrades & Updates

**Node.js Functions:**
- Current: Node 18
- Update `functions/package.json` and `functions/tsconfig.json`
- Test locally: `firebase emulators:start --only functions`
- Deploy: `firebase deploy --only functions`

**Web App Dependencies:**
- Review `apps/web/package.json` quarterly
- Test updates in dev: `pnpm update && pnpm --filter web dev`
- Deploy: `pnpm --filter web build && firebase deploy --only hosting`

**Security Rules:**
- Review quarterly
- Test changes in emulator first
- Deploy with `firebase deploy --only firestore:rules`

---

## Rollback Procedures

### Rollback Web Hosting

If deployment has issues:

```bash
# List recent deployments
firebase hosting:channel:list

# View specific version
firebase hosting:channel:open <version>

# Rollback to previous version
firebase hosting:clone fitian-el-mazba7:live <channel-name>
```

Or redeploy previous git commit:

```bash
git checkout <commit-hash>
pnpm --filter web build
firebase deploy --only hosting
```

### Rollback Functions

```bash
# List function versions
gcloud functions list

# Redeploy from previous commit
git checkout <commit-hash>
cd functions && npm run build && cd ..
firebase deploy --only functions
```

### Rollback Security Rules

```bash
# Rules are versioned in git
git checkout <commit-hash>
firebase deploy --only firestore:rules
```

---

## Support & Troubleshooting

### Get Logs

```bash
# Hosting
firebase hosting:logs <project-id>

# Functions
firebase functions:log

# Real-time monitoring
firebase serve --debug
```

### Contact Firebase Support

For production issues:
1. Check Firebase status: status.firebase.google.com
2. Search existing issues: stackoverflow.com (tag: firebase)
3. Contact Firebase support via Console

### Performance Optimization

1. **Firestore:**
   - Add composite indexes (auto-suggested)
   - Use client-side caching
   - Batch writes (max 500 per batch)

2. **Hosting:**
   - Enable HTTP/2 push (automatic)
   - Cache static assets (configured in firebase.json)
   - Use CDN (automatic with Firebase Hosting)

3. **Functions:**
   - Increase memory allocation for heavy operations
   - Use background function queue for non-critical tasks
   - Monitor cold start times

---

## Production Contacts

| Role | Contact | Responsibility |
|------|---------|-----------------|
| **Admin** | Admin User | User management, data integrity, system monitoring |
| **Servant** | Servants | Daily registration, absence reports |
| **Support** | Dev Team | Bug fixes, feature requests, technical issues |
| **Billing** | Admin | Firebase costs, quota management |

---

## Post-Launch Tasks

- [ ] Monitor Firestore usage daily for first week
- [ ] Collect user feedback
- [ ] Fix critical bugs immediately
- [ ] Plan minor version releases monthly
- [ ] Archive first month of data
- [ ] Update documentation based on user questions
