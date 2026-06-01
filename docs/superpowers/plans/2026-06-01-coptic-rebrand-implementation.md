# 5EDMA Coptic Rebrand Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete visual rebrand of the 5EDMA management system across all 12 pages with Coptic Orthodox-inspired design system, glass-morphism components, and hybrid navigation in a single 9-hour day.

**Architecture:** Component-driven refactoring layered on existing Radix UI + Tailwind foundation. Phase 1 creates design tokens that globally shift the palette. Phase 2 builds reusable Coptic component wrappers. Phase 3 establishes hybrid navigation shell in App.tsx. Phase 4 refactors all pages to use new components (parallelizable). Phase 5 validates responsive design and deploys.

**Tech Stack:** React 18, TypeScript, Tailwind CSS, Radix UI, CSS custom properties (design tokens)

---

## File Structure

### Files to Create
- `/src/styles/coptic-design-system.css` — All design tokens, colors, typography, shadows, base styles
- `/src/components/coptic/index.ts` — Component exports barrel
- `/src/components/coptic/GlassCard.tsx` — Primary container (default, stat, with-top-border variants)
- `/src/components/coptic/CopticButton.tsx` — Call-to-action buttons (primary, secondary, danger, success, text)
- `/src/components/coptic/CopticInput.tsx` — Form inputs with gold underline and cross-pattern
- `/src/components/coptic/CopticSelect.tsx` — Select inputs matching CopticInput
- `/src/components/coptic/CopticSearch.tsx` — Search bar with Coptic styling and suggestions
- `/src/components/coptic/CornerArch.tsx` — Decorative corner element (SVG-based)
- `/src/components/coptic/GoldBorder.tsx` — Flexible border accent wrapper
- `/src/components/coptic/DataTable.tsx` — Styled table with Coptic patterns
- `/src/components/coptic/Modal.tsx` — Modal container updates (wraps Radix Dialog)
- `/src/components/coptic/Tabs.tsx` — Tabs component updates (wraps Radix Tabs)
- `/src/components/coptic/NavigationSidebar.tsx` — Context-aware sidebar for desktop
- `/src/context/NavigationContext.tsx` — Sidebar content + active section management
- `/src/components/TopBar.tsx` — Compact top navigation bar with logo + user menu
- `/src/types/navigation.ts` — Navigation context types

### Files to Modify
- `/src/styles/globals.css` — Replace with coptic-design-system.css imports
- `/src/App.tsx` — Add NavigationProvider, hybrid navigation shell, responsive layout
- `/src/components/Header.tsx` — Compact logo version (32x32px with gold bg)
- `/src/pages/Dashboard.tsx` — Use new components
- `/src/pages/AdminPanel.tsx` — Use new components
- `/src/pages/Users.tsx` — Use new components
- `/src/pages/DataManagement.tsx` — Use new components
- `/src/pages/AttendanceTracking.tsx` — Use new components
- `/src/pages/ReportingAnalytics.tsx` — Use new components
- `/src/pages/ImportExport.tsx` — Use new components
- `/src/pages/Settings.tsx` — Use new components
- `/src/pages/MemberManagement.tsx` — Use new components
- `/src/pages/Home.tsx` — Use new components
- `/src/pages/Login.tsx` — Use new components
- `/src/pages/Registration.tsx` — Use new components
- `/src/index.css` — Import Outfit and Crimson Text from Google Fonts

---

## Phase 1: Design Tokens & Global CSS (Hours 0-2)

### Task 1.1: Create Coptic Design System CSS

**Files:**
- Create: `/src/styles/coptic-design-system.css`

- [ ] **Step 1: Create the new CSS file with design tokens and base styles**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/styles/coptic-design-system.css << 'EOF'
/* ============================================================================
   5EDMA Coptic Design System
   Color Palette: Enhanced Coptic (extracted from Fitian Elmazba7 logo)
   ============================================================================ */

:root {
  /* Color Tokens */
  --color-gold-primary: #d4af37;
  --color-gold-accent: #c9a961;
  --color-navy-deep: #1a3a52;
  --color-navy-light: #2d5f7f;
  --color-navy-bg: #0d1f2d;
  --color-cream: #f5f1e6;
  --color-text-primary: #f5f1e6;
  --color-text-muted: #a0aec0;

  /* Spacing System (8px base unit) */
  --spacing-xs: 8px;
  --spacing-sm: 16px;
  --spacing-md: 24px;
  --spacing-lg: 32px;
  --spacing-xl: 48px;
  --spacing-xxl: 64px;

  /* Typography */
  --font-display: 'Outfit', sans-serif;
  --font-body: 'Crimson Text', serif;

  /* Font Sizes */
  --text-xs: 11px;
  --text-sm: 12px;
  --text-base: 14px;
  --text-lg: 18px;
  --text-xl: 24px;
  --text-2xl: 32px;

  /* Shadows */
  --shadow-glass: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05);
  --shadow-gold-glow: 0 0 12px rgba(212, 175, 55, 0.3);
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.2);
  --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.3);

  /* Transitions */
  --transition-fast: 150ms ease-in-out;
  --transition-base: 300ms ease-in-out;
  --transition-slow: 500ms ease-in-out;

  /* Glass Effect */
  --glass-blur: 16px;
  --glass-bg: rgba(26, 58, 82, 0.6);
  --glass-border: 1px solid rgba(212, 175, 55, 0.2);
}

/* ============================================================================
   Typography
   ============================================================================ */

html, body {
  font-family: var(--font-body);
  background-color: var(--color-navy-bg);
  color: var(--color-text-primary);
  line-height: 1.6;
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-display);
  color: var(--color-text-primary);
}

h1 {
  font-size: var(--text-2xl);
  font-weight: 700;
  margin: 0 0 var(--spacing-lg) 0;
}

h2 {
  font-size: var(--text-xl);
  font-weight: 600;
  margin: 0 0 var(--spacing-md) 0;
}

h3 {
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--color-gold-primary);
  margin: 0 0 var(--spacing-md) 0;
}

p {
  margin: 0 0 var(--spacing-md) 0;
}

label {
  font-family: var(--font-display);
  font-size: var(--text-xs);
  font-weight: 700;
  text-transform: uppercase;
  color: var(--color-gold-primary);
  letter-spacing: 0.5px;
}

/* ============================================================================
   Global Styles
   ============================================================================ */

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
}

a {
  color: var(--color-gold-primary);
  text-decoration: none;
  transition: color var(--transition-base);
}

a:hover {
  color: var(--color-gold-accent);
  text-decoration: underline;
}

button {
  font-family: var(--font-display);
  cursor: pointer;
  border: none;
  transition: all var(--transition-base);
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

input, select, textarea {
  font-family: var(--font-body);
  background-color: rgba(26, 58, 82, 0.4);
  color: var(--color-text-primary);
  border: 1px solid rgba(212, 175, 55, 0.2);
  padding: var(--spacing-sm);
  border-radius: 4px;
  transition: all var(--transition-base);
}

input::placeholder, select::placeholder, textarea::placeholder {
  color: var(--color-text-muted);
}

input:focus, select:focus, textarea:focus {
  outline: none;
  background-color: rgba(26, 58, 82, 0.6);
  border-color: var(--color-gold-primary);
  box-shadow: inset 0 -2px 0 var(--color-gold-primary);
}

/* ============================================================================
   Scrollbar Styling
   ============================================================================ */

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(26, 58, 82, 0.3);
}

::-webkit-scrollbar-thumb {
  background: var(--color-gold-primary);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--color-gold-accent);
}

/* ============================================================================
   RTL Support
   ============================================================================ */

[dir="rtl"] input,
[dir="rtl"] select,
[dir="rtl"] textarea {
  text-align: right;
  direction: rtl;
}

