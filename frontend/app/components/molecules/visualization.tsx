import React from "react";
import { SchemaVisualization } from "~/lib/api/types";
import { Skeleton } from "~/components/ui/skeleton";

interface VisualizationProps {
  visualization: SchemaVisualization;
}

export function Visualization(props: VisualizationProps) {
  //   TODO render visualization here
  return (
    <Skeleton
      style={{
        gridRow: `span ${props.visualization.rows} / span ${props.visualization.rows}`,
        gridColumn: `span ${props.visualization.columns} / span ${props.visualization.columns}`,
      }}
    />
  );
}
