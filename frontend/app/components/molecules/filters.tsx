import { Input } from "~/components/ui/input";
import { DatePicker } from "~/components/ui/date-picker";
import React, { useMemo, useState } from "react";
import { MultiSelect } from "~/components/ui/multi-select";
import {
  useInstitutionsPagination,
  useResearchersPagination,
  useWorksPagination,
} from "~/lib/api/pagination";
import { mapParams } from "~/lib/links";
import { Routes } from "~/routes";
import { Button } from "~/components/ui/button";
import useDebounce from "~/lib/custom-utils";
import { Switch } from "~/components/ui/switch";
import { Checkbox } from "~/components/ui/checkbox";
import { Label } from "~/components/ui/label";

const Nullable = ({ value, onChange, emptyValue, children }) => (
  <div className="flex items-center space-x-2">
    <div className="flex items-center space-x-2">
      <Checkbox
        checked={value === null}
        onCheckedChange={() => onChange(value === null ? emptyValue : null)}
      />
      <Label>Null</Label>
    </div>

    {children}
  </div>
);

export const StringInput = ({ value, onChange }) => (
  <Nullable value={value} onChange={onChange} emptyValue={""}>
    <Input
      type="text"
      value={value ?? ""}
      onChange={(e) => onChange(e.target.value)}
      placeholder="Value"
      className="w-56"
      disabled={value == null}
    />
  </Nullable>
);

export const BooleanInput = ({ value, onChange }) => (
  <Nullable value={value} onChange={onChange} emptyValue={false}>
    <Switch
      checked={value ?? false}
      onCheckedChange={(checked) => onChange(checked)}
      disabled={value == null}
    />
  </Nullable>
);

export const NumberInput = ({ value, onChange }) => (
  <Nullable value={value} onChange={onChange} emptyValue={0}>
    <Input
      type="number"
      value={value ?? 0}
      onChange={(e) => onChange(Number(e.target.value))}
      placeholder="Value"
      className="w-56"
      disabled={value == null}
    />
  </Nullable>
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
    <Nullable value={value} onChange={onChange} emptyValue={new Date()}>
      <DatePicker
        value={value ? new Date(value) : new Date()}
        onChange={(date: Date) => onChange(date.toISOString())}
        triggerClassName="w-56"
        presets={presets}
        disabled={value == null}
      />
    </Nullable>
  );
};

export const WorkPicker = ({ value, onChange }) => {
  const [search, setSearch] = useState<string>();
  const debouncedSearch = useDebounce(search, 500);
  const pagination = useWorksPagination({
    limit: 20,
    q: undefined,
    search: debouncedSearch,
  });
  const options = useMemo(
    () =>
      pagination.data?.pages.flat().map((r) => ({
        value: r.uuid,
        label: r.title,
        link: mapParams(Routes.Institution, { uuid: r.uuid }),
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

export const InstitutionPicker = ({ value, onChange }) => {
  const [search, setSearch] = useState<string>();
  const debouncedSearch = useDebounce(search, 500);
  const pagination = useInstitutionsPagination({
    limit: 20,
    q: undefined,
    search: debouncedSearch,
  });
  const options = useMemo(
    () =>
      pagination.data?.pages.flat().map((r) => ({
        value: r.uuid,
        label: r.name,
        link: mapParams(Routes.Institution, { uuid: r.uuid }),
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
