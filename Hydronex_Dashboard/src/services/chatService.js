import axios from "axios";

const API_BASE_URL = "https://api-hydro-nex.onrender.com/api";

export const sendMessageToBot = async (message) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/chat`, { message });
    return response.data.data.response;
  } catch (error) {
    console.error("Erreur lors de l'envoi du message au chatbot :", error);
    return "Désolé, je n'ai pas pu traiter votre demande pour le moment.";
  }
};

