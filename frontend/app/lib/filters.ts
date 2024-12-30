// TODO eventually fetch all available languages some day
export const INSTITUTION_FIELDS = [
  { name: "uuid", label: "ID", type: "institution" },
  { name: "homepage_url", label: "Homepage URL", type: "string" },
  {
    name: "international_names",
    label: "International names",
    type: "multi",
    children: [
      { name: "ar", label: "Arabic", type: "string" },
      { name: "zh", label: "Chinese (simplified)", type: "string" },
      { name: "zh-cn", label: "Chinese (China)", type: "string" },
      { name: "zh-hant", label: "Chinese (Hong Kong)", type: "string" },
      { name: "en", label: "English", type: "string" },
      { name: "fr", label: "French", type: "string" },
      { name: "de", label: "German", type: "string" },
      { name: "it", label: "Italian", type: "string" },
      { name: "ja", label: "Japanese", type: "string" },
      { name: "kr", label: "Korean", type: "string" },
      { name: "es", label: "Spanish", type: "string" },
    ],
  },
  //   TODO when using UUIDs, use type "institutions"
  {
    name: "parent_institutions_ids",
    label: "Parent institutions (OpenAlex ID)",
    type: "string",
  },
  {
    name: "external_id",
    label: "External ID",
    type: "multi",
    children: [
      { name: "openalex", label: "OpenAlex", type: "string" },
      { name: "ror", label: "ROR", type: "string" },
    ],
  },
  { name: "name", label: "Name", type: "string" },
  { name: "city", label: "City", type: "string" },
  { name: "region", label: "Region", type: "string" },
  { name: "country", label: "Country", type: "string" },
  { name: "topic_keywords", label: "Keywords", type: "string" },
  {
    name: "type",
    label: "Type",
    type: "string",
  },
  { name: "acronyms", label: "Acronyms", type: "string" },
  { name: "alternative_names", label: "Alternative names", type: "string" },
  { name: "imported_at", label: "Imported At", type: "date" },
];

export const RESEARCHER_FIELDS = [
  { name: "uuid", label: "ID", type: "researcher" },
  {
    name: "external_id",
    label: "External ID",
    type: "multi",
    children: [
      { name: "openalex", label: "OpenAlex", type: "string" },
      { name: "orcid", label: "ORCID", type: "string" },
      { name: "dblp", label: "DBLP", type: "string" },
    ],
  },
  { name: "full_name", label: "Full name", type: "string" },
  { name: "alternative_names", label: "Alternative names", type: "string" },
  {
    name: "affiliations",
    label: "Affiliations",
    type: "multi",
    children: [
      { name: "years", label: "Years", type: "number" },
      { name: "type", label: "Type", type: "string" },
      {
        name: "institution",
        label: "Institution",
        isRelation: true,
        children: INSTITUTION_FIELDS,
      },
    ],
  },
  { name: "topic_keywords", label: "Keywords", type: "string" },
  {
    name: "institution",
    label: "Institution",
    isRelation: true,
    children: INSTITUTION_FIELDS,
  },
  { name: "imported_at", label: "Imported At", type: "date" },
];

export const WORK_FIELDS = [
  { name: "uuid", label: "ID", type: "work" },
  {
    name: "external_id",
    label: "External ID",
    type: "multi",
    children: [
      { name: "openalex", label: "OpenAlex", type: "string" },
      { name: "doi", label: "DOI", type: "string" },
      { name: "dblp", label: "DBLP", type: "string" },
    ],
  },
  {
    name: "authors",
    label: "Authors",
    isRelation: true,
    children: RESEARCHER_FIELDS,
  },
  { name: "open_access", label: "Open access", type: "boolean" },
  { name: "publication_date", label: "Publication date", type: "date" },
  { name: "title", label: "Title", type: "string" },
  {
    name: "type",
    label: "Type",
    type: "multi",
    children: [
      { name: "openalex", label: "OpenAlex", type: "string" },
      { name: "dblp", label: "DBLP", type: "string" },
      // { name: "orcid", label: "ORCID", type: "string" },
    ],
  },
  { name: "keywords", label: "Keywords", type: "string" },
  { name: "publication_year", label: "Publication year", type: "number" },
  { name: "language", label: "Language", type: "string" },
  { name: "imported_at", label: "Imported At", type: "date" },
];
