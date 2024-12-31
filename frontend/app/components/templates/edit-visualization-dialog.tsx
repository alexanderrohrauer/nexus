import React, { useRef } from "react";
import { VisualizationForm } from "~/components/molecules/visualization-form";
import { Button } from "~/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogTitle,
  DialogTrigger,
} from "~/components/ui/dialog";
import { Edit } from "lucide-react";
import type { FieldProps } from "formik";
import { FastField, Formik } from "formik";
import type {
  SchemaUpdateVisualizationRequest,
  SchemaVisualization,
  SchemaVisualizationData,
} from "~/lib/api/types";
import { Label } from "~/components/ui/label";
import { VisualizationFilter } from "~/components/templates/visualization-filter";
import { useToast } from "~/lib/toast";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { client } from "~/lib/api/api-client";
import { useNav } from "~/components/context/nav-context";
import { useRevalidator } from "react-router";
import type { ConfirmationModalRef } from "~/components/molecules/confirmation-modal";
import { ConfirmationModal } from "~/components/molecules/confirmation-modal";

interface EditVisualizationProps {
  visualization: SchemaVisualization;
  response: SchemaVisualizationData;
}

export function EditVisualizationDialog(props: EditVisualizationProps) {
  const { dashboard } = useNav();
  const toast = useToast();
  const revalidator = useRevalidator();
  const queryClient = useQueryClient();
  const deleteConf = useRef<ConfirmationModalRef | null>(null);
  const mutation = useMutation({
    mutationFn: (formValues: SchemaUpdateVisualizationRequest) =>
      client.PUT("/dashboards/{uuid}/visualizations/{visualization_uuid}", {
        body: formValues,
        params: {
          path: {
            uuid: dashboard.uuid,
            visualization_uuid: props.visualization.uuid,
          },
        },
      }),
    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey: ["visualization_data", props.visualization.uuid],
      });
      revalidator.revalidate();
      setTimeout(
        () => toast.success("Visualization successfully updated"),
        200,
      );
    },
    onError: async () => {
      setTimeout(() => toast.error("Visualization update failed"), 200);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: () =>
      client.DELETE("/dashboards/{uuid}/visualizations/{visualization_uuid}", {
        params: {
          path: {
            uuid: dashboard.uuid,
            visualization_uuid: props.visualization.uuid,
          },
        },
      }),
    onSuccess: async () => {
      revalidator.revalidate();
      setTimeout(
        () => toast.success("Visualization successfully deleted"),
        200,
      );
    },
    onError: async () => {
      setTimeout(() => toast.error("Visualization update failed"), 200);
    },
  });
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button size="icon" variant="outline" className="relative h-8 w-8">
          <Edit />
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-max">
        <DialogTitle>Edit</DialogTitle>
        <Formik
          initialValues={props.visualization}
          onSubmit={(values) => mutation.mutateAsync(values)}
        >
          <VisualizationForm typeDisabled>
            <div>
              <Label htmlFor="chart">Pre-Filters</Label>
              <FastField name="query_preset">
                {({ field, form }: FieldProps) => (
                  <VisualizationFilter
                    response={props.response}
                    filters={field.value}
                    onFilterChange={(filters) =>
                      form.setFieldValue(field.name, filters)
                    }
                  />
                )}
              </FastField>
            </div>
            <DialogFooter>
              <Button
                type="button"
                variant="destructive"
                onClick={() => deleteConf.current?.trigger(null)}
              >
                Delete
              </Button>
              <DialogTrigger asChild>
                <Button type="submit">Save</Button>
              </DialogTrigger>
            </DialogFooter>
          </VisualizationForm>
        </Formik>
      </DialogContent>
      <ConfirmationModal
        variant="destructive"
        title="Delete visualization"
        description="Do you really want to delete this visualization?"
        okText="Delete"
        ok={() => deleteMutation.mutateAsync()}
        ref={deleteConf}
      />
    </Dialog>
  );
}
