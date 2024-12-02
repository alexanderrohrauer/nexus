import {
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
} from "@remix-run/react";
import type { LinksFunction } from "@remix-run/node";

import styles from "./tailwind.css?url";
import globalStyles from "./styles/global.scss?url";
import { useTheme } from "~/lib/theme";
import { Toaster } from "~/components/ui/sonner";
import { ErrorBoundary } from "~/ErrorBoundary";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useMemo } from "react";
import { Nav } from "~/components/nav/nav";
import { NavProvider } from "~/components/context/nav-context";

export const links: LinksFunction = () => [
  { rel: "preconnect", href: "https://fonts.googleapis.com" },
  {
    rel: "preconnect",
    href: "https://fonts.gstatic.com",
    crossOrigin: "anonymous",
  },
  {
    rel: "stylesheet",
    href: "https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap",
  },
  { rel: "stylesheet", href: styles },
  { rel: "stylesheet", href: globalStyles, loader: "sass" },
];

export function Layout({ children }: { children: React.ReactNode }) {
  const { theme } = useTheme();
  const queryClient = useMemo(() => new QueryClient(), []);

  return (
    <html lang="en" suppressHydrationWarning className={theme}>
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta />
        <Links />
      </head>
      <body>
        <NavProvider>
          <Toaster />
          <QueryClientProvider client={queryClient}>
            <ErrorBoundary />
            <Nav>{children}</Nav>
            <ScrollRestoration />
            <Scripts />
          </QueryClientProvider>
        </NavProvider>
      </body>
    </html>
  );
}

export default function App() {
  return <Outlet />;
}
