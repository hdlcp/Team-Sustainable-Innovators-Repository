import { useState, useEffect, useRef } from "react";
import { BellAlertIcon } from "@heroicons/react/24/outline";
import { useNavigate } from "react-router-dom";

export default function NotificationIndicator({ alert }) {
  const navigate = useNavigate();
  const [expanded, setExpanded] = useState(false);
  const [visible, setVisible] = useState(!!alert);
  const [isHovered, setIsHovered] = useState(false);
  const [fadeOut, setFadeOut] = useState(false);
  const timerRef = useRef(null);

  // Gère le timeout avec pause/reprise au survol
  useEffect(() => {
    if (alert) {
      setVisible(true);
      timerRef.current = setTimeout(() => {
        if (!isHovered) {
          setFadeOut(true);
          setTimeout(() => setVisible(false), 500); // attendre animation
        }
      }, 10000);
    }

    return () => clearTimeout(timerRef.current);
  }, [alert, isHovered]);

  // Stoppe le timer quand survolé
  const handleMouseEnter = () => {
    setIsHovered(true);
    clearTimeout(timerRef.current);
    setExpanded(true);
  };

  // Reprend le timer quand on quitte
  const handleMouseLeave = () => {
    setIsHovered(false);
    setExpanded(false);

    timerRef.current = setTimeout(() => {
      setFadeOut(true);
      setTimeout(() => setVisible(false), 500);
    }, 3000); // on redonne 3s à l'utilisateur
  };

  if (!alert || !visible) return null;

  return (
    <div className="w-full px-4 transition-opacity duration-500">
      <div
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onClick={() => navigate("/recommendations")}
        className={`cursor-pointer bg-red-100 border border-red-400 text-red-700 px-2 py-1 rounded-md shadow-sm transition-all duration-300 w-full max-w-md hover:bg-red-200 ${
          fadeOut ? "opacity-0" : "opacity-100"
        }`}
      >
        {expanded ? (
          <div className="flex items-start gap-2">
            <BellAlertIcon className="h-4 w-4 mt-0.5" />
            <div className="text-xs leading-tight">
              <p className="font-semibold">{alert.title}</p>
<p className="text-xs">Dispositif : <span className="font-semibold">{alert.deviceName}</span></p>
<p className="text-xs">{alert.message}</p>
<p className="text-[10px] text-gray-500 italic">{alert.timestamp}</p>
 </div>
          </div>
        ) : (
          <div className="flex items-center gap-2">
            <BellAlertIcon className="h-4 w-4" />
            <span className="text-xs font-medium">Alerte</span>
          </div>
        )}
      </div>
    </div>
  );
}
