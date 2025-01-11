import React from "react";
import { Outlet, useSearchParams } from "@remix-run/react";
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
} from "~/components/ui/sidebar";
import { Input } from "~/components/ui/input";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogTitle,
  DialogTrigger,
} from "~/components/ui/dialog";
import { Button } from "~/components/ui/button";
import { FilterIcon } from "lucide-react";
import Filter from "~/components/molecules/filter";
import Loader from "~/components/molecules/loader";
import type { UseInfiniteQueryResult } from "@tanstack/react-query";
import { useFilterState } from "~/components/context/filter-context";
import { useNav } from "~/components/context/nav-context";

interface OverviewProps {
  renderItem: (item: unknown) => React.ReactNode;
  filterFields: any;
  pagination: UseInfiniteQueryResult<{ pages: unknown[] }>;
}

export function Overview({
  renderItem,
  pagination,
  filterFields,
}: OverviewProps) {
  const { pageName } = useNav();
  const { filters, setFilters, applyFilters } = useFilterState();
  const [searchParams, setSearchParams] = useSearchParams();
  const items = pagination.data?.pages.flat() ?? [];
  return (
    <div className="h-[calc(100vh-68px)] flex">
      <Sidebar
        collapsible="none"
        className="!bg-transparent !w-max border-r border-r-border"
      >
        <SidebarHeader className="gap-3.5 border-b pb-4">
          <div className="flex w-full items-center justify-between">
            <div className="text-base font-medium text-foreground">
              {pageName}
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
              <DialogContent className="max-w-max top-40">
                <DialogTitle>Filter</DialogTitle>
                <Filter
                  fields={filterFields}
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
        <SidebarContent className="gap-0 overflow-y-auto w-80 overflow-x-hidden">
          <Loader task={pagination}>{items.map(renderItem)}</Loader>
          <Button
            variant="ghost"
            className="mt-3"
            onClick={() => pagination.fetchNextPage()}
          >
            Load more
          </Button>
        </SidebarContent>
      </Sidebar>
      <div className="flex-1 pl-3">
        <Outlet />
      </div>
    </div>
  );
}
