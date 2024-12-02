import React, { useEffect } from "react";
import { useNav } from "~/components/context/nav-context";

interface ResearchersProps {}

export default function Researchers(props: ResearchersProps) {
  const { setPageName } = useNav();
  useEffect(() => {
    setPageName("Researchers");
  }, []);
  return <div>Researchers</div>;
}
