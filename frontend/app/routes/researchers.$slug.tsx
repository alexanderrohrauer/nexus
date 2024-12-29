import type { LoaderFunctionArgs } from "@remix-run/node";
import { client } from "~/lib/api/api-client";
import { useLoaderData } from "@remix-run/react";

interface ResearcherProps {}

export const loader = async ({ params }: LoaderFunctionArgs) => {
  const researcher = await client
    .GET("/researchers/{uuid}", {
      params: { path: { uuid: params.slug } },
    })
    .then((res) => res.data);
  return { researcher };
};

export default function Researcher(props: ResearcherProps) {
  const { researcher } = useLoaderData<typeof loader>();
  return (
    <div>
      <span>{researcher.full_name}</span>
    </div>
  );
}
