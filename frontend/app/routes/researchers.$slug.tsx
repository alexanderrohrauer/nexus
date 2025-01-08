import type { LoaderFunctionArgs } from "@remix-run/node";
import { client } from "~/lib/api/api-client";
import { useLoaderData } from "@remix-run/react";
import { DuplicationSection } from "~/components/templates/duplication-section";
import type { SchemaResearcher } from "~/lib/api/types";
import React from "react";
import { AffiliationsSection } from "~/components/templates/affiliations-section";
import { Separator } from "~/components/ui/separator";

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
    .GET("/researchers/{uuid}/visualizations", {
      params: { path: { uuid: params.slug } },
    })
    .then((res) => res.data);
  return { researcher, duplicates, visualizations };
};

export default function Researcher(props: ResearcherProps) {
  const { researcher, duplicates, visualizations } =
    useLoaderData<typeof loader>();
  console.log(visualizations);
  return (
    <div className="space-y-6">
      <span>{researcher.full_name}</span>
      {visualizations?.affiliations && (
        <section>
          <div className="mb-2">
            <h1 className="text-xl font-semibold mb-1">Affiliations</h1>
            <Separator />
          </div>
          <AffiliationsSection
            entity={researcher}
            affiliations={visualizations.affiliations}
          />
        </section>
      )}
      {duplicates.length > 0 && (
        <section>
          <DuplicationSection
            entity={researcher}
            duplicates={duplicates}
            mutateUrl="/researchers/{uuid}/mark-for-removal"
            renderName={(entity: SchemaResearcher) => entity.full_name}
          />
        </section>
      )}
    </div>
  );
}
