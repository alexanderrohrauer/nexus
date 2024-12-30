import type { MouseEvent } from "react";
import React, { useEffect, useRef, useState } from "react";
import type { SchemaDashboard, SchemaVisualization } from "~/lib/api/types";
import { Popover, PopoverContent } from "~/components/ui/popover";
import { isElementInViewport } from "~/lib/use-in-viewport";
import { useQuery } from "@tanstack/react-query";
import { client } from "~/lib/api/api-client";
import { VisualizationFrame } from "~/components/molecules/visualization-frame";

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
  const [filters, setFilters] = useState({});
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

  const { data, refetch } = useQuery({
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
            query: { q: JSON.stringify(filters) },
          },
        },
      ),
  });

  const getHeight = (container: HTMLDivElement | undefined) => {
    if (container) {
      return container.children[0].clientHeight - container.style.marginTop;
    } else {
      return 0;
    }
  };

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
        className="bg-muted rounded-lg"
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
          <VisualizationFrame
            visualization={props.visualization}
            response={data.data!}
            applyFilters={() => refetch()}
            filters={filters}
            onFiltersChange={(filters) => setFilters(filters)}
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
