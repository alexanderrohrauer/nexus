import React, { useEffect } from "react";
import type {
  SchemaVisualization,
  SchemaVisualizationData,
} from "~/lib/api/types";
import * as echarts from "echarts";

interface EChartsVisualizationProps {
  visualization: SchemaVisualization;
  options: any | undefined;
  response: SchemaVisualizationData;
}

// TODO maybe fix resize window some day...
export const EChartsVisualization = React.forwardRef(function (
  props: EChartsVisualizationProps,
  ref: React.ForwardedRef<HTMLDivElement>,
) {
  useEffect(() => {
    if (ref.current && props.options) {
      console.log(props.options);
      const chart = echarts.init(ref.current);
      const resizeObserver = new ResizeObserver(() => {
        chart.resize();
      });
      setTimeout(() => {
        resizeObserver.observe(ref.current);
        window.addEventListener("resize", () => chart.resize());
      }, 1000);
      chart.setOption(props.options);
    }
  }, [ref, props.options]);
  useEffect(() => {}, []);
  return <div ref={ref} className="w-full" />;
});
