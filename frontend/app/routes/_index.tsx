import type { MetaFunction } from "@remix-run/node";
import { useNav } from "~/components/context/nav-context";
import { useEffect } from "react";

export const meta: MetaFunction = () => {
  return [
    { title: "New Remix App" },
    { name: "description", content: "Welcome to Remix!" },
  ];
};

export default function Index() {
  const { setPageName } = useNav();
  useEffect(() => {
    setPageName("Home");
  }, []);
  return <div>Index page</div>;
}
