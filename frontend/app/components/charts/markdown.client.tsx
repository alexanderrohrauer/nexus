import React, { useMemo } from "react";
import type {
  SchemaVisualization,
  SchemaVisualizationData,
} from "~/lib/api/types";
import Markdown from "react-markdown";

interface MarkdownVisualizationProps {
  visualization: SchemaVisualization;
  options: any | undefined;
  response: SchemaVisualizationData;
}

export const MarkdownVisualization = React.forwardRef(function (
  props: MarkdownVisualizationProps,
  ref: React.ForwardedRef<HTMLDivElement>,
) {
  const md = useMemo(
    () => props.options.series.join("\n\n").trim(),
    [props.options],
  );
  return (
    <div ref={ref} className="w-full">
      <Markdown className="react-markdown">{md}</Markdown>
    </div>
  );
});
