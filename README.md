# 5edma Management System

Modern, cloud-connected church attendance management system with offline-first desktop app and web interface.

## 🎯 Overview

5edma (meaning "service" in Arabic) is a complete rebuild of a PyQt5 church attendance management system using modern web technologies. It provides:

- **Web App** — React SPA hosted on Firebase Hosting
- **Desktop App** — Electron app with offline SQLite support
- **Cloud Database** — Firebase Firestore with real-time sync
- **Security** — Role-based access control (admin, servant, viewer, user)
- **Glass UI** — Modern design with blue gradient and glass morphism

## ✨ Features

### Core Functionality (7 Tabs)
1. **Daily Registration** — Live attendance scanner with session management
2. **Dashboard** — Analytics with charts and stats
3. **Absence Management** — Track absent children by class, assign to servants
4. **Data Management** — Full CRUD for children records, bulk import/export
5. **Early Arrival** — Filter attendees by service time
6. **Attendance Reports** — Date-based reports with export
7. **Comparison Reports** — Multi-date attendance trends

### Technology Features
- **Offline-First** — Works without internet, syncs when online
- **Real-Time Sync** — Automatic Firestore ↔ SQLite synchronization
- **Excel Integration** — Import/export with Arabic support
- **Multi-Role** — Admin, servant, viewer, user permissions
- **Glass Design** — Modern UI with backdrop blur and gradients
- **Mobile Responsive** — Works on tablet and desktop

## 📱 Platforms

| Platform | Status | Features |
|----------|--------|----------|
| **Web** | ✅ Ready | Cloud-based, real-time sync, all browsers |
| **Windows Desktop** | ✅ Ready | Offline support, SQLite cache, native installer |
| **macOS** | 🚧 Planned | (Electron can target macOS) |
| **Mobile** | 🚧 Future | (React Native version) |

## 🚀 Quick Start

### For Development

```bash
# Clone and setup
git clone https://github.com/your-org/5edma-management-system.git
cd 5edma-management-system
pnpm install

# Start web app
pnpm --filter web dev
# Open http://localhost:5173/

# Start desktop app (separate terminal)
pnpm --filter electron dev
```

### For Deployment

```bash
# Build
pnpm build

# Deploy to Firebase
firebase deploy

# Build Windows installer
pnpm --filter electron dist
```

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [**SETUP.md**](./SETUP.md) | Complete setup guide for developers |
| [**DEPLOYMENT.md**](./DEPLOYMENT.md) | Production deployment and operations |
| [**CONTRIBUTING.md**](./CONTRIBUTING.md) | Development guidelines (coming soon) |
| [**apps/web/README.md**](./apps/web/) | Web app documentation |
| [**apps/electron/README.md**](./apps/electron/) | Electron app documentation |
| [**apps/electron/DEVELOPMENT.md**](./apps/electron/DEVELOPMENT.md) | Electron development guide |
| [**apps/electron/INTEGRATION.md**](./apps/electron/INTEGRATION.md) | Offline sync architecture |

## 🏗️ Project Structure

```
5edma-management-system-5ms-/
├── apps/
│   ├── web/                    # React + Vite SPA
│   │   ├── src/
│   │   │   ├── components/     # Radix UI glass components
│   │   │   ├── pages/          # 7 feature pages + auth
│   │   │   ├── lib/
│   │   │   │   ├── firebase.ts
│   │   │   │   ├── firestore/  # Firestore DAL
│   │   │   │   └── data/       # Adapter layer
│   │   │   ├── store/          # Zustand stores
│   │   │   ├── hooks/          # React hooks
│   │   │   └── styles/         # Tailwind + glass design
│   │   └── vite.config.ts
│   └── electron/               # Electron desktop app
│       ├── src/
│       │   ├── main.ts         # Main process
│       │   ├── preload.ts      # Context bridge
│       │   ├── ipc/            # IPC handlers
│       │   ├── sqlite/         # SQLite DAL
│       │   └── sync/           # Offline sync engine
│       └── electron-builder.json
├── packages/
│   └── shared/                 # Shared TypeScript types
├── functions/                  # Cloud Functions
│   ├── src/index.ts           # User mgmt, custom claims
│   ├── package.json
│   └── tsconfig.json
├── firebase.json               # Firebase config
├── firestore.rules             # Security rules
├── firestore.indexes.json      # Query indexes
├── .github/workflows/          # CI/CD
│   ├── deploy.yml             # Auto-deploy to Firebase
│   └── build-electron.yml     # Build Windows installer
└── package.json                # Monorepo root
```

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18 + TypeScript + Vite |
| **Styling** | Tailwind CSS v4 + glass morphism |
| **UI Components** | Radix UI + shadcn/ui |
| **Desktop** | Electron 27 + electron-builder |
| **State** | Zustand + React Query |
| **Database (Cloud)** | Firebase Firestore |
| **Database (Local)** | SQLite via better-sqlite3 |
| **Auth** | Firebase Authentication |
| **Excel** | exceljs with Arabic support |
| **Charts** | Recharts |
| **Hosting** | Firebase Hosting |
| **Functions** | Cloud Functions (Node 18) |
| **Monorepo** | pnpm workspaces |

## 🔐 Security

