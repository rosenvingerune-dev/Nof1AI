# Migration Plan: NiceGUI → FastAPI + React

**Dato:** 2026-01-03
**Beslutning:** Migrere fra NiceGUI til FastAPI (backend) + React (frontend)
**Grunn:** NiceGUI memory leaks, ingen lifecycle hooks, zombie prosesser på Windows

---

## 🎯 MÅL

### Funksjonelle Mål
- Beholde all eksisterende funksjonalitet
- Forbedre responsivitet og ytelse
- Få ekte real-time updates via WebSocket
- Mulighet for automatisert testing (E2E med Playwright)

### Tekniske Mål
- Skille backend og frontend fullstendig
- Gjenbruke EventBus-arkitekturen (allerede implementert)
- Modern React stack med TypeScript
- REST API + WebSocket for real-time

### Ytelsesmål
- Initial load: <2s
- Page navigation: <100ms (ingen reload)
- Real-time updates: <50ms latency
- Memory footprint: <200MB (frontend + backend)

---

## 📋 TEKNOLOGI-STACK

### Backend (Python)
```yaml
Framework: FastAPI 0.109+
WebSocket: FastAPI native WebSocket support
Real-time: EventBus (eksisterende) → WebSocket broadcast
API Docs: Swagger/OpenAPI (auto-generert)
CORS: FastAPI CORS middleware
Authentication: JWT tokens (hvis nødvendig)
```

### Frontend (React)
```yaml
Framework: React 18+ med TypeScript
Build Tool: Vite (rask dev server + build)
State Management: Zustand (lightweight, ikke Redux)
UI Library: shadcn/ui + Tailwind CSS (moderne, tilpassbart)
Charts: Recharts eller ApexCharts
WebSocket: native WebSocket API
HTTP Client: Axios eller fetch
```

### Development Tools
```yaml
Backend Testing: pytest (eksisterende)
Frontend Testing: Vitest + React Testing Library
E2E Testing: Playwright
Linting: ESLint (frontend), Ruff (backend)
Type Checking: TypeScript (frontend), mypy (backend)
```

---

## 🏗️ ARKITEKTUR OVERSIKT

### Current Architecture (NiceGUI)
```
┌─────────────────────────────────────┐
│         NiceGUI (Monolith)          │
│  ┌──────────┐      ┌──────────┐    │
│  │ Python   │◄────►│ FastAPI  │    │
│  │ UI Code  │      │ Backend  │    │
│  └──────────┘      └──────────┘    │
│       ▲                             │
│       │ WebSocket (implicit)        │
│       ▼                             │
│  ┌──────────┐                       │
│  │ Browser  │                       │
│  │ (Vue.js) │                       │
│  └──────────┘                       │
└─────────────────────────────────────┘
```

### New Architecture (FastAPI + React)
```
┌──────────────────────┐         ┌──────────────────────┐
│   React Frontend     │         │  FastAPI Backend     │
│                      │         │                      │
│  ┌────────────────┐  │         │  ┌────────────────┐  │
│  │ UI Components  │  │         │  │  REST API      │  │
│  │  (TypeScript)  │  │         │  │  /api/v1/...   │  │
│  └────────────────┘  │         │  └────────────────┘  │
│         │            │         │         ▲            │
│         ▼            │         │         │            │
│  ┌────────────────┐  │  HTTP   │  ┌────────────────┐  │
│  │  Zustand Store │◄─┼─────────┼─►│  BotService    │  │
│  │  (State Mgmt)  │  │  REST   │  │  StateManager  │  │
│  └────────────────┘  │         │  └────────────────┘  │
│         ▲            │         │         ▲            │
│         │            │         │         │            │
│         │ WebSocket  │         │  ┌────────────────┐  │
│         └────────────┼─────────┼─►│   EventBus     │  │
│                      │  WS     │  │  (Existing!)   │  │
│  ┌────────────────┐  │         │  └────────────────┘  │
│  │  Charts/Tables │  │         │         │            │
│  │  (Recharts)    │  │         │         ▼            │
│  └────────────────┘  │         │  ┌────────────────┐  │
│                      │         │  │  Bot Engine    │  │
└──────────────────────┘         │  │  Trading API   │  │
    Served by Vite                  └────────────────┘  │
    (dev: :5173)                         │              │
    (prod: static files)          └──────┼──────────────┘
                                         │
                                         ▼
                                  ┌────────────────┐
                                  │   Database     │
                                  │   (SQLite)     │
                                  └────────────────┘
```

---

## 📅 MIGRASJONSPLAN - 4 UKER

