"use client";

import * as React from "react";
import { HomeIcon, Landmark, Library, Users } from "lucide-react";

import { NavDashboards } from "~/components/nav/nav-dashboards";
import { NavMain } from "~/components/nav/nav-main";
import { NavSecondary } from "~/components/nav/nav-secondary";
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarRail,
} from "~/components/ui/sidebar";
import { Routes } from "~/routes";

const data = {
  navMain: [
    {
      title: "Home",
      url: Routes.Home,
      icon: HomeIcon,
      idPrefix: "_index",
    },
    {
      title: "Works",
      url: Routes.Works,
      icon: Library,
      idPrefix: "works",
    },
    {
      title: "Researchers",
      url: Routes.Researchers,
      icon: Users,
      idPrefix: "researchers",
    },
    {
      title: "Institutions",
      url: Routes.Institutions,
      icon: Landmark,
      badge: "10",
      idPrefix: "institutions",
    },
  ],
  navSecondary: [],
};

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar className="border-r-0" {...props}>
      <SidebarHeader>
        <NavMain items={data.navMain} />
      </SidebarHeader>
      <SidebarContent>
        <NavDashboards />
        <NavSecondary items={data.navSecondary} className="mt-auto" />
      </SidebarContent>
      <SidebarRail />
    </Sidebar>
  );
}
