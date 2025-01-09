import React, { useEffect, useMemo, useRef, useState } from "react";
import type {
  SchemaVisualization,
  SchemaVisualizationData,
} from "~/lib/api/types";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogTitle,
  DialogTrigger,
} from "~/components/ui/dialog";
import { Button } from "~/components/ui/button";
import { FilterIcon } from "lucide-react";
import { VisualizationFilter } from "~/components/templates/visualization-filter";
import { HighchartsVisualization } from "~/components/charts/highcharts-visualization.client";
import { EChartsVisualization } from "~/components/charts/echarts-visualization.client";
import { LeafletVisualization } from "~/components/charts/leaflet-visualization.client";
import { EditVisualizationDialog } from "~/components/templates/edit-visualization-dialog";
import { DataTableVisualization } from "~/components/charts/data-table.client";

export interface VisualizationFrameProps {
  visualization?: SchemaVisualization;
  title?: string;
  response: SchemaVisualizationData;
  filters: any;
  onFiltersChange(filters: any): void;
  onFiltersApply(): void;
  children?: (props: {
    options: any;
    response: SchemaVisualizationData;
  }) => React.ReactNode;
}

class Nexus {
  seriesMap: any;

  constructor(seriesMap: any) {
    this.seriesMap = seriesMap;
  }

  public series(name: string, options?: any) {
    return options
      ? { ...options, ...this.seriesMap[name].data }
      : this.seriesMap[name].data;
  }
}

export const VisualizationFrame = function (props: VisualizationFrameProps) {
  const frameRef = useRef<HTMLDivElement | null>(null);
  const divRef = useRef<HTMLDivElement | null>(null);
  const nexus = useMemo(
    () => new Nexus(props.response.series.data),
    [props.response],
  );
  const [options, setOptions] = useState();
  useEffect(() => {
    const b64module =
      "data:text/javascript;base64," + btoa(props.response.generator);
    import(b64module)
      .then((module) => {
        setOptions(module.default(nexus));
      })
      .catch(console.error);
  }, [props.response, nexus]);

  useEffect(() => {
    if (divRef.current && frameRef.current) {
      divRef.current.style.height = `${frameRef.current.clientHeight}px`;
    }
  }, [divRef, frameRef]);

  return (
    <div className="flex flex-col h-full p-3 space-y-1">
      <div className="flex items-center justify-between">
        <h1 className="font-medium">
          {props.visualization ? props.visualization.title : props.title}
        </h1>
        <div className="space-x-1">
          <Dialog>
            <DialogTrigger asChild>
              <Button
                size="icon"
                variant="outline"
                className="relative h-8 w-8"
              >
                <FilterIcon />
                {Object.keys(props.filters).length > 0 && (
                  <div className="rounded-full bg-red-500 h-2 w-2 absolute right-1.5 top-2" />
                )}
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-max">
              <DialogTitle>Filter</DialogTitle>
              <VisualizationFilter
                response={props.response}
                filters={props.filters}
                onFilterChange={(filters) => props.onFiltersChange(filters)}
              />
              <DialogFooter>
                <DialogTrigger asChild>
                  <Button onClick={() => props.onFiltersApply()}>Apply</Button>
                </DialogTrigger>
              </DialogFooter>
            </DialogContent>
          </Dialog>
          {props.visualization && (
            <EditVisualizationDialog
              visualization={props.visualization}
              response={props.response}
            />
          )}
        </div>
      </div>
      <div className="flex-1" ref={frameRef}>
        {props.response.chart_template === "ECHARTS" && (
          <EChartsVisualization
            visualization={props.visualization}
            options={options}
            response={props.response}
            ref={divRef}
          />
        )}
        {props.response.chart_template === "HIGHCHARTS" && (
          <HighchartsVisualization
            visualization={props.visualization}
            options={options}
            response={props.response}
            ref={divRef}
          />
        )}
        {props.response.chart_template === "LEAFLET" && (
          <LeafletVisualization
            visualization={props.visualization}
            options={options}
            response={props.response}
            ref={divRef}
          />
        )}
        {props.response.chart_template === "DATATABLE" && (
          <DataTableVisualization
            visualization={props.visualization}
            options={options}
            response={props.response}
            ref={divRef}
          />
        )}
        {options && props.children?.({ options, response: props.response })}
      </div>
    </div>
  );
};
