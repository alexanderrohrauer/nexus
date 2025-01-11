import React, { useMemo, useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { EntityType } from "~/lib/api/types";
import { client } from "~/lib/api/api-client";
import type { VisualizationFrameProps } from "~/components/molecules/visualization-frame";
import { VisualizationFrame } from "~/components/molecules/visualization-frame";
import { Card } from "~/components/ui/card";

interface ProfileVisualizationProps {
  identifier: string;
  title: string;
  entityType: EntityType;
  uuid: string;
  children?: VisualizationFrameProps["children"];
}

const FETCH_URL_MAP = {
  [EntityType.WORK]: "/works/{uuid}/visualizations/{chart_identifier}",
  [EntityType.RESEARCHER]:
    "/researchers/{uuid}/visualizations/{chart_identifier}",
  [EntityType.INSTITUTION]:
    "/institutions/{uuid}/visualizations/{chart_identifier}",
};

export function ProfileVisualization(props: ProfileVisualizationProps) {
  const [filters, setFilters] = useState({});
  const queryKey = useMemo(
    () => [
      props.entityType.toLowerCase() + "_visualizations",
      props.uuid,
      props.identifier,
    ],
    [props.entityType, props.identifier, props.uuid],
  );
  const { data } = useQuery({
    queryKey: queryKey,
    queryFn: () =>
      client
        .GET(FETCH_URL_MAP[props.entityType], {
          params: {
            path: { uuid: props.uuid, chart_identifier: props.identifier },
            query: { q: JSON.stringify(filters) },
          },
        })
        .then((res) => res.data),
  });
  const queryClient = useQueryClient();

  return (
    <Card>
      {data && (
        <VisualizationFrame
          title={props.title}
          response={data}
          filters={filters}
          onFiltersChange={(f) => setFilters(f)}
          onFiltersApply={() =>
            queryClient.invalidateQueries({ queryKey: queryKey })
          }
          children={props.children}
        />
      )}
    </Card>
  );
}
