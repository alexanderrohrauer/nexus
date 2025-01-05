import type { LoaderFunctionArgs } from "@remix-run/node";
import { client } from "~/lib/api/api-client";
import { useLoaderData } from "@remix-run/react";
import { DuplicationSection } from "~/components/templates/duplication-section";
import type { SchemaWorkOutput } from "~/lib/api/types";

interface WorkProps {}

export const loader = async ({ params }: LoaderFunctionArgs) => {
  const work = await client
    .GET("/works/{uuid}", {
      params: { path: { uuid: params.slug } },
    })
    .then((res) => res.data);
  const duplicates = await client
    .GET("/works/{uuid}/duplicates", {
      params: { path: { uuid: params.slug } },
    })
    .then((res) => res.data);
  return { work, duplicates };
};

export default function Work(props: WorkProps) {
  const { work, duplicates } = useLoaderData<typeof loader>();
  return (
    <div>
      <span>{work.title}</span>
      {duplicates.length > 0 && (
        <section>
          <DuplicationSection
            entity={work}
            duplicates={duplicates}
            mutateUrl="/works/{uuid}/mark-for-removal"
            renderName={(entity: SchemaWorkOutput) => entity.title}
          />
        </section>
      )}
    </div>
  );
}
