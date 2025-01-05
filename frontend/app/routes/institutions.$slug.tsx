import type { LoaderFunctionArgs } from "@remix-run/node";
import { client } from "~/lib/api/api-client";
import { useLoaderData } from "@remix-run/react";
import { DuplicationSection } from "~/components/templates/duplication-section";
import type { SchemaInstitution } from "~/lib/api/types";

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
  return { institution, duplicates };
};

export default function Institution(props: InstitutionProps) {
  const { institution, duplicates } = useLoaderData<typeof loader>();
  return (
    <div>
      <span>{institution.name}</span>
      {duplicates.length > 0 && (
        <section>
          <DuplicationSection
            entity={institution}
            duplicates={duplicates}
            mutateUrl="/institutions/{uuid}/mark-for-removal"
            renderName={(entity: SchemaInstitution) => entity.name}
          />
        </section>
      )}
    </div>
  );
}