### **UKE 1: Backend API Foundation**

#### Dag 1-2: FastAPI Setup + Core Endpoints
**Mål:** Sette opp FastAPI backend med basis-endpoints

**Tasks:**
- [ ] Installer FastAPI + Uvicorn
  ```bash
  pip install fastapi[all] uvicorn[standard] python-multipart
  ```
- [ ] Opprett `src/api/` struktur:
  ```
  src/api/
  ├── __init__.py
  ├── main.py              # FastAPI app entry point
  ├── dependencies.py      # DI for services
  ├── middleware.py        # CORS, logging
  └── routes/
      ├── __init__.py
      ├── bot.py           # Bot control endpoints
      ├── positions.py     # Positions endpoints
      ├── trades.py        # Trade history endpoints
      ├── market.py        # Market data endpoints
      └── settings.py      # Settings endpoints
  ```
- [ ] Implementer core REST endpoints:
  ```python
  # GET /api/v1/bot/status
  # POST /api/v1/bot/start
  # POST /api/v1/bot/stop
  # GET /api/v1/positions
  # GET /api/v1/trades?limit=50&offset=0
  # GET /api/v1/market/data
  # GET /api/v1/settings
  # PUT /api/v1/settings
  ```
- [ ] Gjenbruk `BotService`, `StateManager` fra eksisterende kode
- [ ] Legg til CORS middleware for React dev server
- [ ] Valider med Swagger UI (`/docs`)

**Filer å lage:**
- `src/api/main.py` (~150 linjer)
- `src/api/routes/bot.py` (~100 linjer)
- `src/api/routes/positions.py` (~80 linjer)
- `src/api/routes/trades.py` (~100 linjer)
- `src/api/routes/market.py` (~120 linjer)
- `src/api/routes/settings.py` (~80 linjer)
- `src/api/dependencies.py` (~50 linjer)

**Suksess-kriterier:**
- ✅ Swagger UI viser alle endpoints
- ✅ `GET /api/v1/bot/status` returnerer BotState JSON
- ✅ `POST /api/v1/bot/start` starter bot engine
- ✅ CORS tillater requests fra `localhost:5173`

---

#### Dag 3-4: WebSocket Integration
**Mål:** Real-time updates via WebSocket

**Tasks:**
- [ ] Opprett WebSocket endpoint `/ws`
- [ ] Koble EventBus til WebSocket broadcaster:
  ```python
  # src/api/websocket.py
  class ConnectionManager:
      def __init__(self):
          self.active_connections: List[WebSocket] = []
          self.event_bus = get_event_bus()
          self._subscribe_to_events()

      def _subscribe_to_events(self):
          """Subscribe to EventBus and broadcast to all WS clients"""
          self.event_bus.subscribe(EventTypes.STATE_UPDATE, self.broadcast)
          self.event_bus.subscribe(EventTypes.TRADE_EXECUTED, self.broadcast)
          # ...

      async def broadcast(self, message: dict):
          """Send message to all connected clients"""
          for connection in self.active_connections:
              await connection.send_json(message)
  ```
- [ ] Test med `websocat` eller browser console:
  ```javascript
  const ws = new WebSocket('ws://localhost:8000/ws');
  ws.onmessage = (e) => console.log(JSON.parse(e.data));
  ```
- [ ] Implementer reconnection logic (backend)
- [ ] Dokumenter WebSocket message format

**Filer å lage:**
- `src/api/websocket.py` (~150 linjer)
- `src/api/routes/websocket.py` (~80 linjer)

**Suksess-kriterier:**
- ✅ WebSocket connection etableres
- ✅ EventBus events broadcastes til alle klienter
- ✅ Message format er dokumentert (JSON schema)
- ✅ Reconnection fungerer etter disconnect

---

#### Dag 5: API Testing + Documentation
**Mål:** Sikre API kvalitet før frontend-utvikling

**Tasks:**
- [ ] Skriv pytest tests for alle endpoints:
  ```python
  # tests/api/test_bot_routes.py
  def test_get_bot_status(client):
      response = client.get("/api/v1/bot/status")
      assert response.status_code == 200
      assert "is_running" in response.json()

  def test_start_bot(client):
      response = client.post("/api/v1/bot/start")
      assert response.status_code == 200
  ```
- [ ] Test WebSocket med pytest-asyncio
- [ ] Generer OpenAPI spec til fil:
  ```bash
  curl http://localhost:8000/openapi.json > docs/api-spec.json
  ```
- [ ] Lag Postman collection (optional)
- [ ] Dokumenter rate limits (hvis nødvendig)

