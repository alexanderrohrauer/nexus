"use client";

import { ArrowUpRight, Link, MoreHorizontal, Trash2 } from "lucide-react";

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
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { client } from "~/lib/api/api-client";
import { ErrorBox } from "~/components/molecules/error-box";
import * as React from "react";
import { useRef } from "react";
import { NavLink } from "@remix-run/react";
import { mapParams } from "~/lib/links";
import { Routes } from "~/routes";
import { useLocation, useNavigate } from "react-router";
import type { SchemaDashboardMinimal } from "~/lib/api/types";
import { AddDashboardDialog } from "~/components/molecules/add-dashboard-dialog";
import type { ConfirmationModalRef } from "~/components/molecules/confirmation-modal";
import { ConfirmationModal } from "~/components/molecules/confirmation-modal";
import { useToast } from "~/lib/toast";

export function NavDashboards() {
  const { isMobile } = useSidebar();
  const location = useLocation();
  const queryClient = useQueryClient();
  const deleteConf = useRef<ConfirmationModalRef | null>(null);
  const navigate = useNavigate();
  const toast = useToast();

  // TODO error handler
  const { data: dashboards, error } = useQuery({
    queryKey: ["dashboards"],
    queryFn: () => client.GET("/dashboards").then((r) => r.data),
  });

  const deleteMutation = useMutation({
    mutationFn: (uuid: string) =>
      client.DELETE("/dashboards/{uuid}", {
        params: { path: { uuid: uuid } },
      }),
    onSuccess: async (data, variables) => {
      toast.success("Dashboard successfully deleted");
      await queryClient.invalidateQueries({ queryKey: ["dashboards"] });
      const navUrl = mapParams(Routes.Dashboard, { uuid: variables });
      if (location.pathname === navUrl) {
        setTimeout(() => navigate(Routes.Home), 200);
      }
    },
  });

  const isActive = (dashboard: SchemaDashboardMinimal) => {
    const navUrl = mapParams(Routes.Dashboard, { uuid: dashboard.uuid });
    return location.pathname === navUrl;
  };

  const copy = async (dashboard: SchemaDashboardMinimal) => {
    const url = new URL(window.location.href);
    url.pathname = mapParams(Routes.Dashboard, { uuid: dashboard.uuid });
    await navigator.clipboard.writeText(url.toString());
    toast.info("Link copied!", { duration: 2000 });
  };

  // TODO fix error/loading handling
  return (
    <SidebarGroup className="group-data-[collapsible=icon]:hidden">
      <SidebarGroupLabel>Dashboards</SidebarGroupLabel>
      {!error && dashboards ? (
        <SidebarMenu>
          {dashboards.map((item) => (
            <SidebarMenuItem key={"dashboard-" + item.uuid}>
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
                  <DropdownMenuItem onClick={() => copy(item)}>
                    <Link className="text-muted-foreground" />
                    <span>Copy Link</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild>
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
                  {/*<DropdownMenuItem>*/}
                  {/*  <Edit className="text-muted-foreground" />*/}
                  {/*  <span>Edit</span>*/}
                  {/*</DropdownMenuItem>*/}
                  <DropdownMenuItem
                    className="text-destructive"
                    onClick={() => deleteConf.current?.trigger(item)}
                  >
                    <Trash2 />
                    <span>Delete</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </SidebarMenuItem>
          ))}
          <SidebarMenuItem>
            <AddDashboardDialog />
          </SidebarMenuItem>
        </SidebarMenu>
      ) : (
        <ErrorBox />
      )}
      <ConfirmationModal
        variant="destructive"
        title="Delete dashboard"
        description="Do you really want to delete this dashboard?"
        okText="Delete"
        ok={(dashboard: SchemaDashboardMinimal) =>
          deleteMutation.mutateAsync(dashboard.uuid)
        }
        ref={deleteConf}
      />
    </SidebarGroup>
  );
}
