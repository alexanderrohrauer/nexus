import type { LoaderFunctionArgs } from "@remix-run/node";
import { client } from "~/lib/api/api-client";
import { useLoaderData } from "@remix-run/react";
import { DuplicationSection } from "~/components/templates/duplication-section";
import type { SchemaInstitution } from "~/lib/api/types";
import { ChartType, EntityType } from "~/lib/api/types";
import { InstitutionProfile } from "~/components/charts/institution-profile";
import { ProfileSection } from "~/components/molecules/profile-section";
import { ProfileVisualization } from "~/components/templates/profile-visualization";
import React from "react";
import { InstitutionCurrentResearchers } from "~/components/charts/institution-current-researchers";
import { Routes } from "~/routes";

interface InstitutionProps {}

export const loader = async ({ params }: LoaderFunctionArgs) => {
  const institution = await client
    .GET("/institutions/{uuid}", {
      params: { path: { uuid: params.slug } },
    })
    .then((res) => res.data);
  const duplicates = await client
    .GET("/institutions/{uuid}/duplicates", {
      params: { path: { uuid: params.slug } },
    })
    .then((res) => res.data);
  const visualizations = await client
    .GET("/charts/{chart_type}", {
      params: { path: { chart_type: ChartType.INSTITUTION } },
    })
    .then((res) => res.data);
  return { institution, duplicates, visualizations };
};

export default function Institution(props: InstitutionProps) {
  const { institution, duplicates, visualizations } =
    useLoaderData<typeof loader>();
  return (
    <div className="space-y-6 h-full overflow-y-auto pr-3">
      <InstitutionProfile institution={institution} />
      {duplicates.length > 0 && (
        <ProfileSection title="Duplicates">
          <DuplicationSection
            entity={institution}
            duplicates={duplicates}
            mutateUrl="/institutions/{uuid}/mark-for-removal"
            renderName={(entity: SchemaInstitution) => entity.name}
            route={Routes.Institution}
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
              entityType={EntityType.INSTITUTION}
              uuid={institution.uuid}
            >
              {({ options, response }) => (
                <>
                  {visualization.value ===
                    "institution_current_researchers" && (
                    <InstitutionCurrentResearchers
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