**Filer å lage:**
- `tests/api/test_bot_routes.py` (~200 linjer)
- `tests/api/test_positions_routes.py` (~150 linjer)
- `tests/api/test_websocket.py` (~100 linjer)
- `docs/API.md` (dokumentasjon)

**Suksess-kriterier:**
- ✅ 100% test coverage på API routes
- ✅ Alle tests passerer (`pytest tests/api/`)
- ✅ OpenAPI spec er generert
- ✅ API dokumentasjon er komplett

---

### **UKE 2: Frontend Setup + Core Pages**

#### Dag 6-7: React Project Setup
**Mål:** Sette opp moderne React project med TypeScript

**Tasks:**
- [ ] Opprett React app med Vite:
  ```bash
  npm create vite@latest frontend -- --template react-ts
  cd frontend
  npm install
  ```
- [ ] Installer dependencies:
  ```bash
  npm install axios zustand recharts lucide-react
  npm install -D tailwindcss postcss autoprefixer
  npm install -D @types/node
  npx tailwindcss init -p
  ```
- [ ] Installer shadcn/ui:
  ```bash
  npx shadcn-ui@latest init
  npx shadcn-ui@latest add button card table input
  ```
- [ ] Opprett mappestruktur:
  ```
  frontend/
  ├── src/
  │   ├── api/
  │   │   ├── client.ts         # Axios instance
  │   │   └── endpoints.ts      # API functions
  │   ├── components/
  │   │   ├── ui/               # shadcn components
  │   │   ├── Header.tsx
  │   │   ├── Sidebar.tsx
  │   │   └── MetricCard.tsx
  │   ├── pages/
  │   │   ├── Dashboard.tsx
  │   │   ├── Positions.tsx
  │   │   ├── History.tsx
  │   │   ├── Market.tsx
  │   │   ├── Reasoning.tsx
  │   │   ├── Settings.tsx
  │   │   └── Logs.tsx
  │   ├── stores/
  │   │   ├── useBotStore.ts    # Zustand store
  │   │   └── useWebSocket.ts   # WS hook
  │   ├── types/
  │   │   └── index.ts          # TypeScript types
  │   ├── App.tsx
  │   └── main.tsx
  ├── package.json
  ├── tsconfig.json
  ├── vite.config.ts
  └── tailwind.config.js
  ```
- [ ] Konfigurer Vite proxy til backend:
  ```typescript
  // vite.config.ts
  export default defineConfig({
    server: {
      proxy: {
        '/api': 'http://localhost:8000',
        '/ws': {
          target: 'ws://localhost:8000',
          ws: true
        }
      }
    }
  })
  ```
- [ ] Definer TypeScript types fra backend modeller:
  ```typescript
  // src/types/index.ts
  export interface BotState {
    is_running: boolean;
    balance: number;
    total_pnl: number;
    positions: Position[];
    // ... match Python BotState
  }
  ```

**Suksess-kriterier:**
- ✅ `npm run dev` starter utviklingsserver på `:5173`
- ✅ Tailwind CSS fungerer
- ✅ shadcn/ui komponenter er tilgjengelige
- ✅ TypeScript kompilerer uten feil
- ✅ Vite proxy til backend fungerer

---

#### Dag 8-9: Core Components + State Management
**Mål:** Bygge gjenbrukbare komponenter og state management

**Tasks:**
- [ ] Implementer Zustand store:
  ```typescript
  // src/stores/useBotStore.ts
  import create from 'zustand';

  interface BotStore {
    state: BotState | null;
    setState: (state: BotState) => void;
    startBot: () => Promise<void>;
    stopBot: () => Promise<void>;
  }

  export const useBotStore = create<BotStore>((set) => ({
    state: null,
    setState: (state) => set({ state }),
    startBot: async () => {
      await api.startBot();
      // state oppdateres via WebSocket
    },
    stopBot: async () => {
      await api.stopBot();
    }
  }));
  ```
- [ ] Implementer WebSocket hook:
  ```typescript
  // src/stores/useWebSocket.ts
  export function useWebSocket() {
    const { setState } = useBotStore();

    useEffect(() => {
      const ws = new WebSocket('ws://localhost:8000/ws');

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'STATE_UPDATE') {
          setState(data.data);
        }
      };

      return () => ws.close();
    }, []);
  }
  ```
