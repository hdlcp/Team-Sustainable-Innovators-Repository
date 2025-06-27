import { useEffect, useState } from "react";
import { X } from "lucide-react";

export default function DeviceFormModal({ onClose, onSubmit, device = null, isEdit = false }) {
  const [form, setForm] = useState({
    nom: "",
    localisation: "",
    statut: "actif",
  });

  // Pré-remplir le formulaire si on est en mode édition
  useEffect(() => {
    if (isEdit && device) {
      setForm({
        nom: device.nom || "",
        localisation: device.localisation || "",
        statut: device.statut || "actif",
      });
    }
  }, [isEdit, device]);

  // Gestion du changement de champ
  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  // Soumission du formulaire
  const handleSubmit = (e) => {
    e.preventDefault();

    if (!form.nom || !form.localisation || !form.statut) {
      alert("Tous les champs sont requis.");
      return;
    }

    const payload = isEdit && device
      ? { ...form, id: device.id } // inclure l'id en mode édition
      : form;

    onSubmit(payload); // Appel du handler parent
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="bg-white rounded-xl shadow-lg w-full max-w-lg p-6 relative">
        {/* Bouton de fermeture */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-500 hover:text-gray-700"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Titre */}
        <h2 className="text-xl font-semibold text-gray-800 mb-4">
          {isEdit ? "Modifier le dispositif" : "Ajouter un nouveau dispositif"}
        </h2>

        {/* Formulaire */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Champ Nom */}
          <div>
            <label className="block text-sm text-gray-600 mb-1">Nom du dispositif</label>
            <input
              type="text"
              name="nom"
              value={form.nom}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              required
            />
          </div>

          {/* Champ Localisation */}
          <div>
            <label className="block text-sm text-gray-600 mb-1">Localisation</label>
            <input
              type="text"
              name="localisation"
              value={form.localisation}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              required
            />
          </div>

          {/* Champ Statut */}
          <div>
            <label className="block text-sm text-gray-600 mb-1">Statut</label>
            <select
              name="statut"
              value={form.statut}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              required
            >
              <option value="actif">actif</option>
              <option value="inactif">inactif</option>
            </select>
          </div>

          {/* Boutons */}
          <div className="flex justify-end gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition"
            >
              Annuler
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
            >
              {isEdit ? "Mettre à jour" : "Enregistrer"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
