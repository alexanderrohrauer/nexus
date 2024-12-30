import type { LoaderFunctionArgs } from "@remix-run/node";
import { client } from "~/lib/api/api-client";
import { useLoaderData } from "@remix-run/react";

interface ResearcherProps {}

export const loader = async ({ params }: LoaderFunctionArgs) => {
  const work = await client
    .GET("/works/{uuid}", {
      params: { path: { uuid: params.slug } },
    })
    .then((res) => res.data);
  return { work };
};

export default function Researcher(props: ResearcherProps) {
  const { work } = useLoaderData<typeof loader>();
  return (
    <div>
      <span>{work.title}</span>
    </div>
  );
}
