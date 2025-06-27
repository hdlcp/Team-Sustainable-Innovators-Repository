import { useState } from "react";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";

export default function DashboardLayout({ children }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  return (
    <div className="flex bg-[#003366] min-h-screen relative">
      {/* Sidebar */}
      {isSidebarOpen && (
        <Sidebar />
      )}

      {/* Contenu principal */}
      <div className="flex-1 flex flex-col">
        <Topbar toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />

        {/* Conteneur blanc */}
        <div className="bg-white rounded-t-2xl p-6 flex-1">
          {children}
        </div>
      </div>
    </div>
  );
}
