"use client";

import * as React from "react";
import {
  Blocks,
  Calendar,
  Landmark,
  Library,
  MessageCircleQuestion,
  Search,
  Settings2,
  Trash2,
  Users,
} from "lucide-react";

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
      title: "Search",
      url: "#",
      icon: Search,
    },
    {
      title: "Researchers",
      url: Routes.Researchers,
      icon: Users,
    },
    {
      title: "Works",
      url: Routes.Works,
      icon: Library,
    },
    {
      title: "Institutions",
      url: "#",
      icon: Landmark,
      badge: "10",
    },
  ],
  navSecondary: [
    {
      title: "Calendar",
      url: "#",
      icon: Calendar,
    },
    {
      title: "Settings",
      url: "#",
      icon: Settings2,
    },
    {
      title: "Templates",
      url: "#",
      icon: Blocks,
    },
    {
      title: "Trash",
      url: "#",
      icon: Trash2,
    },
    {
      title: "Help",
      url: "#",
      icon: MessageCircleQuestion,
    },
  ],
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
