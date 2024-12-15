import type { ForwardRefExoticComponent } from "react";
import React from "react";
import type { SchemaVisualization } from "~/lib/api/types";

interface VisualizationFrameProps extends React.PropsWithChildren {
  visualization: SchemaVisualization;
}

export const VisualizationFrame = React.forwardRef(function (
  props: VisualizationFrameProps,
  ref: ForwardRefExoticComponent<HTMLDivElement>,
) {
  // TODO finish
  return (
    <div className="flex flex-col h-full p-3 space-y-1">
      <h1>{props.visualization.title}</h1>
      <div className="flex-1" ref={ref}>
        {props.children}
      </div>
    </div>
  );
});
