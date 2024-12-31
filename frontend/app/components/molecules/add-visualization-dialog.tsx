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
import type {
  SchemaCreateVisualizationRequest,
  SchemaDashboard,
} from "~/lib/api/types";
import { Plus } from "lucide-react";
import { useMutation } from "@tanstack/react-query";
import { client } from "~/lib/api/api-client";
import { Formik } from "formik";
import { useRevalidator } from "react-router";
import { useToast } from "~/lib/toast";
import React, { useRef } from "react";
import { VisualizationForm } from "~/components/molecules/visualization-form";

interface AddVisualizationDialogProps {
  dashboard: SchemaDashboard;
}

const initialValues: SchemaCreateVisualizationRequest = {
  title: "",
  // @ts-ignore
  visualization: null,
  rows: 2,
  columns: 2,
  default_query: {},
};

export function AddVisualizationDialog(props: AddVisualizationDialogProps) {
  const revalidator = useRevalidator();
  const btnRef = useRef<HTMLButtonElement | null>(null);
  const toast = useToast();

  // TODO error handler
  const addMutation = useMutation({
    mutationFn: (data: SchemaCreateVisualizationRequest) =>
      client.POST("/dashboards/{uuid}/visualizations", {
        body: data,
        params: { path: { uuid: props.dashboard.uuid! } },
      }),
    onSuccess: () => {
      revalidator.revalidate();
      toast.success("Visualization successfully added");
      setTimeout(() => btnRef.current?.click(), 200);
    },
  });
  return (
    <Dialog>
      <DialogTrigger>
        <Button ref={btnRef} asChild>
          <div>
            <Plus />
            Visualization
          </div>
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add visualization</DialogTitle>
          <DialogDescription>
            You can add a visualization to the dashboard here. Click "add" when
            you're done.
          </DialogDescription>
        </DialogHeader>
        <Formik
          initialValues={initialValues}
          onSubmit={addMutation.mutateAsync}
        >
          <VisualizationForm>
            <DialogFooter>
              <Button type="submit">Add</Button>
            </DialogFooter>
          </VisualizationForm>
        </Formik>
      </DialogContent>
    </Dialog>
  );
}