- [ ] Lag Header komponent (migrer fra NiceGUI):
  ```typescript
  // src/components/Header.tsx
  export function Header() {
    const { state, startBot, stopBot } = useBotStore();

    return (
      <header className="bg-slate-900 border-b border-slate-800 p-4">
        <div className="flex justify-between items-center">
          <h1>NOF1 AI Trading Bot</h1>
          <div className="flex gap-4">
            <span>Balance: ${state?.balance.toFixed(2)}</span>
            <button onClick={state?.is_running ? stopBot : startBot}>
              {state?.is_running ? 'Stop' : 'Start'}
            </button>
          </div>
        </div>
      </header>
    );
  }
  ```
- [ ] Lag Sidebar komponent (React Router)
- [ ] Lag MetricCard komponent (gjenbrukbar)
- [ ] Sett opp React Router:
  ```bash
  npm install react-router-dom
  ```

**Filer å lage:**
- `src/stores/useBotStore.ts` (~150 linjer)
- `src/stores/useWebSocket.ts` (~100 linjer)
- `src/api/client.ts` (~80 linjer)
- `src/api/endpoints.ts` (~200 linjer)
- `src/components/Header.tsx` (~100 linjer)
- `src/components/Sidebar.tsx` (~120 linjer)
- `src/components/MetricCard.tsx` (~50 linjer)

**Suksess-kriterier:**
- ✅ WebSocket kobler til backend
- ✅ State oppdateres real-time
- ✅ Start/Stop knapper fungerer
- ✅ Navigasjon mellom sider fungerer
- ✅ Komponenter renderer riktig

---

#### Dag 10: Dashboard Page
**Mål:** Implementer Dashboard med metrics og charts

**Tasks:**
- [ ] Migrer Dashboard layout fra `dashboard_reactive.py`:
  ```typescript
  // src/pages/Dashboard.tsx
  export function Dashboard() {
    const { state } = useBotStore();

    return (
      <div className="grid grid-cols-4 gap-6">
        <MetricCard
          title="Total Balance"
          value={`$${state?.balance.toFixed(2)}`}
        />
        <MetricCard
          title="Total PnL"
          value={`$${state?.total_pnl.toFixed(2)}`}
          trend={state?.total_pnl >= 0 ? 'up' : 'down'}
        />
        {/* ... mer metrics */}

        <div className="col-span-4">
          <BalanceChart data={state?.balance_history} />
        </div>
      </div>
    );
  }
  ```
- [ ] Implementer BalanceChart med Recharts:
  ```typescript
  import { LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';

  export function BalanceChart({ data }) {
    return (
      <LineChart width={800} height={400} data={data}>
        <XAxis dataKey="timestamp" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="balance" stroke="#10b981" />
      </LineChart>
    );
  }
  ```
- [ ] Legg til activity log (real-time fra WebSocket)
- [ ] Implementer market data view
- [ ] Test responsivitet (mobile/tablet)

**Filer å lage:**
- `src/pages/Dashboard.tsx` (~300 linjer)
- `src/components/BalanceChart.tsx` (~100 linjer)
- `src/components/ActivityLog.tsx` (~80 linjer)

**Suksess-kriterier:**
- ✅ Dashboard viser metrics korrekt
- ✅ Charts renderer med real data
- ✅ Real-time updates fra WebSocket
- ✅ Responsiv design fungerer

---

### **UKE 3: Remaining Pages + Advanced Features**

#### Dag 11-12: Positions + History Pages
**Mål:** Implementer Positions og History med lazy loading

**Tasks:**
- [ ] Implementer Positions tabell:
  ```typescript
  // src/pages/Positions.tsx
  import { Table } from '@/components/ui/table';

  export function Positions() {
    const { state } = useBotStore();

    return (
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Asset</TableHead>
            <TableHead>Amount</TableHead>
            <TableHead>Entry Price</TableHead>
            <TableHead>Current Price</TableHead>
            <TableHead>PnL</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {state?.positions.map((pos) => (
            <TableRow key={pos.id}>
              <TableCell>{pos.asset}</TableCell>
              <TableCell>{pos.amount}</TableCell>
              {/* ... */}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    );
  }
  ```
- [ ] Implementer History med infinite scroll:
  ```typescript
  // src/pages/History.tsx
  import { useInfiniteQuery } from '@tanstack/react-query';

  export function History() {
    const {
      data,
      fetchNextPage,
      hasNextPage
    } = useInfiniteQuery({
      queryKey: ['trades'],
      queryFn: ({ pageParam = 0 }) =>
        api.getTrades({ offset: pageParam, limit: 50 }),
      getNextPageParam: (lastPage, pages) =>
        lastPage.length === 50 ? pages.length * 50 : undefined
    });

    return (
      <div>
        <Table>{/* render trades */}</Table>
        {hasNextPage && (
          <Button onClick={() => fetchNextPage()}>
            Load More
          </Button>
        )}
      </div>
    );
  }
  ```
