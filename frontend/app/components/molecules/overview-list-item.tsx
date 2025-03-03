import React from "react";
import { clsx } from "clsx";
import { mapParams } from "~/lib/links";
import type { Routes } from "~/routes";
import { NavLink, useSearchParams } from "@remix-run/react";
import { Sources } from "~/components/molecules/sources";
import type { Entity } from "../../../custom-types";

interface OverviewListItemProps {
  uuid: string;
  route: Routes;
  title: string;
  subTitle?: string | null;
  item: Entity;
}

export function OverviewListItem({
  uuid,
  route,
  title,
  subTitle,
  item,
}: OverviewListItemProps) {
  const [searchParams] = useSearchParams();
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
        <Sources item={item} />{" "}
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
