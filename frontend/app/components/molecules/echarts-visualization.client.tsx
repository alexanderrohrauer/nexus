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
  const frameRef = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    if (divRef.current && frameRef.current) {
      divRef.current.style.height = `${frameRef.current.clientHeight}px`;
      const chart = echarts.init(divRef.current);
      const resizeObserver = new ResizeObserver(() => {
        chart.resize();
      });
      resizeObserver.observe(divRef.current);
      window.addEventListener("resize", () => chart.resize());
      const spec = { ...props.spec, series: props.data };
      chart.setOption(spec);
    }
  }, [divRef, frameRef, props.spec, props.data]);
  useEffect(() => {}, []);
  return (
    <VisualizationFrame visualization={props.visualization} ref={frameRef}>
      <div ref={divRef} className="w-full" />
    </VisualizationFrame>
  );
}