- [ ] Installer React Query:
  ```bash
  npm install @tanstack/react-query
  ```
- [ ] Legg til filtering (asset, action)
- [ ] Eksporter til CSV funksjon

**Filer å lage:**
- `src/pages/Positions.tsx` (~200 linjer)
- `src/pages/History.tsx` (~250 linjer)
- `src/hooks/useInfiniteScroll.ts` (~80 linjer)

**Suksess-kriterier:**
- ✅ Positions oppdateres real-time
- ✅ History lazy loading fungerer
- ✅ Infinite scroll loader ingen lag
- ✅ CSV export fungerer

---

#### Dag 13: Market, Reasoning, Settings Pages
**Mål:** Implementer resterende sider

**Tasks:**
- [ ] Migrer Market page (market data + sentiments)
- [ ] Migrer Reasoning page (AI reasoning display)
- [ ] Migrer Settings page (form med validation):
  ```typescript
  import { useForm } from 'react-hook-form';
  import { zodResolver } from '@hookform/resolvers/zod';
  import * as z from 'zod';

  const settingsSchema = z.object({
    api_key: z.string().min(1),
    risk_per_trade: z.number().min(0.01).max(1.0),
    // ...
  });

  export function Settings() {
    const { register, handleSubmit } = useForm({
      resolver: zodResolver(settingsSchema)
    });

    const onSubmit = async (data) => {
      await api.updateSettings(data);
    };

    return <form onSubmit={handleSubmit(onSubmit)}>{/* ... */}</form>;
  }
  ```
- [ ] Installer form dependencies:
  ```bash
  npm install react-hook-form zod @hookform/resolvers/zod
  ```

**Filer å lage:**
- `src/pages/Market.tsx` (~250 linjer)
- `src/pages/Reasoning.tsx` (~180 linjer)
- `src/pages/Settings.tsx` (~300 linjer)

**Suksess-kriterier:**
- ✅ Alle 8 sider migrert
- ✅ Form validation fungerer
- ✅ Settings lagres korrekt

---

#### Dag 14: Logs + Notifications
**Mål:** Real-time logs og toast notifications

**Tasks:**
- [ ] Implementer Logs med WebSocket (ikke file polling!):
  ```typescript
  // Backend sender log lines via WebSocket
  // Frontend appender til list (virtual scrolling)
  export function Logs() {
    const [logs, setLogs] = useState<string[]>([]);

    useEffect(() => {
      const ws = new WebSocket('ws://localhost:8000/ws/logs');
      ws.onmessage = (e) => {
        setLogs((prev) => [...prev, e.data].slice(-1000)); // Keep last 1000
      };
    }, []);

    return <VirtualList items={logs} />;
  }
  ```
- [ ] Installer toast library:
  ```bash
  npx shadcn-ui@latest add toast
  ```
- [ ] Legg til notifications for:
  - Trade executed
  - Bot started/stopped
  - Errors
  ```typescript
  // src/stores/useNotifications.ts
  export function useNotifications() {
    const { toast } = useToast();

    useEffect(() => {
      const ws = new WebSocket('ws://localhost:8000/ws');
      ws.onmessage = (e) => {
        const data = JSON.parse(e.data);
        if (data.type === 'TRADE_EXECUTED') {
          toast({
            title: 'Trade Executed',
            description: `${data.action} ${data.asset}`
          });
        }
      };
    }, []);
  }
  ```

**Filer å lage:**
- `src/pages/Logs.tsx` (~150 linjer)
- `src/stores/useNotifications.ts` (~100 linjer)
- `src/components/VirtualList.tsx` (~120 linjer)

**Suksess-kriterier:**
- ✅ Logs streames i real-time
- ✅ Virtual scrolling håndterer 1000+ linjer
- ✅ Toast notifications vises korrekt

---

### **UKE 4: Testing, Polish, Deployment**

#### Dag 15-16: Testing
**Mål:** Comprehensive testing suite

**Tasks:**
- [ ] Unit tests for komponenter (Vitest):
  ```typescript
  // src/components/MetricCard.test.tsx
  import { render, screen } from '@testing-library/react';
  import { MetricCard } from './MetricCard';

  test('renders metric value', () => {
    render(<MetricCard title="Balance" value="$1,000" />);
    expect(screen.getByText('$1,000')).toBeInTheDocument();
  });
  ```
