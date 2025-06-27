import { useState } from "react";
import { XMarkIcon } from "@heroicons/react/24/solid";
import { subscribeNewsletter } from "../services/newsletterService";

export default function NewsletterForm({ onClose }) {
  const [email, setEmail] = useState("");
  const [nom, setNom] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);
    try {
      await subscribeNewsletter({ email, nom });
      setMessage("Merci pour votre inscription !");
      setEmail("");
      setNom("");
    } catch (error) {
      console.error("Erreur lors de l’inscription à la newsletter :", error);
      setMessage("Erreur lors de l'inscription, veuillez réessayer.");
    } finally {
      setLoading(false);
    }
  };

  return (
   <div className="bg-white rounded-lg p-6 max-w-md w-full relative shadow-lg">
      <div className="bg-white rounded-lg p-6 max-w-md w-full relative shadow-lg">
        <button
          className="absolute top-4 right-4 text-gray-500 hover:text-gray-700"
          onClick={onClose}
          aria-label="Fermer"
        >
          <XMarkIcon className="w-6 h-6" />
        </button>
        <h2 className="text-xl font-semibold mb-4">Inscrivez-vous à la newsletter</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block mb-1 font-medium" htmlFor="nom">Nom</label>
            <input
              id="nom"
              type="text"
              className="w-full border border-gray-300 rounded px-3 py-2"
              value={nom}
              onChange={(e) => setNom(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block mb-1 font-medium" htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              className="w-full border border-gray-300 rounded px-3 py-2"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded transition-colors disabled:opacity-50"
          >
            {loading ? "En cours..." : "S'inscrire"}
          </button>
          {message && (
            <p className="mt-2 text-center text-sm text-gray-700">{message}</p>
          )}
        </form>
      </div>
    </div>
  );
}
