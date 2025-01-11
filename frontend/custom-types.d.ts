import type {
  SchemaInstitution,
  SchemaResearcher,
  SchemaWorkOutput,
} from "~/lib/api/types";

interface ChartOptions<SeriesType> {
  series: SeriesType;
}

type Entity = SchemaResearcher | SchemaWorkOutput | SchemaInstitution;
