"use client";

import {
  ArrowUpRight,
  Edit,
  Link,
  MoreHorizontal,
  Plus,
  Trash2,
} from "lucide-react";

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "~/components/ui/dropdown-menu";
import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuAction,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "~/components/ui/sidebar";
import { useQuery } from "@tanstack/react-query";
import { client } from "~/lib/api/api-client";
import { ErrorBox } from "~/components/molecules/error-box";
import * as React from "react";
import { NavLink } from "@remix-run/react";
import { mapParams } from "~/lib/links";
import { Routes } from "~/routes";
import { useLocation } from "react-router";
import { SchemaDashboardMinimal } from "~/lib/api/types";

export function NavDashboards() {
  const { isMobile } = useSidebar();
  const location = useLocation();

  const { data: dashboards, error } = useQuery({
    queryKey: ["dashboards"],
    queryFn: () => client.GET("/dashboards").then((r) => r.data),
  });

  const isActive = (dashboard: SchemaDashboardMinimal) => {
    const navUrl = mapParams(Routes.Dashboard, { uuid: dashboard.uuid });
    return location.pathname === navUrl;
  };

  // TODO fix error/loading handling
  return (
    <SidebarGroup className="group-data-[collapsible=icon]:hidden">
      <SidebarGroupLabel>Dashboards</SidebarGroupLabel>
      {!error && dashboards ? (
        <SidebarMenu>
          {dashboards.map((item) => (
            <SidebarMenuItem key={item.title}>
              <SidebarMenuButton asChild isActive={isActive(item)}>
                <NavLink to={mapParams(Routes.Dashboard, { uuid: item.uuid })}>
                  {item.title}
                </NavLink>
              </SidebarMenuButton>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <SidebarMenuAction showOnHover>
                    <MoreHorizontal />
                    <span className="sr-only">More</span>
                  </SidebarMenuAction>
                </DropdownMenuTrigger>
                <DropdownMenuContent
                  className="w-56 rounded-lg"
                  side={isMobile ? "bottom" : "right"}
                  align={isMobile ? "end" : "start"}
                >
                  <DropdownMenuItem>
                    <Link className="text-muted-foreground" />
                    <span>Copy Link</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <NavLink
                      to={mapParams(Routes.Dashboard, { uuid: item.uuid })}
                      target="_blank"
                      className="flex items-center gap-2"
                    >
                      <ArrowUpRight className="text-muted-foreground" />
                      <span>Open in New Tab</span>
                    </NavLink>
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem>
                    <Edit className="text-muted-foreground" />
                    <span>Edit</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem className="text-destructive">
                    <Trash2 />
                    <span>Delete</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </SidebarMenuItem>
          ))}
          <SidebarMenuItem>
            <SidebarMenuButton className="text-sidebar-foreground/70">
              <Plus />
              <span>Add dashboard</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      ) : (
        <ErrorBox />
      )}
    </SidebarGroup>
  );
}
