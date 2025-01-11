import React from "react";
import type {
  SchemaResearcher,
  SchemaVisualizationData,
} from "~/lib/api/types";
import { NavLink } from "@remix-run/react";
import { mapParams } from "~/lib/links";
import { Routes } from "~/routes";
import type { ChartOptions } from "../../../custom-types";
import { Flag } from "~/components/molecules/misc";

interface InstitutionCurrentResearchersProps {
  options: ChartOptions<[SchemaResearcher[]]>;
  response: SchemaVisualizationData;
  showInstitution?: boolean;
}
export function InstitutionCurrentResearchers(
  props: InstitutionCurrentResearchersProps,
) {
  return (
    <div className="max-h-96 overflow-y-auto space-y-4">
      {props.options.series[0].map((researcher) => {
        return (
          <NavLink
            key={researcher.uuid}
            to={mapParams(Routes.Researcher, {
              uuid: researcher.uuid,
            })}
            target="_blank"
            className="block whitespace-nowrap border-b p-4 leading-tight last:border-b-0 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
          >
            <div>
              <span className="font-bold">{researcher.full_name}</span>
              {props.showInstitution && researcher.institution && (
                <div className="flex space-x-1 items-center mt-1">
                  <Flag
                    code={researcher.institution.country}
                    className="!w-4"
                  />
                  <span className="text-muted-foreground text-sm">
                    {researcher.institution.name}
                  </span>
                </div>
              )}
            </div>
          </NavLink>
        );
      })}
      {props.options.series[0].length == 0 && (
        <span className="empty-state">No researchers found</span>
      )}
    </div>
  );
}
