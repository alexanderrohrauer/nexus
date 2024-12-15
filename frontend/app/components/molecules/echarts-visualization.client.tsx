import React, { useEffect, useRef } from "react";
import { VisualizationFrame } from "~/components/molecules/visualization-frame";
import type { SchemaVisualization } from "~/lib/api/types";
import * as echarts from "echarts";

interface VegaVisualizationProps {
  spec: any;
  data: any;
  visualization: SchemaVisualization;
}

export function EChartsVisualization(props: VegaVisualizationProps) {
  const divRef = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    if (divRef.current) {
      const chart = echarts.init(divRef.current);
      const spec = { ...props.spec, series: props.data };
      console.log(spec);
      chart.setOption(spec);
    }
  }, [divRef, props.spec, props.data]);
  return (
    <VisualizationFrame visualization={props.visualization}>
      <div ref={divRef} className="w-full h-[93%]" />
    </VisualizationFrame>
  );
}
