export const getSpecialFieldLabel = (fieldName: string) => {
  if (fieldName === "aggregate_field_name") {
    return "Group by";
  } else {
    return "INVALID_FIELD";
  }
};

export const getSpecialFieldOptions = (
  chartName: string,
  fieldName: string,
) => {
  if (
    chartName == "mixed_institution_aggregation" &&
    fieldName === "aggregate_field_name"
  ) {
    return [
      { value: "type", label: "Type" },
      { value: "country", label: "Country" },
      { value: "city", label: "City" },
      { value: "region", label: "Region" },
    ];
  }
};
