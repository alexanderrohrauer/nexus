import React from "react";
import { VisualizationFrame } from "~/components/molecules/visualization-frame";
import type { SchemaVisualization } from "~/lib/api/types";
import HighchartsReact from "highcharts-react-official";
import Highcharts from "highcharts";
// TODO lazy loading
import "highcharts/highcharts-more";
import "highcharts/modules/mouse-wheel-zoom";
import "highcharts/modules/accessibility";
import "highcharts/modules/exporting";
import "highcharts/modules/networkgraph";
import "highcharts/modules/venn";
import "highcharts/modules/wordcloud";

interface VegaVisualizationProps {
  spec: any;
  data: any;
  visualization: SchemaVisualization;
}

export function HighchartsVisualization(props: VegaVisualizationProps) {
  return (
    <VisualizationFrame visualization={props.visualization}>
      <HighchartsReact
        highcharts={Highcharts}
        options={{
          ...props.spec,
          chart: {
            ...props.spec.chart,
            // styledMode: true,
            zooming: {
              type: "x",
              mouseWheel: { enabled: true },
            },
            width: props.visualization.columns * 10,
            height: props.visualization.rows * 10,
          },
        }}
      />
    </VisualizationFrame>
  );
}
