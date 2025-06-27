import { useState } from "react";
import DashboardIcon from "../assets/icons/dashboard.png";
import DevicesIcon from "../assets/icons/devices.png";
import AlertIcon from "../assets/icons/alert.png";
import SupportIcon from "../assets/icons/support.png";
import HydroBotIcon from "../assets/icons/hydrobot.png";
import logo from "../assets/logo.png";
import toggleIcon from "../assets/icons/toggleIcon.png";
import { NavLink } from "react-router-dom";


const navItems = [
  { id: "dashboard", label: "Dashboard", icon: DashboardIcon, path: "/dashboard" },
  { id: "devices", label: "Dispositifs", icon: DevicesIcon, path: "/DevicesPage" },
  { id: "alerts", label: "Alertes", icon: AlertIcon, path: "/Recommendations" },
  { id: "supports", label: "Supports", icon: SupportIcon, path: "/Support" },
  { id: "hydrobot", label: "HydroBot", icon: HydroBotIcon, path: "/hydrobot" },
];


export default function Sidebar() {
  const [isOpen, setIsOpen] = useState(true);
  const toggleSidebar = () => setIsOpen(!isOpen);

  return (
    <aside
      className={`min-h-screen bg-[#003366] text-white flex flex-col py-4 transition-all duration-300
        ${isOpen ? "w-52" : "w-16"} relative`}
    >
      <div className="flex items-center px-4 mb-8 gap-3">
  <button
    onClick={toggleSidebar}
    className="p-1 hover:bg-white/20 rounded"
    aria-label={isOpen ? "Fermer le menu" : "Ouvrir le menu"}
  >
    <img src={toggleIcon} alt="Toggle menu" className="h-6 w-6" />
  </button>

  {isOpen && (
    <img src={logo} alt="HydroNex Logo" className="h-8" />
  )}
</div>


      {/* Navigation */}
      <nav className="flex flex-col gap-3 px-2">
        {navItems.map((item) => (
          <NavLink
  key={item.id}
  to={item.path}
  className={({ isActive }) =>
    `flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-all ${
      isActive ? "bg-[#0066cc] text-white" : "hover:bg-[#004080] text-gray-200"
    }`
  }
>
            <img src={item.icon} alt={item.label} className="h-5 w-5" />
            {isOpen && <span className="ml-3 uppercase">{item.label}</span>}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
