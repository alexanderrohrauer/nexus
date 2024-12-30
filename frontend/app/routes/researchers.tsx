import React, { useEffect } from "react";
import { useNav } from "~/components/context/nav-context";
import { NavLink, Outlet, useSearchParams } from "@remix-run/react";
import { useFilterState } from "~/components/context/filter-context";
import { Button } from "~/components/ui/button";
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
} from "~/components/ui/sidebar";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogTitle,
  DialogTrigger,
} from "~/components/ui/dialog";
import Filter from "~/components/molecules/filter";
import { FilterIcon, Users } from "lucide-react";
import { Input } from "~/components/ui/input";
import { mapParams } from "~/lib/links";
import { Routes } from "~/routes";
import { clsx } from "clsx";
import { useResearchersPagination } from "~/lib/api/pagination";
import Loader from "~/components/molecules/loader";
import useDebounce from "~/lib/custom-utils";
import { RESEARCHER_FIELDS } from "~/lib/filters";

interface ResearchersProps {}

export default function Researchers(props: ResearchersProps) {
  const { setPageName } = useNav();
  useEffect(() => {
    setPageName("Researchers");
  }, []);
  const { filters, setFilters, applyFilters } = useFilterState();
  const [searchParams, setSearchParams] = useSearchParams();
  const debouncedSearch = useDebounce(searchParams.get("search"), 500);
  const pagination = useResearchersPagination({
    q: searchParams.has("q")
      ? decodeURIComponent(searchParams.get("q"))
      : undefined,
    limit: 20,
    search: debouncedSearch,
  });
  const researchers = pagination.data?.pages.flat() ?? [];
  return (
    <div className="h-[calc(100vh-68px)] flex">
      <Sidebar
        collapsible="none"
        className="!bg-transparent !w-max border-r border-r-border"
      >
        <SidebarHeader className="gap-3.5 border-b pb-4">
          <div className="flex w-full items-center justify-between">
            <div className="text-base font-medium text-foreground">
              Researchers
            </div>
            {/*  TODO implement sorts*/}
          </div>
          <div className="flex space-x-2">
            <Input
              placeholder="Type to search..."
              onInput={(e) => {
                searchParams.set(
                  "search",
                  (e.target as HTMLInputElement).value,
                );
                setSearchParams(searchParams);
              }}
            />
            <Dialog>
              <DialogTrigger asChild>
                <Button size="icon" variant="outline" className="relative">
                  <FilterIcon />
                  {searchParams.has("q") && (
                    <div className="rounded-full bg-red-500 h-2 w-2 absolute right-1.5 top-2" />
                  )}
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-max">
                <DialogTitle>Filter</DialogTitle>
                <Filter
                  fields={RESEARCHER_FIELDS}
                  filters={filters}
                  setFilters={setFilters}
                />
                <DialogFooter>
                  <DialogTrigger asChild>
                    <Button onClick={applyFilters}>Apply</Button>
                  </DialogTrigger>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </div>
        </SidebarHeader>
        <SidebarContent className="gap-0 overflow-y-auto">
          <Loader task={pagination}>
            {researchers.map((researcher) => (
              <NavLink
                key={researcher.uuid}
                className={({ isActive }) =>
                  clsx(
                    "flex flex-col items-start gap-2 whitespace-nowrap border-b p-4 text-sm leading-tight last:border-b-0 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground",
                    isActive &&
                      "bg-sidebar-accent text-sidebar-accent-foreground",
                  )
                }
                to={
                  mapParams(Routes.Researcher, { uuid: researcher.uuid }) +
                  `?${searchParams}`
                }
              >
                <div className="flex w-full items-center gap-2">
                  <div className="text-xs flex space-x-1 items-center">
                    {/*TODO maybe render the source (dblp) here*/}
                    <Users size="12" strokeWidth={2.5} />
                    <span>Researcher</span>
                  </div>{" "}
                  <span className="ml-auto text-xs" suppressHydrationWarning>
                    {new Date(researcher.imported_at).toLocaleString()}
                  </span>
                </div>
                <span className="font-medium text-md">
                  {researcher.full_name}
                </span>
                {researcher.institution && (
                  <span className="line-clamp-2 w-[260px] whitespace-break-spaces text-xs">
                    {researcher.institution.name}
                  </span>
                )}
              </NavLink>
            ))}
          </Loader>
          <Button
            variant="ghost"
            className="mt-3"
            onClick={() => pagination.fetchNextPage()}
          >
            Load more
          </Button>
        </SidebarContent>
      </Sidebar>
      <div className="flex-1 px-3">
        <Outlet />
      </div>
    </div>
  );
}
