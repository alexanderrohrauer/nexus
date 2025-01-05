import type { LoaderFunctionArgs } from "@remix-run/node";
import { client } from "~/lib/api/api-client";
import { useLoaderData } from "@remix-run/react";
import { DuplicationSection } from "~/components/templates/duplication-section";
import type { SchemaResearcher } from "~/lib/api/types";

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
  return { researcher, duplicates };
};

export default function Researcher(props: ResearcherProps) {
  const { researcher, duplicates } = useLoaderData<typeof loader>();
  return (
    <div>
      <span>{researcher.full_name}</span>
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
