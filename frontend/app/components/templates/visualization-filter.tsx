import React, { useEffect, useMemo, useState } from "react";
import type { SchemaVisualizationData } from "~/lib/api/types";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "~/components/ui/collapsible";
import { ChevronRight } from "lucide-react";
import Filter from "~/components/molecules/filter";
import {
  AFFILIATION_FIELDS,
  INSTITUTION_FIELDS,
  RESEARCHER_FIELDS,
  WORK_FIELDS,
} from "~/lib/filters";

interface VisualizationFilterProps {
  response: SchemaVisualizationData;
  filters: any;
  onFilterChange(filters: any): void;
}

const FIELD_MAP = {
  WORK: WORK_FIELDS,
  RESEARCHER: RESEARCHER_FIELDS,
  INSTITUTION: INSTITUTION_FIELDS,
  AFFILIATIONS: AFFILIATION_FIELDS,
};

export function VisualizationFilter(props: VisualizationFilterProps) {
  const filterNames = useMemo(
    () =>
      Object.keys(props.response.series.data).map((seriesName) => ({
        name: seriesName,
        entityType: props.response.series.data[seriesName].entity_type,
      })),
    [props.response],
  );
  const [filters, setFilters] = useState(props.filters);
  useEffect(() => {
    props.onFilterChange(filters);
  }, [filters]);
  return (
    <div className="min-w-[800px]">
      {filterNames.map(
        (filter) =>
          filter.entityType && (
            <VisualizationFilterRow
              key={filter.name}
              name={filter.name}
              entityType={filter.entityType}
              filter={filters[filter.name] ?? []}
              onChange={(f) =>
                setFilters((prev) => {
                  if (f.length > 0) {
                    return { ...prev, [filter.name]: f };
                  } else {
                    delete prev[filter.name];
                    return prev;
                  }
                })
              }
            />
          ),
      )}
    </div>
  );
}

interface VisualizationFilterRowProps {
  name: string;
  entityType: string;
  filter: any;
  onChange?(filters: any): void;
}

export function VisualizationFilterRow(props: VisualizationFilterRowProps) {
  const [filters, setFilters] = useState(props.filter);
  useEffect(() => {
    props.onChange?.(filters);
  }, [filters]);
  return (
    <Collapsible key={props.name} className="group/collapsible">
      <CollapsibleTrigger className="w-full">
        <div className="group/label rounded-md items-center p-2 flex justify-between space-x-3 w-full font-medium text-sm hover:bg-sidebar-accent hover:text-sidebar-accent-foreground">
          <span>{props.name}</span>
          <ChevronRight className="ml-auto transition-transform group-data-[state=open]/collapsible:rotate-90" />
        </div>
      </CollapsibleTrigger>
      <CollapsibleContent className="p-2">
        <Filter
          filters={filters}
          setFilters={setFilters}
          fields={FIELD_MAP[props.entityType]}
        />
      </CollapsibleContent>
    </Collapsible>
  );
}
