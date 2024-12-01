import React, { useContext, useEffect, useState } from "react";
import { SchemaDashboard } from "~/lib/api/types";
import { useMatches } from "@remix-run/react";

interface DashboardContextType {
  dashboard: SchemaDashboard | null;
  setDashboard: React.Dispatch<React.SetStateAction<SchemaDashboard | null>>;
}

export const DashboardContext = React.createContext<
  DashboardContextType | undefined
>(undefined);

interface DashboardProviderProps extends React.PropsWithChildren {}

export function DashboardProvider(props: DashboardProviderProps) {
  const [dashboard, setDashboard] = useState<SchemaDashboard | null>(null);

  return (
    <DashboardContext.Provider value={{ dashboard, setDashboard }}>
      {props.children}
    </DashboardContext.Provider>
  );
}

export function useDashboard() {
  const dashboardContext = useContext(DashboardContext);
  const matches = useMatches();
  if (!dashboardContext) {
    throw new Error("No dashboard context mounted!");
  }
  useEffect(() => {
    if (!matches.some((m) => m.id === "routes/dashboards.$slug")) {
      dashboardContext.setDashboard(null);
    }
  }, [matches]);
  return dashboardContext;
}