- [ ] Integration tests for stores
- [ ] E2E tests med Playwright:
  ```typescript
  // e2e/dashboard.spec.ts
  import { test, expect } from '@playwright/test';

  test('dashboard loads and displays metrics', async ({ page }) => {
    await page.goto('http://localhost:5173');
    await expect(page.locator('h1')).toContainText('Dashboard');
    await expect(page.locator('.metric-card')).toHaveCount(4);
  });
  ```
- [ ] Installer testing tools:
  ```bash
  npm install -D vitest @testing-library/react @testing-library/jest-dom
  npm install -D playwright @playwright/test
  npx playwright install
  ```
- [ ] WebSocket mocking for tests

**Filer å lage:**
- `src/**/*.test.tsx` (~500 linjer totalt)
- `e2e/**/*.spec.ts` (~300 linjer)
- `vitest.config.ts`
- `playwright.config.ts`

**Suksess-kriterier:**
- ✅ 80%+ test coverage
- ✅ Alle E2E tests passerer
- ✅ CI pipeline kjører tests automatisk

---

#### Dag 17: Performance Optimization
**Mål:** Optimalisere ytelse

**Tasks:**
- [ ] Code splitting (React.lazy):
  ```typescript
  const Dashboard = lazy(() => import('./pages/Dashboard'));
  const Positions = lazy(() => import('./pages/Positions'));
  ```
- [ ] Memo/useMemo for heavy beregninger
- [ ] Virtual scrolling for lange lister (react-window)
- [ ] Debounce/throttle på filters
- [ ] Bundle size analyse:
  ```bash
  npm run build
  npx vite-bundle-visualizer
  ```
- [ ] Lighthouse audit (target: 90+ score)
- [ ] Implementer service worker for offline support (optional)

**Suksess-kriterier:**
- ✅ Initial load <2s
- ✅ Bundle size <500KB (gzipped)
- ✅ Lighthouse score 90+
- ✅ Smooth 60fps scrolling

---

#### Dag 18: UI Polish + Dark Mode
**Mål:** Finpusse UI/UX

**Tasks:**
- [ ] Implementer dark mode toggle:
  ```typescript
  // src/components/ThemeToggle.tsx
  export function ThemeToggle() {
    const [theme, setTheme] = useState('dark');

    useEffect(() => {
      document.documentElement.classList.toggle('dark', theme === 'dark');
    }, [theme]);

    return <button onClick={() => setTheme(t => t === 'dark' ? 'light' : 'dark')}>
      {theme === 'dark' ? '☀️' : '🌙'}
    </button>;
  }
  ```
- [ ] Legg til loading skeletons
- [ ] Forbedre error states
- [ ] Legg til empty states (ingen trades ennå, etc.)
- [ ] Animasjoner (framer-motion - optional):
  ```bash
  npm install framer-motion
  ```
- [ ] Accessibility audit (keyboard navigation, ARIA labels)

**Suksess-kriterier:**
- ✅ Dark/light mode fungerer
- ✅ Loading states for alle API calls
- ✅ Keyboard navigation fungerer
- ✅ WCAG 2.1 AA compliant

---

#### Dag 19-20: Deployment + Documentation
**Mål:** Produksjonsklart deployment

**Tasks:**
- [ ] Build frontend for produksjon:
  ```bash
  cd frontend
  npm run build
  # Output: frontend/dist/
  ```
- [ ] Serve static files fra FastAPI:
  ```python
  # src/api/main.py
  from fastapi.staticfiles import StaticFiles

  app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="frontend")
  ```
- [ ] Oppdater README.md:
  - Installation instructions
  - Development setup
  - Production deployment
  - Architecture diagram
- [ ] Lag deployment scripts:
  ```bash
  # scripts/deploy.sh
  #!/bin/bash
  cd frontend && npm run build && cd ..
  pip install -r requirements.txt
  uvicorn src.api.main:app --host 0.0.0.0 --port 8000
  ```
- [ ] Docker setup (optional):
  ```dockerfile
  # Dockerfile
  FROM python:3.10

  # Install Node.js
  RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
  RUN apt-get install -y nodejs

  # Build frontend
  WORKDIR /app/frontend
  COPY frontend/package*.json ./
  RUN npm install
  COPY frontend/ ./
  RUN npm run build

  # Setup backend
  WORKDIR /app
  COPY requirements.txt ./
  RUN pip install -r requirements.txt
  COPY src/ ./src/

  CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```
