import { AppSidebar } from "~/components/nav/app-sidebar";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbList,
  BreadcrumbPage,
} from "~/components/ui/breadcrumb";
import { Separator } from "~/components/ui/separator";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "~/components/ui/sidebar";
import { useDashboard } from "~/components/context/dashboard-context";
import { useMemo } from "react";
import { Button } from "~/components/ui/button";
import { Edit } from "lucide-react";
import { AddVisualizationDialog } from "~/components/molecules/add-visualization-dialog";

export function Nav(props: React.PropsWithChildren) {
  const { dashboard } = useDashboard();

  const title = useMemo(
    () => (dashboard ? dashboard.title : "Page"),
    [dashboard],
  );

  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset className="px-3">
        <header className="sticky top-0 flex h-14 shrink-0 items-center gap-2 bg-background">
          <div className="flex flex-1 items-center gap-2">
            <SidebarTrigger />
            <Separator orientation="vertical" className="mr-2 h-4" />
            <Breadcrumb>
              <BreadcrumbList>
                <BreadcrumbItem>
                  <BreadcrumbPage className="line-clamp-1">
                    {title}
                  </BreadcrumbPage>
                </BreadcrumbItem>
              </BreadcrumbList>
            </Breadcrumb>
          </div>
          {dashboard && (
            <div className="flex space-x-3">
              <Button variant="outline" size="icon">
                <Edit />
              </Button>
              <AddVisualizationDialog dashboard={dashboard} />
            </div>
          )}
        </header>
        {props.children}
      </SidebarInset>
    </SidebarProvider>
  );
}
