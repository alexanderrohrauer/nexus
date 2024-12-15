import React, { useEffect, useRef, useState } from "react";
import { VisualizationFrame } from "~/components/molecules/visualization-frame";
import type { SchemaVisualization } from "~/lib/api/types";
// TODO lazy loading
import "highcharts/highcharts-more";
import "highcharts/modules/mouse-wheel-zoom";
import "highcharts/modules/accessibility";
import "highcharts/modules/exporting";
import "highcharts/modules/networkgraph";
import "highcharts/modules/venn";
import "highcharts/modules/wordcloud";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";

interface VegaVisualizationProps {
  spec: any;
  data: any;
  visualization: SchemaVisualization;
}

export function HighchartsVisualization(props: VegaVisualizationProps) {
  const divRef = useRef<HTMLDivElement | null>(null);
  const [height, setHeight] = useState(0);

  useEffect(() => {
    if (divRef.current) {
      setHeight(divRef.current.clientHeight);
    }
  }, [divRef]);

  return (
    <VisualizationFrame visualization={props.visualization} ref={divRef}>
      {height && (
        <HighchartsReact
          highcharts={Highcharts}
          options={{
            ...props.spec,
            chart: {
              ...props.spec.chart,
              styledMode: true,
              zooming: {
                type: "x",
                mouseWheel: { enabled: true },
              },
              // width: props.visualization.columns * 10,
              // height: props.visualization.rows * 10,
              height,
            },
          }}
        />
      )}
    </VisualizationFrame>
  );
}
