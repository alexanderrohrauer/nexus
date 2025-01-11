import { EntityType } from "~/lib/api/types";
import { mapParams } from "~/lib/links";
import { Routes } from "~/routes";

export const getNexusLink = (meta) => {
  if (meta) {
    if (meta.type === EntityType.RESEARCHER) {
      return mapParams(Routes.Researcher, { uuid: meta.id });
    } else if (meta.type === EntityType.INSTITUTION) {
      return mapParams(Routes.Institution, { uuid: meta.id });
    } else if (meta.type === EntityType.WORK) {
      return mapParams(Routes.Work, { uuid: meta.id });
    } else {
      return null;
    }
  } else {
    return null;
  }
};

export const getExternalUrl = (
  source: string,
  id: string | number,
  entityType = EntityType.RESEARCHER,
) => {
  if (
    id.toString().startsWith("https://") ||
    id.toString().startsWith("http://")
  ) {
    return id as string;
  } else if (source === "openalex") {
    return `https://openalex.org/${id}`;
  } else if (source === "orcid") {
    return `https://orcid.org/${id}`;
  } else if (source === "doi") {
    return `https://doi.org/${id}`;
  } else if (source === "ror") {
    return `https://ror.org/${id}`;
  } else if (source === "dblp" && entityType === EntityType.RESEARCHER) {
    return `https://dblp.org/pid/${id}.html`;
  }
};
