# Changelog

All notable changes to 5edma Management System are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-31

### ✨ Added

#### Phase 1: Monorepo Foundation
- pnpm workspaces with `apps/web`, `apps/electron`, `packages/shared`
- Vite + React 18 + TypeScript for web app
- Electron 27 + electron-builder for Windows packaging
- Tailwind CSS v4 with glass morphism design system
- Git workflow with rebuild/modern-stack branch

#### Phase 2: Design System & Auth
- Glass morphism UI components (GlassCard, GlassButton, GlassInput)
- Blue gradient (#1e40af → #3b82f6 → #6366f1) + near-black (#020408)
- Radix UI primitives + shadcn/ui integration
- Login page with Firebase Auth
- Role-based route protection (admin, servant, viewer, user)
- User management page (admin only)
- Dashboard with role-based navigation

#### Phase 3: Data Layer
- Firestore DAL: children.ts, attendance.ts, settings.ts
- SQLite mirror database for Electron app
- Zustand stores for children, attendance, settings state
- Offline sync engine with last-write-wins strategy
- Retry logic with exponential backoff (max 3 retries)
- Sync queue management in SQLite

#### Phase 4: Feature Pages (7 Tabs)
- **Registration** — Live attendance scanner with session stats
- **Dashboard** — Analytics with Recharts (pie, bar, line)
- **Absence** — Manage absent children, server assignment modal
- **Data Management** — Full CRUD for children with grid/list toggle
- **Early Arrival** — Filter by service time with settings dialog
- **Attendance Report** — Date-based report with stats
- **Comparison Report** — Multi-date attendance trends

#### Phase 5: Excel Integration
- Export functions: children, absence, attendance, comparison reports
- Import with validation: required fields, numeric codes, class names
- Arabic column header support (both English and Arabic)
- Drag-drop file upload UI component
- Error reporting (max 10 shown + overflow count)
- Blank template download
- Incremental import mode (skip existing codes)

#### Phase 6: Electron Packaging
- IPC handlers for database CRUD operations
- Preload script with context isolation
- Native file dialogs for Excel open/save
- Sync queue management via IPC
- Platform utilities for data paths
- electron-builder NSIS installer configuration
- useElectronAPI React hook for data access
- Data adapter layer (Firestore/SQLite abstraction)
- Connection status indicator with pending sync count
- useConnectionStatus hook for offline tracking

#### Phase 7: Firebase Deployment
- firebase.json with Hosting, Firestore, Functions config
- Firestore security rules with role-based access
- Firestore composite indexes for query optimization
- Cloud Functions for user management:
  - setCustomClaims (sync role to auth)
  - createUserDocument (on auth user creation)
  - inviteUser (admin creates users)
  - updateUserRole (admin changes roles)
  - deleteUser (admin removes users)
  - updateLastSignIn (track activity)
- GitHub Actions workflows:
  - deploy.yml — Auto-deploy web + functions on push to main
  - build-electron.yml — Build Windows installer on version tags
- Complete documentation:
  - DEPLOYMENT.md — Production setup and operations
  - SETUP.md — Developer and system setup guide
  - README.md — Project overview and quick start
  - CHANGELOG.md — Version history

### 📊 Statistics

- **Total Lines of Code:** ~7,800
- **Web App:** ~2,200 lines (components, pages, utilities)
- **Electron App:** ~1,800 lines (IPC, SQLite, sync)
- **Cloud Functions:** ~400 lines (user management)
- **Documentation:** ~3,200 lines
- **Configuration:** ~200 lines (firebase.json, rules, etc.)

### 🏗️ Architecture

- **Monorepo:** pnpm workspaces with isolated apps
- **Frontend:** React 18 + TypeScript + Vite
- **Desktop:** Electron with SQLite offline support
- **Cloud DB:** Firebase Firestore with real-time sync
- **Auth:** Firebase Auth with custom claims for roles
- **State:** Zustand for UI and data stores
- **UI Design:** Radix UI + Tailwind CSS glass morphism
- **Data Access:** Adapter pattern (Firestore/SQLite)

### 🔐 Security

- Context isolation in Electron (preload bridge)
- Firestore rules with document-level access control
- JWT custom claims for role enforcement
- Password-based authentication via Firebase
- User invitation flow with email confirmation
- Offline sync with last-write-wins conflict resolution

### 🌍 Internationalization

- RTL (right-to-left) support for Arabic
- All UI text in Arabic
- Excel import/export with Arabic field names
- Arabic date formatting and localization

### 📱 Cross-Platform

- **Web:** All modern browsers (Chrome, Safari, Firefox, Edge)
- **Desktop:** Windows 10+ (NSIS installer)
- **Database:** Cloud (Firestore) + Local (SQLite for Electron)

### 🚀 Deployment

- Firebase Hosting for web SPA
- GitHub Actions CI/CD for auto-deployment
- Cloud Functions for backend logic
- Firestore with automatic scaling

---

## [Unreleased]

### 🚧 Planned

- [ ] macOS support (Electron)
- [ ] Mobile app (React Native)
- [ ] Two-factor authentication
- [ ] Audit logging for all operations
- [ ] Backup/restore functionality
- [ ] Bulk attendance via QR codes
- [ ] SMS notifications for absences
- [ ] Payment integration for fees
- [ ] Volunteer scheduling
- [ ] Document management (photos, IDs)
- [ ] Parent communication portal
- [ ] Performance analytics
- [ ] Multi-language support (not just Arabic)

### 📋 Known Issues

- [ ] macOS builds not tested
- [ ] Mobile UI needs optimization for small screens
- [ ] Very large Excel imports (1000+ rows) may be slow
- [ ] Electron app requires manual update restarts

---

## Git History

### Commits by Phase

1. **Phase 1** — Monorepo scaffold (~1,092 lines)
2. **Phase 2** — Design system + Auth (~669 lines)
3. **Phase 3** — Data layer (~986 lines)
4. **Phase 4** — Feature pages (~1,881 lines)
5. **Phase 5** — Excel import/export (~686 lines)
6. **Phase 6** — Electron packaging (~1,814 lines)
7. **Phase 7** — Firebase deployment (~2,200 lines)

**Total:** 7 commits, ~8,800 lines

---

## How to Use This Changelog

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes

For detailed information, see [Keep a Changelog](https://keepachangelog.com/).

---

## Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)
- **MAJOR** — Breaking changes
- **MINOR** — New features (backwards compatible)
- **PATCH** — Bug fixes and minor improvements

### Release Process

1. Update CHANGELOG.md with new version and date
2. Update version in package.json files
3. Commit changes: `git commit -m "chore: bump version to X.Y.Z"`
4. Tag release: `git tag vX.Y.Z`
5. Push: `git push origin main --tags`
6. GitHub Actions automatically builds and releases

---

## Contributors

- **Original Author:** [Your Name]
- **Contributors:** [List here]

---

## Support

- **GitHub Issues:** [Report bugs](https://github.com/your-org/5edma-management-system/issues)
- **Email:** [your-email@example.com]
- **Documentation:** See [README.md](./README.md) and [SETUP.md](./SETUP.md)

---

**Last Updated:** May 31, 2026
