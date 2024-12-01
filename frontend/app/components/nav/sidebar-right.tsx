import * as React from "react";
import { Save } from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarSeparator,
} from "~/components/ui/sidebar";
import { Button } from "~/components/ui/button";

export function SidebarRight({
  ...props
}: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar
      collapsible="none"
      className="sticky flex top-0 h-[100vh-56px] rounded-lg border-2 border-sidebar-border"
      {...props}
    >
      <SidebarHeader className="border-b border-sidebar-border text-sm text-muted-foreground">
        Dashboard
      </SidebarHeader>
      <SidebarContent>
        <SidebarSeparator className="mx-0" />
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <Button className="w-full">
              <Save />
              Save
            </Button>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}
