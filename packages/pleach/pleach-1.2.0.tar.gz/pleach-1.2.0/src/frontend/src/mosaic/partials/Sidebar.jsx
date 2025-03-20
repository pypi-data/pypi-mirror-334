import React, { useEffect, useRef, useState } from "react";
import { NavLink, useLocation } from "react-router-dom";

import SidebarLinkGroup from "./SidebarLinkGroup";

function Sidebar({ sidebarOpen, setSidebarOpen, variant = "default" }) {
  const location = useLocation();
  const { pathname } = location;

  const trigger = useRef(null);
  const sidebar = useRef(null);

  const storedSidebarExpanded = localStorage.getItem("sidebar-expanded");
  const [sidebarExpanded, setSidebarExpanded] = useState(
    storedSidebarExpanded === null ? false : storedSidebarExpanded === "true",
  );

  // close on click outside
  useEffect(() => {
    const clickHandler = ({ target }) => {
      if (!sidebar.current || !trigger.current) return;
      if (
        !sidebarOpen ||
        sidebar.current.contains(target) ||
        trigger.current.contains(target)
      )
        return;
      setSidebarOpen(false);
    };
    document.addEventListener("click", clickHandler);
    return () => document.removeEventListener("click", clickHandler);
  });

  // close if the esc key is pressed
  useEffect(() => {
    const keyHandler = ({ keyCode }) => {
      if (!sidebarOpen || keyCode !== 27) return;
      setSidebarOpen(false);
    };
    document.addEventListener("keydown", keyHandler);
    return () => document.removeEventListener("keydown", keyHandler);
  });

  useEffect(() => {
    localStorage.setItem("sidebar-expanded", sidebarExpanded);
    if (sidebarExpanded) {
      document.querySelector("body").classList.add("sidebar-expanded");
    } else {
      document.querySelector("body").classList.remove("sidebar-expanded");
    }
  }, [sidebarExpanded]);

  return (
    <div className="min-w-fit">
      {/* Sidebar backdrop (mobile only) */}
      <div
        className={`fixed inset-0 z-40 bg-gray-900/30 transition-opacity duration-200 lg:z-auto lg:hidden ${
          sidebarOpen ? "opacity-100" : "pointer-events-none opacity-0"
        }`}
        aria-hidden="true"
      ></div>

      {/* Sidebar */}
      <div
        id="sidebar"
        ref={sidebar}
        className={`lg:flex! no-scrollbar lg:sidebar-expanded:!w-64 2xl:w-64! lg:sidebar-expanded:p-4 absolute left-0 top-0 z-40 flex h-[100dvh] w-64 shrink-0 flex-col overflow-y-scroll bg-white p-4 transition-all duration-200 ease-in-out dark:bg-gray-800 lg:static lg:left-auto lg:top-auto lg:w-20 lg:translate-x-0 lg:overflow-y-auto lg:p-4 ${sidebarOpen ? "translate-x-0" : "-translate-x-64"} ${variant === "v2" ? "border-r border-gray-200 dark:border-gray-700/60" : "shadow-xs rounded-r-2xl"}`}
      >
        {/* Links */}
        <div className="space-y-8">
          {/* Pages group */}
          <div>
            <ul className="mt-3">
            <li className={`pl-4 pr-3 py-2 rounded-lg mb-0.5 last:mb-0 bg-[linear-gradient(135deg,var(--tw-gradient-stops))] ${pathname === "/dashboard" && "from-violet-500/[0.12] dark:from-violet-500/[0.24] to-violet-500/[0.04]"}`}>
                <NavLink
                  end
                  to="/dashboard"
                  className={`block truncate text-gray-800 transition duration-150 dark:text-gray-100 ${
                    pathname.includes("dashboard")
                      ? ""
                      : "hover:text-gray-900 dark:hover:text-white"
                  }`}
                >
                  <div className="flex items-center">
                  <svg
                              className={`shrink-0 fill-current ${pathname === "/" || pathname.includes("dashboard") ? "text-violet-500" : "text-gray-400 dark:text-gray-500"}`}
                              xmlns="http://www.w3.org/2000/svg"
                              width="16"
                              height="16"
                              viewBox="0 0 16 16"
                            >
                              <path d="M5.936.278A7.983 7.983 0 0 1 8 0a8 8 0 1 1-8 8c0-.722.104-1.413.278-2.064a1 1 0 1 1 1.932.516A5.99 5.99 0 0 0 2 8a6 6 0 1 0 6-6c-.53 0-1.045.076-1.548.21A1 1 0 1 1 5.936.278Z" />
                              <path d="M6.068 7.482A2.003 2.003 0 0 0 8 10a2 2 0 1 0-.518-3.932L3.707 2.293a1 1 0 0 0-1.414 1.414l3.775 3.775Z" />
                            </svg>
                    <span className="lg:sidebar-expanded:opacity-100 ml-4 text-sm font-medium duration-200 lg:opacity-0 2xl:opacity-100">
                      Dashboard
                    </span>
                  </div>
                </NavLink>
              </li>

              <li className={`pl-4 pr-3 py-2 rounded-lg mb-0.5 last:mb-0 bg-[linear-gradient(135deg,var(--tw-gradient-stops))] ${pathname === "/flows" && "from-violet-500/[0.12] dark:from-violet-500/[0.24] to-violet-500/[0.04]"}`}>
                <NavLink
                  end
                  to="/flows"
                  className={`block truncate text-gray-800 transition duration-150 dark:text-gray-100 ${
                    pathname.includes("flows")
                      ? ""
                      : "hover:text-gray-900 dark:hover:text-white"
                  }`}
                >
                  <div className="flex items-center">
                    <svg
                      className={`shrink-0 fill-current ${pathname.includes("flows") ? "text-violet-500" : "text-gray-400 dark:text-gray-500"}`}
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 16 16"
                    >
                      <path d="M9 6.855A3.502 3.502 0 0 0 8 0a3.5 3.5 0 0 0-1 6.855v1.656L5.534 9.65a3.5 3.5 0 1 0 1.229 1.578L8 10.267l1.238.962a3.5 3.5 0 1 0 1.229-1.578L9 8.511V6.855ZM6.5 3.5a1.5 1.5 0 1 1 3 0 1.5 1.5 0 0 1-3 0Zm4.803 8.095c.005-.005.01-.01.013-.016l.012-.016a1.5 1.5 0 1 1-.025.032ZM3.5 11c.474 0 .897.22 1.171.563l.013.016.013.017A1.5 1.5 0 1 1 3.5 11Z" />
                    </svg>
                    <span className="lg:sidebar-expanded:opacity-100 ml-4 text-sm font-medium duration-200 lg:opacity-0 2xl:opacity-100">
                      Flows
                    </span>
                  </div>
                </NavLink>
              </li>

              <li className={`pl-4 pr-3 py-2 rounded-lg mb-0.5 last:mb-0 bg-[linear-gradient(135deg,var(--tw-gradient-stops))] ${pathname === "/settings/general" && "from-violet-500/[0.12] dark:from-violet-500/[0.24] to-violet-500/[0.04]"}`}>
                <NavLink
                  end
                  to="/settings/general"
                  className={`block truncate text-gray-800 transition duration-150 dark:text-gray-100 ${
                    pathname.includes("/settings/general")
                      ? ""
                      : "hover:text-gray-900 dark:hover:text-white"
                  }`}
                >
                  <div className="flex items-center">
                  <svg
                              className={`shrink-0 fill-current ${pathname.includes("settings") ? "text-violet-500" : "text-gray-400 dark:text-gray-500"}`}
                              xmlns="http://www.w3.org/2000/svg"
                              width="16"
                              height="16"
                              viewBox="0 0 16 16"
                            >
                              <path
                                d="M10.5 1a3.502 3.502 0 0 1 3.355 2.5H15a1 1 0 1 1 0 2h-1.145a3.502 3.502 0 0 1-6.71 0H1a1 1 0 0 1 0-2h6.145A3.502 3.502 0 0 1 10.5 1ZM9 4.5a1.5 1.5 0 1 1 3 0 1.5 1.5 0 0 1-3 0ZM5.5 9a3.502 3.502 0 0 1 3.355 2.5H15a1 1 0 1 1 0 2H8.855a3.502 3.502 0 0 1-6.71 0H1a1 1 0 1 1 0-2h1.145A3.502 3.502 0 0 1 5.5 9ZM4 12.5a1.5 1.5 0 1 0 3 0 1.5 1.5 0 0 0-3 0Z"
                                fillRule="evenodd"
                              />
                            </svg>
                    <span className="lg:sidebar-expanded:opacity-100 ml-4 text-sm font-medium duration-200 lg:opacity-0 2xl:opacity-100">
                      Settings
                    </span>
                  </div>
                </NavLink>
              </li>



              <li className={`pl-4 pr-3 py-2 rounded-lg mb-0.5 last:mb-0 bg-[linear-gradient(135deg,var(--tw-gradient-stops))] ${pathname === "/admin" && "from-violet-500/[0.12] dark:from-violet-500/[0.24] to-violet-500/[0.04]"}`}>
                <NavLink
                  end
                  to="/admin"
                  className={`block truncate text-gray-800 transition duration-150 dark:text-gray-100 ${
                    pathname.includes("admin")
                      ? ""
                      : "hover:text-gray-900 dark:hover:text-white"
                  }`}
                >
                  <div className="flex items-center">
                  <svg
                      className={`shrink-0 fill-current ${pathname.includes("admin") ? "text-violet-500" : "text-gray-400 dark:text-gray-500"}`}
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 16 16"
                    >
                      <path d="M5 4a1 1 0 0 0 0 2h6a1 1 0 1 0 0-2H5Z" />
                      <path d="M4 0a4 4 0 0 0-4 4v8a4 4 0 0 0 4 4h8a4 4 0 0 0 4-4V4a4 4 0 0 0-4-4H4ZM2 4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V4Z" />
                      <path d="M4 0a4 4 0 0 0-4 4v8a4 4 0 0 0 4 4h8a4 4 0 0 0 4-4V4a4 4 0 0 0-4-4H4ZM2 4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V4Z" />
                    </svg>
                    <span className="lg:sidebar-expanded:opacity-100 ml-4 text-sm font-medium duration-200 lg:opacity-0 2xl:opacity-100">
                      Admin Page
                    </span>
                  </div>
                </NavLink>
              </li>

              
              <li className={`pl-4 pr-3 py-2 rounded-lg mb-0.5 last:mb-0 bg-[linear-gradient(135deg,var(--tw-gradient-stops))] ${pathname === "/logout" && "from-violet-500/[0.12] dark:from-violet-500/[0.24] to-violet-500/[0.04]"}`}>
                <NavLink
                  end
                  to="/logout"
                  className={`block truncate text-gray-800 transition duration-150 dark:text-gray-100 ${
                    pathname.includes("logout")
                      ? ""
                      : "hover:text-gray-900 dark:hover:text-white"
                  }`}
                >
                  <div className="flex items-center">
                  <svg
                              className={`shrink-0 fill-current ${pathname.includes("logout") ? "text-violet-500" : "text-gray-400 dark:text-gray-500"}`}
                              xmlns="http://www.w3.org/2000/svg"
                              width="16"
                              height="16"
                              viewBox="0 0 16 16"
                            >
                              <path d="M14.75 2.5a1.25 1.25 0 1 0 0-2.5 1.25 1.25 0 0 0 0 2.5ZM14.75 16a1.25 1.25 0 1 0 0-2.5 1.25 1.25 0 0 0 0 2.5ZM2.5 14.75a1.25 1.25 0 1 1-2.5 0 1.25 1.25 0 0 1 2.5 0ZM1.25 2.5a1.25 1.25 0 1 0 0-2.5 1.25 1.25 0 0 0 0 2.5Z" />
                              <path d="M8 2a6 6 0 1 0 0 12A6 6 0 0 0 8 2ZM4 8a4 4 0 1 1 8 0 4 4 0 0 1-8 0Z" />
                            </svg>
                    <span className="lg:sidebar-expanded:opacity-100 ml-4 text-sm font-medium duration-200 lg:opacity-0 2xl:opacity-100">
                      Logout
                    </span>
                  </div>
                </NavLink>
              </li>

            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Sidebar;
