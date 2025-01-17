import React, { useMemo } from "react";
import type {
  SchemaVisualization,
  SchemaVisualizationData,
} from "~/lib/api/types";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";

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
      <Markdown
        className="react-markdown"
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw]}
      >
        {md}
      </Markdown>
    </div>
  );
});
