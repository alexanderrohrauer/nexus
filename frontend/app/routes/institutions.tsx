import React, { useEffect } from "react";
import { useNav } from "~/components/context/nav-context";
import { useInstitutionsPagination } from "~/lib/api/pagination";
import { useSearchParams } from "@remix-run/react";
import useDebounce from "~/lib/custom-utils";
import { Overview } from "~/components/templates/overview";
import { Routes } from "~/routes";
import type { SchemaInstitution } from "~/lib/api/types";
import { INSTITUTION_FIELDS } from "~/lib/filters";
import { OverviewListItem } from "~/components/molecules/overview-list-item";
import { getCountryName } from "~/lib/text-util";

interface ResearchersProps {}

export default function Researchers(props: ResearchersProps) {
  const { setPageName } = useNav();
  useEffect(() => {
    setPageName("Institutions");
  }, []);
  const [searchParams] = useSearchParams();
  const debouncedSearch = useDebounce(searchParams.get("search"), 500);
  const pagination = useInstitutionsPagination({
    q: searchParams.has("q")
      ? decodeURIComponent(searchParams.get("q"))
      : undefined,
    limit: 20,
    search: debouncedSearch,
  });
  return (
    <Overview
      renderItem={(institution: SchemaInstitution) => (
        <OverviewListItem
          uuid={institution.uuid}
          route={Routes.Institution}
          title={institution.name}
          item={institution}
          subTitle={getCountryName(institution.country)}
          key={institution.uuid}
        />
      )}
      filterFields={INSTITUTION_FIELDS}
      pagination={pagination}
    />
  );
}
