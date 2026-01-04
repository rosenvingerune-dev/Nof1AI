# Changelog Update - 2026-01-04

## Features Implemented

### 1. Recommendations Engine & UI
- **Backend API**: Added endpoints for managing trade proposals:
  - `GET /api/v1/proposals/`: List pending proposals.
  - `POST /api/v1/proposals/{id}/approve`: Approve a proposal for execution.
  - `POST /api/v1/proposals/{id}/reject`: Reject a proposal.
- **Frontend Page**: Created `RecommendationsPage` (`/recommendations`) to display pending AI trade opportunities.
  - Shows confident levels, entry price, take profit, stop loss, and AI rationale.
  - Allows manual "Approve" (execute) or "Reject" actions.
- **Sidebar Integration**: Added "Recommendations" link to the main navigation.

### 2. Trade History Improvements
- **Data Filtering**: Filtered out `hold` actions from the "Trade History" page (`Trades.tsx`) to show only executed trades (Buy/Sell).
- **Statistics**: Added summary cards for "Total Trades", "Buy Orders", and "Sell Orders" to the Trades page.

### 3. Market Data Enhancements
- **Layout Update**: Moved "Market Sentiment" summary to the top of the `MarketPage`.
- **New Metrics**: Added "Open Interest" to the asset cards.
- **Visual Improvements**: Added color-coded "HIGH/MODERATE/LOW" indicators for Volume and Open Interest to make data easier to scan.

### 4. Settings & Configuration
- **Auto-Trade Threshold**: Added persistence for the `auto_trade_threshold` setting.
- **UI Update**: Added a numeric input field in `SettingsPage` to configure the confidence threshold (default 80%) for auto-trading. 
- **Persistence**: Ensures that toggling "Auto-Trade" and changing the threshold are saved to `config.json` and survive restarts.

## Technical Details
- **State Management**: Updated `useBotStore` to handle `proposals` state and actions (`approveProposal`, `rejectProposal`).
- **Dependencies**: Added `@radix-ui/react-progress` for the confidence bar in Recomendations.
- **Refactoring**: Cleaned up `BotService` to properly handle configuration saving/loading for new fields.