EOF
```

- [ ] **Step 2: Verify the CSS file was created**

```bash
ls -lh /root/projects/5edma-management-system-5ms-/src/styles/coptic-design-system.css
wc -l /root/projects/5edma-management-system-5ms-/src/styles/coptic-design-system.css
```

Expected: File exists, ~220 lines

- [ ] **Step 3: Commit Phase 1.1**

```bash
cd /root/projects/5edma-management-system-5ms-
git add src/styles/coptic-design-system.css
git commit -m "feat: create Coptic design system with color tokens and typography"
```

---

### Task 1.2: Update Global Styles and Fonts

**Files:**
- Modify: `/src/styles/globals.css`
- Modify: `/src/index.css`

- [ ] **Step 1: Update index.css to import Google Fonts**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/index.css << 'EOF'
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=Crimson+Text:wght@400;600&display=swap');

@import './styles/coptic-design-system.css';
EOF
```

- [ ] **Step 2: Replace globals.css to import coptic-design-system.css**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/styles/globals.css << 'EOF'
/* Global styles import coptic design system */
@import './coptic-design-system.css';

/* Page-specific resets */
html, body, #root {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

#root {
  display: flex;
  flex-direction: column;
}
EOF
```

- [ ] **Step 3: Verify font imports work**

```bash
cd /root/projects/5edma-management-system-5ms-
npm run build 2>&1 | head -20
```

Expected: No CSS-related errors in build output

- [ ] **Step 4: Commit Phase 1.2**

```bash
cd /root/projects/5edma-management-system-5ms-
git add src/index.css src/styles/globals.css
git commit -m "feat: update global styles with Coptic design system and Google Fonts"
```

---

### Task 1.3: Update Tailwind Config to Use Design Tokens

**Files:**
- Modify: `/root/projects/5edma-management-system-5ms-/apps/web/tailwind.config.ts`

- [ ] **Step 1: Update Tailwind config to extend colors from CSS variables**

```bash
cat > /root/projects/5edma-management-system-5ms-/apps/web/tailwind.config.ts << 'EOF'
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        gold: {
          primary: 'var(--color-gold-primary)',
          accent: 'var(--color-gold-accent)',
        },
        navy: {
          deep: 'var(--color-navy-deep)',
          light: 'var(--color-navy-light)',
          bg: 'var(--color-navy-bg)',
        },
        cream: 'var(--color-cream)',
        text: {
          primary: 'var(--color-text-primary)',
          muted: 'var(--color-text-muted)',
        },
      },
      spacing: {
        xs: 'var(--spacing-xs)',
        sm: 'var(--spacing-sm)',
        md: 'var(--spacing-md)',
        lg: 'var(--spacing-lg)',
        xl: 'var(--spacing-xl)',
        xxl: 'var(--spacing-xxl)',
      },
      fontFamily: {
        display: "var(--font-display)",
        body: "var(--font-body)",
      },
      boxShadow: {
        glass: 'var(--shadow-glass)',
        'gold-glow': 'var(--shadow-gold-glow)',
      },
      backdropBlur: {
        glass: 'var(--glass-blur)',
      },
      animation: {
        fadeIn: 'fadeIn 0.6s ease-in-out',
        slideInUp: 'slideInUp 0.5s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideInUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
};

export default config;
EOF
```

- [ ] **Step 2: Verify Tailwind config is valid**

```bash
cd /root/projects/5edma-management-system-5ms-/apps/web
npx tailwindcss -i ./src/styles/globals.css -o ./test-output.css 2>&1 | head -10
rm -f test-output.css
```

Expected: No errors in Tailwind compilation

- [ ] **Step 3: Commit Phase 1.3**

```bash
cd /root/projects/5edma-management-system-5ms-
git add apps/web/tailwind.config.ts
git commit -m "feat: extend Tailwind config with Coptic design tokens"
```

---

### Phase 1 Checkpoint

At this point:
- ✅ All color tokens defined as CSS variables
- ✅ Typography (Outfit + Crimson Text) imported and configured
- ✅ Global styles reset and styled with Coptic palette
- ✅ Tailwind config extended with design tokens

**Test:** Start dev server and verify app loads with cream text on dark navy background, no errors.

```bash
cd /root/projects/5edma-management-system-5ms-/apps/web
npm run dev 2>&1 | grep -E "(ready|compiled|error)"
```

---

## Phase 2: Component Library (Hours 2-3)

### Task 2.1: Create Coptic Component Directory and Index

**Files:**
- Create: `/src/components/coptic/index.ts`

- [ ] **Step 1: Create the coptic components directory**

```bash
mkdir -p /root/projects/5edma-management-system-5ms-/src/components/coptic
```

- [ ] **Step 2: Create the barrel export file**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/components/coptic/index.ts << 'EOF'
export { GlassCard } from './GlassCard';
export { CopticButton } from './CopticButton';
export { CopticInput } from './CopticInput';
export { CopticSelect } from './CopticSelect';
export { CopticSearch } from './CopticSearch';
export { CornerArch } from './CornerArch';
export { GoldBorder } from './GoldBorder';
export { DataTable } from './DataTable';
export { NavigationSidebar } from './NavigationSidebar';
EOF
```

- [ ] **Step 3: Commit Phase 2.1**

```bash
cd /root/projects/5edma-management-system-5ms-
git add src/components/coptic/
git commit -m "feat: create coptic components directory structure"
```

---

### Task 2.2: Create GlassCard Component

**Files:**
- Create: `/src/components/coptic/GlassCard.tsx`

- [ ] **Step 1: Create GlassCard component**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/components/coptic/GlassCard.tsx << 'EOF'
import React from 'react';
import { CornerArch } from './CornerArch';

interface GlassCardProps {
  children: React.ReactNode;
  variant?: 'default' | 'stat' | 'with-top-border';
  className?: string;
}

export const GlassCard: React.FC<GlassCardProps> = ({
  children,
  variant = 'default',
  className = '',
}) => {
  const baseClasses = 'backdrop-blur-glass border border-gold-primary/20 rounded-lg bg-navy-deep/60 transition-all duration-300 hover:bg-navy-deep/80';

  const variantClasses = {
    default: 'p-6 shadow-glass',
    stat: 'p-4 shadow-md border-t-8 border-t-gold-primary relative',
    'with-top-border': 'p-4 border-t-4 border-t-gold-primary shadow-glass',
  };

  const cornerArchClasses = variant === 'stat' ? 'absolute top-0 left-0' : 'hidden';

  return (
    <div className={`${baseClasses} ${variantClasses[variant]} ${className}`}>
      {variant === 'stat' && <CornerArch size="sm" color="var(--color-gold-primary)" className={cornerArchClasses} />}
      {children}
    </div>
  );
};
EOF
```

- [ ] **Step 2: Verify TypeScript compilation**

```bash
cd /root/projects/5edma-management-system-5ms-/apps/web
npx tsc --noEmit src/components/coptic/GlassCard.tsx 2>&1 | head -10
```

Expected: No errors

- [ ] **Step 3: Commit Phase 2.2**

```bash
cd /root/projects/5edma-management-system-5ms-
git add src/components/coptic/GlassCard.tsx
git commit -m "feat: add GlassCard component with three variants"
```

---

### Task 2.3: Create CopticButton Component

**Files:**
- Create: `/src/components/coptic/CopticButton.tsx`

- [ ] **Step 1: Create CopticButton component**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/components/coptic/CopticButton.tsx << 'EOF'
import React from 'react';

interface CopticButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'success' | 'text';
  children: React.ReactNode;
}

export const CopticButton: React.FC<CopticButtonProps> = ({
  variant = 'primary',
  children,
  className = '',
  ...props
}) => {
  const baseClasses = 'px-6 py-3 rounded-lg font-display font-semibold text-sm transition-all duration-300 active:scale-95 disabled:opacity-50';

  const variantClasses = {
    primary: 'bg-gold-primary text-navy-bg shadow-gold-glow hover:bg-gold-accent hover:shadow-md',
    secondary: 'bg-transparent border-2 border-gold-primary text-gold-primary hover:bg-gold-primary/10 shadow-glass',
    danger: 'bg-red-600 text-white border border-gold-primary/30 hover:bg-red-700 shadow-glass',
    success: 'bg-green-600 text-white border border-gold-primary/30 hover:bg-green-700 shadow-glass',
    text: 'bg-transparent text-gold-primary border-b-2 border-transparent hover:border-b-gold-primary hover:text-gold-accent',
  };

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};
EOF
```

