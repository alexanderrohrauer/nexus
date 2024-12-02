import React, { MouseEvent, useEffect, useRef, useState } from "react";
import { SchemaVisualization } from "~/lib/api/types";
import { Skeleton } from "~/components/ui/skeleton";
import { Popover, PopoverContent } from "~/components/ui/popover";
import { isElementInViewport } from "~/lib/use-in-viewport";

interface VisualizationProps {
  visualization: SchemaVisualization;
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

  return (
    <>
      <Skeleton
        style={{
          gridRow: `span ${props.visualization.rows} / span ${props.visualization.rows}`,
          gridColumn: `span ${props.visualization.columns} / span ${props.visualization.columns}`,
        }}
        onClick={onClick}
      />
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
