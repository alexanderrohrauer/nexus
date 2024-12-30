import React, { useEffect } from "react";
import { useNav } from "~/components/context/nav-context";
import { useWorksPagination } from "~/lib/api/pagination";
import { useSearchParams } from "@remix-run/react";
import useDebounce from "~/lib/custom-utils";
import { Overview } from "~/components/templates/overview";
import { Routes } from "~/routes";
import type { SchemaWork } from "~/lib/api/types";
import { WORK_FIELDS } from "~/lib/filters";
import { OverviewListItem } from "~/components/molecules/overview-list-item";

interface ResearchersProps {}

export default function Researchers(props: ResearchersProps) {
  const { setPageName } = useNav();
  useEffect(() => {
    setPageName("Works");
  }, []);
  const [searchParams] = useSearchParams();
  const debouncedSearch = useDebounce(searchParams.get("search"), 500);
  const pagination = useWorksPagination({
    q: searchParams.has("q")
      ? decodeURIComponent(searchParams.get("q"))
      : undefined,
    limit: 20,
    search: debouncedSearch,
  });
  const getWorkSubtitle = (work: SchemaWork) => {
    const name =
      work.authors.length >= 3
        ? work.authors[0].full_name + " et al."
        : work.authors
            .slice(0, 2)
            .map((a) => a.full_name)
            .join(", ");
    return name + ` (${work.publication_year})`;
  };

  return (
    <Overview
      renderItem={(work: SchemaWork) => (
        <OverviewListItem
          uuid={work.uuid}
          route={Routes.Work}
          title={work.title}
          item={work}
          subTitle={getWorkSubtitle(work)}
          key={work.uuid}
        />
      )}
      filterFields={WORK_FIELDS}
      pagination={pagination}
    />
  );
}