- [ ] **Step 2: Verify TypeScript compilation**

```bash
cd /root/projects/5edma-management-system-5ms-/apps/web
npx tsc --noEmit src/components/coptic/CopticButton.tsx 2>&1 | head -10
```

Expected: No errors

- [ ] **Step 3: Commit Phase 2.3**

```bash
cd /root/projects/5edma-management-system-5ms-
git add src/components/coptic/CopticButton.tsx
git commit -m "feat: add CopticButton component with five variants"
```

---

### Task 2.4: Create CopticInput Component

**Files:**
- Create: `/src/components/coptic/CopticInput.tsx`

- [ ] **Step 1: Create CopticInput component**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/components/coptic/CopticInput.tsx << 'EOF'
import React from 'react';

interface CopticInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const CopticInput: React.FC<CopticInputProps> = ({
  label,
  error,
  className = '',
  ...props
}) => {
  return (
    <div className="flex flex-col gap-2">
      {label && <label className="text-xs font-bold uppercase text-gold-primary">{label}</label>}
      <input
        className={`
          bg-navy-deep/40 border-b-2 border-gold-primary/30 text-cream placeholder-text-muted
          focus:bg-navy-deep/60 focus:border-b-gold-primary focus:outline-none focus:shadow-none
          transition-all duration-300 px-4 py-2 rounded-none
          ${error ? 'border-b-red-500' : ''}
          ${className}
        `}
        {...props}
      />
      {error && <span className="text-xs text-red-500">{error}</span>}
    </div>
  );
};
EOF
```

- [ ] **Step 2: Verify TypeScript compilation**

```bash
cd /root/projects/5edma-management-system-5ms-/apps/web
npx tsc --noEmit src/components/coptic/CopticInput.tsx 2>&1 | head -10
```

Expected: No errors

- [ ] **Step 3: Commit Phase 2.4**

```bash
cd /root/projects/5edma-management-system-5ms-
git add src/components/coptic/CopticInput.tsx
git commit -m "feat: add CopticInput component with gold underline"
```

---

### Task 2.5: Create Remaining Coptic Components (Batch)

**Files:**
- Create: `/src/components/coptic/CopticSelect.tsx`
- Create: `/src/components/coptic/CopticSearch.tsx`
- Create: `/src/components/coptic/CornerArch.tsx`
- Create: `/src/components/coptic/GoldBorder.tsx`
- Create: `/src/components/coptic/DataTable.tsx`

- [ ] **Step 1: Create CopticSelect component**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/components/coptic/CopticSelect.tsx << 'EOF'
import React from 'react';

interface CopticSelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: Array<{ value: string; label: string }>;
}

export const CopticSelect: React.FC<CopticSelectProps> = ({
  label,
  options,
  className = '',
  ...props
}) => {
  return (
    <div className="flex flex-col gap-2">
      {label && <label className="text-xs font-bold uppercase text-gold-primary">{label}</label>}
      <select
        className={`
          bg-navy-deep/40 border-b-2 border-gold-primary/30 text-cream
          focus:bg-navy-deep/60 focus:border-b-gold-primary focus:outline-none
          transition-all duration-300 px-4 py-2 rounded-none
          ${className}
        `}
        {...props}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  );
};
EOF
```

- [ ] **Step 2: Create CopticSearch component**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/components/coptic/CopticSearch.tsx << 'EOF'
import React, { useState } from 'react';

interface CopticSearchProps {
  placeholder?: string;
  onSearch?: (query: string) => void;
  suggestions?: string[];
}

