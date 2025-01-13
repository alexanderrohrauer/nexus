import React from "react";
import type { SchemaVisualizationData } from "~/lib/api/types";
import { NavLink } from "@remix-run/react";
import { mapParams } from "~/lib/links";
import { Routes } from "~/routes";
import { TextTooltip } from "~/components/molecules/text-tooltip";
import type { ChartOptions } from "../../../custom-types";
import { Flag } from "~/components/molecules/misc";

interface AffiliationsSectionProps {
  options: ChartOptions<[any]>;
  response: SchemaVisualizationData;
}
export function AffiliationsVisualization(props: AffiliationsSectionProps) {
  return (
    <div className="space-y-4">
      {props.options.series[0]
        .sort((a1, a2) => {
          const yearsMaxA1 = Math.max(...a1.years);
          const yearsMaxA2 = Math.max(...a2.years);
          return yearsMaxA2 - yearsMaxA1;
        })
        .map((affiliation) => {
          const firstYears = affiliation.years.slice(0, 10).join(", ");
          const plusMore = affiliation.years.length - 10;
          return (
            <NavLink
              key={affiliation.uuid}
              to={mapParams(Routes.Institution, {
                uuid: affiliation.institution.uuid,
              })}
              target="_blank"
              className="flex space-y-2 flex-col whitespace-nowrap border-b p-4 leading-tight last:border-b-0 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
            >
              <div className="flex space-x-1 items-center">
                {affiliation.institution.country && (
                  <Flag code={affiliation.institution.country} />
                )}
                <span className="font-bold">
                  {affiliation.institution.name}
                </span>
              </div>
              <span className="text-xs text-muted-foreground">
                {firstYears}{" "}
                {plusMore > 0 && (
                  <TextTooltip text={affiliation.years.slice(10).join(", ")}>
                    <span>+{plusMore} more</span>
                  </TextTooltip>
                )}
              </span>
            </NavLink>
          );
        })}
      {props.options.series[0].length == 0 && (
        <span className="empty-state">No affiliations found</span>
      )}
    </div>
  );
}
