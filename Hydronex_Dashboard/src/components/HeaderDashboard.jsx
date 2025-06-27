import { useEffect, useState } from "react";
import { fetchDeviceLocations, fetchRealTimeData } from "../services/deviceService";

const HeaderDashboard = ({ onFilterChange }) => {
  const [batteryLevel, setBatteryLevel] = useState(null);
  const [deviceId, setDeviceId] = useState("");
  const [date, setDate] = useState(() => {
    const today = new Date();
    return today.toISOString().split("T")[0];
  });
  const [devices, setDevices] = useState([]);

  const batteryColor =
    batteryLevel > 60
      ? "bg-green-500"
      : batteryLevel > 30
      ? "bg-yellow-400"
      : "bg-red-500";

  useEffect(() => {
    const loadDevices = async () => {
      try {
        const data = await fetchDeviceLocations();
        setDevices(data);
      } catch (err) {
        console.error("Erreur lors du chargement des dispositifs :", err);
      }
    };
    loadDevices();
  }, []);

  useEffect(() => {
    onFilterChange({ dispositifId: deviceId, date });
  }, [deviceId, date, onFilterChange]);

  useEffect(() => {
    if (!deviceId) {
      setBatteryLevel(null);
      return;
    }
    const fetchBattery = async () => {
      try {
        const data = await fetchRealTimeData(deviceId);
        setBatteryLevel(data.battery_level);
      } catch (err) {
        console.error("Erreur en récupérant les données temps réel :", err);
      }
    };
    fetchBattery();
  }, [deviceId]);

  return (
    <div className="flex flex-wrap justify-between items-end gap-4 mb-6">
      <div className="flex items-center gap-3">
        <div className="relative w-10 h-4 bg-gray-300 rounded-sm">
          <div
            className={`h-full rounded-sm ${batteryColor}`}
            style={{ width: `${batteryLevel ?? 0}%` }}
          />
          <div className="absolute top-1 left-full w-1.5 h-2 bg-gray-300 rounded-r-sm ml-0.5" />
        </div>
        <span className="text-sm font-medium">
          {batteryLevel !== null ? `${batteryLevel}%` : "--"}
        </span>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Dispositif</label>
        <select
  value={deviceId}
  onChange={(e) => setDeviceId(e.target.value)} // garder string ici
  className="bg-gray-100 text-sm px-4 py-2 rounded-lg shadow-sm"
>
  <option value="">-- Choisir un dispositif --</option>
  {devices.map((device) => (
    <option key={device.id} value={device.id}>
      {device.nom} – {device.localisation}
    </option>
  ))}
</select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Date</label>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          className="bg-gray-100 text-sm px-4 py-2 rounded-lg shadow-sm"
        />
      </div>
    </div>
  );
};

export default HeaderDashboard;
