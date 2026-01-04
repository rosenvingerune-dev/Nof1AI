# Nof1 Alpha Arena - System Overview & Architecture

## 1. System Architecture
High-level overview of how the system components interact.

```mermaid
graph TD
    User[User / Web Browser] -->|HTTP/WS| FE[Frontend (React + Vite)]
    FE -->|REST API| BE[Backend (FastAPI)]
    FE -->|WebSocket| WS[WebSocket Manager]
    BE -->|Controls| Engine[Trading Bot Engine]
    
    subgraph "Backend Core"
        BE
        WS
        Engine -->|Analysis| AI[AI Agent / LLM]
        Engine -->|Executes| Dex[Hyperliquid/Paper Exchange]
        Engine -->|Fetches| Mkt[Market Data (Taapi.io)]
    end

    subgraph "Frontend Layer"
        FE -->|State Mgmt| STORE[Zustand Store]
        STORE -->|Updates| UI[UI Components]
    end
```

## 2. Component Hierarchy & Tools
Detailed breakdown of the frontend and backend structure.

### Frontend (React Ecosystem)
The frontend is built for performance and instant visual feedback (Shadcn UI + Tailwind).

```mermaid
graph LR
    subgraph "Tools"
        Vite[Vite: Build Tool]
        Tailwind[TailwindCSS: Styling]
        Shadcn[Shadcn UI: Components]
    end

    subgraph "App Structure"
        Main[Main.tsx] --> Router[React Router]
        Router --> Layout[Layout (Sidebar + Shell)]
        Layout --> Pages
    end

    subgraph "Pages"
        Pages --> Dash[Dashboard]
        Pages --> Pos[Positions]
        Pages --> Trd[Trades]
        Pages --> MktP[Market]
        Pages --> Set[Settings]
    end

    subgraph "State & Data"
        Dash -->|Reads| Store[useBotStore (Zustand)]
        Store -->|Fetches| API[Axios Client]
        Store -->|Listens| WSC[WebSocket Hook]
    end
```

### Backend (Python/FastAPI)
The brain of the operation.

```mermaid
graph LR
    API[FastAPI App] --> Routes
    
    subgraph "Routes"
        Routes --> Bot[Bot Control]
        Routes --> Mkt[Market Data]
        Routes --> WS[WebSocket Stream]
    end

    API --> Services
    
    subgraph "Services"
        Services --> BotSvc[Bot Service]
        BotSvc --> Engine[Trading Engine]
        Engine --> Agent[Decision Agent]
    end
```

## 3. Tool Dependencies
| Layer | Tool | Purpose |
|-------|------|---------|
| **Frontend** | React 18 | UI Library |
| | Vite | Fast Build Tool & Dev Server |
| | TailwindCSS | Utility-first CSS |
| | Zustand | State Management (Simpler than Redux) |
| | Axios | API Requests |
| **Backend** | FastAPI | High-performance Python API |
| | Uvicorn | ASGI Server |
| | Pydantic | Data Validation |
| | Pandas | Data Analysis |

## 4. How to Run (Startup Guide)

To run the full stack locally, you need two terminal windows.

### Terminal 1: Backend
The backend serves the API and the WebSocket connection.
```powershell
# From project root
python -m uvicorn src.api.main:app --reload
```
*Expected Output:* `Application startup complete. Uvicorn running on http://127.0.0.1:8000`

### Terminal 2: Frontend
The frontend serves the user interface.
```powershell
# From project root
cd frontend
npm run dev
```
*Expected Output:* `Local: http://localhost:5173/`

### Automatic Startup
You can use the helper script `scripts/start_dev.ps1` to launch both easily.
