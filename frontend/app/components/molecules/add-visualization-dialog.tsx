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
import {
  SchemaCreateVisualizationRequest,
  SchemaDashboard,
} from "~/lib/api/types";
import { Info, Plus, X } from "lucide-react";
import { useMutation } from "@tanstack/react-query";
import { client } from "~/lib/api/api-client";
import { Form, Formik } from "formik";
import { useRevalidator } from "react-router";
import { TextTooltip } from "~/components/molecules/TextTooltip";
import { ComboboxField, ComboboxOption } from "~/components/ui/combobox";
import { useToast } from "~/lib/toast";
import { useRef } from "react";

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

// TODO extract this to endpoint
const visualizationOptions: ComboboxOption[] = [
  { label: "Visualization 1", value: "vis-1" },
  { label: "Visualization 2", value: "vis-2" },
  { label: "Visualization 3", value: "vis-3" },
];

export function AddVisualizationDialog(props: AddVisualizationDialogProps) {
  const revalidator = useRevalidator();
  const btnRef = useRef<HTMLButtonElement | null>(null);
  const toast = useToast();
  // TODO error handler
  const addMutation = useMutation({
    mutationFn: (data: SchemaCreateVisualizationRequest) =>
      client.POST("/dashboards/{uuid}/visualizations", {
        body: data,
        params: { path: { uuid: props.dashboard.uuid } },
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
        <Button ref={btnRef}>
          <Plus />
          Visualization
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
          <Form className="space-y-3">
            {/*TODO maybe create a separate component for this div...*/}
            <div>
              <Label htmlFor="title">Title</Label>
              <InputField name="title" placeholder="Title" required />
            </div>

            <div>
              <Label htmlFor="visualization">Visualization</Label>
              <ComboboxField
                name="visualization"
                options={visualizationOptions}
                placeholder="Select visualization"
              />
            </div>

            <div>
              <Label className="flex item-center space-x-1">
                <span>Size</span>{" "}
                <TextTooltip text={"Format: rows x columns"}>
                  <Info size={16} />
                </TextTooltip>
              </Label>
              <div className="flex space-x-3 items-center">
                <InputField
                  type="number"
                  name="rows"
                  min={2}
                  max={12}
                  placeholder="Rows"
                />
                <X size={40} />
                <InputField
                  type="number"
                  name="columns"
                  min={2}
                  max={12}
                  placeholder="Columns"
                />
              </div>
            </div>
            <DialogFooter>
              <Button type="submit">Add</Button>
            </DialogFooter>
          </Form>
        </Formik>
      </DialogContent>
    </Dialog>
  );
}
