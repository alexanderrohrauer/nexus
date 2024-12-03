import React from "react";
import type { SchemaVisualization } from "~/lib/api/types";

interface VisualizationFrameProps extends React.PropsWithChildren {
  visualization: SchemaVisualization;
}

export function VisualizationFrame(props: VisualizationFrameProps) {
  // TODO finish
  return (
    <div className="h-full w-full p-3 space-y-[1%]">
      <h1 className="text-[hsl(224_71.4%_4.1%)]">
        {props.visualization.title}
      </h1>
      {props.children}
    </div>
  );
}
