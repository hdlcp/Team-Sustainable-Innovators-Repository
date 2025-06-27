// src/components/LoadingMessage.jsx
import { Loader2 } from "lucide-react";

export default function LoadingMessage({ message = "Chargement des dispositifs..." }) {
  return (
    <div className="p-4 flex items-center gap-2 text-gray-600 font-medium">
      <Loader2 className="w-5 h-5 animate-spin text-blue-500" />
      {message}
    </div>
  );
}
