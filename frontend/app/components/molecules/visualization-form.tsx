import React from "react";
import { Label } from "~/components/ui/label";
import { InputField } from "~/components/ui/input";
import { ComboboxField } from "~/components/ui/combobox";
import { TextTooltip } from "~/components/molecules/text-tooltip";
import { Info, X } from "lucide-react";
import type { FieldProps } from "formik";
import { Field, Form } from "formik";
import { useQuery } from "@tanstack/react-query";
import { client } from "~/lib/api/api-client";
import { ChartType } from "~/lib/api/types";
import {
  getSpecialFieldLabel,
  getSpecialFieldOptions,
} from "~/lib/special-fields-util";

interface VisualizationFormProps extends React.PropsWithChildren {
  typeDisabled?: boolean;
  chartName?: string;
}

export function VisualizationForm(props: VisualizationFormProps) {
  const { data: mixedChartTypes } = useQuery({
    queryKey: ["mixed-chart-types"],
    queryFn: () =>
      client
        .GET("/charts/{chart_type}", {
          params: { path: { chart_type: ChartType.MIXED } },
        })
        .then((res) => res.data),
  });
  return (
    <Form className="space-y-3">
      {/*TODO maybe create a separate component for this div...*/}
      <div>
        <Label htmlFor="title">Title</Label>
        <InputField name="title" placeholder="Title" required />
      </div>

      <div>
        <Label htmlFor="chart">Chart</Label>
        <ComboboxField
          name="chart"
          options={mixedChartTypes ?? []}
          placeholder="Select chart"
          disabled={props.typeDisabled}
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
          <InputField type="number" name="rows" min={2} placeholder="Rows" />
          <X size={40} />
          <InputField
            type="number"
            name="columns"
            min={2}
            placeholder="Columns"
          />
        </div>
      </div>
      <Field name="special_fields">
        {({ field }: FieldProps) =>
          Object.keys(field.value).map((specialFieldName) => (
            <div key={specialFieldName}>
              <Label>{getSpecialFieldLabel(specialFieldName)}</Label>
              <ComboboxField
                name={`${field.name}.${specialFieldName}`}
                options={getSpecialFieldOptions(
                  props.chartName,
                  specialFieldName,
                )}
                placeholder="Select field"
              />
            </div>
          ))
        }
      </Field>
      {props.children}
    </Form>
  );
}
