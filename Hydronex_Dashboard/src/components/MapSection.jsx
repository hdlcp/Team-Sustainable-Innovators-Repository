import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Pour corriger l'icône des marqueurs par défaut
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-shadow.png',
});

export default function MapSection() {
  return (
    <div className="bg-white p-4 rounded-xl shadow-md w-full h-[320px]">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold text-gray-800">Carte des dispositifs</h3>
      </div>

      {/* Carte interactive */}
      <div className="w-full h-full rounded-lg overflow-hidden">
        <MapContainer
          center={[6.3703, 2.3912]} // Coordonnées de Cotonou (exemple)
          zoom={13}
          scrollWheelZoom={false}
          style={{ height: '240px', width: '100%' }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution="© OpenStreetMap contributors"
          />
          <Marker position={[6.3703, 2.3912]}>
            <Popup>
              Capteur principal - Cotonou
            </Popup>
          </Marker>
        </MapContainer>
      </div>
    </div>
  );
}
