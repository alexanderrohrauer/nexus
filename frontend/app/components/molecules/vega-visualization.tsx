import React, { useRef, useState } from "react";
import { Vega } from "react-vega";
import { VisualizationFrame } from "~/components/molecules/visualization-frame";
import type { SchemaVisualization } from "~/lib/api/types";

interface VegaVisualizationProps {
  spec: any;
  data: any;
  visualization: SchemaVisualization;
}

export function VegaVisualization(props: VegaVisualizationProps) {
  const [dimensions, setDimensions] = useState({ height: 100, width: 100 });
  const divRef = useRef<HTMLDivElement | null>(null);
  // useEffect(() => {
  //   if (divRef.current) {
  //     setDimensions({
  //       height: divRef.current.clientHeight / 1.1,
  //       width: divRef.current.clientWidth - 24,
  //     });
  //   }
  // }, [divRef]);
  // useEffect(() => {
  //   window.addEventListener(
  //     "resize",
  //     debounce(() => {
  //       if (divRef.current) {
  //         setDimensions({
  //           height: divRef.current.clientHeight / 1.15 - 24,
  //           width: divRef.current.clientWidth - 14,
  //         });
  //       }
  //     }),
  //   );
  // }, []);
  const ref = useRef(null);
  return (
    <VisualizationFrame visualization={props.visualization}>
      <div className="bg-[hsl(220_14.3%_95.9%)]">
        <Vega
          spec={props.spec}
          data={props.data}
          renderer="svg"
          className="vega-wrapper z-10"
          ref={ref}
        />
      </div>
    </VisualizationFrame>
  );
}
