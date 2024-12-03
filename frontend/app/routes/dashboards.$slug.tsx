import React, { useEffect } from "react";
import { client } from "~/lib/api/api-client";
import type { LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { useNav } from "~/components/context/nav-context";
import { Visualization } from "~/components/molecules/visualization";

interface DashboardProps {}

export const loader = async ({ params }: LoaderFunctionArgs) => {
  const { data: dashboard } = await client.GET("/dashboards/{uuid}", {
    params: { path: { uuid: params.slug as string } },
  });
  // TODO error handler
  if (!dashboard) {
    throw new Error("Error while loading dashboard");
  }
  return { dashboard };
};
export default function Dashboard(props: DashboardProps) {
  const { dashboard } = useLoaderData<typeof loader>();
  const { setDashboard, setPageName } = useNav();

  useEffect(() => {
    setDashboard(dashboard);
    setPageName(dashboard.title);
  }, [dashboard]);

  return (
    <div className="flex space-x-3 pb-3">
      {/*TODO eventually make scrollable*/}
      {/*<div className="grid auto-rows-[6.2vh] grid-cols-12 h-[calc(100vh-68px)] gap-3 flex-1 overflow-auto">*/}
      <div className="flex flex-row flex-wrap gap-3 items-start justify-start">
        {dashboard.visualizations.map((visualization) => (
          <Visualization
            key={"vis-" + visualization.uuid}
            visualization={visualization}
            dashboard={dashboard}
          />
        ))}
      </div>
      {/*<SidebarRight />*/}
    </div>
  );
}
