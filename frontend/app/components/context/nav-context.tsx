import React, { useContext, useEffect, useState } from "react";
import { SchemaDashboard } from "~/lib/api/types";
import { useMatches } from "@remix-run/react";

interface NavContextType {
  dashboard: SchemaDashboard | null;
  pageName: string | null;
  setDashboard: React.Dispatch<React.SetStateAction<SchemaDashboard | null>>;
  setPageName: React.Dispatch<React.SetStateAction<string | null>>;
}

export const NavContext = React.createContext<NavContextType | undefined>(
  undefined,
);

interface NavProviderProps extends React.PropsWithChildren {}

export function NavProvider(props: NavProviderProps) {
  const [dashboard, setDashboard] = useState<SchemaDashboard | null>(null);
  const [pageName, setPageName] = useState<string | null>(null);

  return (
    <NavContext.Provider
      value={{ dashboard, pageName, setDashboard, setPageName }}
    >
      {props.children}
    </NavContext.Provider>
  );
}

export function useNav() {
  const navContext = useContext(NavContext);
  const matches = useMatches();
  if (!navContext) {
    throw new Error("No nav context mounted!");
  }
  useEffect(() => {
    if (!matches.some((m) => m.id === "routes/dashboards.$slug")) {
      navContext.setDashboard(null);
    }
  }, [matches]);
  return navContext;
}
