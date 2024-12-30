import React, { useEffect } from "react";
import { useNav } from "~/components/context/nav-context";
import { useResearchersPagination } from "~/lib/api/pagination";
import { useSearchParams } from "@remix-run/react";
import useDebounce from "~/lib/custom-utils";
import { Overview } from "~/components/templates/overview";
import { Routes } from "~/routes";
import type { SchemaResearcher } from "~/lib/api/types";
import { RESEARCHER_FIELDS } from "~/lib/filters";
import { OverviewListItem } from "~/components/molecules/overview-list-item";

interface ResearchersProps {}

export default function Researchers(props: ResearchersProps) {
  const { setPageName } = useNav();
  useEffect(() => {
    setPageName("Researchers");
  }, []);
  const [searchParams] = useSearchParams();
  const debouncedSearch = useDebounce(searchParams.get("search"), 500);
  const pagination = useResearchersPagination({
    q: searchParams.has("q")
      ? decodeURIComponent(searchParams.get("q"))
      : undefined,
    limit: 20,
    search: debouncedSearch,
  });
  return (
    <Overview
      renderItem={(researcher: SchemaResearcher) => (
        <OverviewListItem
          uuid={researcher.uuid}
          route={Routes.Researcher}
          title={researcher.full_name}
          item={researcher}
          subTitle={researcher.institution && researcher.institution.name}
          key={researcher.uuid}
        />
      )}
      filterFields={RESEARCHER_FIELDS}
      pagination={pagination}
    />
  );
}
