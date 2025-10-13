import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import { useMap } from './MapContext';

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

function Map({
  center = [-37.8136, 144.9631],
  zoom = 13,
}: MapProps) {
    const { markers } = useMap();
    return(
        <div className="relative w-screen h-screen rounded-lg overflow-hidden shadow">
            <MapContainer center={center} zoom={zoom} scrollWheelZoom={true} className="w-full h-full">
                <TileLayer
                attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
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