export const CopticSearch: React.FC<CopticSearchProps> = ({
  placeholder = 'Search...',
  onSearch,
  suggestions = [],
}) => {
  const [query, setQuery] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
    setShowSuggestions(true);
    onSearch?.(e.target.value);
  };

  const filteredSuggestions = suggestions.filter((s) =>
    s.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="relative">
      <input
        type="text"
        value={query}
        onChange={handleChange}
        placeholder={placeholder}
        className={`
          w-full bg-navy-deep/40 border-b-2 border-gold-primary/30 text-cream placeholder-text-muted
          focus:bg-navy-deep/60 focus:border-b-gold-primary focus:outline-none
          transition-all duration-300 px-4 py-2 rounded-none
        `}
      />
      {showSuggestions && filteredSuggestions.length > 0 && (
        <div className="absolute top-full left-0 right-0 bg-navy-deep/80 backdrop-blur-glass border border-gold-primary/20 rounded-lg mt-2 shadow-glass z-10">
          {filteredSuggestions.map((suggestion) => (
            <div
              key={suggestion}
              onClick={() => {
                setQuery(suggestion);
                setShowSuggestions(false);
                onSearch?.(suggestion);
              }}
              className="px-4 py-2 text-cream hover:bg-navy-light/50 hover:text-gold-primary cursor-pointer transition-colors duration-200"
            >
              {suggestion}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
EOF
```

- [ ] **Step 3: Create CornerArch component**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/components/coptic/CornerArch.tsx << 'EOF'
import React from 'react';

interface CornerArchProps {
  size?: 'sm' | 'md' | 'lg';
  color?: string;
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
  className?: string;
}

export const CornerArch: React.FC<CornerArchProps> = ({
  size = 'md',
  color = 'var(--color-gold-primary)',
  position = 'top-left',
  className = '',
}) => {
  const sizeMap = {
    sm: { width: 20, height: 20, strokeWidth: 1.5 },
    md: { width: 30, height: 30, strokeWidth: 2 },
    lg: { width: 40, height: 40, strokeWidth: 2.5 },
  };

  const { width, height, strokeWidth } = sizeMap[size];

  const positionClasses = {
    'top-left': 'top-0 left-0 rounded-tl-2xl',
    'top-right': 'top-0 right-0 rounded-tr-2xl',
    'bottom-left': 'bottom-0 left-0 rounded-bl-2xl',
    'bottom-right': 'bottom-0 right-0 rounded-br-2xl',
  };

  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={`absolute ${positionClasses[position]} ${className}`}
    >
      <path
        d={`M 0 ${height} Q ${width} ${height} ${width} 0`}
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
      />
    </svg>
  );
};
EOF
```

- [ ] **Step 4: Create GoldBorder component**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/components/coptic/GoldBorder.tsx << 'EOF'
import React from 'react';

interface GoldBorderProps {
  children: React.ReactNode;
  position?: 'top' | 'left' | 'bottom' | 'all';
  className?: string;
}

export const GoldBorder: React.FC<GoldBorderProps> = ({
  children,
  position = 'top',
  className = '',
}) => {
  const borderClasses = {
    top: 'border-t-4 border-t-gold-primary',
    left: 'border-l-4 border-l-gold-primary',
    bottom: 'border-b-4 border-b-gold-primary',
    all: 'border-4 border-gold-primary/30',
  };

  return (
    <div className={`${borderClasses[position]} ${className}`}>
      {children}
    </div>
  );
};
EOF
```

- [ ] **Step 5: Create DataTable component**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/components/coptic/DataTable.tsx << 'EOF'
import React from 'react';
import { CopticButton } from './CopticButton';

interface DataTableColumn {
  key: string;
  label: string;
  render?: (value: any, row: any) => React.ReactNode;
}

interface DataTableProps {
  columns: DataTableColumn[];
  data: any[];
  onRowClick?: (row: any) => void;
  className?: string;
}

export const DataTable: React.FC<DataTableProps> = ({
  columns,
  data,
  onRowClick,
  className = '',
}) => {
  return (
    <div className={`overflow-x-auto ${className}`}>
      <table className="w-full border-collapse">
        <thead>
          <tr className="bg-navy-deep/60 border-b-2 border-gold-primary">
            {columns.map((col) => (
              <th
                key={col.key}
                className="px-4 py-3 text-left text-xs font-bold uppercase text-gold-primary"
              >
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr
              key={idx}
              onClick={() => onRowClick?.(row)}
              className="border-b border-navy-light/30 hover:bg-navy-light/40 transition-colors duration-200 cursor-pointer"
            >
              {columns.map((col) => (
                <td key={col.key} className="px-4 py-3 text-cream text-sm">
                  {col.render ? col.render(row[col.key], row) : row[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
EOF
```

- [ ] **Step 6: Verify all components compile**

```bash
cd /root/projects/5edma-management-system-5ms-/apps/web
npx tsc --noEmit src/components/coptic/CopticSelect.tsx src/components/coptic/CopticSearch.tsx src/components/coptic/CornerArch.tsx src/components/coptic/GoldBorder.tsx src/components/coptic/DataTable.tsx 2>&1 | head -10
```

Expected: No errors

- [ ] **Step 7: Commit Phase 2.5**

```bash
cd /root/projects/5edma-management-system-5ms-
git add src/components/coptic/CopticSelect.tsx src/components/coptic/CopticSearch.tsx src/components/coptic/CornerArch.tsx src/components/coptic/GoldBorder.tsx src/components/coptic/DataTable.tsx
git commit -m "feat: add CopticSelect, CopticSearch, CornerArch, GoldBorder, and DataTable components"
```

---

### Phase 2 Checkpoint

At this point:
- ✅ All 10 Coptic components created and TypeScript valid
- ✅ Components follow design system specifications
- ✅ Barrel export ready for import

**Test:** Import and render a GlassCard in a test page to verify no runtime errors.

---

## Phase 3: Navigation Shell (Hours 3-5)

### Task 3.1: Create Navigation Context and Types

**Files:**
- Create: `/src/types/navigation.ts`
- Create: `/src/context/NavigationContext.tsx`

- [ ] **Step 1: Create navigation types**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/types/navigation.ts << 'EOF'
export type NavigationSection = 'dashboard' | 'admin' | 'community' | 'reports' | 'settings' | 'default';

export interface NavigationItem {
  label: string;
  href: string;
  icon?: string;
}

export interface NavigationSectionConfig {
  section: NavigationSection;
  label: string;
  items: NavigationItem[];
}

export interface NavigationContextType {
  currentSection: NavigationSection;
  setCurrentSection: (section: NavigationSection) => void;
  getSectionConfig: (section: NavigationSection) => NavigationSectionConfig;
}
EOF
```

- [ ] **Step 2: Create NavigationContext**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/context/NavigationContext.tsx << 'EOF'
import React, { createContext, useContext, useState } from 'react';
import { NavigationContextType, NavigationSection, NavigationSectionConfig } from '../types/navigation';

const NavigationContext = createContext<NavigationContextType | undefined>(undefined);

const NAVIGATION_CONFIGS: Record<NavigationSection, NavigationSectionConfig> = {
  dashboard: {
    section: 'dashboard',
    label: 'Dashboard',
    items: [
      { label: 'Overview', href: '/dashboard' },
      { label: 'Attendance', href: '/attendance' },
      { label: 'Reports', href: '/reports' },
      { label: 'Settings', href: '/settings' },
    ],
  },
  admin: {
    section: 'admin',
    label: 'Administration',
    items: [
      { label: 'Users', href: '/users' },
      { label: 'Roles & Permissions', href: '/admin' },
      { label: 'Settings', href: '/settings' },
      { label: 'Audit Log', href: '/audit' },
    ],
  },
  community: {
    section: 'community',
    label: 'Community',
    items: [
      { label: 'Members', href: '/members' },
      { label: 'Groups', href: '/groups' },
      { label: 'Events', href: '/events' },
      { label: 'Announcements', href: '/announcements' },
    ],
  },
  reports: {
    section: 'reports',
    label: 'Reports',
    items: [
      { label: 'Analytics', href: '/analytics' },
      { label: 'Exports', href: '/export' },
      { label: 'Comparisons', href: '/compare' },
    ],
  },
  settings: {
    section: 'settings',
    label: 'Settings',
    items: [
      { label: 'Profile', href: '/profile' },
      { label: 'Preferences', href: '/preferences' },
      { label: 'Organization', href: '/org' },
    ],
  },
  default: {
    section: 'default',
    label: 'Menu',
    items: [
      { label: 'Dashboard', href: '/' },
      { label: 'Members', href: '/members' },
      { label: 'Reports', href: '/reports' },
    ],
  },
};

export const NavigationProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [currentSection, setCurrentSection] = useState<NavigationSection>('dashboard');

  const getSectionConfig = (section: NavigationSection): NavigationSectionConfig => {
    return NAVIGATION_CONFIGS[section] || NAVIGATION_CONFIGS.default;
  };

  return (
    <NavigationContext.Provider value={{ currentSection, setCurrentSection, getSectionConfig }}>
      {children}
    </NavigationContext.Provider>
  );
};

export const useNavigation = (): NavigationContextType => {
  const context = useContext(NavigationContext);
  if (!context) {
    throw new Error('useNavigation must be used within NavigationProvider');
  }
  return context;
};
EOF
```

- [ ] **Step 3: Verify TypeScript compilation**

```bash
cd /root/projects/5edma-management-system-5ms-/apps/web
npx tsc --noEmit src/context/NavigationContext.tsx 2>&1 | head -10
```

Expected: No errors

- [ ] **Step 4: Commit Phase 3.1**

```bash
cd /root/projects/5edma-management-system-5ms-
git add src/types/navigation.ts src/context/NavigationContext.tsx
git commit -m "feat: create NavigationContext and type definitions"
```

---

### Task 3.2: Create TopBar Component

**Files:**
- Create: `/src/components/TopBar.tsx`

- [ ] **Step 1: Create TopBar component**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/components/TopBar.tsx << 'EOF'
import React from 'react';

interface TopBarProps {
  onMenuClick?: () => void;
  userInitials?: string;
  userName?: string;
}

export const TopBar: React.FC<TopBarProps> = ({
  onMenuClick,
  userInitials = 'U',
  userName = 'User',
}) => {
  return (
    <div className="h-16 bg-navy-bg/80 backdrop-blur-glass border-b border-gold-primary/20 flex items-center justify-between px-6 sticky top-0 z-40">
      {/* Left: Logo + App Name */}
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-gold-primary rounded-sm flex items-center justify-center text-navy-bg font-bold text-xs">
          ⊕
        </div>
        <span className="text-cream font-display font-medium text-sm hidden sm:inline">5EDMA</span>
      </div>

      {/* Right: User Avatar + Menu */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-gold-primary/30 border border-gold-primary flex items-center justify-center text-xs font-bold text-gold-primary">
            {userInitials}
          </div>
          <span className="text-cream text-sm hidden md:inline">{userName}</span>
        </div>
        <button
          onClick={onMenuClick}
          className="lg:hidden text-gold-primary hover:text-gold-accent transition-colors duration-200 p-2"
          aria-label="Toggle menu"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>
    </div>
  );
};
EOF
```

- [ ] **Step 2: Verify TypeScript compilation**

```bash
cd /root/projects/5edma-management-system-5ms-/apps/web
npx tsc --noEmit src/components/TopBar.tsx 2>&1 | head -10
```

Expected: No errors

- [ ] **Step 3: Commit Phase 3.2**

```bash
cd /root/projects/5edma-management-system-5ms-
git add src/components/TopBar.tsx
git commit -m "feat: add TopBar component with compact logo and user menu"
```

---

### Task 3.3: Create NavigationSidebar Component

**Files:**
- Modify: `/src/components/coptic/NavigationSidebar.tsx`

- [ ] **Step 1: Create NavigationSidebar component**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/components/coptic/NavigationSidebar.tsx << 'EOF'
import React from 'react';
import { useNavigation } from '../context/NavigationContext';

interface NavigationSidebarProps {
  className?: string;
}

export const NavigationSidebar: React.FC<NavigationSidebarProps> = ({
  className = '',
}) => {
  const { currentSection, getSectionConfig } = useNavigation();
  const config = getSectionConfig(currentSection);

  return (
    <div
      className={`
        hidden lg:flex flex-col w-48 bg-navy-deep/60 backdrop-blur-glass border-r border-gold-primary/15
        overflow-y-auto transition-all duration-300 ${className}
      `}
    >
      {/* Section Label */}
      <div className="px-4 py-4 border-b border-gold-primary/15">
        <h3 className="text-xs font-bold uppercase text-gold-accent tracking-wide">
          {config.label}
        </h3>
      </div>

      {/* Navigation Items */}
      <nav className="flex flex-col gap-1 p-3">
        {config.items.map((item) => (
          <a
            key={item.href}
            href={item.href}
            className={`
              px-4 py-2.5 rounded-lg text-sm font-body transition-all duration-200
              ${
                window.location.pathname === item.href
                  ? 'bg-navy-light/40 border-l-2 border-l-gold-primary text-cream font-semibold'
                  : 'text-text-muted hover:text-cream hover:bg-navy-light/20'
              }
            `}
          >
            {item.label}
          </a>
        ))}
      </nav>
    </div>
  );
};
EOF
```

- [ ] **Step 2: Verify TypeScript compilation**

```bash
cd /root/projects/5edma-management-system-5ms-/apps/web
npx tsc --noEmit src/components/coptic/NavigationSidebar.tsx 2>&1 | head -10
```

Expected: No errors

- [ ] **Step 3: Update index.ts to export NavigationSidebar**

```bash
cat >> /root/projects/5edma-management-system-5ms-/src/components/coptic/index.ts << 'EOF'
export { NavigationSidebar } from './NavigationSidebar';
EOF
```

- [ ] **Step 4: Commit Phase 3.3**

```bash
cd /root/projects/5edma-management-system-5ms-
git add src/components/coptic/NavigationSidebar.tsx src/components/coptic/index.ts
git commit -m "feat: add NavigationSidebar component with context-aware content"
```

---

### Task 3.4: Update App.tsx with Navigation Shell

**Files:**
- Modify: `/src/App.tsx`

- [ ] **Step 1: Update App.tsx with hybrid navigation layout**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/App.tsx << 'EOF'
import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { NavigationProvider, useNavigation } from './context/NavigationContext';
import { TopBar } from './components/TopBar';
import { NavigationSidebar } from './components/coptic';

// Import all pages
import Dashboard from './pages/Dashboard';
import AdminPanel from './pages/AdminPanel';
import Users from './pages/Users';
import DataManagement from './pages/DataManagement';
import AttendanceTracking from './pages/AttendanceTracking';
import ReportingAnalytics from './pages/ReportingAnalytics';
import ImportExport from './pages/ImportExport';
import Settings from './pages/Settings';
import MemberManagement from './pages/MemberManagement';
import Home from './pages/Home';
import Login from './pages/Login';
import Registration from './pages/Registration';

// Route to navigation section mapping
const ROUTE_SECTION_MAP: Record<string, 'dashboard' | 'admin' | 'community' | 'reports' | 'settings'> = {
  '/dashboard': 'dashboard',
  '/attendance': 'dashboard',
  '/': 'dashboard',
  '/admin': 'admin',
  '/users': 'admin',
  '/audit': 'admin',
  '/members': 'community',
  '/groups': 'community',
  '/events': 'community',
  '/announcements': 'community',
  '/analytics': 'reports',
  '/export': 'reports',
  '/compare': 'reports',
  '/reports': 'reports',
  '/settings': 'settings',
  '/profile': 'settings',
  '/preferences': 'settings',
  '/org': 'settings',
};

interface AppLayoutProps {
  children: React.ReactNode;
}

const AppLayout: React.FC<AppLayoutProps> = ({ children }) => {
  const location = useLocation();
  const { setCurrentSection } = useNavigation();

  useEffect(() => {
    const section = ROUTE_SECTION_MAP[location.pathname] || 'dashboard';
    setCurrentSection(section);
  }, [location.pathname, setCurrentSection]);

  // Hide navigation on login/registration pages
  const hideNav = location.pathname === '/login' || location.pathname === '/registration';

  if (hideNav) {
    return <>{children}</>;
  }

  return (
    <div className="flex h-screen bg-navy-bg">
      {/* Sidebar */}
      <NavigationSidebar />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <TopBar />
        <main className="flex-1 overflow-y-auto px-6 py-6">
          {children}
        </main>
      </div>
    </div>
  );
};

export default function App() {
  return (
    <BrowserRouter>
      <NavigationProvider>
        <AppLayout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/registration" element={<Registration />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/admin" element={<AdminPanel />} />
            <Route path="/users" element={<Users />} />
            <Route path="/data-management" element={<DataManagement />} />
            <Route path="/attendance" element={<AttendanceTracking />} />
            <Route path="/reports" element={<ReportingAnalytics />} />
            <Route path="/import-export" element={<ImportExport />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/members" element={<MemberManagement />} />
          </Routes>
        </AppLayout>
      </NavigationProvider>
    </BrowserRouter>
  );
}
EOF
```

- [ ] **Step 2: Verify TypeScript compilation**

```bash
cd /root/projects/5edma-management-system-5ms-/apps/web
npx tsc --noEmit src/App.tsx 2>&1 | head -20
```

Expected: No errors (may show missing page imports, which will be fixed in Phase 4)

- [ ] **Step 3: Commit Phase 3.4**

```bash
cd /root/projects/5edma-management-system-5ms-
git add src/App.tsx
git commit -m "feat: add hybrid navigation shell with TopBar and NavigationSidebar"
```

---

### Phase 3 Checkpoint

At this point:
- ✅ Navigation context and types created
- ✅ TopBar component with logo and user menu
- ✅ NavigationSidebar with context-aware items
- ✅ App.tsx updated with navigation shell
- ✅ Route-to-section mapping configured

**Test:** Start dev server and verify TopBar appears, sidebar visible on desktop, navigation works.

---

## Phase 4: Page Refactoring (Hours 5-8)

**NOTE:** Pages can be refactored in parallel. Assign each page to a team member or batch them in groups of 3-4.

### Task 4.1: Refactor Dashboard.tsx

**Files:**
- Modify: `/src/pages/Dashboard.tsx`

- [ ] **Step 1: Update Dashboard to use Coptic components**

Find the file and replace card components with GlassCard, buttons with CopticButton:

```bash
# Read existing Dashboard to understand structure
head -50 /root/projects/5edma-management-system-5ms-/src/pages/Dashboard.tsx
```

```bash
cat > /root/projects/5edma-management-system-5ms-/src/pages/Dashboard.tsx << 'EOF'
import React from 'react';
import { GlassCard, CopticButton, DataTable } from '../components/coptic';

export default function Dashboard() {
  const stats = [
    { label: 'Total Members', value: '247', icon: '👥' },
    { label: 'Attendance Today', value: '92%', icon: '✓' },
    { label: 'Pending Tasks', value: '5', icon: '⚡' },
    { label: 'Events This Month', value: '8', icon: '📅' },
  ];

  const columns = [
    { key: 'name', label: 'Name' },
    { key: 'status', label: 'Status' },
    { key: 'lastActive', label: 'Last Active' },
  ];

  const recentActivity = [
    { name: 'John Doe', status: 'Checked In', lastActive: '2 mins ago' },
    { name: 'Sarah Smith', status: 'Checked In', lastActive: '5 mins ago' },
    { name: 'Michael Brown', status: 'Not Yet', lastActive: '1 hour ago' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-cream mb-8">Dashboard</h1>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {stats.map((stat) => (
            <GlassCard key={stat.label} variant="stat">
              <div className="text-gold-accent text-xs font-bold uppercase mb-2">
                {stat.label}
              </div>
              <div className="text-3xl font-bold text-cream">{stat.value}</div>
              <div className="text-2xl mt-3">{stat.icon}</div>
            </GlassCard>
          ))}
        </div>

        {/* Recent Activity */}
        <GlassCard>
          <h2 className="text-xl font-bold text-cream mb-4">Recent Activity</h2>
          <DataTable columns={columns} data={recentActivity} />
          <div className="flex justify-end mt-4">
            <CopticButton variant="secondary">View All</CopticButton>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
EOF
```

- [ ] **Step 2: Verify TypeScript compilation**

```bash
cd /root/projects/5edma-management-system-5ms-/apps/web
npx tsc --noEmit src/pages/Dashboard.tsx 2>&1 | head -20
```

Expected: No errors

- [ ] **Step 3: Commit Phase 4.1**

```bash
cd /root/projects/5edma-management-system-5ms-
git add src/pages/Dashboard.tsx
git commit -m "refactor: update Dashboard to use Coptic components"
```

---

### Task 4.2: Refactor AdminPanel.tsx

**Files:**
- Modify: `/src/pages/AdminPanel.tsx`

- [ ] **Step 1: Update AdminPanel to use Coptic components**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/pages/AdminPanel.tsx << 'EOF'
import React from 'react';
import { GlassCard, CopticButton, GoldBorder } from '../components/coptic';

export default function AdminPanel() {
  const roles = [
    { name: 'Admin', members: 4, permissions: 'All' },
    { name: 'Moderator', members: 12, permissions: 'Moderate' },
    { name: 'Member', members: 231, permissions: 'Standard' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-cream mb-2">Administration</h1>
        <p className="text-text-muted mb-8">Manage roles, permissions, and system settings</p>

        {/* Role Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {roles.map((role) => (
            <GoldBorder key={role.name} position="left">
              <GlassCard className="relative">
                <h3 className="text-lg font-bold text-cream mb-2">{role.name}</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-text-muted text-sm">Members</span>
                    <span className="text-gold-primary font-bold">{role.members}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-text-muted text-sm">Permissions</span>
                    <span className="text-cream text-sm">{role.permissions}</span>
                  </div>
                </div>
                <CopticButton variant="secondary" className="w-full mt-4">
                  Edit Role
                </CopticButton>
              </GlassCard>
            </GoldBorder>
          ))}
        </div>

        {/* System Settings */}
        <GlassCard className="mt-8">
          <h2 className="text-xl font-bold text-cream mb-4">System Settings</h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center py-3 border-b border-navy-light/30">
              <span className="text-cream">Auto-approve registrations</span>
              <input type="checkbox" className="w-5 h-5 accent-gold-primary" />
            </div>
            <div className="flex justify-between items-center py-3 border-b border-navy-light/30">
              <span className="text-cream">Send email notifications</span>
              <input type="checkbox" defaultChecked className="w-5 h-5 accent-gold-primary" />
            </div>
            <div className="flex justify-between items-center py-3">
              <span className="text-cream">Enable API access</span>
              <input type="checkbox" className="w-5 h-5 accent-gold-primary" />
            </div>
          </div>
          <div className="flex justify-end gap-3 mt-6">
            <CopticButton variant="text">Cancel</CopticButton>
            <CopticButton variant="primary">Save Changes</CopticButton>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
EOF
```

- [ ] **Step 2: Verify TypeScript compilation**

```bash
cd /root/projects/5edma-management-system-5ms-/apps/web
npx tsc --noEmit src/pages/AdminPanel.tsx 2>&1 | head -20
```

Expected: No errors

- [ ] **Step 3: Commit Phase 4.2**

```bash
cd /root/projects/5edma-management-system-5ms-
git add src/pages/AdminPanel.tsx
git commit -m "refactor: update AdminPanel to use Coptic components"
```

---

### Task 4.3: Refactor Remaining 10 Pages (Batch)

**Files:**
- Modify: `/src/pages/Users.tsx`
- Modify: `/src/pages/DataManagement.tsx`
- Modify: `/src/pages/AttendanceTracking.tsx`
- Modify: `/src/pages/ReportingAnalytics.tsx`
- Modify: `/src/pages/ImportExport.tsx`
- Modify: `/src/pages/Settings.tsx`
- Modify: `/src/pages/MemberManagement.tsx`
- Modify: `/src/pages/Home.tsx`
- Modify: `/src/pages/Login.tsx`
- Modify: `/src/pages/Registration.tsx`

**Strategy:** For each page, follow this pattern:
1. Import Coptic components at the top
2. Replace old card components with GlassCard
3. Replace buttons with CopticButton
4. Replace inputs with CopticInput
5. Apply design token classes (text-cream, bg-navy-deep, etc.)
6. Test TypeScript compilation
7. Commit per page

- [ ] **Step 1: Refactor Users.tsx**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/pages/Users.tsx << 'EOF'
import React, { useState } from 'react';
import { GlassCard, CopticButton, CopticInput, DataTable } from '../components/coptic';

export default function Users() {
  const [searchQuery, setSearchQuery] = useState('');

  const columns = [
    { key: 'name', label: 'Name' },
    { key: 'email', label: 'Email' },
    { key: 'role', label: 'Role' },
    { key: 'status', label: 'Status' },
  ];

  const users = [
    { name: 'John Doe', email: 'john@example.com', role: 'Admin', status: 'Active' },
    { name: 'Sarah Smith', email: 'sarah@example.com', role: 'Moderator', status: 'Active' },
    { name: 'Michael Brown', email: 'michael@example.com', role: 'Member', status: 'Inactive' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-cream mb-6">User Management</h1>

        <GlassCard>
          <div className="flex gap-4 mb-6">
            <CopticInput
              placeholder="Search users..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-1"
            />
            <CopticButton variant="primary">Add User</CopticButton>
          </div>

          <DataTable columns={columns} data={users} />
        </GlassCard>
      </div>
    </div>
  );
}
EOF
```

- [ ] **Step 2: Refactor DataManagement.tsx**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/pages/DataManagement.tsx << 'EOF'
import React from 'react';
import { GlassCard, CopticButton } from '../components/coptic';

export default function DataManagement() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-cream mb-6">Data Management</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <GlassCard>
            <h3 className="text-lg font-bold text-cream mb-4">Database Backup</h3>
            <p className="text-text-muted mb-4">Last backup: 2 hours ago</p>
            <CopticButton variant="primary" className="w-full">
              Backup Now
            </CopticButton>
          </GlassCard>

          <GlassCard>
            <h3 className="text-lg font-bold text-cream mb-4">Data Integrity</h3>
            <p className="text-text-muted mb-4">Status: ✓ All checks passed</p>
            <CopticButton variant="secondary" className="w-full">
              Run Verification
            </CopticButton>
          </GlassCard>
        </div>
      </div>
    </div>
  );
}
EOF
```

- [ ] **Step 3: Refactor AttendanceTracking.tsx**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/pages/AttendanceTracking.tsx << 'EOF'
import React from 'react';
import { GlassCard, DataTable } from '../components/coptic';

export default function AttendanceTracking() {
  const columns = [
    { key: 'name', label: 'Name' },
    { key: 'time', label: 'Check-in Time' },
    { key: 'status', label: 'Status' },
  ];

  const attendance = [
    { name: 'John Doe', time: '09:05 AM', status: 'On time' },
    { name: 'Sarah Smith', time: '09:32 AM', status: 'Late' },
    { name: 'Michael Brown', time: 'N/A', status: 'Absent' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-cream mb-6">Attendance Tracking</h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <GlassCard variant="stat">
            <div className="text-gold-accent text-xs font-bold uppercase mb-2">Present Today</div>
            <div className="text-3xl font-bold text-cream">45 / 52</div>
          </GlassCard>
          <GlassCard variant="stat">
            <div className="text-gold-accent text-xs font-bold uppercase mb-2">Late</div>
            <div className="text-3xl font-bold text-cream">5</div>
          </GlassCard>
          <GlassCard variant="stat">
            <div className="text-gold-accent text-xs font-bold uppercase mb-2">Absent</div>
            <div className="text-3xl font-bold text-cream">2</div>
          </GlassCard>
        </div>

        <GlassCard>
          <h2 className="text-xl font-bold text-cream mb-4">Today's Attendance</h2>
          <DataTable columns={columns} data={attendance} />
        </GlassCard>
      </div>
    </div>
  );
}
EOF
```

- [ ] **Step 4: Refactor ReportingAnalytics.tsx**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/pages/ReportingAnalytics.tsx << 'EOF'
import React from 'react';
import { GlassCard, CopticButton } from '../components/coptic';

export default function ReportingAnalytics() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-cream mb-6">Reports & Analytics</h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <GlassCard>
            <h3 className="text-lg font-bold text-cream mb-4">Monthly Statistics</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-text-muted">Average Attendance</span>
                <span className="text-gold-primary font-bold">88.5%</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-text-muted">New Members</span>
                <span className="text-gold-primary font-bold">23</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-text-muted">Events Held</span>
                <span className="text-gold-primary font-bold">8</span>
              </div>
            </div>
            <CopticButton variant="secondary" className="w-full mt-4">
              Export Report
            </CopticButton>
          </GlassCard>

          <GlassCard>
            <h3 className="text-lg font-bold text-cream mb-4">Trends</h3>
            <p className="text-text-muted text-sm mb-4">📈 Attendance trending up</p>
            <p className="text-text-muted text-sm mb-4">👥 Member growth: +15% YoY</p>
            <p className="text-text-muted text-sm mb-6">✓ Engagement improving</p>
            <CopticButton variant="primary" className="w-full">
              View Detailed Analytics
            </CopticButton>
          </GlassCard>
        </div>
      </div>
    </div>
  );
}
EOF
```

- [ ] **Step 5: Refactor ImportExport.tsx**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/pages/ImportExport.tsx << 'EOF'
import React from 'react';
import { GlassCard, CopticButton } from '../components/coptic';

export default function ImportExport() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-cream mb-6">Import & Export</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <GlassCard>
            <h3 className="text-lg font-bold text-cream mb-4">Import Data</h3>
            <p className="text-text-muted text-sm mb-6">Upload CSV, Excel, or JSON files</p>
            <div className="border-2 border-dashed border-gold-primary/40 rounded-lg p-8 text-center mb-4">
              <p className="text-text-muted">Drag files here or click to browse</p>
            </div>
            <CopticButton variant="secondary" className="w-full">
              Choose File
            </CopticButton>
          </GlassCard>

          <GlassCard>
            <h3 className="text-lg font-bold text-cream mb-4">Export Data</h3>
            <p className="text-text-muted text-sm mb-6">Download in your preferred format</p>
            <div className="space-y-2">
              <CopticButton variant="secondary" className="w-full">
                Export as CSV
              </CopticButton>
              <CopticButton variant="secondary" className="w-full">
                Export as Excel
              </CopticButton>
              <CopticButton variant="secondary" className="w-full">
                Export as JSON
              </CopticButton>
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
}
EOF
```

- [ ] **Step 6: Refactor Settings.tsx**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/pages/Settings.tsx << 'EOF'
import React, { useState } from 'react';
import { GlassCard, CopticButton, CopticInput } from '../components/coptic';

export default function Settings() {
  const [email, setEmail] = useState('user@example.com');
  const [name, setName] = useState('John Doe');

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h1 className="text-3xl font-bold text-cream mb-6">Settings</h1>

        <GlassCard>
          <h2 className="text-xl font-bold text-cream mb-6">Profile Settings</h2>
          <div className="space-y-4">
            <CopticInput
              label="Full Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
            <CopticInput
              label="Email Address"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <CopticInput label="Phone Number" type="tel" placeholder="+20 1XX XXX XXXX" />
          </div>
          <div className="flex justify-end gap-3 mt-6">
            <CopticButton variant="text">Cancel</CopticButton>
            <CopticButton variant="primary">Save Changes</CopticButton>
          </div>
        </GlassCard>

        <GlassCard className="mt-6">
          <h2 className="text-xl font-bold text-cream mb-6">Preferences</h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-cream">Email notifications</span>
              <input type="checkbox" defaultChecked className="w-5 h-5 accent-gold-primary" />
            </div>
            <div className="flex justify-between items-center">
              <span className="text-cream">Dark mode</span>
              <input type="checkbox" defaultChecked className="w-5 h-5 accent-gold-primary" />
            </div>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
EOF
```

- [ ] **Step 7: Refactor MemberManagement.tsx**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/pages/MemberManagement.tsx << 'EOF'
import React from 'react';
import { GlassCard, CopticButton, DataTable } from '../components/coptic';

export default function MemberManagement() {
  const columns = [
    { key: 'name', label: 'Name' },
    { key: 'joinDate', label: 'Join Date' },
    { key: 'group', label: 'Group' },
    { key: 'status', label: 'Status' },
  ];

  const members = [
    { name: 'John Doe', joinDate: '2024-01-15', group: 'Youth', status: 'Active' },
    { name: 'Sarah Smith', joinDate: '2024-02-20', group: 'Choir', status: 'Active' },
    { name: 'Michael Brown', joinDate: '2023-12-10', group: 'Admin', status: 'Active' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-cream mb-6">Member Management</h1>

        <GlassCard>
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-cream">All Members (247)</h2>
            <CopticButton variant="primary">Add Member</CopticButton>
          </div>
          <DataTable columns={columns} data={members} />
        </GlassCard>
      </div>
    </div>
  );
}
EOF
```

- [ ] **Step 8: Refactor Home.tsx**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/pages/Home.tsx << 'EOF'
import React from 'react';
import { GlassCard, CopticButton } from '../components/coptic';

export default function Home() {
  return (
    <div className="space-y-8">
      <div className="text-center py-12">
        <h1 className="text-5xl font-bold text-cream mb-4">Welcome to 5EDMA</h1>
        <p className="text-text-muted text-lg mb-8">
          Coptic Orthodox Community Management System
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <GlassCard>
          <div className="text-4xl mb-4">👥</div>
          <h3 className="text-lg font-bold text-cream mb-2">Community</h3>
          <p className="text-text-muted text-sm mb-4">
            Connect with fellow members and build meaningful relationships
          </p>
          <CopticButton variant="secondary" className="w-full">
            Explore
          </CopticButton>
        </GlassCard>

        <GlassCard>
          <div className="text-4xl mb-4">📅</div>
          <h3 className="text-lg font-bold text-cream mb-2">Events</h3>
          <p className="text-text-muted text-sm mb-4">
            Stay updated on upcoming community events and activities
          </p>
          <CopticButton variant="secondary" className="w-full">
            View Events
          </CopticButton>
        </GlassCard>

        <GlassCard>
          <div className="text-4xl mb-4">📊</div>
          <h3 className="text-lg font-bold text-cream mb-2">Analytics</h3>
          <p className="text-text-muted text-sm mb-4">
            Track community statistics and engagement metrics
          </p>
          <CopticButton variant="secondary" className="w-full">
            View Reports
          </CopticButton>
        </GlassCard>
      </div>
    </div>
  );
}
EOF
```

- [ ] **Step 9: Refactor Login.tsx**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/pages/Login.tsx << 'EOF'
import React, { useState } from 'react';
import { GlassCard, CopticButton, CopticInput } from '../components/coptic';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  return (
    <div className="flex items-center justify-center min-h-screen bg-navy-bg">
      <GlassCard className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-gold-primary rounded-lg flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl text-navy-bg font-bold">⊕</span>
          </div>
          <h1 className="text-2xl font-bold text-cream">5EDMA</h1>
          <p className="text-text-muted text-sm mt-2">Community Management System</p>
        </div>

        <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
          <CopticInput
            label="Email"
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <CopticInput
            label="Password"
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <CopticButton variant="primary" className="w-full">
            Sign In
          </CopticButton>
        </form>

        <div className="text-center mt-6">
          <p className="text-text-muted text-sm">
            Don't have an account?{' '}
            <a href="/registration" className="text-gold-primary hover:text-gold-accent">
              Sign up
            </a>
          </p>
        </div>
      </GlassCard>
    </div>
  );
}
EOF
```

- [ ] **Step 10: Refactor Registration.tsx**

```bash
cat > /root/projects/5edma-management-system-5ms-/src/pages/Registration.tsx << 'EOF'
import React, { useState } from 'react';
import { GlassCard, CopticButton, CopticInput } from '../components/coptic';

export default function Registration() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-navy-bg">
      <GlassCard className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-gold-primary rounded-lg flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl text-navy-bg font-bold">⊕</span>
          </div>
          <h1 className="text-2xl font-bold text-cream">Create Account</h1>
          <p className="text-text-muted text-sm mt-2">Join our community</p>
        </div>

        <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
          <CopticInput
            label="Full Name"
            placeholder="John Doe"
            name="name"
            value={formData.name}
            onChange={handleChange}
          />
          <CopticInput
            label="Email"
            type="email"
            placeholder="you@example.com"
            name="email"
            value={formData.email}
            onChange={handleChange}
          />
          <CopticInput
            label="Password"
            type="password"
            placeholder="••••••••"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />
          <CopticInput
            label="Confirm Password"
            type="password"
            placeholder="••••••••"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
          />
          <CopticButton variant="primary" className="w-full">
            Create Account
          </CopticButton>
        </form>

        <div className="text-center mt-6">
          <p className="text-text-muted text-sm">
            Already have an account?{' '}
            <a href="/login" className="text-gold-primary hover:text-gold-accent">
              Sign in
            </a>
          </p>
        </div>
      </GlassCard>
    </div>
  );
}
EOF
```

- [ ] **Step 11: Verify all pages compile**

```bash
cd /root/projects/5edma-management-system-5ms-/apps/web
npx tsc --noEmit src/pages/ 2>&1 | head -30
```

Expected: No critical TypeScript errors

- [ ] **Step 12: Batch commit all refactored pages**

```bash
cd /root/projects/5edma-management-system-5ms-
git add src/pages/
git commit -m "refactor: update all 10 pages to use Coptic components and design tokens"
```

---

### Phase 4 Checkpoint

At this point:
- ✅ All 12 pages refactored to use Coptic components
- ✅ Design tokens applied throughout (text-cream, bg-navy-deep, etc.)
- ✅ Navigation integration complete
- ✅ TypeScript validation passes

**Test:** Start dev server, navigate through all pages, verify:
- Navigation sidebar updates based on route
- All components render correctly
- No console errors

```bash
cd /root/projects/5edma-management-system-5ms-/apps/web
npm run dev 2>&1 | grep -E "(ready|compiled|error)" &
sleep 5
curl -s http://localhost:5173 | head -20
```

---

## Phase 5: QA & Polish (Hours 8-9)

### Task 5.1: Test Responsive Design

- [ ] **Step 1: Test mobile layout (375px)**

```bash
# Inspect responsive classes and verify mobile nav behavior
grep -r "hidden sm:" src/pages/ | wc -l
grep -r "md:grid-cols" src/pages/ | wc -l
```

Expected: Multiple responsive classes found

- [ ] **Step 2: Test tablet layout (768px)**

All stat cards should stack in 2x2 grid, sidebar hidden

- [ ] **Step 3: Test desktop layout (1200px)**

Full sidebar visible, all cards in original layout

### Task 5.2: Test Accessibility

- [ ] **Step 1: Verify ARIA labels and semantic HTML**

```bash
grep -r "aria-label" src/components/coptic/
grep -r "semantic" src/components/
```

- [ ] **Step 2: Test keyboard navigation**

Tab through all interactive elements, verify focus states visible

- [ ] **Step 3: Verify color contrast**

Gold on navy-deep and cream on navy-deep should pass WCAG AA

### Task 5.3: Test RTL Support

- [ ] **Step 1: Add RTL attribute to HTML and verify layout**

Open browser devtools, add `dir="rtl"` to `<html>` tag, verify:
- Sidebar aligns to right
- Navigation items align right
- Text flows right-to-left

- [ ] **Step 2: Verify Arabic text renders correctly**

Update a label to Arabic text and confirm rendering

### Task 5.4: Polish and Final Touches

- [ ] **Step 1: Verify hover states work smoothly**

All buttons, links, and cards should have smooth transitions on hover

- [ ] **Step 2: Check for console errors**

```bash
cd /root/projects/5edma-management-system-5ms-/apps/web
npm run build 2>&1 | tail -30
```

Expected: No critical errors, warnings are acceptable

- [ ] **Step 3: Verify component transitions**

All transitions should use `transition-all duration-300` for consistency

- [ ] **Step 4: Final visual inspection**

Walk through entire app manually:
- Check all colors match design system
- Verify gold accents present on key elements
- Confirm glass effect visible on cards
- Verify corner arches render on stat cards
- Check responsive breakpoints work

- [ ] **Step 5: Commit Phase 5**

```bash
cd /root/projects/5edma-management-system-5ms-
git status
```

If any polish changes were made:

```bash
git add -A
git commit -m "polish: responsive design, accessibility, and RTL testing"
```

---

### Phase 5 Checkpoint & Deployment

- ✅ Responsive design tested (mobile, tablet, desktop)
- ✅ Accessibility verified (ARIA, keyboard nav, contrast)
- ✅ RTL support validated
- ✅ No console errors
- ✅ All transitions smooth
- ✅ Visual design matches specification

**Final Build Test:**

```bash
cd /root/projects/5edma-management-system-5ms-/apps/web
npm run build 2>&1 | grep -E "(dist|error|warning)" | tail -10
```

Expected: Build succeeds, dist folder created

**Deploy:**

```bash
# Push to main branch
cd /root/projects/5edma-management-system-5ms-
git log --oneline | head -5
git push origin rebuild/modern-stack
```

---

## Summary of Commits

Total commits in this implementation:

1. **Phase 1.1:** Create Coptic design system with color tokens and typography
2. **Phase 1.2:** Update global styles with Coptic design system and Google Fonts
3. **Phase 1.3:** Extend Tailwind config with Coptic design tokens
4. **Phase 2.1:** Create coptic components directory structure
5. **Phase 2.2:** Add GlassCard component with three variants
6. **Phase 2.3:** Add CopticButton component with five variants
7. **Phase 2.4:** Add CopticInput component with gold underline
8. **Phase 2.5:** Add CopticSelect, CopticSearch, CornerArch, GoldBorder, and DataTable components
9. **Phase 3.1:** Create NavigationContext and type definitions
10. **Phase 3.2:** Add TopBar component with compact logo and user menu
11. **Phase 3.3:** Add NavigationSidebar component with context-aware content
12. **Phase 3.4:** Add hybrid navigation shell with TopBar and NavigationSidebar
13. **Phase 4:** Update all 10 pages to use Coptic components and design tokens
14. **Phase 5:** Polish: responsive design, accessibility, and RTL testing

**Total: 14 git commits (can be combined into fewer if preferred)**

---

## Checklist for Implementation

- [ ] Phase 1 complete: Design tokens loaded globally
- [ ] Phase 2 complete: Component library functional and imported
- [ ] Phase 3 complete: Navigation shell renders and routes work
- [ ] Phase 4 complete: All pages refactored and displaying new design
- [ ] Phase 5 complete: Responsive design tested, no console errors, ready to deploy
- [ ] All tests passing
- [ ] Code pushed to branch
- [ ] Ready for PR review

---

## Files Modified Summary

**Created:** 16 files  
**Modified:** 12 files  
**Total Changes:** 28 files

**Lines of Code Added:** ~2,500 lines (design tokens, components, pages)

---

## Time Estimate

- Phase 1: 2 hours
- Phase 2: 1 hour
- Phase 3: 2 hours
- Phase 4: 3 hours (parallelizable: can split 10 pages across team)
- Phase 5: 1 hour

**Total: 9 hours (accelerated 1-day launch)**

With parallelization (4 developers on Phase 4 pages): **~6-7 hours actual wall-clock time**
