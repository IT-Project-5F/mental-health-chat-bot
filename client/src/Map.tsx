import { MapContainer, TileLayer, Marker, Popup, useMap as useLeafletMap } from 'react-leaflet';
import L from 'leaflet';
import { useMap } from './MapContext';
import { useEffect } from 'react';

import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

const DefaultIcon = L.icon({
    iconUrl: markerIcon,
    shadowUrl: markerShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
});

L.Marker.prototype.options.icon = DefaultIcon;

type MapProps = {
    center?: [number, number];
    zoom?: number;
}

// Component to handle map view updates
function MapViewController({ markers }: { markers: any[] }) {
    const map = useLeafletMap();

    useEffect(() => {
        if (markers && markers.length > 0) {
            // If single marker, center on it
            if (markers.length === 1) {
                map.setView(markers[0].position, 14, { animate: true });
            }
            // If multiple markers, fit bounds to show all
            else {
                const bounds = L.latLngBounds(markers.map(m => m.position));
                map.fitBounds(bounds, { padding: [50, 50], animate: true });
            }
        }
    }, [markers, map]);

    return null;
}

function Map({
  center = [-37.8136, 144.9631],
  zoom = 13,
}: MapProps) {
    const { markers } = useMap();

    return(
        <div className="relative w-screen h-screen rounded-lg overflow-hidden shadow">
            <MapContainer
                center={center}
                zoom={zoom}
                scrollWheelZoom={true}
                className="w-full h-full"
            >
                <TileLayer
                attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <MapViewController markers={markers} />
                {markers.map((m) => (
                    <Marker key={m.id} position={m.position}>
                        <Popup>
                            <div className="space-y-2">
                                <h3 className="font-bold text-sm">{m.details.organisation}</h3>
                                <p className="text-xs">{m.details.service_name}</p>
                                <p className="text-xs text-gray-600">{m.address}</p>
                            </div>
                        </Popup>
                    </Marker>
                ))}

            </MapContainer>
        </div>
    );
}

export default Map;