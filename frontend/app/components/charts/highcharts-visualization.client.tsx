import React, { useEffect, useRef } from "react";
import type {
  SchemaVisualization,
  SchemaVisualizationData,
} from "~/lib/api/types";
// TODO maybe lazy loading
import "highcharts/modules/accessibility";
import "highcharts/highcharts-more";
import "highcharts/modules/mouse-wheel-zoom";
import "highcharts/modules/exporting";
import "highcharts/modules/networkgraph";
import "highcharts/modules/venn";
import "highcharts/modules/wordcloud";
import Highcharts from "highcharts";

interface HighchartsVisualizationProps {
  visualization: SchemaVisualization;
  options: any | undefined;
  response: SchemaVisualizationData;
}

// TODO maybe fix resize window some day...
export const HighchartsVisualization = React.forwardRef(function (
  props: HighchartsVisualizationProps,
  ref: React.ForwardedRef<HTMLDivElement>,
) {
  const chartRef = useRef<Highcharts.Chart>();
  useEffect(() => {
    if (ref.current && props.options) {
      // const resizeObserver = new ResizeObserver(() => {
      //   chart.resize();
      // });
      // setTimeout(() => {
      //   resizeObserver.observe(ref.current);
      //   window.addEventListener("resize", () => chart.resize());
      // }, 1000);
      console.log({
        ...props.options,
        chart: {
          ...props.options.chart,
          // styledMode: true,
          zooming: {
            type: "xy",
            mouseWheel: { enabled: true },
          },
          height: ref.current.clientHeight,
        },
      });
      if (chartRef.current) {
        chartRef.current.destroy();
      }
      chartRef.current = Highcharts.chart(ref.current, {
        ...props.options,
        chart: {
          ...props.options.chart,
          // styledMode: true,
          zooming: {
            type: "xy",
            mouseWheel: { enabled: true },
          },
          height: ref.current.clientHeight,
        },
      });
    }
  }, [ref, props.options]);

  return <div ref={ref} className="w-full" />;
});
