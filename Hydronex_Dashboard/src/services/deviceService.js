import axios from "axios";

const API_BASE_URL = "https://api-hydro-nex.onrender.com/api";

// Récupérer tous les dispositifs
export const fetchDevices = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/dispositifs`);
    return response.data.data;
  } catch (error) {
    console.error("Erreur lors du chargement des dispositifs :", error);
    throw error;
  }
};

// Alias pour compatibilité avec HeaderDashboard
export const fetchDeviceLocations = async () => {
  return await fetchDevices();
};

// Ajouter un nouveau dispositif
export const addDevice = async (deviceData) => {
  try {
    const token = localStorage.getItem("token");
    const response = await axios.post(
      `${API_BASE_URL}/dispositifs`,
      deviceData,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );
    return response.data.data;
  } catch (error) {
    console.error("Erreur lors de l'ajout du dispositif :", error);
    throw error;
  }
};

// Mettre à jour un dispositif existant
export const updateDevice = async (id, deviceData) => {
  try {
    const token = localStorage.getItem("token");
    const response = await axios.put(
      `${API_BASE_URL}/dispositifs/${id}`,
      deviceData,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data.data;
  } catch (error) {
    console.error("Erreur lors de la mise à jour du dispositif :", error);
    throw error;
  }
};

// Obtenir les données en temps réel d’un dispositif
export const fetchRealTimeData = async (dispositifId) => {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/donnees/temps-reel`,
      { params: { dispositif_id: dispositifId } }
    );
    return response.data.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des données temps réel :", error);
    throw error;
  }
};

// Obtenir l'historique des données d’un dispositif pour une date donnée (date_debut = date_fin)
export const fetchHistoricalData = async (dispositifId, date) => {
  try {
    const dateStart = `${date}T00:00:00`;
    const dateEnd = `${date}T23:59:59`;
    const response = await axios.get(
      `${API_BASE_URL}/donnees/historique`,
      {
        params: {
          dispositif_id: dispositifId,
          date_debut: dateStart,
          date_fin: dateEnd,
          page: 1,
          per_page: 1000,
        },
      }
    );
    return response.data.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des données historiques :", error);
    throw error;
  }
};
// Récupérer les alertes d’un dispositif
export const fetchAlerts = async (dispositifId, page = 1, perPage = 10) => {
  try {
    // Préparer les params en évitant de passer dispositif_id si null ou undefined
    const params = {
      page,
      per_page: perPage,
    };
    if (dispositifId !== null && dispositifId !== undefined) {
      params.dispositif_id = dispositifId;
    }

    const response = await axios.get(`${API_BASE_URL}/alertes`, { params });

    // Accès au tableau d'alertes : response.data.data.data
    const alertData = response.data?.data?.data;

    if (!Array.isArray(alertData)) {
      console.error("fetchAlerts : format inattendu des données reçues", alertData);
      return [];
    }

    return alertData;
  } catch (error) {
    console.error("Erreur lors de la récupération des alertes :", error);
    return [];
  }
};


export const fetchLastAlert = async () => {
  try {
    // Récupérer la dernière alerte (page 1, 1 seule alerte)
    const response = await axios.get(`${API_BASE_URL}/alertes`, {
      params: {
        page: 1,
        per_page: 1,
      },
    });

    // ✅ Correction importante ici : accéder à response.data.data.data
    const lastAlert = response.data?.data?.data?.[0];
    if (!lastAlert) return null;

    // Récupérer les dispositifs pour faire correspondre le nom
    const devices = await fetchDevices();
    const matchingDevice = devices.find((d) => d.id === lastAlert.dispositif_id);
    const deviceName = matchingDevice ? matchingDevice.nom : `Dispositif ${lastAlert.dispositif_id}`;

    return {
      title: lastAlert.alerte,
      message: lastAlert.recommandation,
      timestamp: new Date(lastAlert.created_at).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
      deviceName,
    };
  } catch (error) {
    console.error("Erreur lors de la récupération de la dernière alerte :", error);
    return null;
  }
};
