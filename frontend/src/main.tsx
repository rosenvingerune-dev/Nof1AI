import React from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom'
import './index.css'
import { Layout } from './components/layout/Layout'
import { DashboardPage } from './pages/Dashboard'
import { PositionsPage } from './pages/Positions'
import { TradesPage } from './pages/Trades'
import { MarketPage } from './pages/Market'
import { SettingsPage } from './pages/Settings'

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        index: true,
        element: <DashboardPage />,
      },
      {
        path: "positions",
        element: <PositionsPage />,
      },
      {
        path: "trades",
        element: <TradesPage />,
      },
      {
        path: "market",
        element: <MarketPage />,
      },
      {
        path: "settings",
        element: <SettingsPage />,
      },
    ],
  },
  {
    path: "*",
    element: <Navigate to="/" replace />
  }
])

createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
