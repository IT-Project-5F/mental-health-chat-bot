import { createRoot } from 'react-dom/client'
import './index.css'
import 'leaflet/dist/leaflet.css'
import App from './App.tsx'

// StrictMode disabled due to Leaflet MapContainer incompatibility with double-mounting
// Leaflet throws "Map container is already initialized" error in StrictMode
createRoot(document.getElementById('root')!).render(
  <App />
)
