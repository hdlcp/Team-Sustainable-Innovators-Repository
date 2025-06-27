import axios from "axios";

const API_BASE_URL = "https://api-hydro-nex.onrender.com/api";

export const subscribeNewsletter = async ({ email, nom }) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/newsletter/subscribe`, {
      email,
      nom,
    });
    return response.data;
  } catch (error) {
    console.error("Erreur lors de l'inscription à la newsletter :", error);
    throw error;
  }
};
