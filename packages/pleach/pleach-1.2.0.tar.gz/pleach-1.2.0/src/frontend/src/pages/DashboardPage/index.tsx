  import React, { useState } from "react";

  import { Button } from "@/components/ui/button";
  import { useCustomNavigate } from "@/customization/hooks/use-custom-navigate";
  import { ChevronRight } from "lucide-react";
  import TemplatesModal from "../../modals/templatesModal";
  import Datepicker from "../../mosaic/components/Datepicker";
  import AnalyticsCard01 from "../../mosaic/partials/analytics/AnalyticsCard01";
  import AnalyticsCard02 from "../../mosaic/partials/analytics/AnalyticsCard02";
  import AnalyticsCard03 from "../../mosaic/partials/analytics/AnalyticsCard03";
  import AnalyticsCard04 from "../../mosaic/partials/analytics/AnalyticsCard04";
  import AnalyticsCard05 from "../../mosaic/partials/analytics/AnalyticsCard05";
  import AnalyticsCard06 from "../../mosaic/partials/analytics/AnalyticsCard06";
  import AnalyticsCard07 from "../../mosaic/partials/analytics/AnalyticsCard07";
  import AnalyticsCard08 from "../../mosaic/partials/analytics/AnalyticsCard08";
  import AnalyticsCard09 from "../../mosaic/partials/analytics/AnalyticsCard09";
  import AnalyticsCard10 from "../../mosaic/partials/analytics/AnalyticsCard10";
  import AnalyticsCard11 from "../../mosaic/partials/analytics/AnalyticsCard11";
  import Header from "../../mosaic/partials/Header";
  import Sidebar from "../../mosaic/partials/Sidebar";

  function Analytics() {
    const navigate = useCustomNavigate();
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [newProjectModal, setNewProjectModal] = useState(false); // State for the modal

    return (
      <div className="relative flex flex-1 flex-col overflow-y-auto overflow-x-hidden">
        {/* Templates Modal */}
        <TemplatesModal open={newProjectModal} setOpen={setNewProjectModal} />

        <main className="grow">
          <div className="mx-auto w-full px-4 py-8 sm:px-6 lg:px-8">
            {/* Page header */}
            <div className="mb-8 sm:flex sm:items-center sm:justify-between">
              {/* Left: Title */}
              <div className="mb-4 sm:mb-0">
                <h1 className="text-2xl font-bold text-gray-800 dark:text-gray-100 md:text-3xl">
                  Dashboard
                </h1>
              </div>

              {/* Right: Actions */}
              {/* <div className="grid grid-flow-col sm:auto-cols-max justify-start sm:justify-end gap-2">
            <Button onClick={() => navigate('/flow/new')} className='bg-violet-500 text-white hover:bg-violet-600'>
                Create Flow <ChevronRight className="ml-2 h-4 w-4" />
              </Button>      
            </div> */}
              <div className="grid grid-flow-col justify-start gap-2 sm:auto-cols-max sm:justify-end">
                <Button
                  onClick={() => setNewProjectModal(true)} // Open modal instead of navigating
                  className="bg-violet-500 text-white hover:bg-violet-600"
                >
                  Create Flow <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </div>

            {/* Cards */}
            <div className="grid grid-cols-12 gap-6">
              {/* Line chart (Analytics) */}
              <AnalyticsCard01 />
              {/*  Line chart (Active Users Right Now) */}
              <AnalyticsCard02 />
              {/* Stacked bar chart (Acquisition Channels) */}
              <AnalyticsCard03 />
              {/* Horizontal bar chart (Audience Overview) */}
              <AnalyticsCard04 />
              {/* Report card (Top Channels) */}
              <AnalyticsCard05 />
              {/* Report card (Top Pages) */}
              <AnalyticsCard06 />
              {/* Report card (Top Countries) */}
              <AnalyticsCard07 />
              {/* Doughnut chart (Sessions By Device) */}
              <AnalyticsCard08 />
              {/* Doughnut chart (Visit By Age Category) */}
              <AnalyticsCard09 />
              {/* Polar chart (Sessions By Gender) */}
              <AnalyticsCard10 />
              {/* Table (Top Products) */}
              <AnalyticsCard11 />
            </div>
          </div>
        </main>
      </div>
    );
  }

  export default Analytics;
