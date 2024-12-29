import { Input } from "~/components/ui/input";
import { DatePicker } from "~/components/ui/date-picker";
import { useMemo, useState } from "react";
import { MultiSelect } from "~/components/ui/multi-select";
import { useResearchersPagination } from "~/lib/api/pagination";
import { mapParams } from "~/lib/links";
import { Routes } from "~/routes";
import { Button } from "~/components/ui/button";
import useDebounce from "~/lib/custom-utils";

export const StringInput = ({ value, onChange }) => (
  <Input
    type="text"
    value={value}
    onChange={(e) => onChange(e.target.value)}
    placeholder="Value"
    className="w-56"
  />
);

export const NumberInput = ({ value, onChange }) => (
  <Input
    type="number"
    value={value}
    onChange={(e) => onChange(Number(e.target.value))}
    placeholder="Value"
    className="w-56"
  />
);

export const DateInput = ({ value, onChange }) => {
  const presets = useMemo(() => {
    const lastHour = new Date();
    lastHour.setHours(lastHour.getHours() - 1);
    const lastMonth = new Date();
    lastMonth.setMonth(lastMonth.getMonth() - 1);
    const lastThreeMonths = new Date();
    lastThreeMonths.setMonth(lastThreeMonths.getMonth() - 3);
    const lastYear = new Date();
    lastYear.setFullYear(lastYear.getFullYear() - 1);
    const lastFiveYears = new Date();
    lastFiveYears.setFullYear(lastFiveYears.getFullYear() - 5);
    const lastTenYears = new Date();
    lastTenYears.setFullYear(lastTenYears.getFullYear() - 10);
    return [
      { label: "Last hour", date: lastHour },
      { label: "Last month", date: lastMonth },
      { label: "Last 3 months", date: lastThreeMonths },
      { label: "Last year", date: lastYear },
      { label: "Last 5 years", date: lastFiveYears },
      { label: "Last 10 years", date: lastTenYears },
    ];
  }, []);
  return (
    <DatePicker
      value={value ? new Date(value) : new Date()}
      onChange={(date: Date) => onChange(date.toISOString())}
      triggerClassName="w-56"
      presets={presets}
    />
  );
};

export const ResearcherPicker = ({ value, onChange }) => {
  const [search, setSearch] = useState<string>();
  const debouncedSearch = useDebounce(search, 500);
  const pagination = useResearchersPagination({
    limit: 20,
    q: undefined,
    search: debouncedSearch,
  });
  const options = useMemo(
    () =>
      pagination.data?.pages.flat().map((r) => ({
        value: r.uuid,
        label: r.full_name,
        link: mapParams(Routes.Researcher, { uuid: r.uuid }),
      })) ?? [],
    [pagination.data],
  );
  return (
    <MultiSelect
      options={options}
      onValueChange={onChange}
      selectedValue={value || []}
      className="w-72"
      maxCount={1}
      onSearch={setSearch}
      loadMoreButton={
        <Button
          variant="outline"
          size="sm"
          onClick={() => pagination.fetchNextPage()}
        >
          Load more
        </Button>
      }
    />
  );
};
