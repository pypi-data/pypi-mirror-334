import AppHeader from "@/components/core/appHeaderComponent";
import useTheme from "@/customization/hooks/use-custom-theme";
import { useState } from "react";
import { Outlet } from "react-router-dom";
import Header from "../../mosaic/partials/Header";
import Sidebar from "../../mosaic/partials/Sidebar";

export function DashboardWrapperPage() {
  useTheme();

  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen w-full flex-col overflow-hidden">
      <AppHeader />
      <div className="flex h-[100dvh] overflow-hidden">
        <Sidebar sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />
        <div className="flex w-full flex-1 flex-row overflow-hidden">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
