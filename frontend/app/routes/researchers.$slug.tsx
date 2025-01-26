import type { LoaderFunctionArgs } from "@remix-run/node";
import { client } from "~/lib/api/api-client";
import { useLoaderData } from "@remix-run/react";
import { DuplicationSection } from "~/components/templates/duplication-section";
import type { SchemaResearcher } from "~/lib/api/types";
import { ChartType, EntityType } from "~/lib/api/types";
import React from "react";
import { ProfileVisualization } from "~/components/templates/profile-visualization";
import { ProfileSection } from "~/components/molecules/profile-section";
import { AffiliationsVisualization } from "~/components/charts/affiliations-visualization";
import { ResearcherProfile } from "~/components/charts/researcher-profile";
import { Routes } from "~/routes";

interface ResearcherProps {}

export const loader = async ({ params }: LoaderFunctionArgs) => {
  const researcher = await client
    .GET("/researchers/{uuid}", {
      params: { path: { uuid: params.slug } },
    })
    .then((res) => res.data);
  const duplicates = await client
    .GET("/researchers/{uuid}/duplicates", {
      params: { path: { uuid: params.slug } },
    })
    .then((res) => res.data);
  const visualizations = await client
    .GET("/charts/{chart_type}", {
      params: { path: { chart_type: ChartType.RESEARCHER } },
    })
    .then((res) => res.data);
  return { researcher, duplicates, visualizations };
};

export default function Researcher(props: ResearcherProps) {
  const { researcher, duplicates, visualizations } =
    useLoaderData<typeof loader>();
  return (
    <div className="space-y-6 h-full overflow-y-auto pr-3">
      <ResearcherProfile researcher={researcher} />
      {duplicates.length > 0 && (
        <ProfileSection title="Duplicates">
          <DuplicationSection
            entity={researcher}
            duplicates={duplicates}
            mutateUrl="/researchers/{uuid}/mark-for-removal"
            renderName={(entity: SchemaResearcher) => entity.full_name}
            route={Routes.Researcher}
          />
        </ProfileSection>
      )}
      <ProfileSection title="Visualizations">
        <div className="space-y-2">
          {visualizations.map((visualization) => (
            <ProfileVisualization
              key={visualization.value}
              identifier={visualization.value}
              title={visualization.label}
              entityType={EntityType.RESEARCHER}
              uuid={researcher.uuid}
            >
              {({ options, response }) => (
                <>
                  {visualization.value === "researcher_affiliations" && (
                    <AffiliationsVisualization
                      options={options}
                      response={response}
                    />
                  )}
                </>
              )}
            </ProfileVisualization>
          ))}
        </div>
      </ProfileSection>
    </div>
  );
}