- [ ] Environment variables setup (.env):
  ```env
  DATABASE_URL=sqlite:///./data/trading.db
  HYPERLIQUID_API_KEY=xxx
  OPENAI_API_KEY=xxx
  ```
- [ ] Health check endpoint:
  ```python
  @app.get("/health")
  async def health():
      return {"status": "ok", "version": "2.0.0"}
  ```

**Filer å lage:**
- `README.md` (oppdatert, ~200 linjer)
- `ARCHITECTURE.md` (ny, ~150 linjer)
- `scripts/deploy.sh`
- `Dockerfile` (optional)
- `docker-compose.yml` (optional)
- `.env.example`

**Suksess-kriterier:**
- ✅ Production build fungerer
- ✅ FastAPI server static files
- ✅ Dokumentasjon er komplett
- ✅ Deployment script fungerer
- ✅ Health check responderer

---

## 🔧 GJENBRUK AV EKSISTERENDE KODE

### Hva kan gjenbrukes direkte? (Minimal endring)

✅ **Backend Services (100% gjenbruk):**
- `src/backend/bot_engine.py` - Bot logic
- `src/backend/trading_api.py` - Hyperliquid integration
- `src/backend/ai/` - All AI reasoning logic
- `src/database/` - Database models og queries
- `src/gui/services/event_bus.py` - EventBus (nøkkelkomponent!)
- `src/gui/services/state_manager.py` - State management
- `src/gui/services/bot_service.py` - Business logic
- `src/gui/services/cache_manager.py` - Caching

✅ **Data Structures (100% gjenbruk):**
- `BotState` dataclass
- `Position`, `Trade` models
- All database schemas

✅ **Configuration (100% gjenbruk):**
- `config.yaml`
- `.env` settings

### Hva må skrives på nytt? (React komponenter)

❌ **UI Components (0% gjenbruk):**
- All NiceGUI kode må skrives om til React
- Men: Logikken kan kopieres nesten 1:1
- Eksempel mapping:
  ```python
  # NiceGUI (OLD)
  with ui.card():
      ui.label('Balance').classes('text-xl')
      ui.label(f'${balance}').classes('text-3xl font-bold')
  ```
  ```typescript
  // React (NEW)
  <Card>
    <CardHeader className="text-xl">Balance</CardHeader>
    <CardContent className="text-3xl font-bold">
      ${balance}
    </CardContent>
  </Card>
  ```

### Estimat Kodelinjer

| Kategori | Gjenbruk | Ny kode | Totalt |
|----------|----------|---------|--------|
| Backend (Python) | 3,500 | 800 (API routes) | 4,300 |
| Frontend (TypeScript) | 0 | 3,500 (React) | 3,500 |
| Tests | 500 | 800 | 1,300 |
| Config/Docs | 200 | 300 | 500 |
| **TOTALT** | **4,200** | **5,400** | **9,600** |

**Estimert arbeidstid:**
- Backend API: 5 dager (allerede har business logic)
- Frontend React: 10 dager (UI from scratch)
- Testing + Polish: 3 dager
- Deployment: 2 dager
- **Total: ~4 uker (20 arbeidsdager)**

---

## 📊 FORVENTET YTELSE

### Current (NiceGUI)
```
CPU (idle):           80%  (8 timers polling!)
CPU (active):         95%
Memory:               450MB
Initial load:         8s   (10,000 trades)
Page navigation:      1.5s (full rebuild)
Update latency:       2-10s (timer interval)
Memory leak:          +50MB/hour (zombie handlers)
```

### Target (React + FastAPI)
```
CPU (idle):           5%   (no polling, only WS)
CPU (active):         20%  (efficient rendering)
Memory:               180MB (no zombie handlers)
Initial load:         1.2s (lazy loading)
Page navigation:      80ms (SPA, no rebuild)
Update latency:       <50ms (WebSocket direct)
Memory leak:          0MB/hour (proper cleanup)
```

### Performance Gains
- **94% CPU reduction** (80% → 5%)
- **60% memory reduction** (450MB → 180MB)
- **85% faster initial load** (8s → 1.2s)
- **95% faster navigation** (1.5s → 80ms)
- **200x faster updates** (2-10s → 50ms)

---

## 🚨 RISIKO ANALYSE

### Høy Risiko
| Risiko | Sannsynlighet | Impact | Mitigering |
|--------|---------------|--------|------------|
| WebSocket connection drops | Medium | High | Auto-reconnect logic + fallback polling |
| CORS issues i produksjon | Medium | High | Test med production-like setup tidlig |
| State sync issues (WS vs REST) | Low | High | Single source of truth (Zustand) |

