import React from "react";
import type {
  SchemaVisualization,
  SchemaVisualizationData,
} from "~/lib/api/types";
// TODO maybe lazy loading
import "highcharts/modules/accessibility";
import "highcharts/highcharts-more";
import "highcharts/modules/mouse-wheel-zoom";
import "highcharts/modules/venn";
import "highcharts/modules/wordcloud";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";

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
  return (
    <div ref={ref}>
      {props.options && (
        <HighchartsReact
          highcharts={Highcharts}
          options={{
            ...props.options,
            chart: {
              ...props.options.chart,
              // styledMode: true,
              animation: false,
              zooming: {
                type: "xy",
                mouseWheel: { enabled: true },
              },
              height: ref.current.clientHeight,
            },
          }}
        />
      )}
    </div>
  );
});
