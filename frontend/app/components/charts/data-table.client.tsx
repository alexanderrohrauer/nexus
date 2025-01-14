import React, { useEffect, useMemo, useRef } from "react";
import type {
  SchemaVisualization,
  SchemaVisualizationData,
} from "~/lib/api/types";

interface DataTableVisualizationProps {
  visualization: SchemaVisualization;
  options: any | undefined;
  response: SchemaVisualizationData;
}

export const DataTableVisualization = React.forwardRef(function (
  props: DataTableVisualizationProps,
  frameRef: React.ForwardedRef<HTMLDivElement>,
) {
  const tbodyRef = useRef<HTMLTableSectionElement | null>(null);

  const series = useMemo(
    () => props.options?.series[0] ?? { header: [], rows: [] },
    [props.options],
  );

  useEffect(() => {
    if (frameRef.current && tbodyRef.current) {
      const newHeight = frameRef.current.clientHeight - 40;
      tbodyRef.current.style.maxHeight = newHeight + "px";
    }
  }, [frameRef, tbodyRef]);

  return (
    <table className="datatable">
      <thead>
        <tr>
          {series.header.map((header, hi) => (
            <th key={`${props.visualization.uuid}-th-${hi}`}>{header}</th>
          ))}
        </tr>
      </thead>
      <tbody ref={tbodyRef}>
        {series.rows.map((row, j) => (
          <tr key={`${props.visualization.uuid}-tr-${j}`}>
            {row.map((col, k) => (
              <td key={`${props.visualization.uuid}-td-${k}`}>
                {typeof col === "number"
                  ? col.toFixed(col % 1 === 0 ? undefined : 2)
                  : col}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
});
