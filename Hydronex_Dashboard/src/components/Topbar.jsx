import { useEffect, useState } from "react";

export default function Topbar({ toggleSidebar }) {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(interval);
  }, []);

  const formattedDate = time.toLocaleDateString("fr-FR", {
    weekday: "short",
    day: "2-digit",
    month: "long",
  });

  const formattedTime = time.toLocaleTimeString("fr-FR", {
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <div className="bg-[#003366] text-white flex justify-between items-center px-6 py-3 w-full">
         {/* Bouton hamburger (à gauche) */}
      <button onClick={toggleSidebar} className="md:hidden block">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6 text-white"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
      {/* Filtres de sélection */}
      <div className="flex items-center gap-4">
        <div className=" text-sm px-4 py-1.5 rounded-md">
         
        </div>
        <div className=" text-sm px-4 py-1.5 rounded-md">
          
        </div>
      </div>

      {/* Batterie + Date + Heure */}
      <div className="flex items-center gap-6 text-sm">

        {/* Date */}
        <span>{formattedDate}</span>

        {/* Heure */}
        <span>{formattedTime}</span>
      </div>
    </div>
  );
}
