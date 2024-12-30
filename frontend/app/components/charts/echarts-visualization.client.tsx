import React, { useEffect } from "react";
import type {
  SchemaVisualization,
  SchemaVisualizationData,
} from "~/lib/api/types";
import * as echarts from "echarts";

interface VegaVisualizationProps {
  // TODO remove
  spec: any;
  data: any;
  visualization: SchemaVisualization;
  options: any | undefined;
  response: SchemaVisualizationData;
}

// TODO maybe fix resize window some day...
export const EChartsVisualization = React.forwardRef<
  HTMLDivElement,
  React.HTMLProps<HTMLDivElement>
>(function (props: VegaVisualizationProps, ref) {
  useEffect(() => {
    if (ref.current && props.options) {
      const chart = echarts.init(ref.current);
      const resizeObserver = new ResizeObserver(() => {
        chart.resize();
      });
      setTimeout(() => {
        resizeObserver.observe(ref.current);
        window.addEventListener("resize", () => chart.resize());
      }, 1000);
      console.log("options", props.options);
      chart.setOption(props.options);
    }
  }, [ref, props.spec, props.data, props.options]);
  useEffect(() => {}, []);
  return <div ref={ref} className="w-full" />;
});