### Medium Risiko
| Risiko | Sannsynlighet | Impact | Mitigering |
|--------|---------------|--------|------------|
| TypeScript type mismatch | High | Medium | Generate types from OpenAPI spec |
| React re-render performance | Medium | Medium | React.memo, useMemo, profiling |
| Deployment complexity | Medium | Medium | Docker image + deploy script |

### Lav Risiko
| Risiko | Sannsynlighet | Impact | Mitigering |
|--------|---------------|--------|------------|
| UI/UX regression | Low | Low | Screenshot comparison tests |
| Bundle size bloat | Low | Medium | Bundle analyzer, code splitting |

---

## ✅ SUKSESS-KRITERIER

### Funksjonelle Krav
- [ ] All eksisterende funksjonalitet fungerer identisk
- [ ] Ingen regresjoner i trading logic
- [ ] Real-time updates <100ms latency
- [ ] Alle 8 sider migrert og fungerer

### Tekniske Krav
- [ ] CPU idle <10%
- [ ] Memory <200MB
- [ ] Initial load <2s
- [ ] Page navigation <200ms
- [ ] 80%+ test coverage
- [ ] Zero memory leaks (tested over 8 hours)

### Brukeropplevelse
- [ ] Ingen merkbar forsinkelse på UI updates
- [ ] Smooth scrolling og animasjoner (60fps)
- [ ] Responsiv design (desktop + tablet)
- [ ] Dark mode support
- [ ] Keyboard navigation fungerer

### Deployment
- [ ] Single command deployment (`scripts/deploy.sh`)
- [ ] Health check endpoint fungerer
- [ ] Dokumentasjon er komplett
- [ ] Docker image bygger uten feil (optional)

---

## 📚 RESSURSER

### Dokumentasjon
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- Vite: https://vitejs.dev/
- shadcn/ui: https://ui.shadcn.com/
- Zustand: https://github.com/pmndrs/zustand
- React Query: https://tanstack.com/query/latest
- Recharts: https://recharts.org/

### Tutorials (anbefalt)
- FastAPI WebSocket: https://fastapi.tiangolo.com/advanced/websockets/
- React + TypeScript: https://react-typescript-cheatsheet.netlify.app/
- Zustand guide: https://docs.pmnd.rs/zustand/getting-started/introduction

### Verktøy
- Vite Bundle Analyzer: `npx vite-bundle-visualizer`
- Lighthouse: Chrome DevTools > Lighthouse
- React DevTools: Chrome extension
- Playwright Inspector: `npx playwright test --debug`

---

## 🎯 NESTE STEG (I MORGEN)

### Prioritet 1: Backend Foundation
1. Installer FastAPI + dependencies
2. Opprett `src/api/` struktur
3. Implementer `/api/v1/bot/status` endpoint (test med Swagger)
4. Koble til eksisterende `BotService`

### Quick Win Test
Når `/api/v1/bot/status` fungerer:
```bash
curl http://localhost:8000/api/v1/bot/status
# Expected: {"is_running": false, "balance": 10000, ...}
```

Dette bekrefter at:
- ✅ FastAPI fungerer
- ✅ BotService kan gjenbrukes direkte
- ✅ JSON serialization fungerer
- ✅ Grunnlaget for React frontend er klart

**Forventet tidsbruk dag 1:** 2-3 timer for basic FastAPI setup + 1 endpoint.

---

## 📞 SUPPORT & SPØRSMÅL

Hvis du støter på problemer under migrasjonen:

1. **FastAPI issues:** Sjekk Swagger UI (`/docs`) først
2. **React issues:** Bruk React DevTools for debugging
3. **WebSocket issues:** Test med `websocat` eller browser console
4. **Performance issues:** Bruk React Profiler + Chrome Performance tab
5. **TypeScript errors:** Sjekk `tsconfig.json` strict mode settings

**Viktig:** Ta en feature om gangen, test grundig, commit ofte. Ikke prøv å migrere alt på én gang.

---

## 🏁 KONKLUSJON

Denne migrasjonen vil:
- ✅ Løse alle NiceGUI problemer (memory leaks, zombie prosesser, performance)
- ✅ Gi moderne, testbar arkitektur
- ✅ 10x bedre ytelse (94% CPU reduksjon)
- ✅ Professional-grade løsning som kan skaleres videre
- ✅ Gjenbruke 70% av eksisterende backend kode

**Estimert tid:** 4 uker (kan justeres ned til 3 uker hvis du kutter optional features).

**Lykke til! 🚀**
