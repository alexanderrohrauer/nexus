import type { MouseEvent } from "react";
import React, { useEffect, useRef, useState } from "react";
import type { SchemaDashboard, SchemaVisualization } from "~/lib/api/types";
import { Popover, PopoverContent } from "~/components/ui/popover";
import { isElementInViewport } from "~/lib/use-in-viewport";
import { useQuery } from "@tanstack/react-query";
import { client } from "~/lib/api/api-client";
import { HighchartsVisualization } from "~/components/molecules/highcharts-visualization.client";

interface VisualizationProps {
  visualization: SchemaVisualization;
  dashboard: SchemaDashboard;
}

export function Visualization(props: VisualizationProps) {
  const [mousePosition, setMousePosition] = useState({
    pageX: 0,
    pageY: 0,
  });
  const [contentPosition, setContentPosition] = useState({
    left: 0,
    top: 0,
  });
  const contentRef = useRef<HTMLDivElement | null>(null);
  //   TODO render visualization here
  const onClick = (ev: MouseEvent) => {
    setMousePosition({ pageX: ev.pageX, pageY: ev.pageY });
    setOpen(true);
  };

  // TODO exract popover to separate component
  useEffect(() => {
    if (contentRef.current) {
      const isVisible = isElementInViewport(contentRef.current);
      const left = isVisible
        ? mousePosition.pageX
        : mousePosition.pageX - contentRef.current.clientWidth;
      const top = isVisible
        ? mousePosition.pageY
        : mousePosition.pageY - contentRef.current.clientHeight;
      setContentPosition({ left, top });
    }
  }, [contentRef, mousePosition]);

  const [open, setOpen] = useState(false);

  const { data } = useQuery({
    queryKey: ["visualization_data", props.visualization.uuid],
    queryFn: () =>
      client.GET(
        "/dashboards/{uuid}/visualizations/{visualization_uuid}/data",
        {
          params: {
            path: {
              uuid: props.dashboard.uuid!,
              visualization_uuid: props.visualization.uuid!,
            },
          },
        },
      ),
  });

  return (
    <>
      {/*<Skeleton*/}
      {/*  style={{*/}
      {/*    gridRow: `span ${props.visualization.rows}`,*/}
      {/*    gridColumn: `span ${props.visualization.columns}`,*/}
      {/*  }}*/}
      {/*  onClick={onClick}*/}
      {/*/>*/}
      <div
        className="bg-[hsl(220_14.3%_95.9%)] rounded-lg"
        style={{
          gridRow: `span ${props.visualization.rows}`,
          gridColumn: `span ${props.visualization.columns}`,
        }}
      >
        {/*{data && (*/}
        {/*  <VegaVisualization*/}
        {/*    spec={data.data!.spec}*/}
        {/*    data={data.data!.data}*/}
        {/*    visualization={props.visualization}*/}
        {/*  />*/}
        {/*)}*/}
        {data && (
          <HighchartsVisualization
            spec={data.data!.spec}
            data={{}}
            visualization={props.visualization}
          />
        )}
      </div>

      <Popover open={open}>
        <PopoverContent
          className="w-80 fixed"
          style={{ left: contentPosition.left, top: contentPosition.top }}
          avoidCollisions
          ref={contentRef}
        >
          Blah
        </PopoverContent>
      </Popover>
    </>
  );
}
