import React, { createContext, useContext, useState, type ReactNode } from 'react';

interface MapMarker {
  id: number;
  position: [number, number]; // [lat, lng]
  title: string;
  address: string;
  details: {
    organisation: string;
    service_name: string;
    street: string;
    suburb: string;
    state: string;
    postcode: string;
  };
}

interface MapContextType {
  markers: MapMarker[];
  setMarkers: (markers: MapMarker[]) => void;
  updateMarkers: (newMarkers: MapMarker[]) => void;
}

const MapContext = createContext<MapContextType | undefined>(undefined);

export const MapProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [markers, setMarkers] = useState<MapMarker[]>([]);

  const updateMarkers = (newMarkers: MapMarker[]) => {
    if (newMarkers && newMarkers.length > 0) {
      setMarkers(newMarkers);
    }
  };

  return (
    <MapContext.Provider value={{ markers, setMarkers, updateMarkers }}>
      {children}
    </MapContext.Provider>
  );
};

export const useMap = () => {
  const context = useContext(MapContext);
  if (context === undefined) {
    throw new Error('useMap must be used within a MapProvider');
  }
  return context;
};

export type { MapMarker };