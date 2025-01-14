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
  } else if (
    chartName == "mixed_work_aggregation" &&
    fieldName === "aggregate_field_name"
  ) {
    return [
      { value: "publication_year", label: "Publication year" },
      { value: "dblp_type", label: "Type (DBLP)" },
      { value: "openalex_type", label: "Type (OpenAlex)" },
      { value: "language", label: "Language" },
      { value: "region", label: "Region" },
    ];
  }
};
