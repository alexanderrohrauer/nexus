import React, { useEffect } from "react";
import { client } from "~/lib/api/api-client";
import { LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { Visualization } from "~/components/molecules/visualization";
import { SidebarRight } from "~/components/nav/sidebar-right";
import { useDashboard } from "~/components/context/dashboard-context";

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
  const { setDashboard } = useDashboard();

  useEffect(() => {
    setDashboard(dashboard);
  }, [dashboard]);

  return (
    <div className="flex space-x-3 pb-3">
      {/*TODO eventually make scrollable*/}
      <div className="grid grid-rows-12 grid-cols-12 min-h-[calc(100vh-68px)] gap-3 flex-1 overflow-auto">
        {dashboard.visualizations.map((visualization) => (
          <Visualization
            key={"vis-" + visualization.uuid}
            visualization={visualization}
          />
        ))}
      </div>
      <SidebarRight />
    </div>
  );
}
