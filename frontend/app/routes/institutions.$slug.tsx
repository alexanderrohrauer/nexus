import type { LoaderFunctionArgs } from "@remix-run/node";
import { client } from "~/lib/api/api-client";
import { useLoaderData } from "@remix-run/react";

interface ResearcherProps {}

export const loader = async ({ params }: LoaderFunctionArgs) => {
  const institution = await client
    .GET("/institutions/{uuid}", {
      params: { path: { uuid: params.slug } },
    })
    .then((res) => res.data);
  return { institution };
};

export default function Researcher(props: ResearcherProps) {
  const { institution } = useLoaderData<typeof loader>();
  return (
    <div>
      <span>{institution.name}</span>
    </div>
  );
}
