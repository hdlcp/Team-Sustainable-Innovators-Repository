import axios from "axios";

const API_URL = "https://api-hydro-nex.onrender.com/api";

export const loginUser = async (email, password) => {
  const response = await axios.post(`${API_URL}/auth/login`, { email, password });
  console.log("Données renvoyées par l'API :", response.data);
  return response.data.data.token; // ✅ Correction ici
};
