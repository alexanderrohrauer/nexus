import { Button } from "~/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "~/components/ui/dialog";
import { InputField } from "~/components/ui/input";
import { Label } from "~/components/ui/label";
import { SchemaCreateDashboardRequest } from "~/lib/api/types";
import { Plus } from "lucide-react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { client } from "~/lib/api/api-client";
import { Form, Formik } from "formik";
import { useToast } from "~/lib/toast";
import * as React from "react";
import { useRef } from "react";
import { SidebarMenuButton } from "~/components/ui/sidebar";
import { mapParams } from "~/lib/links";
import { Routes } from "~/routes";
import { useNavigate } from "react-router";

interface AddDashboardDialogProps {}

const initialValues: SchemaCreateDashboardRequest = {
  title: "",
  visualizations: [],
};

export function AddDashboardDialog(props: AddDashboardDialogProps) {
  const btnRef = useRef<HTMLButtonElement | null>(null);
  const toast = useToast();
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  // TODO error handler
  const addMutation = useMutation({
    mutationFn: (data: SchemaCreateDashboardRequest) =>
      client.POST("/dashboards", {
        body: data,
      }),
    onSuccess: async ({ data }) => {
      await queryClient.invalidateQueries({ queryKey: ["dashboards"] });
      btnRef.current?.click();
      setTimeout(() => toast.success("Dashboard successfully created"), 200);
      navigate(mapParams(Routes.Dashboard, { uuid: data!.uuid }));
    },
  });
  return (
    <Dialog>
      <DialogTrigger className="w-full" ref={btnRef}>
        <SidebarMenuButton className="text-sidebar-foreground/70" asChild>
          <div>
            <Plus />
            <span>Create dashboard</span>
          </div>
        </SidebarMenuButton>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Create dashboard</DialogTitle>
          <DialogDescription>
            You can create a dashboard here. Click "add" when you're done.
          </DialogDescription>
        </DialogHeader>
        <Formik
          initialValues={initialValues}
          onSubmit={addMutation.mutateAsync}
        >
          <Form className="space-y-3">
            {/*TODO maybe create a separate component for this div...*/}
            <div>
              <Label htmlFor="title">Title</Label>
              <InputField name="title" placeholder="Title" required />
            </div>
            <DialogFooter>
              <Button type="submit">Create</Button>
            </DialogFooter>
          </Form>
        </Formik>
      </DialogContent>
    </Dialog>
  );
}
