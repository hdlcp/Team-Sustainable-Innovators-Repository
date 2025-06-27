// DevicesPage.jsx
import { useEffect, useState } from "react";
import { Eye, Plus, RotateCcw, SatelliteDish, Pencil } from "lucide-react";
import { toast } from "react-toastify";

import DeviceDetailsModal from "../components/DeviceDetailsModal";
import DeviceFormModal from "../components/DeviceFormModal";
import PasswordPromptModal from "../components/PasswordPromptModal";
import LoadingMessage from "../components/Spinner";

import { fetchDevices, addDevice, updateDevice } from "../services/deviceService";

export default function DevicesPage() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [selectedDevice, setSelectedDevice] = useState(null);
  const [showModal, setShowModal] = useState(false); // Voir
  const [showAddModal, setShowAddModal] = useState(false); // Formulaire ajout/modif
  const [showPasswordModal, setShowPasswordModal] = useState(false); // Mot de passe
  const [isEditMode, setIsEditMode] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    loadDevices();
  }, []);

  const loadDevices = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchDevices();
      setDevices(data);
      if (data.length === 0) toast.info("Aucun dispositif trouvé.");
    } catch (err) {
      console.error("Erreur lors du chargement :", err);
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (error && !loading) {
      toast.error("Erreur : impossible de charger les dispositifs !");
    }
  }, [error, loading]);

  const handleClickAddDispositif = () => {
    setIsEditMode(false);
    setSelectedDevice(null);
    if (isAuthenticated) {
      setShowAddModal(true);
    } else {
      setShowPasswordModal(true);
    }
  };

  const handleClickEditDevice = (device) => {
    setSelectedDevice(device);
    setIsEditMode(true);
    if (isAuthenticated) {
      setShowAddModal(true);
    } else {
      setShowPasswordModal(true);
    }
  };

  const handlePasswordSuccess = () => {
    setIsAuthenticated(true);
    setShowPasswordModal(false);
    setShowAddModal(true);
  };

  const handleViewClick = (device) => {
    setSelectedDevice(device);
    setShowModal(true);
  };

  const handleAddDevice = async (newDevice) => {
    try {
      await addDevice(newDevice);
      await loadDevices();
      setShowAddModal(false);
      toast.success("Dispositif ajouté avec succès !");
    } catch (err) {
      console.error("Erreur lors de l'ajout :", err);
      toast.error(err.response?.data?.message || "Erreur lors de l'ajout.");
    }
  };

  const handleEditSubmit = async (updatedDevice) => {
    if (!selectedDevice) return;
    try {
      await updateDevice(selectedDevice.id, {
        ...updatedDevice,
        id: selectedDevice.id,
      });
      await loadDevices();
      setShowAddModal(false);
      setIsEditMode(false);
      setSelectedDevice(null);
      toast.success("Dispositif mis à jour avec succès !");
    } catch (err) {
      console.error("Erreur lors de la mise à jour :", err.response?.data || err);
      toast.error(err.response?.data?.message || "Erreur lors de la mise à jour.");
    }
  };

  return (
    <div className="flex">
      <div className="flex-1 p-8 bg-gray-50 min-h-screen">
        {/* En-tête */}
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-2xl font-semibold text-gray-800 flex items-center gap-2">
            <SatelliteDish className="w-10 h-10 text-blue-600" />
            Liste de Dispositifs
          </h3>

          <div className="flex gap-2">
            <button
              onClick={loadDevices}
              disabled={loading}
              className="flex items-center gap-2 bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-md transition disabled:opacity-50"
            >
              <RotateCcw className="w-4 h-4" />
              Rafraîchir
            </button>
            <button
              onClick={handleClickAddDispositif}
              disabled={loading}
              className={`flex items-center gap-2 px-4 py-2 rounded-md transition ${
                loading
                  ? "bg-blue-300 text-white cursor-not-allowed"
                  : "bg-blue-600 hover:bg-blue-700 text-white"
              }`}
            >
              <Plus className="w-4 h-4" />
              Ajouter un dispositif
            </button>
          </div>
        </div>

        {/* Tableau */}
        <div className="bg-white shadow-md rounded-lg border border-gray-200 overflow-hidden">
          {loading ? (
            <LoadingMessage />
          ) : devices.length === 0 ? (
            <p className="p-4 text-gray-600">Aucun dispositif trouvé.</p>
          ) : (
            <table className="min-w-full table-auto text-sm">
              <thead className="bg-blue-50">
                <tr>
                  <th className="text-left px-6 py-3 font-semibold text-gray-600">Nom</th>
                  <th className="text-left px-6 py-3 font-semibold text-gray-600">Localisation</th>
                  <th className="text-left px-6 py-3 font-semibold text-gray-600">Statut</th>
                  <th className="text-right px-6 py-3 font-semibold text-gray-600">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {devices.map((device) => (
                  <tr key={device.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">{device.nom}</td>
                    <td className="px-6 py-4">{device.localisation}</td>
                    <td className="px-6 py-4">
                      <span
                        className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                          device.statut === "actif"
                            ? "bg-green-100 text-green-700"
                            : "bg-red-100 text-red-700"
                        }`}
                      >
                        <span
                          className={`h-2 w-2 rounded-full mr-2 ${
                            device.statut === "actif"
                              ? "bg-green-500"
                              : "bg-red-500"
                          }`}
                        />
                        {device.statut === "actif" ? "Actif" : "Inactif"}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex justify-end gap-4">
                        {!isAuthenticated && (
                          <button
                            className="inline-flex items-center text-blue-600 hover:underline"
                            onClick={() => handleViewClick(device)}
                          >
                            <Eye className="w-4 h-4 mr-1" />
                            Voir
                          </button>
                        )}

                        {isAuthenticated && (
                          <button
                            className="inline-flex items-center text-yellow-600 hover:underline"
                            onClick={() => handleClickEditDevice(device)}
                          >
                            <Pencil className="w-4 h-4 mr-1" />
                            Modifier
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* Modales */}
        {showModal && selectedDevice && (
          <DeviceDetailsModal
            device={selectedDevice}
            onClose={() => {
              setShowModal(false);
              setSelectedDevice(null);
            }}
          />
        )}

        {showPasswordModal && (
          <PasswordPromptModal
            onClose={() => setShowPasswordModal(false)}
            onSuccess={handlePasswordSuccess}
          />
        )}

        {showAddModal && (
          <DeviceFormModal
            device={isEditMode ? selectedDevice : null}
            isEdit={isEditMode}
            onClose={() => {
              setShowAddModal(false);
              setIsEditMode(false);
              setSelectedDevice(null);
            }}
            onSubmit={isEditMode ? handleEditSubmit : handleAddDevice}
          />
        )}
      </div>
    </div>
  );
}
