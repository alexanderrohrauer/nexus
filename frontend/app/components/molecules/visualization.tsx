import React, { useState } from "react";
import type { SchemaDashboard, SchemaVisualization } from "~/lib/api/types";
import { useQuery } from "@tanstack/react-query";
import { client } from "~/lib/api/api-client";
import { VisualizationFrame } from "~/components/molecules/visualization-frame";
import { Skeleton } from "~/components/ui/skeleton";

interface VisualizationProps {
  visualization: SchemaVisualization;
  dashboard: SchemaDashboard;
}

export function Visualization(props: VisualizationProps) {
  const [filters, setFilters] = useState({});

  const { data, isLoading } = useQuery({
    queryKey: ["visualization_data", props.visualization.uuid],
    queryFn: () =>
      client.GET(
        "/dashboards/{uuid}/visualizations/{visualization_uuid}/data",
        {
          params: {
            path: {
              uuid: props.dashboard.uuid!,
              visualization_uuid: props.visualization.uuid!,
            },
            query: { q: JSON.stringify(filters) },
          },
        },
      ),
  });

  return (
    <>
      {isLoading ? (
        <Skeleton
          style={{
            gridRow: `span ${props.visualization.rows}`,
            gridColumn: `span ${props.visualization.columns}`,
          }}
        />
      ) : (
        <div
          className="bg-muted rounded-lg"
          style={{
            gridRow: `span ${props.visualization.rows}`,
            gridColumn: `span ${props.visualization.columns}`,
          }}
        >
          {data && (
            <VisualizationFrame
              visualization={props.visualization}
              response={data.data!}
              filters={filters}
              onFiltersChange={(filters) => setFilters(filters)}
            />
          )}
        </div>
      )}
    </>
  );
}
