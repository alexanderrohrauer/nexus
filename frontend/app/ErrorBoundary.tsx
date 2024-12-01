import React from "react";
import { useRouteError } from "react-router";

export function ErrorBoundary() {
  const error = useRouteError();
  // @ts-ignore
  return <React.Fragment>{error && <p>Unknown error</p>}</React.Fragment>;
}
