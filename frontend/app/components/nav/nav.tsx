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
import { useNav } from "~/components/context/nav-context";
import { Button } from "~/components/ui/button";
import { Edit } from "lucide-react";
import { AddVisualizationDialog } from "~/components/molecules/add-visualization-dialog";

export function Nav(props: React.PropsWithChildren) {
  const { dashboard, pageName } = useNav();

  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset className="px-3">
        <header className="sticky top-0 flex h-14 shrink-0 items-center gap-2 bg-background z-50">
          <div className="flex flex-1 items-center gap-2">
            <SidebarTrigger />
            <Separator orientation="vertical" className="mr-2 h-4" />
            <Breadcrumb>
              <BreadcrumbList>
                <BreadcrumbItem>
                  <BreadcrumbPage className="line-clamp-1">
                    {pageName}
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
