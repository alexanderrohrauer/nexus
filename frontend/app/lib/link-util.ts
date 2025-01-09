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
