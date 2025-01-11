import type { LoaderFunctionArgs } from "@remix-run/node";
import { client } from "~/lib/api/api-client";
import { useLoaderData } from "@remix-run/react";
import { DuplicationSection } from "~/components/templates/duplication-section";
import type { SchemaInstitution } from "~/lib/api/types";
import { InstitutionProfile } from "~/components/charts/institution-profile";
import { ProfileSection } from "~/components/molecules/profile-section";

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
    <div className="space-y-6 h-full overflow-y-auto pr-3">
      <InstitutionProfile institution={institution} />
      {duplicates.length > 0 && (
        <ProfileSection title="Duplicates">
          <DuplicationSection
            entity={institution}
            duplicates={duplicates}
            mutateUrl="/institutions/{uuid}/mark-for-removal"
            renderName={(entity: SchemaInstitution) => entity.name}
          />
        </ProfileSection>
      )}
    </div>
  );
}
