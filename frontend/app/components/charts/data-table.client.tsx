import React from "react";
import type {
  SchemaVisualization,
  SchemaVisualizationData,
} from "~/lib/api/types";

interface DataTableVisualizationProps {
  visualization: SchemaVisualization;
  options: any | undefined;
  response: SchemaVisualizationData;
}

// TODO fix this visualization template
export const DataTableVisualization = React.forwardRef(function (
  props: DataTableVisualizationProps,
  ref: React.ForwardedRef<HTMLDivElement>,
) {
  return (
    <div ref={ref} className="w-full">
      <table>
        <tr>
          {props.options.header.map((header) => (
            <th>{header}</th>
          ))}
        </tr>
        {props.options.rows.map((row) => (
          <tr>
            {row.map((col) => (
              <td>{col}</td>
            ))}
          </tr>
        ))}
      </table>
    </div>
  );
});