- **Authentication** — Firebase email/password auth
- **Authorization** — Role-based access control (RBAC)
- **Context Isolation** — Electron preload bridge
- **Security Rules** — Firestore document-level access control
- **Custom Claims** — JWT-based role enforcement
- **Offline** — Last-write-wins conflict resolution

### User Roles

| Role | Permissions |
|------|-----------|
| **Admin** | Full access: CRUD children, manage users, all reports |
| **Servant** | Can register attendance, manage absence, view reports |
| **Viewer** | Read-only access to all dashboards and reports |
| **User** | Reserved for future features (same as viewer) |

## 🔄 Offline Sync

The Electron app works offline and automatically syncs:

1. **Offline** → Operations stored in SQLite `sync_queue`
2. **Online** → `SyncEngine` drains queue to Firestore
3. **Conflict** → Last-write-wins by `updatedAt` timestamp
4. **Status** → UI shows pending operations count

```
User goes offline
    ↓
Child added to SQLite
    ↓
sync_queue entry created
    ↓
User goes online
    ↓
Auto-drain: sync_queue → Firestore
    ↓
Status: "✓ Synced"
```

## 📊 Database Schema

### Collections

**`children/{code}`** — Child profiles
```typescript
{
  code: string              // Unique ID (e.g., "101")
  name: string              // Arabic full name
  class: "الصف الأول" | "الصف الثاني" | "الصف الثالث"
  region, building, street, floor, apartment  // Address
  childMobile, fatherMobile, motherMobile, homeLine  // Contact
  school, isDeacon, confessorFather, notes  // Extra fields
  createdAt, updatedAt: Timestamp
  createdBy: string         // User UID
}
```

**`attendance/{YYYY-MM-DD}`** — Daily attendance
```typescript
{
  date: string
  records: { [code]: string }  // { "101": "18:45" }
  serviceDay: boolean
  updatedAt: Timestamp
}
```

**`settings/config`** — System settings
```typescript
{
  serviceDay: "Thursday"
  serviceTime: "19:00"
  orgName: "Church Name"
}
```

**`users/{uid}`** — User accounts
```typescript
{
  email: string
  displayName: string
  role: "admin" | "servant" | "viewer" | "user"
  createdAt, lastSignIn: Timestamp
}
```

## 🚢 Deployment

### Web (Firebase Hosting)

```bash
pnpm --filter web build
firebase deploy --only hosting
# → https://fitian-el-mazba7.web.app
```

### Desktop (Windows Installer)

```bash
git tag v1.0.0
git push origin v1.0.0
# → GitHub Actions builds .exe installer
# → Download from GitHub Releases
```

### Automatic CI/CD

Workflows in `.github/workflows/`:
- **deploy.yml** — Auto-deploys on push to main
- **build-electron.yml** — Builds Windows installer on tags

## 📈 Development Phases

| Phase | Status | Focus |
|-------|--------|-------|
| 1 | ✅ | Monorepo scaffold, TypeScript, Vite |
| 2 | ✅ | Design system, glass UI, authentication |
| 3 | ✅ | Firestore & SQLite data layer, sync engine |
| 4 | ✅ | All 7 feature pages with UI |
| 5 | ✅ | Excel import/export with validation |
| 6 | ✅ | Electron packaging, IPC bridge, offline sync |
| 7 | ✅ | Firebase deployment, security rules, CI/CD |

## 📋 Features Complete

- ✅ Web app (React + Vite)
- ✅ Desktop app (Electron + SQLite)
- ✅ Firestore backend with real-time sync
- ✅ Authentication (4 user roles)
- ✅ All 7 original feature tabs
- ✅ Excel import/export
- ✅ Glass morphism UI design
- ✅ Offline-first architecture
- ✅ Security rules & custom claims
- ✅ Cloud Functions for user management
- ✅ Automatic CI/CD pipelines

## 🎓 Learning & References

- [Electron Best Practices](https://www.electronjs.org/docs/tutorial/security)
- [Firebase Security Rules](https://firebase.google.com/docs/firestore/security/get-started)
- [React Patterns](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Radix UI](https://www.radix-ui.com/)
- [Zustand](https://github.com/pmndrs/zustand)

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and test locally
3. Push to GitHub: `git push origin feature/your-feature`
4. Create Pull Request
5. Wait for CI/CD checks to pass
6. Merge when approved

## 📝 License

This project is proprietary. All rights reserved.

## 👥 Support

| Issue | Contact |
|-------|---------|
| Development Help | Tech Lead |
| Deployment Issues | DevOps Team |
| Feature Requests | Product Owner |
| Bug Reports | GitHub Issues |

## 🎯 Vision

5edma is the modern, open architecture replacement for the original PyQt5 system. It provides:

- **Accessibility** — Web and desktop versions for all platforms
- **Reliability** — Cloud backup with Firestore + local SQLite fallback
- **Scalability** — Grows from 1 church to hundreds
- **Maintainability** — Modern stack, fully documented, automated tests
- **Extensibility** — Plugin architecture for future features

## 📞 Contact

- **Project Lead**: [Your Name]
- **GitHub Issues**: [Report bugs](https://github.com/your-org/5edma-management-system/issues)
- **Email**: [your-email@example.com]

---

**Last Updated:** May 31, 2026
**Current Version:** 1.0.0
**Status:** Production Ready ✅
