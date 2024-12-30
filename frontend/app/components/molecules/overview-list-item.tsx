import React, { useMemo } from "react";
import { clsx } from "clsx";
import { mapParams } from "~/lib/links";
import type { Routes } from "~/routes";
import { NavLink, useSearchParams } from "@remix-run/react";
import { TextTooltip } from "~/components/molecules/text-tooltip";

interface OverviewListItemProps {
  uuid: string;
  route: Routes;
  title: string;
  subTitle?: string | null;
  item: { dblp_meta?: any; openalex_meta?: any; imported_at?: string };
}

export function OverviewListItem({
  uuid,
  route,
  title,
  subTitle,
  item,
}: OverviewListItemProps) {
  const [searchParams] = useSearchParams();
  const sources = useMemo(
    () =>
      Object.keys(item)
        .filter((i) => i.endsWith("_meta") && item[i])
        .map((i) => i.replace("_meta", "")),
    [item],
  );

  return (
    <NavLink
      key={uuid}
      className={({ isActive }) =>
        clsx(
          "flex flex-col items-start gap-2 whitespace-nowrap border-b p-4 text-sm leading-tight last:border-b-0 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground",
          isActive && "bg-sidebar-accent text-sidebar-accent-foreground",
        )
      }
      to={mapParams(route, { uuid: uuid }) + `?${searchParams}`}
    >
      <div className="flex w-full items-center gap-2">
        <div className="text-xs flex space-x-1 items-center">
          {sources.map((source) => (
            <TextTooltip text={source}>
              <img
                src={`/icons/sources/${source}.png`}
                className="h-4 w-4 bg-muted rounded-sm border border-border"
              />
            </TextTooltip>
          ))}
        </div>{" "}
        <span className="ml-auto text-xs" suppressHydrationWarning>
          {new Date(item.imported_at!).toLocaleString()}
        </span>
      </div>
      <span className="font-medium text-md text-wrap">{title}</span>
      {subTitle && (
        <span className="line-clamp-2 w-[260px] whitespace-break-spaces text-xs text-wrap">
          {subTitle}
        </span>
      )}
    </NavLink>
  );
}
